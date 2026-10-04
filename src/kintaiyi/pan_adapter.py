"""C12 legacy pan snapshot -> pan v2 适配层。

用途：未来旧 Taiyi.pan() 仍返回 flat dict 时，可在返回前调用 attach_v2_to_snapshot()
附加一个严格 v2。

本模块只搬运已经存在的盘面事实，不调用任何太乙算法；旧军事、旧七术断语、
旧运筹博弈结果不会被提升为 canonical analysis/modern。
"""

from __future__ import annotations

import copy
from typing import Any

from .pan_v2 import build_pan_v2
from .legacy_schema import (
    CALENDAR_MAP as _CALENDAR_MAP,
    CALC_FIELDS as _CALC_FIELDS,
    CYCLE_FIELDS as _CYCLE_FIELDS,
    DOOR_FIELDS as _DOOR_FIELDS,
    GENERAL_FIELDS as _GENERAL_FIELDS,
    META_MAP as _META_MAP,
    QUARANTINED_LEGACY_KEYS as _QUARANTINED_LEGACY_KEYS,
    SIMPLE_BOARD_FACTS as _SIMPLE_BOARD_FACTS,
)

ADAPTER_VERSION = "taiyi-c12-snapshot-adapter-v1"

def _normalize_legacy_json_containers(value: Any) -> Any:
    """把旧 snapshot 常见的整数宫位 dict key 规范为 JSON object 字符串 key。

    只做容器表示转换，不改值的术义；未知复杂 key 直接拒绝。
    """
    if value is None or isinstance(value, (str, int, float, bool)):
        return copy.deepcopy(value)
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if isinstance(key, str):
                new_key = key
            elif isinstance(key, (int, float, bool)):
                new_key = str(key)
            else:
                raise TypeError(f"legacy snapshot含不支持的dict key类型: {type(key).__name__}")
            result[new_key] = _normalize_legacy_json_containers(item)
        return result
    if isinstance(value, (list, tuple)):
        return [_normalize_legacy_json_containers(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return [_normalize_legacy_json_containers(item) for item in sorted(value, key=repr)]
    return copy.deepcopy(value)


def _copy_if_present(source: dict[str, Any], aliases: dict[str, str]) -> tuple[dict[str, Any], set[str]]:
    out: dict[str, Any] = {}
    consumed: set[str] = set()
    for legacy_key, new_key in aliases.items():
        if legacy_key in source and new_key not in out:
            out[new_key] = copy.deepcopy(source[legacy_key])
            consumed.add(legacy_key)
    return out, consumed


def _calc_fact(value: Any) -> dict[str, Any]:
    """只拆旧 [数, 描述] 容器，不重算描述。"""
    if isinstance(value, (list, tuple)):
        result: dict[str, Any] = {}
        if value:
            result["value"] = copy.deepcopy(value[0])
        if len(value) > 1:
            result["legacy_description"] = copy.deepcopy(value[1])
        if len(value) > 2:
            result["legacy_extra"] = copy.deepcopy(list(value[2:]))
        return result
    return {"value": copy.deepcopy(value)}


def _eye_fact(value: Any) -> dict[str, Any]:
    """文昌旧值通常为 [所在, 描述]；这里只拆容器。"""
    if isinstance(value, (list, tuple)):
        result: dict[str, Any] = {}
        if value:
            result["sector"] = copy.deepcopy(value[0])
        if len(value) > 1:
            result["legacy_description"] = copy.deepcopy(value[1])
        if len(value) > 2:
            result["legacy_extra"] = copy.deepcopy(list(value[2:]))
        return result
    return {"sector": copy.deepcopy(value)}


def extract_legacy_snapshot_facts(snapshot: dict[str, Any]) -> dict[str, Any]:
    """从旧 flat snapshot 提取可明确识别的事实，不运行算法。"""
    if not isinstance(snapshot, dict):
        raise TypeError("snapshot须为dict")

    consumed: set[str] = set()

    meta, used = _copy_if_present(snapshot, _META_MAP)
    consumed |= used
    meta["adapter"] = ADAPTER_VERSION

    calendar, used = _copy_if_present(snapshot, _CALENDAR_MAP)
    consumed |= used

    board: dict[str, Any] = {
        "taiyi": {},
        "eyes": {},
        "calculations": {},
        "generals": {},
        "doors": {},
    }

    for legacy_key, (section, field) in _SIMPLE_BOARD_FACTS.items():
        if legacy_key in snapshot and field not in board[section]:
            board[section][field] = copy.deepcopy(snapshot[legacy_key])
            consumed.add(legacy_key)

    for legacy_key, new_key in _CALC_FIELDS.items():
        if legacy_key in snapshot and new_key not in board["calculations"]:
            board["calculations"][new_key] = _calc_fact(snapshot[legacy_key])
            consumed.add(legacy_key)

    for legacy_key, new_key in _GENERAL_FIELDS.items():
        if legacy_key in snapshot and new_key not in board["generals"]:
            board["generals"][new_key] = {"palace": copy.deepcopy(snapshot[legacy_key])}
            consumed.add(legacy_key)

    # 只搬已知盘面“眼”事实；不调用五行、九宫或七术算法。
    if "文昌" in snapshot:
        board["eyes"]["skyeyes"] = _eye_fact(snapshot["文昌"])
        consumed.add("文昌")
    if "始擊" in snapshot:
        board["eyes"]["shiji"] = {"sector": copy.deepcopy(snapshot["始擊"])}
        consumed.add("始擊")
    elif "始击" in snapshot:
        board["eyes"]["shiji"] = {"sector": copy.deepcopy(snapshot["始击"])}
        consumed.add("始击")
    if "定目" in snapshot:
        board["eyes"]["settled_eye"] = {"sector": copy.deepcopy(snapshot["定目"])}
        consumed.add("定目")

    for legacy_key, new_key in _DOOR_FIELDS.items():
        if legacy_key in snapshot and new_key not in board["doors"]:
            board["doors"][new_key] = copy.deepcopy(snapshot[legacy_key])
            consumed.add(legacy_key)

    cycles: dict[str, Any] = {
        "three_bases": {},
        "five_blessings": {},
        "big_wander": {},
        "small_wander": {},
        "four_taiyi": {},
    }
    for legacy_key, (section, field) in _CYCLE_FIELDS.items():
        if legacy_key in snapshot and field not in cycles[section]:
            cycles[section][field] = copy.deepcopy(snapshot[legacy_key])
            consumed.add(legacy_key)

    quarantined = sorted(key for key in snapshot if key in _QUARANTINED_LEGACY_KEYS)
    unported = sorted(
        key for key in snapshot
        if key not in consumed and key not in _QUARANTINED_LEGACY_KEYS and key != "v2"
    )

    return {
        "meta": _normalize_legacy_json_containers(meta),
        "calendar": _normalize_legacy_json_containers(calendar),
        "board": _normalize_legacy_json_containers(board),
        "cycles": _normalize_legacy_json_containers(cycles),
        "consumed_legacy_keys": sorted(consumed),
        "quarantined_legacy_keys": quarantined,
        "unported_legacy_keys": unported,
    }


def build_v2_from_legacy_snapshot(
    snapshot: dict[str, Any],
    *,
    analysis: dict[str, Any] | None = None,
    modern: dict[str, Any] | None = None,
    source_variants: dict[str, Any] | None = None,
    scenario: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """用旧 snapshot 的事实 + 显式结构化结果构建 v2。

    analysis/modern 必须由调用方显式传入；不会读取旧“軍事戰略”“運籌博弈分析”
    或旧七术顶层中文断语来冒充新结构。
    """
    facts = extract_legacy_snapshot_facts(snapshot)

    compat = {
        "legacy_top_level": True,
        "legacy_schema": "pan-v1-flat",
        "adapter": ADAPTER_VERSION,
        "consumed_legacy_keys": facts["consumed_legacy_keys"],
        "quarantined_legacy_keys": facts["quarantined_legacy_keys"],
        "unported_legacy_keys": facts["unported_legacy_keys"],
        "legacy_analysis_promoted": False,
        "legacy_modern_promoted": False,
    }

    return build_pan_v2(
        meta=facts["meta"],
        calendar=facts["calendar"],
        board=facts["board"],
        cycles=facts["cycles"],
        analysis=copy.deepcopy(analysis or {}),
        modern=copy.deepcopy(modern or {}),
        source_variants=copy.deepcopy(source_variants or {}),
        compat=compat,
        scenario=copy.deepcopy(scenario) if scenario is not None else None,
    )


def attach_v2_to_snapshot(
    snapshot: dict[str, Any],
    *,
    analysis: dict[str, Any] | None = None,
    modern: dict[str, Any] | None = None,
    source_variants: dict[str, Any] | None = None,
    scenario: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """返回带 v2 的旧 snapshot 副本；不原地修改调用方对象。"""
    if not isinstance(snapshot, dict):
        raise TypeError("snapshot须为dict")
    result = copy.deepcopy(snapshot)
    result["v2"] = build_v2_from_legacy_snapshot(
        snapshot,
        analysis=analysis,
        modern=modern,
        source_variants=source_variants,
        scenario=scenario,
    )
    return result
