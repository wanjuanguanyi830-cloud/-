"""C11 / pan v2 纯 builder。

只组装上游已经算出的事实，不导入 Taiyi，不复制任何太乙算法。
"""

from __future__ import annotations

import copy
import json
from typing import Any, TypedDict

from .eight_divinations import analyze_eight_divinations, sancai_analysis
from .four_taiyi import four_taiyi_positions
from .junshi_zhanlue import junshi_zhanlue
from .seven_methods import analyze_seven_methods
from .taiyi_common import NINE_PALACES, ROLE_ELEMENTS, integer, sector_detail
from .taiyi_cycles import (
    big_wander, five_blessings, minister_base, people_base, ruler_base, small_wander,
)

SCHEMA_VERSION = "2.0"

BOARD_KEYS = ("taiyi", "eyes", "calculations", "generals", "doors", "sixteen_palaces")
CYCLE_KEYS = ("three_bases", "five_blessings", "big_wander", "small_wander", "four_taiyi")
ANALYSIS_KEYS = ("patterns", "eight_divinations", "seven_methods", "military")
SCENARIO_KEYS = (
    "enemy_start_year_branch",
    "enemy_camp_day_taiyi_palace",
    "enemy_first_arrival_taiyi_palace",
)


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("pan v2 dict key须为str")
            result[key] = _json_safe(item)
        return result
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return [_json_safe(item) for item in sorted(value, key=repr)]
    raise TypeError(f"pan v2存在非JSON-safe类型: {type(value).__name__}")


def _with_required_children(value: dict[str, Any] | None, required: tuple[str, ...]) -> dict[str, Any]:
    data = copy.deepcopy(value or {})
    if not isinstance(data, dict):
        raise TypeError("v2区段须为dict")
    for key in required:
        data.setdefault(key, {})
    return data


def _normalize_scenario(scenario: dict[str, Any] | None) -> dict[str, Any]:
    if scenario is None:
        return {}
    if not isinstance(scenario, dict):
        raise TypeError("scenario须为dict")
    unknown = sorted(set(scenario) - set(SCENARIO_KEYS))
    if unknown:
        raise ValueError(f"未知scenario字段: {', '.join(unknown)}")
    return {key: copy.deepcopy(scenario[key]) for key in SCENARIO_KEYS if key in scenario}


def _force_center_sector_null(board: dict[str, Any]) -> None:
    """中五无 Sector16；只修表示层，不计算宫位。"""
    taiyi = board.get("taiyi")
    if isinstance(taiyi, dict) and taiyi.get("palace_id", taiyi.get("palace")) == 5:
        taiyi["sector"] = None

    generals = board.get("generals")
    if isinstance(generals, dict):
        for general in generals.values():
            if isinstance(general, dict) and general.get("palace_id", general.get("palace")) == 5:
                general["sector"] = None
                if "representative_sector" in general:
                    general["representative_sector"] = None

    calculations = board.get("calculations")
    if isinstance(calculations, dict):
        for item in calculations.values():
            if isinstance(item, dict) and item.get("palace") == 5:
                item["sector"] = None


def build_pan_v2(*, meta: dict[str, Any] | None = None,
                 calendar: dict[str, Any] | None = None,
                 board: dict[str, Any] | None = None,
                 cycles: dict[str, Any] | None = None,
                 analysis: dict[str, Any] | None = None,
                 modern: dict[str, Any] | None = None,
                 source_variants: dict[str, Any] | None = None,
                 compat: dict[str, Any] | None = None,
                 scenario: dict[str, Any] | None = None) -> dict[str, Any]:
    """构建完整 pan v2 根结构。

    所有参数都是已经算好的事实。本函数不调用八占、七术、周期或军事算法。
    """
    meta_data = copy.deepcopy(meta or {})
    if not isinstance(meta_data, dict):
        raise TypeError("meta须为dict")
    scenario_data = _normalize_scenario(scenario)
    if scenario_data:
        meta_data["scenario"] = scenario_data

    board_data = _with_required_children(board, BOARD_KEYS)
    cycle_data = _with_required_children(cycles, CYCLE_KEYS)
    analysis_data = _with_required_children(analysis, ANALYSIS_KEYS)
    _force_center_sector_null(board_data)

    compat_data = copy.deepcopy(compat or {
        "legacy_top_level": True,
        "legacy_schema": "pan-v1-flat",
    })
    if not isinstance(compat_data, dict):
        raise TypeError("compat须为dict")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "meta": meta_data,
        "calendar": copy.deepcopy(calendar or {}),
        "board": board_data,
        "cycles": cycle_data,
        "analysis": analysis_data,
        "modern": copy.deepcopy(modern or {}),
        "source_variants": copy.deepcopy(source_variants or {}),
        "compat": compat_data,
    }
    safe = _json_safe(payload)
    # 二次保证未来修改不会悄悄放入非 JSON-safe 对象。
    json.dumps(safe, ensure_ascii=False)
    return safe


