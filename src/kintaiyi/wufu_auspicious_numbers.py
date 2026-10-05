"""C68 《太乙统宗宝鉴》五福吉算所利术。

本层只解释正文已经得到的“宫法所余”1..45，不从积年自动计算五福位置。
原因：
- 五福位置在 C67 按统宗/金镜 source profile 分离；
- 吉算正文只要求取“不满宫法所余”判所利对象；
- 不应把 C67 的盈差/外周选择静默带入 C68。

统宗当前可核直接见证将 1..45 分成十组：
- 尾数1 -> 君王
- 尾数2 -> 公侯
- 尾数3 -> 后妃
- 尾数4 -> 太子
- 尾数5 -> 民
- 6/16/26/36 -> 师帅
- 7/17/27/37 -> 上将军
- 8/18/28/38 -> 中将军
- 9/19/29/39 -> 下将军
- 10/20/30/40 -> 士卒

这里不是简单“个位数公式”的无证推断；每个集合均由正文逐项列举并写入表。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C68_VERSION = "taiyi-c68-wufu-auspicious-number-v1"

NUMBER_GROUPS = {
    "君王": (1, 11, 21, 31, 41),
    "公侯": (2, 12, 22, 32, 42),
    "后妃": (3, 13, 23, 33, 43),
    "太子": (4, 14, 24, 34, 44),
    "民": (5, 15, 25, 35, 45),
    "师帅": (6, 16, 26, 36),
    "上将军": (7, 17, 27, 37),
    "中将军": (8, 18, 28, 38),
    "下将军": (9, 19, 29, 39),
    "士卒": (10, 20, 30, 40),
}

NUMBER_TO_BENEFICIARY = {
    number: beneficiary
    for beneficiary, numbers in NUMBER_GROUPS.items()
    for number in numbers
}

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙统宗宝鉴",
        "section": "明五福吉算所利术",
        "witnesses": [
            {
                "id": "NGJ892411999009267118912",
                "volume": 7,
                "status": "direct",
                "cycle_text": "二百二十五年为一周，四十五年为一宫",
            },
            {
                "id": "CADAL02094393",
                "volume": 6,
                "status": "direct_collation",
                "cycle_text": "二百二十五年为一周，四十五年行一宫",
            },
        ],
    },
    "number_groups_status": "direct_lists_collated_across_two_tongzong_witnesses",
    "volume_status": "witness_volume_variant",
}

VARIANTS = {
    "title": {
        "readings": ["明五福吉算所利术", "明五福算所利术"],
        "canonical_selected": "明五福吉算所利术",
        "reason": "目录与多见证完整题名支持“吉算”。",
    },
    "beneficiary_2": {
        "ngj": "公侯",
        "cadal": "王侯臣宰",
        "stable_core": "公侯/王侯等贵臣阶层",
        "runtime_label": "公侯",
    },
    "beneficiary_5": {
        "ngj": "民",
        "cadal": "民",
        "other_witness": "庶民",
        "runtime_label": "民",
    },
    "later_250_cycle": {
        "source": "太白兵备统宗宝鉴/后期见证",
        "cycle_years": 250,
        "status": "source_variant_not_applied",
        "canonical_selected": None,
        "reason": "与统宗两直接见证225年一周冲突；C68只解释1..45余数，不选该周期。",
    },
}

C67_BOUNDARY = {
    "position_runtime": "C67",
    "auto_position_lookup_used": False,
    "auto_remainder_from_accumulated_count_used": False,
    "accepted_input": "explicit_remainder_1_to_45",
    "policy": (
        "C68不调用C67，不继承统宗+115/2250或金镜225位置profile；"
        "调用方须显式提供已经取得的宫法余数。"
    ),
}


def wufu_auspicious_beneficiary(remainder: int) -> dict[str, Any]:
    """按正文显式1..45吉算余数返回所利对象。"""
    value = integer(remainder, 1, 45)
    beneficiary = NUMBER_TO_BENEFICIARY[value]

    return {
        "schema_version": "1.0",
        "canonical": C68_VERSION,
        "rule_id": "C68-WUFU-AUSPICIOUS-NUMBER",
        "source_profile": "tongzong_wufu_auspicious_number",
        "remainder": value,
        "beneficiary": beneficiary,
        "group_numbers": list(NUMBER_GROUPS[beneficiary]),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "variants": copy.deepcopy(VARIANTS),
        "c67_boundary": copy.deepcopy(C67_BOUNDARY),
        "policy": (
            "只解释统宗正文逐项列出的1..45宫法余数；"
            "不把个位规律当作来源，不从积年或C67位置自动生成余数。"
        ),
    }


def c68_catalog() -> dict[str, Any]:
    return {
        "canonical": C68_VERSION,
        "rule_id": "C68-WUFU-AUSPICIOUS-NUMBER",
        "source_profile": "tongzong_wufu_auspicious_number",
        "number_groups": copy.deepcopy(NUMBER_GROUPS),
        "number_to_beneficiary": copy.deepcopy(NUMBER_TO_BENEFICIARY),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "variants": copy.deepcopy(VARIANTS),
        "c67_boundary": copy.deepcopy(C67_BOUNDARY),
    }
