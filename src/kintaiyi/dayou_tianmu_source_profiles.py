"""C104 大游天目：金镜 / 统宗 source-specific profiles。

共同路径：
- 起天道；
- 顺行十六神；
- 大武、阴德各重留一算；
- 共18步。

来源参数：
- 金镜：元法72，再周法18；
- 统宗：加神盈差214，大周180，再小周18。

两来源不得静默合并。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import GOD_POSITION, integer

C104_VERSION = "taiyi-c104-dayou-tianmu-source-profiles-v1"

TIANMU_PATH = (
    "天道",
    "大武",
    "大武",
    "武德",
    "太簇",
    "阴主",
    "阴德",
    "阴德",
    "大义",
    "地主",
    "阳德",
    "和德",
    "吕申",
    "高丛",
    "太阳",
    "大炅",
    "大神",
    "大威",
)

PROFILES = {
    "jinjing": {
        "rule_id": "C104-DAYOU-TIANMU-JINJING",
        "source_profile": "jinjing_volume5_dayou_tianmu",
        "work": "太乙金镜式经",
        "section": "推大游天目所在法",
        "surplus_name": None,
        "surplus": 0,
        "outer_cycle_name": "天目元法",
        "outer_cycle": 72,
        "small_cycle_name": "天目周法",
        "small_cycle": 18,
        "status": "primary_direct",
    },
    "tongzong": {
        "rule_id": "C104-DAYOU-TIANMU-TONGZONG",
        "source_profile": "tongzong_volume7_dayou_tianmu",
        "work": "太乙统宗宝鉴",
        "section": "明太游天目所主术",
        "surplus_name": "神盈差",
        "surplus": 214,
        "outer_cycle_name": "太游大周法",
        "outer_cycle": 180,
        "small_cycle_name": "小周法",
        "small_cycle": 18,
        "status": "primary_direct",
    },
}

SOURCE_WITNESS = {
    "jinjing": {
        "url": "https://ctext.org/wiki.pl?chapter=606969&if=gb",
        "formula_core": (
            "置上元以来积年以天目元法七十二去之，不尽以天目周法十八去之；"
            "命起天道，顺行十六神，遇大武阴德重留一算。"
        ),
    },
    "tongzong": {
        "urls": [
            "https://www.shidianguji.com/book/CADAL02055529/chapter/1l5erk9igsxeb",
            "https://www.shidianguji.com/book/SK0122/chapter/1l9rdmvwzdrm7",
        ],
        "formula_core": (
            "置积年加神盈差二百一十四；大周一百八十，小周一十八；"
            "起天道，顺行十六神，遇大武阴德重留一算。"
        ),
        "ocr_boundary": (
            "统宗一电子转录起点字形见“天通”类OCR；"
            "《易学象数论》及金镜平行文明确为天道，故规范路径取天道并保留OCR边界。"
        ),
    },
}

RECENT_WORK_RECOVERY = {
    "branch": "codex/taiyi-base-motion-2026-10-04",
    "file": "rules/dayou/tianmu.json",
    "file_commit": "7f2d1b5dc74e",
    "file_commit_date": "2026-10-04T03:26:49Z",
    "recovered": {
        "jinjing_outer_cycle": 72,
        "small_cycle": 18,
        "path": list(TIANMU_PATH),
    },
    "old_reference_note": (
        "10月4日记录当时把%180/+214旧实现仅列deprecated_reference；"
        "C104经直接统宗/象数论来源重核后，确认+214/180/18本身有来源，"
        "因此应建立独立tongzong profile，而不是继续整体隔离。"
    ),
    "time_window_policy": "only_2026-10-04_and_2026-10-05_prior_work",
}

BOUNDARY = {
    "dayou_palace_runtime": "separate_source_specific_layer",
    "auto_dayou_palace_lookup_used": False,
    "relation_omens_applied": False,
    "policy": (
        "C104只求大游天目位置；不自动读取大游太乙所在宫，"
        "不应用卷七天目所主治理断语或同宫关系。"
    ),
}


def _profile(name: str) -> dict[str, Any]:
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError("source_profile须为jinjing/tongzong") from exc


def _cycle_count(value: int, cycle: int) -> tuple[int, int]:
    remainder = value % cycle
    return remainder, remainder or cycle


def dayou_tianmu_position(
    accumulated_count: int,
    *,
    source_profile: str,
) -> dict[str, Any]:
    """按显式来源 profile 求大游天目18步位置。"""
    count = integer(accumulated_count, 1)
    spec = _profile(source_profile)

    adjusted = count + spec["surplus"]
    outer_remainder, outer_count = _cycle_count(adjusted, spec["outer_cycle"])
    small_remainder, small_count = _cycle_count(outer_count, spec["small_cycle"])

    step_index = small_count - 1
    god = TIANMU_PATH[step_index]
    position = GOD_POSITION[god]

    return {
        "schema_version": "1.0",
        "canonical": C104_VERSION,
        "rule_id": spec["rule_id"],
        "source_profile": spec["source_profile"],
        "profile_key": source_profile,
        "source_work": spec["work"],
        "source_section": spec["section"],
        "accumulated_count": count,
        "surplus_name": spec["surplus_name"],
        "surplus": spec["surplus"],
        "adjusted_count": adjusted,
        "outer_cycle_name": spec["outer_cycle_name"],
        "outer_cycle": spec["outer_cycle"],
        "outer_remainder": outer_remainder,
        "outer_count": outer_count,
        "small_cycle_name": spec["small_cycle_name"],
        "small_cycle": spec["small_cycle"],
        "small_remainder": small_remainder,
        "small_count": small_count,
        "step_number": small_count,
        "god": god,
        "position": position,
        "path": list(TIANMU_PATH),
        "source_witness": copy.deepcopy(SOURCE_WITNESS[source_profile]),
        "recent_work_recovery": copy.deepcopy(RECENT_WORK_RECOVERY),
        "boundary": copy.deepcopy(BOUNDARY),
    }


def c104_catalog() -> dict[str, Any]:
    return {
        "canonical": C104_VERSION,
        "profiles": copy.deepcopy(PROFILES),
        "path": list(TIANMU_PATH),
        "path_length": len(TIANMU_PATH),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "recent_work_recovery": copy.deepcopy(RECENT_WORK_RECOVERY),
        "boundary": copy.deepcopy(BOUNDARY),
        "default_profile": None,
        "source_profile_required": True,
    }
