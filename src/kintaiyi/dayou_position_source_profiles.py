"""C107 大游太乙所在宫：金镜 / 统宗 source-specific profiles。

共同稳定核心：
- 小周 / 宫周 288；
- 每宫36年；
- 起七宫；
- 顺行八宫；
- 不入中五；
- 路径 7,8,9,1,2,3,4,6。

来源差异：
- 《太乙金镜式经》：元法4320，无统宗宫盈差34；
- 《太乙统宗宝鉴》：宫盈差34；算法层见大周2880；
  同条前文与平行见证明确宫周288。电子转录“小周三百八十八”
  与36×8及本条“二百八十八年一周”冲突，作为转录异读保留，
  不写入执行小周。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C107_VERSION = "taiyi-c107-dayou-position-source-profiles-v1"

PALACE_PATH = (7, 8, 9, 1, 2, 3, 4, 6)

PROFILES = {
    "jinjing": {
        "rule_id": "C107-DAYOU-JINJING",
        "source_profile": "jinjing_volume5_dayou_position",
        "work": "太乙金镜式经",
        "section": "推大游太乙所在",
        "epoch": "上元甲寅",
        "surplus_name": None,
        "surplus": 0,
        "outer_cycle_name": "元法",
        "outer_cycle": 4320,
        "secondary_cycle_metadata": {"纪法": 720},
        "small_cycle": 288,
        "years_per_palace": 36,
        "status": "primary_direct",
    },
    "tongzong": {
        "rule_id": "C107-DAYOU-TONGZONG",
        "source_profile": "tongzong_volume7_dayou_position",
        "work": "太乙统宗宝鉴",
        "section": "明太游太乙所主术",
        "epoch": "上元甲子",
        "surplus_name": "宫盈差",
        "surplus": 34,
        "outer_cycle_name": "太游大周法",
        "outer_cycle": 2880,
        "secondary_cycle_metadata": None,
        "small_cycle": 288,
        "years_per_palace": 36,
        "status": "primary_direct_with_numeric_collation",
    },
}

SOURCE_WITNESS = {
    "jinjing": {
        "url": "https://www.shidianguji.com/book/SK1615/chapter/1l9lira3cuf49",
        "formula_core": (
            "置上元甲寅所求积年，以元法四千三百二十去之；"
            "以大游小周法二百八十八去之；以三十六除之为宫数；"
            "命起七宫，顺行八宫，不游中五。"
        ),
        "historical_example_context": (
            "同卷另列开元十二年积13331与元法4320/纪法720/小周288参数。"
        ),
    },
    "tongzong": {
        "url": "https://www.shidianguji.com/zh/book/CADAL02094393/chapter/1lcppwvvwt996",
        "formula_core": (
            "置上元甲子至所求积年，加宫盈差三十四；"
            "算法转录见太游大周法二千八百八十；"
            "行宫率三十六；命起七宫，顺行八宫，不入中五。"
        ),
        "same_section_stable_statement": "其神三十六年考治一宫，二百八十八年一周而行其罚。",
        "small_cycle_transcription_variant": {
            "electronic_reading": "三百八十八",
            "execution_value": 288,
            "status": "resolved_numeric_transcription_conflict",
            "reason": (
                "同条前文明言二百八十八年一周；8宫×36年=288；"
                "《易学象数论》又明确宫周288、宫率36、宫盈差34。"
            ),
        },
        "parallel_witness": {
            "work": "易学象数论",
            "url": "https://www.shidianguji.com/book/SK0122/chapter/1kfib48aa4ahx",
            "statement": "宫周二百八十八，宫率三十六，宫盈差三十四；起七宫坤，顺行八宫。",
        },
    },
}

RECENT_WORK_RECOVERY = {
    "branch": "codex/taiyi-base-motion-2026-10-04",
    "file": "rules/dayou/dayou.json",
    "file_commit": "7f2d1b5dc74e",
    "file_commit_date": "2026-10-04T03:26:49Z",
    "recovered_core": {
        "jinjing_outer_cycle": 4320,
        "small_cycle": 288,
        "years_per_palace": 36,
        "path": list(PALACE_PATH),
    },
    "status": "recovered_and_direct_source_reverified",
    "time_window_policy": "only_2026-10-04_and_2026-10-05_prior_work",
}

BOUNDARY = {
    "c41_relation": (
        "C41是大游重卦/策数/动爻；C107是大游太乙所在宫。"
        "C107不调用C41，也不从C41反推行宫。"
    ),
    "auto_conjunction_omens": False,
    "auto_three_bases_relations": False,
    "policy": (
        "C107只求位置；C65/C91等同宫关系仍须显式same_palace证据。"
        "金镜与统宗参数不静默合并。"
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


def dayou_position(
    accumulated_count: int,
    *,
    source_profile: str,
) -> dict[str, Any]:
    """按显式来源 profile 求大游太乙所在宫与入宫年。"""
    count = integer(accumulated_count, 1)
    spec = _profile(source_profile)

    adjusted = count + spec["surplus"]
    outer_remainder, outer_count = _cycle_count(adjusted, spec["outer_cycle"])
    small_remainder, small_count = _cycle_count(outer_count, spec["small_cycle"])

    zero_index = small_count - 1
    palace_index = zero_index // spec["years_per_palace"]
    year_in_palace = zero_index % spec["years_per_palace"] + 1
    palace = PALACE_PATH[palace_index]

    return {
        "schema_version": "1.0",
        "canonical": C107_VERSION,
        "rule_id": spec["rule_id"],
        "source_profile": spec["source_profile"],
        "profile_key": source_profile,
        "source_work": spec["work"],
        "source_section": spec["section"],
        "epoch": spec["epoch"],
        "accumulated_count": count,
        "surplus_name": spec["surplus_name"],
        "surplus": spec["surplus"],
        "adjusted_count": adjusted,
        "outer_cycle_name": spec["outer_cycle_name"],
        "outer_cycle": spec["outer_cycle"],
        "outer_remainder": outer_remainder,
        "outer_count": outer_count,
        "secondary_cycle_metadata": copy.deepcopy(spec["secondary_cycle_metadata"]),
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


def c107_catalog() -> dict[str, Any]:
    return {
        "canonical": C107_VERSION,
        "profiles": copy.deepcopy(PROFILES),
        "path": list(PALACE_PATH),
        "excluded_palace": 5,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "recent_work_recovery": copy.deepcopy(RECENT_WORK_RECOVERY),
        "boundary": copy.deepcopy(BOUNDARY),
        "default_profile": None,
        "source_profile_required": True,
    }
