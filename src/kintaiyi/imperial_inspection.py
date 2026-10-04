"""C62 《太乙统宗宝鉴》卷五：明天子巡狩之期术。

来源边界：
- 《太乙统宗宝鉴》卷五：太乙与天目在四维之岁为巡狩之期；
  出方以天目/文昌所临决之；另见囚、挟、格、对为行期之月条件。
- 《太乙金镜式经》卷十“推天子巡狩”独立参校：
  同样以太乙、天目在四维判巡狩，以主目四维所临定出方。

本模块只做：
1. 巡狩年资格；
2. 天目四维对应出方；
3. 显式记录囚/挟/格/对是否已检查。

本模块不做：
- 不从日期/积年自动推太乙或天目；
- 不从其他格局 runtime 自动制造囚/挟/格/对；
- 原文此段未给月份数值换算，因此绝不自行输出具体月份。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import GOD_POSITION, SIXTEEN, position

C62_VERSION = "taiyi-c62-imperial-inspection-v1"

CORNER_POSITIONS = frozenset(("乾", "艮", "巽", "坤"))

DIRECTION_BY_TIANMU = {
    "乾": {
        "source_god": "阴德",
        "direction": "东方",
    },
    "艮": {
        "source_god": "和德",
        "direction": "南方",
    },
    "巽": {
        "source_god": "大炅",
        "direction": "西方",
    },
    "坤": {
        "source_god": "大武",
        "direction": "北方",
    },
}

MONTH_PATTERNS = frozenset(("囚", "挟", "格", "对"))
PATTERN_ALIASES = {"挾": "挟", "對": "对"}

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙统宗宝鉴",
        "volume": 5,
        "section": "明天子巡狩之期术",
        "year_rule": "太乙与天目在四维之岁，则为巡狩之期",
        "direction_rule": "以天目文昌所临而决之",
        "month_condition": "太乙囚挟格对之下，是谓行期之月",
        "fallback": "若不巡狩，则临轩并遣使按行风俗",
    },
    "collation": {
        "work": "太乙金镜式经",
        "volume": 10,
        "section": "推天子巡狩",
        "year_rule": "太乙与天目在四维之岁则为天子巡狩",
        "direction_rule": "以主目所临起处决之",
        "fallback": "若不出则遣使者按行风俗",
    },
    "west_name_witness": {
        "stable_position": "巽",
        "stable_direction": "西方",
        "jinjing_name": "大炅",
        "tongzong_online_ocr_variants": ["太昊", "太靈"],
        "canonical_policy": "以稳定的巽位→西方为规则事实；神名异读留证，不反写为第二套方向公式。",
    },
}

LEGACY_BOUNDARY = {
    "legacy_flat_field": "明天子巡狩之期術",
    "migrate_whole": False,
    "reason": (
        "旧flat可能已把巡狩年、出方、行月条件揉成展示文本；"
        "C62要求太乙位、天目位与月格局检查分别显式输入。"
    ),
}


def _normalize_pattern(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("month_patterns须为字符串list或None")
    normalized = PATTERN_ALIASES.get(value, value)
    if normalized not in MONTH_PATTERNS:
        raise ValueError("month_patterns仅允许囚/挟/格/对")
    return normalized


def _validate_patterns(value: list[str] | None) -> tuple[list[str], bool]:
    if value is None:
        return [], False
    if not isinstance(value, list):
        raise TypeError("month_patterns须为字符串list或None")
    normalized = [_normalize_pattern(item) for item in value]
    return list(dict.fromkeys(normalized)), True


def imperial_inspection(
    *,
    taiyi_position: str | int,
    tianmu_position: str | int,
    month_patterns: list[str] | None = None,
) -> dict[str, Any]:
    """判巡狩年与出方；月份只保存显式格局条件，不自行换算。"""
    taiyi = position(taiyi_position)
    tianmu = position(tianmu_position)
    patterns, patterns_checked = _validate_patterns(month_patterns)

    taiyi_in_corner = taiyi in CORNER_POSITIONS
    tianmu_in_corner = tianmu in CORNER_POSITIONS
    inspection_year = taiyi_in_corner and tianmu_in_corner

    direction_record = DIRECTION_BY_TIANMU.get(tianmu) if inspection_year else None
    direction = direction_record["direction"] if direction_record else None

    month_condition_met = (
        inspection_year and patterns_checked and bool(set(patterns) & MONTH_PATTERNS)
    )
    pending: list[str] = []
    if inspection_year and not patterns_checked:
        pending.append("巡狩年已成立；行期之月须显式检查太乙是否见囚/挟/格/对")
    if inspection_year and patterns_checked and not patterns:
        pending.append("已显式检查月份格局，但未见囚/挟/格/对；本条不自行给出行月")

    status = "not_inspection_year"
    if inspection_year:
        status = (
            "inspection_year_month_condition_checked"
            if patterns_checked
            else "inspection_year_month_condition_unchecked"
        )

    return {
        "schema_version": "1.0",
        "canonical": C62_VERSION,
        "rule_id": "C62-IMPERIAL-INSPECTION",
        "source_profile": "tongzong_volume5_imperial_inspection",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "taiyi_position": taiyi,
        "tianmu_position": tianmu,
        "taiyi_in_corner": taiyi_in_corner,
        "tianmu_in_corner": tianmu_in_corner,
        "inspection_year": inspection_year,
        "direction": direction,
        "direction_basis": (
            copy.deepcopy(direction_record) if direction_record is not None else None
        ),
        "month_patterns": patterns,
        "month_patterns_checked": patterns_checked,
        "month_condition_met": month_condition_met,
        "month_number": None,
        "month_number_computation_supported": False,
        "fallback_if_not_inspection": (
            "遣使按行风俗；统宗并见临轩百僚陪列"
            if not inspection_year
            else None
        ),
        "pending": pending,
        "status": status,
        "legacy_boundary": copy.deepcopy(LEGACY_BOUNDARY),
        "auto_taiyi_lookup_used": False,
        "auto_tianmu_lookup_used": False,
        "auto_pattern_inference_used": False,
        "policy": (
            "巡狩年须太乙与天目都显式落四维；出方只按天目四维映射。"
            "囚/挟/格/对只作为显式行月条件；因本条无月份数值换算，month_number恒为None。"
        ),
    }


def c62_catalog() -> dict[str, Any]:
    return {
        "canonical": C62_VERSION,
        "rule_id": "C62-IMPERIAL-INSPECTION",
        "source_profile": "tongzong_volume5_imperial_inspection",
        "corner_positions": sorted(CORNER_POSITIONS, key=SIXTEEN.index),
        "direction_by_tianmu": copy.deepcopy(DIRECTION_BY_TIANMU),
        "month_patterns": sorted(MONTH_PATTERNS),
        "month_number_computation_supported": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_boundary": copy.deepcopy(LEGACY_BOUNDARY),
    }
