"""C19 《太乙紫庭经》已定位篇目的静态主来源事实。

只录目前能从主来源正文直接支持的事实，不运行旧统宗算法。
"""

from __future__ import annotations

import copy
from typing import Any

SOURCE_FACTS_VERSION = "taiyi-c19-zitingjing-source-facts-v1"

NINE_STAR_FACTS = [
    {"star": "天蓬", "palace": 1, "region": "冀州", "auspice": "凶"},
    {"star": "天芮", "palace": 2, "region": "荆州", "auspice": "凶"},
    {"star": "天冲", "palace": 3, "region": "青州", "auspice": "凶"},
    {"star": "天辅", "palace": 4, "region": "徐州", "auspice": "吉"},
    {"star": "天禽", "palace": 5, "region": "豫州", "auspice": "吉"},
    {"star": "天心", "palace": 6, "region": "雍州", "auspice": "吉"},
    {"star": "天柱", "palace": 7, "region": "梁益州", "auspice": "凶"},
    {"star": "天任", "palace": 8, "region": "兖州", "auspice": "吉"},
    {"star": "天英", "palace": 9, "region": "扬州", "auspice": "凶"},
]

WENCHANG_CHANGE_FACTS = {
    "identity": {
        "heaven_name": "天目",
        "earth_name": "文昌",
        "element": "土",
        "role": "辅相",
    },
    "relations": [
        {"relation": "囚", "condition": "文昌与太乙同宫", "effect": "不利主人"},
        {"relation": "外迫", "condition": "文昌在太乙前一宫", "effect": "臣下有外谋"},
        {"relation": "内迫", "condition": "文昌在太乙后一宫", "effect": "臣下有内谋或后宫之私"},
        {"relation": "对", "condition": "文昌与太乙相冲", "effect": "臣下失礼，王纲不振"},
        {"relation": "二目相关", "condition": "文昌与始击同宫", "effect": "以旺相定主客胜负"},
    ],
    "two_eyes_groups": {
        "primary_text_home_favored": [1, 8, 3, 7],
        "primary_text_away_favored": [4, 9, 6, 2],
    },
    "palace_examples": [
        {"taiyi": 1, "wenchang": 9, "label": "对宫", "subject": "辅相"},
        {"taiyi": 2, "wenchang": 8, "label": "有变", "subject": "君父"},
        {"taiyi": 6, "wenchang": 4, "label": "有变", "subject": "宰辅将相"},
    ],
}

SOURCE_VARIANTS = {
    "wenchang_two_eyes_groups": {
        "primary_taiyi_zitingjing": {
            "home_favored": [1, 8, 3, 7],
            "away_favored": [4, 9, 6, 2],
        },
        "tongzong_volume6_collation_excerpt": {
            "home_favored": [8, 3, 7],
            "away_favored": [4, 9, 2, 6],
        },
        "status": "variant_requires_collation",
        "policy": (
            "主来源与统宗参校摘录在主方组上存在1宫差异；"
            "不得用参校本静默删去主来源的一宫。"
        ),
    }
}


def zitingjing_nine_star_source_facts() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "canonical": SOURCE_FACTS_VERSION,
        "source": "太乙紫庭经",
        "chapter": "释九宫所值九星",
        "facts": copy.deepcopy(NINE_STAR_FACTS),
        "cycle_note": {
            "value_star_cycle_years": 10,
            "source_statement": "九星配九宫，十年一易",
        },
        "computational_formula_promoted": False,
        "policy": (
            "本函数只保存主来源静态事实；"
            "不直接采用旧统宗太乙九星函数的大周900/小周90算法。"
        ),
    }


def zitingjing_wenchang_change_source_facts() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "canonical": SOURCE_FACTS_VERSION,
        "source": "太乙紫庭经",
        "chapter": "释天目变化",
        "facts": copy.deepcopy(WENCHANG_CHANGE_FACTS),
        "source_variants": copy.deepcopy(SOURCE_VARIANTS),
        "computational_formula_promoted": False,
        "policy": (
            "天目=文昌的关系规则直接来自主来源；"
            "如参校文本有异文，保留variant，不无痕合并。"
        ),
    }


def c19_source_fact_bundle() -> dict[str, Any]:
    return {
        "canonical": SOURCE_FACTS_VERSION,
        "primary_source": "zitingjing",
        "primary_source_title": "太乙紫庭经",
        "rules": {
            "taiyi_nine_stars": zitingjing_nine_star_source_facts(),
            "wenchang_changes": zitingjing_wenchang_change_source_facts(),
        },
        "implemented_as_source_facts_only": [
            "taiyi_nine_stars",
            "wenchang_changes",
        ],
        "not_yet_implemented_from_primary_text": [
            "wenchang_nine_stars",
            "shiji_changes",
            "three_banners",
            "nine_palace_nobles",
        ],
    }
