"""C95 2026-10-04 snapshot collector 回收。

从旧分支 codex/c1-c7-canonical 的 kintaiyi.py 回收
collect_core_snapshot() 的接口思想，但不恢复旧 Taiyi facade 或旧周期公式。

职责：
- 从已有 calendar/board engine 收集最小原始事实；
- 每个 primitive 对同一 style 只调用一次；
- 年积年明确使用 style=0；
- 日太乙明确使用 style=2；
- 不做任何来源规则计算、不构建 v2、不推断日期。
"""

from __future__ import annotations

import copy
from typing import Any

C95_VERSION = "taiyi-c95-snapshot-collector-recovery-v1"

CORE_METHODS = {
    "wenchang_sector": "skyeyes",
    "shiji_sector": "sf",
    "dingmu_sector": "se",
    "home_cal": "home_cal",
    "away_cal": "away_cal",
    "fixed_cal": "set_cal",
    "home_general": "home_general",
    "home_assistant": "home_vgen",
    "away_general": "away_general",
    "away_assistant": "away_vgen",
}

RECOVERY = {
    "branch": "codex/c1-c7-canonical",
    "file": "src/kintaiyi/kintaiyi.py",
    "relevant_commits": [
        {
            "sha": "e3ca5af6d434",
            "date": "2026-10-04T19:53:06Z",
            "role": "legacy delegation/facade refactor",
        },
        {
            "sha": "18635deed7b9",
            "date": "2026-10-04T19:53:43Z",
            "role": "canonical snapshot facade and collector",
        },
        {
            "sha": "266d69628c05",
            "date": "2026-10-04T19:55:13Z",
            "role": "selection/compatibility hardening",
        },
    ],
    "time_window_policy": "only_2026-10-04_and_2026-10-05_prior_work",
    "recovered_symbols": ["collect_core_snapshot", "selection_validation_intent"],
    "not_recovered": [
        "TaiyiCanonicalMixin旧周期委托",
        "Taiyi(snapshot).pan旧聚合路径",
        "project_legacy_pan旧覆盖逻辑",
    ],
}

BOUNDARY = {
    "builds_pan_v2": False,
    "calls_cycle_rules": False,
    "calls_analysis_rules": False,
    "infers_calendar": False,
    "output": "raw_core_snapshot",
    "next_layer": "C30 pan_v2_contract / caller-owned explicit assembly",
}


def _int_range(name: str, value: int, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name}须为整数")
    if not low <= value <= high:
        raise ValueError(f"{name}须在{low}..{high}")
    return value


def validate_snapshot_selection(
    snapshot: dict[str, Any],
    *,
    ji_style: int,
    taiyi_acumyear: int,
) -> dict[str, Any]:
    """校验显式 selection，不修改 snapshot。"""
    if not isinstance(snapshot, dict):
        raise TypeError("snapshot须为dict")
    style = _int_range("ji_style", ji_style, 0, 4)
    profile = _int_range("taiyi_acumyear", taiyi_acumyear, 0, 3)

    for name, requested in (
        ("ji_style", style),
        ("taiyi_acumyear", profile),
    ):
        if name in snapshot and snapshot[name] != requested:
            raise ValueError(f"snapshot的{name}与请求不符")

    return {
        "canonical": C95_VERSION,
        "ji_style": style,
        "taiyi_acumyear": profile,
        "selection_matches": True,
    }


def collect_core_snapshot(
    engine: Any,
    ji_style: int,
    taiyi_acumyear: int,
) -> dict[str, Any]:
    """从现有 engine 一次性收集盘面原始事实。

    engine 必须自己提供积年/太乙/眼/算/将等 primitive。
    本函数只调用并搬运，不实现任何古法。
    """
    style = _int_range("ji_style", ji_style, 0, 4)
    profile = _int_range("taiyi_acumyear", taiyi_acumyear, 0, 3)

    acc = engine.accnum(style, profile)
    taiyi = engine.ty(style, profile)

    year_acc = acc if style == 0 else engine.accnum(0, profile)
    day_taiyi = taiyi if style == 2 else engine.ty(2, profile)

    data: dict[str, Any] = {
        "collector_version": C95_VERSION,
        "accumulated_year": copy.deepcopy(acc),
        "taiyi_palace": copy.deepcopy(taiyi),
        "year_accumulated_year": copy.deepcopy(year_acc),
        "day_taiyi_palace": copy.deepcopy(day_taiyi),
        "ji_style": style,
        "taiyi_acumyear": profile,
    }

    for field, method_name in CORE_METHODS.items():
        method = getattr(engine, method_name)
        data[field] = copy.deepcopy(method(style, profile))

    data["collector_boundary"] = copy.deepcopy(BOUNDARY)
    data["recovery"] = copy.deepcopy(RECOVERY)
    return data


def c95_catalog() -> dict[str, Any]:
    return {
        "canonical": C95_VERSION,
        "core_methods": copy.deepcopy(CORE_METHODS),
        "recovery": copy.deepcopy(RECOVERY),
        "boundary": copy.deepcopy(BOUNDARY),
    }
