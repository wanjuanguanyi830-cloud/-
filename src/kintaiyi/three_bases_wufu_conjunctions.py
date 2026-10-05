"""C74 三基 / 五福同宫关系显式层。

来源：《太乙统宗宝鉴》卷六 / 卷七见证。
本层只处理君基、臣基、民基、五福四者之间六个 pair。

边界：
- 不读取 C66 / C67 自动比较位置；
- same_palace 必须显式给 True/False/None；
- 五福条“同宫在初交之始”的附加断语要求 initial_conjunction 显式输入；
- 同一 pair 在“三基条”和“五福条”中的附加细节分别保存，不揉成单一伪原文；
- 五福条另见“君基相冲”属于不同关系，不在本同宫层自动应用。
"""

from __future__ import annotations

import copy
from typing import Any

C74_VERSION = "taiyi-c74-three-bases-wufu-conjunctions-v1"

ENTITY_ORDER = ("君基", "臣基", "民基", "五福")
ENTITIES = frozenset(ENTITY_ORDER)

PAIR_RULES: dict[tuple[str, str], dict[str, Any]] = {
    ("君基", "臣基"): {
        "source_sections": ["明君基太乙所主术"],
        "base_effects": [
            "君臣际会",
            "君治以道",
            "臣辅克忠",
            "国殷民安",
            "万物咸遂",
        ],
        "wufu_effects": [],
        "initial_conjunction_effects": [],
        "status": "direct_single_section",
    },
    ("君基", "民基"): {
        "source_sections": ["明君基太乙所主术"],
        "base_effects": [
            "务农桑",
            "安百姓",
            "出入有名",
            "使人以时",
            "巡狩省方观民风",
        ],
        "wufu_effects": [],
        "initial_conjunction_effects": [],
        "status": "direct_single_section_normalized_core",
    },
    ("臣基", "民基"): {
        "source_sections": ["明臣基太乙所主术"],
        "base_effects": [
            "下贤者进朝",
            "民安其业",
            "政讼和平",
            "百姓丰厚",
        ],
        "wufu_effects": [],
        "initial_conjunction_effects": [],
        "status": "direct_single_section",
    },
    ("君基", "五福"): {
        "source_sections": ["明君基太乙所主术", "明五福太乙所主术"],
        "base_effects": [
            "皇室巩固",
            "海宇肃清",
            "君国有嘉祥福瑞之庆",
        ],
        "wufu_effects": [
            "人君福寿祚享",
        ],
        "initial_conjunction_effects": [
            "合生后储太子",
        ],
        "status": "direct_two_sections_layered",
        "adjacent_non_same_palace_clause": {
            "relation": "五福与君基相冲",
            "effect": "草冠之君",
            "applied_in_c74": False,
            "reason": "相冲不是同宫关系，留待独立关系层。",
        },
    },
    ("臣基", "五福"): {
        "source_sections": ["明臣基太乙所主术", "明五福太乙所主术"],
        "base_effects": [
            "利为宰辅",
            "贵极人臣",
            "常亲帝座",
            "任其大事",
            "临大治乱皆致亨通",
            "所临分野人民丰稔",
            "世出英杰",
        ],
        "wufu_effects": [
            "福利辅宰",
        ],
        "initial_conjunction_effects": [
            "贤相当生贵人之家",
        ],
        "status": "direct_two_sections_layered",
    },
    ("民基", "五福"): {
        "source_sections": ["明民基太乙所主术", "明五福太乙所主术"],
        "base_effects": [
            "其民富寿",
            "贤福之人生于民家",
        ],
        "wufu_effects": [
            "四民乐业",
            "天下熙和",
        ],
        "initial_conjunction_effects": [
            "其分富贵人生于白屋之家",
        ],
        "status": "direct_two_sections_layered",
    },
}

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "witness_volumes": [6, 7],
    "volume_status": "witness_volume_variant",
    "sections": [
        "明君基太乙所主术",
        "明臣基太乙所主术",
        "明民基太乙所主术",
        "明五福太乙所主术",
    ],
    "collation": {
        "ngj": "卷七见证",
        "cadal": "卷六见证",
        "status": "core_pair_meanings_concordant_with_ocr_variants",
    },
}

