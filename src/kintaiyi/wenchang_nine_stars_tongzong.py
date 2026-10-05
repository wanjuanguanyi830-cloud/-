"""C70 《太乙统宗宝鉴》卷六文昌九宫/九星 source-specific runtime。

本模块只选择一个明确见证：
- 《太乙统宗宝鉴》卷六 NGJ892411999009267118912。

该见证内部算法一致：
- 每星30年一宫；
- 大周2700；
- 小周270；
- 宫率30；
- 命起一宫文昌，顺行九宫。

它与 CADAL 见证“前文10年、算法30年”的内部冲突，以及《紫庭秘诀》
附篇正文未取得的问题，均保持分层，不据此宣布跨来源统一 canonical。

本模块只计算：
1. 当前直事文昌星；
2. 入本星第几年；
3. 若显式给 year_stem，则按正文“命加所求年干建禄之宫”给直事星落宫/分野。

不在 C70 推定九星完整动态分布。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C70_VERSION = "taiyi-c70-tongzong-wenchang-nine-stars-v1"

DIRECT_TEXT_EVIDENCE = {
    "witness_id": "NGJ892411999009267118912",
    "section": "明文昌九宫所主分野术",
    "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny526c1g8iw",
    "facts": {
        "star_names": ["文昌", "玄凤", "明维", "阴德", "招摇", "华明", "玄武", "玄冥", "维明"],
        "years_per_star": 30,
        "small_cycle": 270,
        "large_cycle": 2700,
        "rate": 30,
        "start": "一宫文昌",
        "direction": "顺行九宫",
        "landing_rule": "命加所求年干建禄之宫",
        "example": "甲辰年玄凤直事，十一年在青州；乙巳在徐",
    },
    "boundary": (
        "本证据只固定NGJ卷六profile；另有CADAL见证作每星十年并与算法口径冲突，"
        "保持独立异文；《紫庭秘诀》附篇正文未取得前不得反填。"
    ),
}

STAR_TABLE = (
    {"index": 1, "star": "文昌", "palace": "乾", "stem": "壬", "region": "冀州"},
    {"index": 2, "star": "玄凤", "palace": "离", "stem": "丁", "region": "荆州"},
    {"index": 3, "star": "明维", "palace": "艮", "stem": "甲", "region": "青州"},
    {"index": 4, "star": "阴德", "palace": "震", "stem": "乙", "region": "徐州"},
    {"index": 5, "star": "招摇", "palace": "中", "stem": "戊己", "region": "豫州"},
    {"index": 6, "star": "华明", "palace": "兑", "stem": "辛", "region": "雍州"},
    {"index": 7, "star": "玄武", "palace": "坤", "stem": "庚", "region": "梁益州"},
    {"index": 8, "star": "玄冥", "palace": "坎", "stem": "癸", "region": "兖州"},
    {"index": 9, "star": "维明", "palace": "巽", "stem": "丙", "region": "扬州"},
)

STEM_LANDING = {
    "甲": {"palace": "艮", "region": "青州", "table_index": 3},
    "乙": {"palace": "震", "region": "徐州", "table_index": 4},
    "丙": {"palace": "巽", "region": "扬州", "table_index": 9},
    "丁": {"palace": "离", "region": "荆州", "table_index": 2},
    "戊": {"palace": "中", "region": "豫州", "table_index": 5},
    "己": {"palace": "中", "region": "豫州", "table_index": 5},
    "庚": {"palace": "坤", "region": "梁益州", "table_index": 7},
    "辛": {"palace": "兑", "region": "雍州", "table_index": 6},
    "壬": {"palace": "乾", "region": "冀州", "table_index": 1},
    "癸": {"palace": "坎", "region": "兖州", "table_index": 8},
}

STEM_DISASTER_GROUPS = {
    "甲乙": ["疾疫", "风雷"],
    "丙丁": ["火旱", "口舌妖言"],
    "庚辛": ["兵戈盗贼", "攻战死丧"],
    "壬癸": ["霪沉淋雨", "大水", "后妃不安"],
    "戊己": ["土工", "蝗虫", "崩陷", "丧亡"],
}

SOURCE_WITNESS = {
    "primary_for_this_profile": {
        "work": "太乙统宗宝鉴",
        "volume": 6,
        "witness_id": "NGJ892411999009267118912",
        "section": "明文昌九宫所主分野术",
        "cycle": {
            "prose_years_per_star": 30,
            "large_cycle": 2700,
            "small_cycle": 270,
            "rate": 30,
            "internally_consistent": True,
        },
        "example": (
            "甲辰年玄凤直事，十一年在青州；乙巳在徐。"
            "用于证明直事星周期与年干落宫/分野是两层。"
        ),
    },
    "variants_not_merged": {
        "tongzong_cadal": {
            "prose_rate": 10,
            "algorithm_rate": 30,
            "small_cycle": 270,
            "large_cycle": 2700,
            "status": "internal_conflict",
        },
        "sancai_shiwei": {
            "rate": 30,
            "large_cycle_reading": 270,
            "small_cycle_reading": 270,
            "status": "external_collation_with_cycle_number_variant",
        },
        "zitingjing_appendix": {
            "section": "附太乙文昌九星值宫术",
            "status": "catalog_attested_primary_text_pending",
            "direct_text_available": False,
        },
    },
}

NAME_VARIANTS = {
    "third": ["明维", "明雄"],
    "fourth": ["阴德", "阴玄"],
    "fifth": ["招摇", "招煥"],
    "ninth": ["维明", "雄明"],
    "policy": "C70只采用NGJ见证读法；其他读法保留为variant，不无痕归一。",
}

LEGACY_AUDIT = {
    "identifier": "config.wenchang_nine_stars",
    "canonical_equivalent": False,
    "promotion_allowed": False,
    "problems": [
        "旧星名表混入文曲/昭摇/立华等非C70-NGJ读法",
        "旧年干落宫表丁→巽9，直接表应丁→离2",
        "旧年干落宫表壬→中5，直接表应壬→乾1",
        "旧完整分布循环计算了gong变量却未使用，实际仍输出固定星宫表",
        "旧实现未保存统宗见证内部10/30年冲突与紫庭附篇正文pending边界",
    ],
    "replacement": "C70-TONGZONG-WENCHANG-NINE-STARS",
}

DYNAMIC_DISTRIBUTION_BOUNDARY = {
    "supported": False,
    "reason": (
        "当前直接正文足以计算直事星并按年干给其落宫/分野；"
        "九星其余八星如何随直事星整体动态重排，C70不由旧代码反推。"
    ),
}


def _stem_group(stem: str) -> str:
    for group in STEM_DISASTER_GROUPS:
        if stem in group:
            return group
    raise ValueError("year_stem须为十天干")


def wenchang_nine_star_tongzong(
    accumulated_count: int,
    *,
    year_stem: str | None = None,
) -> dict[str, Any]:
    """按统宗卷六NGJ见证计算直事星；年干落宫为可选显式层。"""
    count = integer(accumulated_count, 1)

    big_remainder = count % 2700
    big_cycle_count = big_remainder or 2700

    small_remainder = big_cycle_count % 270
    small_cycle_count = small_remainder or 270

    zero_index = small_cycle_count - 1
    star_index = zero_index // 30
    year_in_star = zero_index % 30 + 1
    star = STAR_TABLE[star_index]

    landing = None
    disaster_group = None
    disaster_effects = None
    if year_stem is not None:
        if year_stem not in STEM_LANDING:
            raise ValueError("year_stem须为十天干")
        landing = copy.deepcopy(STEM_LANDING[year_stem])
        disaster_group = _stem_group(year_stem)
        disaster_effects = copy.deepcopy(STEM_DISASTER_GROUPS[disaster_group])

    return {
        "schema_version": "1.0",
        "canonical": C70_VERSION,
        "rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
        "source_profile": "tongzong_volume6_ngj_wenchang_nine_stars",
        "accumulated_count": count,
        "large_cycle": 2700,
        "large_cycle_remainder": big_remainder,
        "large_cycle_count": big_cycle_count,
        "small_cycle": 270,
        "small_cycle_remainder": small_remainder,
        "small_cycle_count": small_cycle_count,
        "years_per_star": 30,
        "direct_star_number": star_index + 1,
        "direct_star": star["star"],
        "year_in_star": year_in_star,
        "year_stem": year_stem,
        "direct_star_landing": landing,
        "stem_disaster_group": disaster_group,
        "stem_disaster_effects": disaster_effects,
        "full_dynamic_distribution": None,
        "dynamic_distribution_boundary": copy.deepcopy(DYNAMIC_DISTRIBUTION_BOUNDARY),
        "name_variants": copy.deepcopy(NAME_VARIANTS),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_audit": copy.deepcopy(LEGACY_AUDIT),
        "direct_text_evidence": copy.deepcopy(DIRECT_TEXT_EVIDENCE),
        "cross_source_canonical_selected": None,
        "policy": (
            "C70是统宗NGJ source-specific runtime，不等于紫庭附篇canonical。"
            "30年周期只对本见证成立；其他见证10/30及大周异读继续并列。"
        ),
    }


def c70_catalog() -> dict[str, Any]:
    return {
        "canonical": C70_VERSION,
        "rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
        "source_profile": "tongzong_volume6_ngj_wenchang_nine_stars",
        "star_table": copy.deepcopy(list(STAR_TABLE)),
        "stem_landing": copy.deepcopy(STEM_LANDING),
        "stem_disaster_groups": copy.deepcopy(STEM_DISASTER_GROUPS),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "name_variants": copy.deepcopy(NAME_VARIANTS),
        "legacy_audit": copy.deepcopy(LEGACY_AUDIT),
        "direct_text_evidence": copy.deepcopy(DIRECT_TEXT_EVIDENCE),
        "dynamic_distribution_boundary": copy.deepcopy(DYNAMIC_DISTRIBUTION_BOUNDARY),
        "cross_source_canonical_selected": None,
    }
