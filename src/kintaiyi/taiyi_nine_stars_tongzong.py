"""C124 《太乙统宗宝鉴》卷六太乙九星 source-specific runtime。

本模块与《太乙紫庭经》〈释九宫所值九星〉静态九宫表分层：
- 《紫庭》层保存九宫、九星、分野、吉凶的直接主来源表；
- C124 只实现《统宗》卷六“明太乙九星所值吉凶术 / 明九星行支干造化所主术”
  所给的动态直符与按年干布九星法。

当前采用 NGJ892411999009267118912 与 CADAL02055529 两个直接见证互校：
- 90 年一小周，900 年一大周；
- 星率以 10 年为一星；
- 命起天蓬，顺行九星；
- 元嘉至甲辰积 1121 年的原例应得“天禽直符，初入一年”，可反校星率为 10；
- 六甲年令当前直符伏本宫；乙、丙、丁及戊己庚辛壬癸按六干星宫锚点布置，
  然后顺九宫排其余八星。

不得把本模块的动态周期反填成《紫庭经》太乙九星 canonical。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer


C124_VERSION = "taiyi-c124-tongzong-taiyi-nine-stars-v1"
RULE_ID = "C124-TONGZONG-TAIYI-NINE-STARS"

STAR_TABLE = (
    {"index": 1, "star": "天蓬", "base_palace": 1, "stem_anchor": "戊", "region": "冀州", "fortune": "凶"},
    {"index": 2, "star": "天芮", "base_palace": 2, "stem_anchor": "己", "region": "荆州", "fortune": "凶"},
    {"index": 3, "star": "天冲", "base_palace": 3, "stem_anchor": "庚", "region": "青州", "fortune": "凶"},
    {"index": 4, "star": "天辅", "base_palace": 4, "stem_anchor": "辛", "region": "徐州", "fortune": "吉"},
    {"index": 5, "star": "天禽", "base_palace": 5, "stem_anchor": "壬", "region": "豫州", "fortune": "吉"},
    {"index": 6, "star": "天心", "base_palace": 6, "stem_anchor": "癸", "region": "雍州", "fortune": "吉"},
    {"index": 7, "star": "天柱", "base_palace": 7, "stem_anchor": "丁", "region": "梁益州", "fortune": "凶"},
    {"index": 8, "star": "天任", "base_palace": 8, "stem_anchor": "丙", "region": "兖州", "fortune": "吉"},
    {"index": 9, "star": "天英", "base_palace": 9, "stem_anchor": "乙", "region": "扬州", "fortune": "凶"},
)

STEM_FIXED_PALACE = {
    "乙": 9,
    "丙": 8,
    "丁": 7,
    "戊": 1,
    "己": 2,
    "庚": 3,
    "辛": 4,
    "壬": 5,
    "癸": 6,
}

SOURCE_EVIDENCE = {
    "ngj": {
        "witness_id": "NGJ892411999009267118912",
        "section": "明太乙九星所值吉凶术 / 明九星行支干造化所主术",
        "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny526c1g8iw",
        "facts": [
            "九十年为一小周，九百年为一大周",
            "命起天蓬，顺行九星",
            "六甲年当前直符伏本宫；六乙加九宫；六丙加八宫；余准此",
            "丙年天蓬直符例：天蓬八宫、天芮九宫、天冲一宫，顺次布九星",
        ],
    },
    "cadal": {
        "witness_id": "CADAL02055529",
        "section": "明太乙九星所直吉凶之术 / 明九星行支干造化所主术",
        "url": "https://www.shidianguji.com/book/CADAL02055529/chapter/1l5erk6w4nokn",
        "facts": [
            "九十年一小周，九百年为一大周",
            "余以星率十约之而一",
            "元嘉至甲辰积一千一百二十一年，得天禽为直符，初入一年",
        ],
    },
    "rate_resolution": {
        "selected_years_per_star": 10,
        "reason": (
            "CADAL直接见证读“星率十”；且1121原例按900/90/10恰得天禽直符、初入一年。"
            "个别OCR见证出现“星率九”时视为识读异文，不覆盖内证。"
        ),
    },
}

BOUNDARY = {
    "ziting_primary_static_table": "kintaiyi.zitingjing_primary.taiyi_nine_stars_primary",
    "cross_source_merge_allowed": False,
    "policy": (
        "C124是《统宗》卷六动态profile；《紫庭经》太乙九星仍以其直接正文静态表为primary。"
        "二者星名/九宫底表可互校，但周期与动态布星不得静默互相移植。"
    ),
}


def _direct_star(accumulated_count: int) -> tuple[dict[str, Any], int, int, int, int]:
    count = integer(accumulated_count, 1)

    large_remainder = count % 900
    large_count = large_remainder or 900

    small_remainder = large_count % 90
    small_count = small_remainder or 90

    zero_index = small_count - 1
    star_index = zero_index // 10
    year_in_star = zero_index % 10 + 1
    return STAR_TABLE[star_index], year_in_star, large_remainder, large_count, small_count


def _anchor_palace(direct_star: dict[str, Any], year_stem: str) -> int:
    if year_stem == "甲":
        return int(direct_star["base_palace"])
    if year_stem in STEM_FIXED_PALACE:
        return STEM_FIXED_PALACE[year_stem]
    raise ValueError("year_stem须为十天干")


def _distribution(anchor_palace: int) -> list[dict[str, Any]]:
    rows = []
    for offset, star in enumerate(STAR_TABLE):
        palace = ((anchor_palace - 1 + offset) % 9) + 1
        rows.append(
            {
                "star": star["star"],
                "current_palace": palace,
                "base_palace": star["base_palace"],
                "fortune": star["fortune"],
                "region": star["region"],
            }
        )
    return rows


def taiyi_nine_stars_tongzong(
    accumulated_count: int,
    *,
    year_stem: str | None = None,
) -> dict[str, Any]:
    """计算《统宗》卷六太乙九星直符；给年干时同时布九星。"""

    direct_star, year_in_star, large_remainder, large_count, small_count = _direct_star(
        accumulated_count
    )

    anchor = None
    distribution = None
    if year_stem is not None:
        anchor = _anchor_palace(direct_star, year_stem)
        distribution = _distribution(anchor)

    return {
        "schema_version": "1.0",
        "canonical": C124_VERSION,
        "rule_id": RULE_ID,
        "source_profile": "tongzong_volume6_taiyi_nine_stars",
        "accumulated_count": integer(accumulated_count, 1),
        "large_cycle": 900,
        "large_cycle_remainder": large_remainder,
        "large_cycle_count": large_count,
        "small_cycle": 90,
        "small_cycle_count": small_count,
        "years_per_star": 10,
        "direct_star_number": direct_star["index"],
        "direct_star": direct_star["star"],
        "year_in_star": year_in_star,
        "year_stem": year_stem,
        "direct_star_anchor_palace": anchor,
        "full_dynamic_distribution": distribution,
        "star_table": copy.deepcopy(list(STAR_TABLE)),
        "source_evidence": copy.deepcopy(SOURCE_EVIDENCE),
        "boundary": copy.deepcopy(BOUNDARY),
    }


def c124_catalog() -> dict[str, Any]:
    return {
        "canonical": C124_VERSION,
        "rule_id": RULE_ID,
        "source_profile": "tongzong_volume6_taiyi_nine_stars",
        "cycle": {
            "large_cycle": 900,
            "small_cycle": 90,
            "years_per_star": 10,
            "start_star": "天蓬",
            "direction": "顺行九星",
        },
        "star_table": copy.deepcopy(list(STAR_TABLE)),
        "stem_fixed_palace": copy.deepcopy(STEM_FIXED_PALACE),
        "source_evidence": copy.deepcopy(SOURCE_EVIDENCE),
        "boundary": copy.deepcopy(BOUNDARY),
    }