POSITION_BOUNDARY = {
    "three_bases_position_runtime": "C66",
    "wufu_position_runtime": "C67",
    "auto_position_lookup_used": False,
    "auto_same_palace_inference_used": False,
    "policy": "C74不调用C66/C67自动判断同宫；关系证据必须显式输入。",
}


def _entity(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("对象名须为字符串")
    if name not in ENTITIES:
        raise ValueError("对象须为君基/臣基/民基/五福")
    return name


def _pair_key(first: str, second: str) -> tuple[str, str]:
    if first == second:
        raise ValueError("同宫pair须为两个不同对象")
    a = ENTITY_ORDER.index(first)
    b = ENTITY_ORDER.index(second)
    return (first, second) if a < b else (second, first)


def same_palace_relation(
    first: str,
    second: str,
    *,
    same_palace: bool | None,
    initial_conjunction: bool | None = None,
) -> dict[str, Any]:
    """解释三基/五福显式同宫关系，不从位置 runtime 自动推断。"""
    a = _entity(first)
    b = _entity(second)
    key = _pair_key(a, b)
    rule = PAIR_RULES[key]

    if same_palace not in (None, True, False):
        raise TypeError("same_palace须为bool或None")
    if initial_conjunction not in (None, True, False):
        raise TypeError("initial_conjunction须为bool或None")

    has_wufu = "五福" in key
    if not has_wufu and initial_conjunction is not None:
        raise ValueError("initial_conjunction仅用于含五福的同宫pair")
    if same_palace is False and initial_conjunction is True:
        raise ValueError("不同宫时不能声明同宫初交")
    if same_palace is None and initial_conjunction is not None:
        raise ValueError("未确认同宫时不能判断同宫初交")

    applied_effects: list[dict[str, Any]] = []
    pending: list[str] = []

    if same_palace is None:
        status = "same_palace_unchecked"
        pending.append("须显式确认是否同宫；C74不从C66/C67自动判断")
    elif same_palace is False:
        status = "not_same_palace"
    else:
        status = "explicit_same_palace_rule_matched"
        if rule["base_effects"]:
            applied_effects.append({
                "layer": "base_section",
                "effects": copy.deepcopy(rule["base_effects"]),
                "source_sections": [rule["source_sections"][0]],
            })
        if rule["wufu_effects"]:
            applied_effects.append({
                "layer": "wufu_section",
                "effects": copy.deepcopy(rule["wufu_effects"]),
                "source_sections": ["明五福太乙所主术"],
            })
        if rule["initial_conjunction_effects"]:
            if initial_conjunction is True:
                applied_effects.append({
                    "layer": "wufu_initial_conjunction",
                    "effects": copy.deepcopy(rule["initial_conjunction_effects"]),
                    "source_sections": ["明五福太乙所主术"],
                })
            elif initial_conjunction is None:
                pending.append("五福条另有“同宫在初交之始”附加断语，须显式检查initial_conjunction")
            else:
                # Explicitly checked and absent: no initial-conjunction effects.
                pass

    return {
        "schema_version": "1.0",
        "canonical": C74_VERSION,
        "rule_id": "C74-THREE-BASES-WUFU-SAME-PALACE",
        "source_profile": "tongzong_three_bases_wufu_relations",
        "first": a,
        "second": b,
        "pair": list(key),
        "same_palace": same_palace,
        "initial_conjunction": initial_conjunction,
        "applied_effects": applied_effects,
        "pending": pending,
        "status": status,
        "source_rule_status": rule["status"],
        "source_sections": copy.deepcopy(rule["source_sections"]),
        "adjacent_non_same_palace_clause": copy.deepcopy(
            rule.get("adjacent_non_same_palace_clause")
        ),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
        "policy": (
            "同一pair在三基条与五福条的文字分别保存；"
            "C74只在显式same_palace=True时解释同宫规则，"
            "五福初交附加断语另须initial_conjunction=True。"
        ),
    }


def c74_catalog() -> dict[str, Any]:
    return {
        "canonical": C74_VERSION,
        "rule_id": "C74-THREE-BASES-WUFU-SAME-PALACE",
        "source_profile": "tongzong_three_bases_wufu_relations",
        "entities": list(ENTITY_ORDER),
        "pair_rules": copy.deepcopy(PAIR_RULES),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
    }
