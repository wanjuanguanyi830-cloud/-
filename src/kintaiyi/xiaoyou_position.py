"""C101 小游太乙所在：金镜 / 统宗 source-specific profiles。

共同稳定核心：
- 小周24；
- 每宫3年；
- 起一宫；
- 顺行八宫；
- 不入中五；
- 宫序 1,2,3,4,6,7,8,9。

来源差异：
- 《太乙金镜式经》：大周240；
- 《太乙统宗宝鉴》：纪元周360。

不得把两个外周压成一个“统一周期”。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C101_VERSION = "taiyi-c101-xiaoyou-position-source-profiles-v1"

PALACE_PATH = (1, 2, 3, 4, 6, 7, 8, 9)

PROFILES = {
    "jinjing": {
        "rule_id": "C101-XIAOYOU-JINJING",
        "source_profile": "jinjing_volume5_xiaoyou_position",
        "work": "太乙金镜式经",
        "section": "推小游太乙积年法",
        "outer_cycle_name": "大周",
        "outer_cycle": 240,
        "small_cycle": 24,
        "years_per_palace": 3,
        "status": "primary_direct",
    },
    "tongzong": {
        "rule_id": "C101-XIAOYOU-TONGZONG",
        "source_profile": "tongzong_volume7_xiaoyou_position",
        "work": "太乙统宗宝鉴",
        "section": "明小游太乙所在术",
        "outer_cycle_name": "纪元周",
        "outer_cycle": 360,
        "small_cycle": 24,
        "years_per_palace": 3,
        "status": "primary_direct",
    },
}

SOURCE_WITNESS = {
    "jinjing": {
        "url": "https://www.shidianguji.com/book/SK1615/chapter/1l9lira3cv4eh",
        "formula_core": (
            "置积以小游大周法二百四十去之，不尽以小周二十四除之，"
            "不尽以三约之为宫数；命起一宫，顺行八宫，不游中五。"
        ),
    },
    "tongzong": {
        "url": "https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppwvvwt996",
        "formula_core": (
            "置演上元甲子至所求积年，以小游纪元周法三百六十除之，"
            "不尽以宫法二十四去之；余以行宫率三约之而一；"
            "命起一宫，顺行八宫，不入中五。"
        ),
    },
}

RECENT_WORK_RECOVERY = {
    "branch": "codex/taiyi-base-motion-2026-10-04",
    "file": "rules/xiaoyou/xiaoyou.json",
    "file_commit": "3c9161b5e7b3",
    "file_commit_date": "2026-10-04T03:19:43Z",
    "recovered_core": {
        "path": list(PALACE_PATH),
        "small_cycle": 24,
        "years_per_palace": 3,
        "jinjing_outer_cycle": 240,
    },
    "status": "recovered_and_direct_source_reverified",
    "time_window_policy": "only_2026-10-04_and_2026-10-05_prior_work",
}

BOUNDARY = {
    "c47_relation": (
        "C47是小游轨运内外卦/重卦；C101是小游太乙所在宫。"
        "二者共享部分24/3节律不等于同一术层。"
    ),
    "auto_conjunction_omens": False,
    "auto_three_bases_relations": False,
    "policy": "C101只求位置；C91等关系层仍须显式same_palace证据。",
}


def _profile(name: str) -> dict[str, Any]:
    try:
        return PROFILES[name]
    except KeyError as exc:
        raise ValueError("source_profile须为jinjing/tongzong") from exc


def _cycle_count(value: int, cycle: int) -> tuple[int, int]:
    remainder = value % cycle
    count = remainder or cycle
    return remainder, count


def xiaoyou_position(
    accumulated_count: int,
    *,
    source_profile: str,
) -> dict[str, Any]:
    """按显式来源 profile 求小游太乙所在宫与入宫年。"""
    count = integer(accumulated_count, 1)
    spec = _profile(source_profile)

    outer_remainder, outer_count = _cycle_count(count, spec["outer_cycle"])
    small_remainder, small_count = _cycle_count(outer_count, spec["small_cycle"])

    zero_index = small_count - 1
    palace_index = zero_index // spec["years_per_palace"]
    year_in_palace = zero_index % spec["years_per_palace"] + 1
    palace = PALACE_PATH[palace_index]

    return {
        "schema_version": "1.0",
        "canonical": C101_VERSION,
        "rule_id": spec["rule_id"],
        "source_profile": spec["source_profile"],
        "profile_key": source_profile,
        "source_work": spec["work"],
        "source_section": spec["section"],
        "accumulated_count": count,
        "outer_cycle_name": spec["outer_cycle_name"],
        "outer_cycle": spec["outer_cycle"],
        "outer_remainder": outer_remainder,
        "outer_count": outer_count,
        "small_cycle": spec["small_cycle"],
        "small_remainder": small_remainder,
        "small_count": small_count,
        "years_per_palace": spec["years_per_palace"],
        "palace_index": palace_index + 1,
        "palace": palace,
        "palace_id": palace,
        "year_in_palace": year_in_palace,
        "path": list(PALACE_PATH),
        "excluded_palace": 5,
        "direction": "forward",
        "source_witness": copy.deepcopy(SOURCE_WITNESS[source_profile]),
        "recent_work_recovery": copy.deepcopy(RECENT_WORK_RECOVERY),
        "boundary": copy.deepcopy(BOUNDARY),
        "same_palace_omens_applied": False,
    }


def c101_catalog() -> dict[str, Any]:
    return {
        "canonical": C101_VERSION,
        "profiles": copy.deepcopy(PROFILES),
        "path": list(PALACE_PATH),
        "excluded_palace": 5,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "recent_work_recovery": copy.deepcopy(RECENT_WORK_RECOVERY),
        "boundary": copy.deepcopy(BOUNDARY),
        "default_profile": None,
        "source_profile_required": True,
    }
