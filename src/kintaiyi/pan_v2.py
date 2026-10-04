"""C11 / pan v2 纯 builder。

只组装上游已经算出的事实，不导入 Taiyi，不复制任何太乙算法。
"""

from __future__ import annotations

import copy
import json
from typing import Any

from .taiyi_rules import (
    GENERAL_INTRINSIC_WX, GOD_POSITION, PALACE_YIN_YANG, POSITION_WX,
    calc_components, integer, nine_palace_representative_sector,
    nine_palace_to_trigram, palace_element, sector_to_nine_palace,
)

SCHEMA_VERSION = "2.0"

BOARD_KEYS = ("taiyi", "eyes", "calculations", "generals", "sixteen_sectors", "doors", "other_gods")
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
    data = copy.deepcopy({} if value is None else value)
    if not isinstance(data, dict):
        raise TypeError("v2区段须为dict")
    for key in required:
        data.setdefault(key, {})
    return data


def _merge_defaults(value: dict[str, Any] | None, defaults: dict[str, Any]) -> dict[str, Any]:
    data = copy.deepcopy({} if value is None else value)
    if not isinstance(data, dict):
        raise TypeError("v2区段须为dict")
    merged = copy.deepcopy(defaults)
    for key, item in data.items():
        if isinstance(defaults.get(key), dict) and isinstance(item, dict):
            merged[key] = _merge_defaults(item, defaults[key])
        else:
            merged[key] = item
    return merged


def _add_child_defaults(data: dict[str, Any], name: str, defaults: dict[str, Any]) -> None:
    child = data.get(name)
    if child is None:
        child = {}
    if not isinstance(child, dict):
        raise TypeError(f"{name}须为dict")
    data[name] = _merge_defaults(child, defaults)


def _normalize_scenario(scenario: dict[str, Any] | None) -> dict[str, Any]:
    if scenario is None:
        return {}
    if not isinstance(scenario, dict):
        raise TypeError("scenario须为dict")
    if any(not isinstance(key, str) for key in scenario):
        raise TypeError("scenario字段名须为str")
    unknown = sorted(set(scenario) - set(SCENARIO_KEYS))
    if unknown:
        raise ValueError(f"未知scenario字段: {', '.join(unknown)}")
    return {key: copy.deepcopy(scenario[key]) for key in SCENARIO_KEYS if key in scenario}


def _force_center_sector_null(board: dict[str, Any]) -> None:
    """中五无 Sector16；只修表示层，不计算宫位。"""
    def palace_id(item: dict[str, Any]) -> Any:
        for key in ("palace_id", "palace", "nine_palace"):
            if item.get(key) is not None:
                return item[key]
        return None

    taiyi = board.get("taiyi")
    if isinstance(taiyi, dict) and palace_id(taiyi) == 5:
        taiyi["sector"] = None

    generals = board.get("generals")
    if isinstance(generals, dict):
        for general in generals.values():
            if isinstance(general, dict) and palace_id(general) == 5:
                general["sector"] = None

    calculations = board.get("calculations")
    if isinstance(calculations, dict):
        for item in calculations.values():
            if isinstance(item, dict) and palace_id(item) == 5:
                item["sector"] = None

    eyes = board.get("eyes")
    if isinstance(eyes, dict):
        for eye in eyes.values():
            if isinstance(eye, dict) and palace_id(eye) == 5:
                eye["sector"] = None


def taiyi_board(palace_id: int) -> dict[str, Any]:
    """Create a coordinate-typed Taiyi fact; 5-center has no 16-sector point."""
    palace_id = integer(palace_id, 1, 9)
    sector = nine_palace_representative_sector(palace_id)
    return {
        "coordinate": "nine_palace",
        "palace_id": palace_id,
        "palace": palace_id,
        "trigram": nine_palace_to_trigram(palace_id),
        "sector": sector,
        "element": palace_element(palace_id),
        "yin_yang": PALACE_YIN_YANG[palace_id],
    }