def validate_pan_v2(payload: dict[str, Any]) -> dict[str, Any]:
    """验证 v2 结构与几条关键不变量，不验证古法答案本身。"""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        return {"valid": False, "errors": ["payload须为dict"], "warnings": []}

    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version必须为2.0")

    for key in ("meta", "calendar", "board", "cycles", "analysis", "modern", "source_variants", "compat"):
        if key not in payload:
            errors.append(f"缺根区段:{key}")
        elif not isinstance(payload[key], dict):
            errors.append(f"{key}须为dict")

    board = payload.get("board")
    if isinstance(board, dict):
        for key in BOARD_KEYS:
            if key not in board:
                errors.append(f"缺board.{key}")

        taiyi = board.get("taiyi")
        if isinstance(taiyi, dict) and taiyi.get("palace_id", taiyi.get("palace")) == 5 and taiyi.get("sector") is not None:
            errors.append("board.taiyi中五sector必须为null")

        generals = board.get("generals")
        if isinstance(generals, dict):
            for name, general in generals.items():
                if isinstance(general, dict) and general.get("palace_id", general.get("palace")) == 5 and (general.get("sector") is not None or general.get("representative_sector") is not None):
                    errors.append(f"board.generals.{name}中五sector必须为null")
                if isinstance(general, dict):
                    if "intrinsic_element" in general and "palace_element" not in general:
                        warnings.append(f"board.generals.{name}有intrinsic_element但缺palace_element")

    cycles = payload.get("cycles")
    if isinstance(cycles, dict):
        for key in CYCLE_KEYS:
            if key not in cycles:
                errors.append(f"缺cycles.{key}")

    analysis = payload.get("analysis")
    if isinstance(analysis, dict):
        for key in ANALYSIS_KEYS:
            if key not in analysis:
                errors.append(f"缺analysis.{key}")

    try:
        json.dumps(_json_safe(payload), ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "schema_version": payload.get("schema_version"),
    }


class PanCoreSnapshot(TypedDict, total=False):
    accumulated_year: int
    year_accumulated_year: int
    ji_style: int
    taiyi_acumyear: int
    taiyi_palace: int
    wenchang_sector: str
    shiji_sector: str
    dingmu_sector: str
    home_cal: int
    away_cal: int
    fixed_cal: int
    home_general: int
    home_assistant: int
    away_general: int
    away_assistant: int
    day_taiyi_palace: int
    four_taiyi_yuan: int
    big_wander_profile: str
    doors: dict[str, Any]
    calendar: dict[str, Any]
    patterns: dict[str, Any]


def _missing_fact(name):
    return {"computable": False, "missing_inputs": [name], "reason": "snapshot缺明确输入"}


def _calc_number(value, name):
    if value is None:
        return _missing_fact(name)
    facts = sancai_analysis(value)
    return {"computable": True, "value": value, "components": facts["components"],
            "missing_components": facts["missing_components"], "classic_tags": facts["classic_tags"],
            "parity": "odd" if value % 2 else "even", "last_digit": value % 10}


def _palace_fact(value, name):
    if value is None:
        return _missing_fact(name)
    return {**NINE_PALACES[integer(value, 1, 9)], "palace": value, "computable": True}


