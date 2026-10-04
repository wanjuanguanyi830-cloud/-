"""C65 卷七天乙 / 地乙 / 直符同宫灾应显式证据层。

来源：《太乙统宗宝鉴》卷七三神各自条下的“与X同宫”断语。

边界：
- 本模块不读取 C64 位置；
- 调用方必须显式给 same_palace=True/False；
- 只实现卷七三神条下直接列出的 pair；
- 未在本批直接条文出现的 pair 不以对称、类推或常识补造。
"""

from __future__ import annotations

import copy
from typing import Any

C65_VERSION = "taiyi-c65-volume7-three-spirit-conjunctions-v1"

ENTITY_ORDER = ("天乙", "地乙", "直符", "四神", "大游", "小游")
CANONICAL_ENTITIES = frozenset(ENTITY_ORDER)

NAME_ALIASES = {
    "太游": "大游",
    "太遊": "大游",
    "大遊": "大游",
    "小遊": "小游",
    "四神水宿": "四神",
}

LEGACY_NAME_AUDIT = {
    "值符": {
        "canonical_name": "直符",
        "status": "legacy_or_title_variant",
        "default_alias_enabled": False,
    },
}

PAIR_RULES: dict[tuple[str, str], dict[str, Any]] = {
    ("天乙", "地乙"): {
        "source_section": "明天乙太乙金神所主术",
        "effects": [
            "兵戈发",
            "土工兴废",
            "农桑有伤",
            "百姓交兵结雠",
            "盗贼侵攘",
            "人民愁困",
        ],
        "status": "primary_direct_normalized_core",
    },
    ("天乙", "直符"): {
        "source_section": "明天乙太乙金神所主术",
        "effects": ["火旱", "刀兵", "饥馑", "疾困"],
        "status": "primary_direct",
    },
    ("天乙", "四神"): {
        "source_section": "明天乙太乙金神所主术",
        "effects": ["水涝", "霜雪", "兵盗为患", "舟车不通"],
        "status": "primary_direct",
    },
    ("天乙", "大游"): {
        "source_section": "明天乙太乙金神所主术",
        "effects": ["兵丧祸乱", "饥馑", "民流"],
        "status": "primary_direct",
    },
    ("天乙", "小游"): {
        "source_section": "明天乙太乙金神所主术",
        "effects": ["下凌于上", "不利有为"],
        "status": "primary_direct",
    },
    ("地乙", "直符"): {
        "source_section": "明地乙太乙土神所主术",
        "effects": ["火旱", "兵盗", "土工大兴", "人民灾疾", "五谷不成"],
        "status": "primary_direct",
    },
    ("地乙", "四神"): {
        "source_section": "明地乙太乙土神所主术",
        "effects": ["水旱不调", "民多疾困", "地生妖异"],
        "status": "primary_direct",
    },
    ("地乙", "大游"): {
        "source_section": "明地乙太乙土神所主术",
        "effects": ["兵丧大作", "荒俭民流", "贼盗啸聚"],
        "status": "primary_direct",
    },
    ("地乙", "小游"): {
        "source_section": "明地乙太乙土神所主术",
        "effects": ["土工大兴", "法令暴虐", "致生兵盗"],
        "status": "primary_direct",
    },
    ("直符", "四神"): {
        "source_section": "明直符太乙火神所主术",
        "effects": [
            "水旱不调",
            "四序失节",
            "民饥疾疫",
            "多生兵盗",
            "水火刀兵之厄",
        ],
        "status": "primary_direct_normalized_core",
    },
    ("直符", "大游"): {
        "source_section": "明直符太乙火神所主术",
        "effects": ["兵丧民流", "五谷无成", "灾横暴起"],
        "status": "primary_direct",
    },
    ("直符", "小游"): {
        "source_section": "明直符太乙火神所主术",
        "effects": ["风火兵革", "人民不安"],
        "status": "primary_direct",
    },
}

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "volume": 7,
    "sections": [
        "明天乙太乙金神所主术",
        "明地乙太乙土神所主术",
        "明直符太乙火神所主术",
    ],
    "collation": [
        {
            "work": "三才世纬",
            "role": "later_collation",
            "scope": "三神同宫断语与360/36行宫结构",
        }
    ],
    "policy": (
        "effects采用直接见证稳定核心；OCR词形不稳处只正规化语义核心，"
        "不以另一书补造统宗未列pair。"
    ),
}

