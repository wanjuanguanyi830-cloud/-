"""C39 《太乙统宗宝鉴》卷十“五运六气”细表校勘。

本模块只保存已核表格与传本差异：
- 五运配五音；
- 六气配五行/化气；
- 太过、不及、平气纪名；
- 天会/岁会/逆会/辐辏枚举异文；
- 太乙天符判法仍需九宫天符等结构化输入，不以年干捷径代替。
"""

from __future__ import annotations

import copy
from typing import Any

C39_VERSION = "taiyi-c39-wuyun-volume10-collation-v1"

MOVEMENT_TONES = {
    "土": {"tone": "宫", "heaven_qi": "黄天"},
    "金": {"tone": "商", "heaven_qi": "素天"},
    "水": {"tone": "羽", "heaven_qi": "玄天"},
    "木": {"tone": "角", "heaven_qi": "苍天"},
    "火": {"tone": "徵", "heaven_qi": "丹天"},
}

SIX_QI_ELEMENTS = {
    "厥阴": {
        "element": "木", "qi": "风",
        "tongzong_witness": "厥阴风木风化", "collation": "风化",
    },
    "少阴": {
        "element": "火", "qi": "君火",
        "tongzong_witness": "少阴君火势化", "collation": "热化",
        "status": "ocr_or_textual_variant_preserved",
    },
    "太阴": {
        "element": "土", "qi": "湿",
        "tongzong_witness": "太阴温土雨化", "collation": "湿土雨化",
        "status": "ocr_or_textual_variant_preserved",
    },
    "少阳": {
        "element": "火", "qi": "相火",
        "tongzong_witness": "少阳相火水化", "collation": "暑化",
        "status": "ocr_or_textual_variant_preserved",
    },
    "阳明": {
        "element": "金", "qi": "燥",
        "tongzong_witness": "阳明燥金清化", "collation": "清化",
    },
    "太阳": {
        "element": "水", "qi": "寒",
        "tongzong_witness": "太阳寒水寒化", "collation": "寒化",
    },
}

# 统宗在线见证中个别字存在OCR/传本文字差异；不静默归一。
MOVEMENT_PERIOD_WITNESSES = {
    "太过": {
        "木": {"tongzong": "发生之纪", "collation": "发生之纪"},
        "火": {"tongzong": "赫曦之纪", "collation": "赫曦之纪"},
        "土": {"tongzong": "崇阜之纪", "collation": "敦阜之纪",
              "status": "textual_variant_preserved"},
        "金": {"tongzong": "坚成之纪", "collation": "坚成之纪"},
        "水": {"tongzong": "流衍之纪", "collation": "流衍之纪"},
    },
    "不及": {
        "木": {"tongzong": "委和之纪", "collation": "委和之纪"},
        "火": {"tongzong": "伏明之纪", "collation": "伏明之纪"},
        "土": {"tongzong": "卑坚之纪", "collation": "卑监之纪",
              "status": "ocr_or_textual_variant_preserved"},
        "金": {"tongzong": "从革之纪", "collation": "从革之纪"},
        "水": {"tongzong": "涸流之纪", "collation": "涸流之纪"},
    },
    "平气": {
        "木": {"tongzong": "敷和之纪", "collation": "敷和之纪"},
        "火": {"tongzong": "外明之纪", "collation": "升明之纪",
              "status": "ocr_correction_candidate_preserved"},
        "土": {"tongzong": "备化之纪", "collation": "备化之纪"},
        "金": {"tongzong": "主君之纪", "collation": "审平之纪",
              "status": "ocr_correction_candidate_preserved"},
        "水": {"tongzong": "静顺之纪", "collation": "静顺之纪"},
    },
}

MEETING_ENUM_WITNESSES = {
    "tongzong": {
        "source": "太乙统宗宝鉴",
        "items": ["天会", "岁会", "逆会"],
        "convergence": "三合辐辏则为太乙天符",
        "item_count": 3,
    },
    "taibai_bingbei": {
        "source": "太白兵备统宗宝鉴",
        "items": ["天会", "岁会", "逆会", "辐辏"],
        "convergence": "四类并列见证",
        "item_count": 4,
    },
}


def volume10_wuyun_collation() -> dict[str, Any]:
    """返回卷十已校基础表与仍未决的会类边界。"""
    return {
        "schema_version": "1.0",
        "canonical": C39_VERSION,
        "source_profile": "tongzong_volume10_wuyun_collation",
        "movement_tones": copy.deepcopy(MOVEMENT_TONES),
        "six_qi_elements": copy.deepcopy(SIX_QI_ELEMENTS),
        "movement_period_witnesses": copy.deepcopy(MOVEMENT_PERIOD_WITNESSES),
        "meeting_enum_witnesses": copy.deepcopy(MEETING_ENUM_WITNESSES),
        "core_tables_status": "collated",
        "meeting_enum_status": "source_variant_unresolved",
        "taiyi_tianfu_formula_status": "requires_structured_nine_palace_and_meeting_inputs",
        "year_stem_only_finalizes_taiguo_buji": False,
        "policy": (
            "五运配五音、六气配五行及三类纪名表已校；"
            "天会/岁会/逆会/辐辏枚举存在传本差异。"
            "不得仅凭年干阳阴把某年直接判为太过/不及，"
            "也不得在缺九宫天符/三旗合会输入时生成太乙天符。"
        ),
    }


def movement_tone(element: str) -> dict[str, Any]:
    if element not in MOVEMENT_TONES:
        raise ValueError("element须为木火土金水")
    return {
        "element": element,
        **copy.deepcopy(MOVEMENT_TONES[element]),
        "source_profile": "tongzong_volume10_wuyun_collation",
    }


def six_qi_element(qi_name: str) -> dict[str, Any]:
    if qi_name not in SIX_QI_ELEMENTS:
        raise ValueError("qi_name须为六气名")
    return {
        "qi_name": qi_name,
        **copy.deepcopy(SIX_QI_ELEMENTS[qi_name]),
        "source_profile": "tongzong_volume10_wuyun_collation",
    }


def movement_period_witness(state: str, element: str) -> dict[str, Any]:
    if state not in MOVEMENT_PERIOD_WITNESSES:
        raise ValueError("state须为太过/不及/平气")
    if element not in MOVEMENT_PERIOD_WITNESSES[state]:
        raise ValueError("element须为木火土金水")
    return {
        "state": state,
        "element": element,
        **copy.deepcopy(MOVEMENT_PERIOD_WITNESSES[state][element]),
        "canonical_selected": None,
    }


def meeting_enum_collation() -> dict[str, Any]:
    return {
        "canonical": C39_VERSION,
        "witnesses": copy.deepcopy(MEETING_ENUM_WITNESSES),
        "canonical_selected": None,
        "cross_source_merge": False,
        "status": "source_variant_unresolved",
    }