def sector_board(sector: str) -> dict[str, Any]:
    """Create a fact on the 16-sector ring and state whether it represents a 9-palace."""
    if sector not in POSITION_WX:
        raise ValueError("须为十六辰位置")
    god = next((name for name, point in GOD_POSITION.items() if point == sector), None)
    palace_id = sector_to_nine_palace(sector)
    return {
        "coordinate": "sixteen_sector",
        "sector": sector,
        "god": god,
        "nine_palace": palace_id,
        "sector_element": POSITION_WX[sector],
        "nine_palace_element": palace_element(palace_id) if palace_id is not None else None,
    }


def general_board(role: str, palace_id: int) -> dict[str, Any]:
    """Keep a general's intrinsic element separate from the palace element."""
    aliases = {"home_vassal": "home_assistant", "away_vassal": "away_assistant"}
    role = aliases.get(role, role)
    if role not in GENERAL_INTRINSIC_WX:
        raise ValueError("未知将帅角色")
    palace_id = integer(palace_id, 1, 9)
    return {
        "role": role,
        "coordinate": "nine_palace",
        "palace_id": palace_id,
        "palace": palace_id,
        "sector": nine_palace_representative_sector(palace_id),
        "intrinsic_element": GENERAL_INTRINSIC_WX[role],
        "palace_element": palace_element(palace_id),
    }


def calculation_board(value: int, *, palace_id: int | None = None) -> dict[str, Any]:
    """Keep arithmetic components distinct from D8 tags and optional palace facts."""
    parts = calc_components(value)
    from .eight_divinations import sancai
    out = {
        "value": value,
        "components": parts,
        "missing_components": [
            name for name, present in (("ten", parts["ten"]), ("five", parts["five"]), ("one", parts["one"]))
            if not present
        ],
        "classic_tags": sancai(value)["classic_tags"],
        "parity": "奇" if value % 2 else "偶",
        "last_digit": value % 10,
    }
    if palace_id is not None:
        palace_id = integer(palace_id, 1, 9)
        out.update({"coordinate": "nine_palace", "palace_id": palace_id,
                    "palace": palace_id,
                    "sector": nine_palace_representative_sector(palace_id)})
    return out


def _same(left: dict[str, Any], right: dict[str, Any], coordinate: str,
          left_value: str, right_value: str | None = None) -> bool | None:
    if left.get("coordinate") != coordinate or right.get("coordinate") != coordinate:
        return None
    right_value = right_value or left_value
    if left.get(left_value) is None or right.get(right_value) is None:
        return None
    return left[left_value] == right[right_value]


def same_nine_palace(left: dict[str, Any], right: dict[str, Any]) -> bool | None:
    return _same(left, right, "nine_palace", "palace_id", "palace_id")


def same_sixteen_sector(left: dict[str, Any], right: dict[str, Any]) -> bool | None:
    return _same(left, right, "sixteen_sector", "sector")


def same_four_taiyi_palace(left: dict[str, Any], right: dict[str, Any]) -> bool | None:
    return _same(left, right, "four_taiyi_palace", "palace_id", "palace_id")


def same_wufu_domain(left: dict[str, Any], right: dict[str, Any]) -> bool | None:
    return _same(left, right, "wufu_domain", "domain")