def build_pan_v2_from_snapshot(snapshot: PanCoreSnapshot, *, scenario=None):
    """Canonical builder from explicit numeric/coordinate inputs; no Taiyi import.

    Missing event, calendar and cycle inputs remain structured unavailable facts.
    The older build_pan_v2 remains a pure assembler for already computed facts.
    """
    if not isinstance(snapshot, dict):
        raise TypeError("snapshot须为dict")
    snapshot = copy.deepcopy(snapshot)
    scenario = _normalize_scenario(scenario)
    acc = snapshot.get("accumulated_year")
    year_acc = snapshot.get("year_accumulated_year")
    if year_acc is None and snapshot.get("ji_style") == 0:
        year_acc = acc  # selected accumulation is explicitly annual in this case.
    taiyi = _palace_fact(snapshot.get("taiyi_palace"), "taiyi_palace")
    eyes = {}
    for role, input_name in (("skyeyes", "wenchang_sector"), ("shiji", "shiji_sector"), ("dingmu", "dingmu_sector")):
        value = snapshot.get(input_name)
        eyes[role] = {**sector_detail(value), "computable": True} if value is not None else _missing_fact(input_name)
    generals = {}
    for role in ("home_general", "home_assistant", "away_general", "away_assistant"):
        fact = _palace_fact(snapshot.get(role), role)
        generals[role] = {**fact, "role": role, "intrinsic_element": ROLE_ELEMENTS[role]}
        if fact["computable"]:
            generals[role]["palace_element"] = fact["element"]
            generals[role]["representative_sector"] = fact["sector"]
    calculations = {role: _calc_number(snapshot.get(key), key) for role, key in
                    (("home", "home_cal"), ("away", "away_cal"), ("fixed", "fixed_cal"))}
    cycle_data = {
        "three_bases": {role: fn(acc) if acc is not None else _missing_fact("accumulated_year")
                        for role, fn in (("ruler", ruler_base), ("minister", minister_base), ("people", people_base))},
        "five_blessings": five_blessings(acc) if acc is not None else _missing_fact("accumulated_year"),
        "small_wander": small_wander(acc) if acc is not None else _missing_fact("accumulated_year"),
        "big_wander": big_wander(year_acc, profile=snapshot.get("big_wander_profile", "tongzong"))
                      if year_acc is not None else _missing_fact("year_accumulated_year"),
        "four_taiyi": four_taiyi_positions(acc, yuan=snapshot.get("four_taiyi_yuan", 1))
                      if acc is not None else _missing_fact("accumulated_year"),
    }
    cycle_data["big_wander"].update({"year_accumulated_year": year_acc, "selected_accumulated_year": acc})
    d8 = analyze_eight_divinations(snapshot.get("taiyi_palace"), snapshot.get("wenchang_sector"),
                                   snapshot.get("home_cal"), snapshot.get("away_cal"))
    t7 = analyze_seven_methods(
        home_general=snapshot.get("home_general"), home_assistant=snapshot.get("home_assistant"),
        away_general=snapshot.get("away_general"), away_assistant=snapshot.get("away_assistant"),
        day_taiyi_palace=snapshot.get("day_taiyi_palace"), scenario=scenario,
    )
    military = junshi_zhanlue(home_cal=snapshot.get("home_cal"), away_cal=snapshot.get("away_cal"),
                             taiyi=snapshot.get("taiyi_palace"), skyeyes=snapshot.get("wenchang_sector"))
    return build_pan_v2(
        meta={"accumulated_year": acc, "year_accumulated_year": year_acc,
              "ji_style": snapshot.get("ji_style"), "taiyi_acumyear": snapshot.get("taiyi_acumyear"),
              "source_profile": "project_canonical", "four_taiyi_yuan": snapshot.get("four_taiyi_yuan", 1),
              "four_taiyi_yuan_basis": "explicit" if "four_taiyi_yuan" in snapshot else "base_start"},
        calendar=snapshot.get("calendar", {}),
        board={"taiyi": taiyi, "eyes": eyes, "calculations": calculations,
               "generals": generals, "doors": snapshot.get("doors", _missing_fact("doors"))},
        cycles=cycle_data,
        analysis={"patterns": snapshot.get("patterns", _missing_fact("patterns")),
                  "eight_divinations": d8, "seven_methods": t7, "military": military},
        modern={}, source_variants={"seven_methods": {k: v["variants"] for k, v in t7.items()},
                                   "eight_divinations": {"D8-02": {side: d8["D8-02"][side].get("variants", []) for side in ("home", "away")}}},
        scenario=scenario,
    )