POSITION_BOUNDARY = {
    "position_runtime": "C64",
    "position_module": "state_spirit_cycles",
    "auto_position_lookup_used": False,
    "auto_same_palace_inference_used": False,
    "policy": "C65不读取C64结果自动比较宫位；same_palace必须由调用方显式声明。",
}


def canonical_entity_name(
    name: str,
    *,
    allow_legacy_zhifu_alias: bool = False,
) -> str:
    if not isinstance(name, str):
        raise TypeError("神名须为字符串")
    if name in CANONICAL_ENTITIES:
        return name
    if name in NAME_ALIASES:
        return NAME_ALIASES[name]
    if name == "值符":
        if allow_legacy_zhifu_alias:
            return "直符"
        raise ValueError("值符不是C65 canonical名称；兼容时显式开启alias")
    raise ValueError("未知C65同宫对象")


def _pair_key(first: str, second: str) -> tuple[str, str]:
    if first == second:
        raise ValueError("同宫pair须为两个不同对象")
    a = ENTITY_ORDER.index(first)
    b = ENTITY_ORDER.index(second)
    return (first, second) if a < b else (second, first)


def same_palace_omen(
    first: str,
    second: str,
    *,
    same_palace: bool | None,
    allow_legacy_zhifu_alias: bool = False,
) -> dict[str, Any]:
    """解释显式同宫证据；不从位置runtime自动推同宫。"""
    a = canonical_entity_name(
        first,
        allow_legacy_zhifu_alias=allow_legacy_zhifu_alias,
    )
    b = canonical_entity_name(
        second,
        allow_legacy_zhifu_alias=allow_legacy_zhifu_alias,
    )
    key = _pair_key(a, b)
    rule = PAIR_RULES.get(key)

    if same_palace not in (None, True, False):
        raise TypeError("same_palace须为bool或None")

    pending: list[str] = []
    matched_omens: list[dict[str, Any]] = []

    if same_palace is None:
        pending.append("须显式确认两对象是否同宫；C65不从C64自动判断")
        status = "same_palace_unchecked"
    elif same_palace is False:
        status = "not_same_palace"
    elif rule is None:
        status = "same_palace_no_direct_c65_rule"
    else:
        status = "explicit_same_palace_rule_matched"
        matched_omens.append({
            "pair": list(key),
            "effects": copy.deepcopy(rule["effects"]),
            "source_section": rule["source_section"],
            "source_status": rule["status"],
        })

    return {
        "schema_version": "1.0",
        "canonical": C65_VERSION,
        "rule_id": "C65-THREE-SPIRIT-SAME-PALACE",
        "source_profile": "tongzong_volume7_three_spirit_conjunctions",
        "first": a,
        "second": b,
        "pair": list(key),
        "same_palace": same_palace,
        "direct_rule_available": rule is not None,
        "matched_omens": matched_omens,
        "status": status,
        "pending": pending,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
        "policy": (
            "只解释卷七天乙/地乙/直符条下直接列出的同宫pair；"
            "未列pair不以对称扩张之外的类推补断，不读取C64位置自动制造同宫。"
        ),
    }


def c65_catalog() -> dict[str, Any]:
    return {
        "canonical": C65_VERSION,
        "rule_id": "C65-THREE-SPIRIT-SAME-PALACE",
        "source_profile": "tongzong_volume7_three_spirit_conjunctions",
        "pair_rules": copy.deepcopy(PAIR_RULES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
        "legacy_name_audit": copy.deepcopy(LEGACY_NAME_AUDIT),
    }
