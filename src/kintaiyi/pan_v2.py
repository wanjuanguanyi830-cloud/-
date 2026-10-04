"""C11 / pan v2 纯 builder。

只组装上游已经算出的事实，不导入 Taiyi，不复制任何太乙算法。
"""

from __future__ import annotations

import copy
import json
from typing import Any

SCHEMA_VERSION = "2.0"

BOARD_KEYS = ("taiyi", "eyes", "calculations", "generals", "doors", "sixteen_palaces")
CYCLE_KEYS = ("three_bases", "five_blessings", "big_wander", "small_wander", "four_taiyi", "limits")
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
    if isinstance(taiyi, dict) and taiyi.get("palace") == 5:
        taiyi["sector"] = None

    generals = board.get("generals")
    if isinstance(generals, dict):
        for general in generals.values():
            if isinstance(general, dict) and general.get("palace") == 5:
                general["sector"] = None

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
        if isinstance(taiyi, dict) and taiyi.get("palace") == 5 and taiyi.get("sector") is not None:
            errors.append("board.taiyi中五sector必须为null")

        generals = board.get("generals")
        if isinstance(generals, dict):
            for name, general in generals.items():
                if isinstance(general, dict) and general.get("palace") == 5 and general.get("sector") is not None:
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