def build_pan_v2(*, meta: dict[str, Any] | None = None,
                 calendar: dict[str, Any] | None = None,
                 board: dict[str, Any] | None = None,
                 cycles: dict[str, Any] | None = None,
                 analysis: dict[str, Any] | None = None,
                 modern: dict[str, Any] | None = None,
                 source_variants: dict[str, Any] | None = None,
                 derived: list[Any] | None = None,
                 pending: list[Any] | None = None,
                 compat: dict[str, Any] | None = None,
                 scenario: dict[str, Any] | None = None) -> dict[str, Any]:
    """构建完整 pan v2 根结构。

    所有参数都是已经算好的事实。本函数不调用八占、七术、周期或军事算法。
    """
    meta_data = _merge_defaults(meta, {
        "ji_style": None, "method": None,
        "accumulated_year": None, "source_profile": None,
    })
    scenario_data = _normalize_scenario(scenario)
    if scenario_data:
        existing_scenario = meta_data.get("scenario") or {}
        if not isinstance(existing_scenario, dict):
            raise TypeError("meta.scenario须为dict")
        meta_data["scenario"] = {**existing_scenario, **scenario_data}

    calendar_data = _merge_defaults(calendar, {
        "gregorian": {"year": None, "month": None, "day": None, "hour": None, "minute": None},
        "ganzhi": {"year": None, "month": None, "day": None, "hour": None},
        "branches": {"year": None, "month": None, "day": None, "hour": None},
        "lunar": {}, "jieqi": None,
    })
    board_data = _merge_defaults(board, {
        "taiyi": None,
        "eyes": {"wenchang": None, "shiji": None, "dingmu": None, "skyeyes": None},
        "calculations": {"home": None, "away": None, "fixed": None},
        "generals": {
            "home_general": None, "home_assistant": None,
            "away_general": None, "away_assistant": None,
        },
        "sixteen_sectors": {}, "doors": {}, "other_gods": {},
    })
    cycle_data = _merge_defaults(cycles, {key: None for key in CYCLE_KEYS})
    analysis_data = _with_required_children(analysis, ANALYSIS_KEYS)
    _force_center_sector_null(board_data)

    modern_data = copy.deepcopy({} if modern is None else modern)
    source_variant_data = copy.deepcopy({} if source_variants is None else source_variants)
    compat_data = copy.deepcopy({
        "legacy_top_level": True, "legacy_schema": "pan-v1-flat",
    } if compat is None else compat)
    if not isinstance(compat_data, dict):
        raise TypeError("compat须为dict")
    if not isinstance(modern_data, dict) or not isinstance(source_variant_data, dict):
        raise TypeError("modern与source_variants须为dict")
    derived_data = copy.deepcopy([] if derived is None else derived)
    pending_data = copy.deepcopy([] if pending is None else pending)
    if not isinstance(derived_data, list) or not isinstance(pending_data, list):
        raise TypeError("derived与pending须为list")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "meta": meta_data,
        "calendar": calendar_data,
        "board": board_data,
        "cycles": cycle_data,
        "analysis": analysis_data,
        "modern": modern_data,
        "source_variants": source_variant_data,
        "derived": derived_data,
        "pending": pending_data,
        "compat": compat_data,
    }
    safe = _json_safe(payload)
    # 二次保证未来修改不会悄悄放入非 JSON-safe 对象。
    json.dumps(safe, ensure_ascii=False)
    return safe


def pan(**kwargs) -> dict[str, Any]:
    """Public pan v2 entry point; legacy presentation is returned under compat."""
    return build_pan_v2(**kwargs)


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

    for key in ("derived", "pending"):
        if key not in payload:
            errors.append(f"缺根区段:{key}")
        elif not isinstance(payload[key], list):
            errors.append(f"{key}须为list")

    board = payload.get("board")
    if isinstance(board, dict):
        for key in BOARD_KEYS:
            if key not in board:
                errors.append(f"缺board.{key}")

        taiyi = board.get("taiyi")
        palace = None
        if isinstance(taiyi, dict):
            palace = taiyi.get("palace_id") if taiyi.get("palace_id") is not None else taiyi.get("palace")
        if isinstance(taiyi, dict) and palace == 5 and taiyi.get("sector") is not None:
            errors.append("board.taiyi中五sector必须为null")

        generals = board.get("generals")
        if isinstance(generals, dict):
            for name, general in generals.items():
                palace = None
                if isinstance(general, dict):
                    palace = (general.get("palace_id") if general.get("palace_id") is not None
                              else general.get("palace"))
                if isinstance(general, dict) and palace == 5 and general.get("sector") is not None:
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
