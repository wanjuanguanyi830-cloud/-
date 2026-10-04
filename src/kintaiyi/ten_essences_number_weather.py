"""C59 十精太乙数天气断语层。

消费 C54 太乙数，但不重算数值。
所有合/冲/挟/并等关系必须由调用方显式提供；不从位置自动推关系。
"""

from __future__ import annotations

import copy
from typing import Any

C59_VERSION = "taiyi-c59-ten-essence-number-weather-v1"

ALLOWED_RELATIONS = frozenset({
    "合太乙",
    "冲太乙",
    "合天目",
    "太乙挟天目",
    "合飞鸟",
    "与天地并",
    "与主计合",
    "与天地相当",
    "与太乙飞鸟合",
})

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙统宗宝鉴",
        "section": "明十精太乙所主术·太乙数",
        "witness_volumes": [18, 20],
    },
    "collation": [
        {"work": "太乙金镜式经", "section": "推太乙数法"},
        {"work": "武经总要", "section": "十精太乙数"},
        {"work": "三才世纬", "role": "later_collation"},
    ],
}

DIRECT_NUMBER_RULES = {
    30: {
        "effects": ["日晕", "大风"],
        "status": "direct_parallel",
    },
    40: {
        "effects": ["阴雨", "黄雾"],
        "status": "direct_parallel",
    },
}

NUMBER_50_VARIANT = {
    "status": "source_punctuation_or_clause_variant_unresolved",
    "tongzong_online": "数得五十，与天目相合，日晕（句读近似合并）",
    "jinjing": "数得五十与天目合旺相，日晕",
    "wujing_zongyao": "数得五十，日晕大风；数得天目旺相合，日晕",
    "canonical_standalone_50_effects": None,
    "safe_intersection_when_50_and_tianmu_wangxiang": ["日晕"],
    "policy": "不把武经的50单独‘日晕大风’静默覆盖统宗/金镜合天目读法。",
}

RELATION_RULES = {
    "合太乙": {
        "effects": ["日晕", "大风"],
        "status": "direct_parallel",
    },
    "冲太乙": {
        "effects": ["日晕", "风起"],
        "status": "direct_parallel",
    },
    "太乙挟天目": {
        "effects": ["阴雨", "日晕", "大风"],
        "status": "direct_parallel",
    },
    "与天地并": {
        "effects": ["日晕"],
        "status": "direct_parallel",
        "source_numbers": {"天": 10, "地": 9},
    },
    "与主计合": {
        "effects": ["日晕"],
        "status": "direct_or_collated",
        "source_note": "武经一见证并见‘主计八合’",
    },
    "与天地相当": {
        "effects": ["大风"],
        "status": "direct_parallel",
        "source_numbers": {"天": 10, "地": 9},
    },
    "与太乙飞鸟合": {
        "effects": ["疾风"],
        "status": "direct_parallel",
    },
}

FLYBIRD_PALACE_RULE = {
    "relation": "合飞鸟",
    "required_palaces": [6, 8, 9],
    "effects": ["日晕"],
    "status": "direct_parallel",
}

TIANMU_RULE = {
    "relation": "合天目",
    "required_qi_state": "旺相",
    "effects": ["日晕"],
    "status": "collation_direct_primary_clause_ambiguous",
}

LEGACY_AUDIT = {
    "function": "yunqi.shijing_shu",
    "numeric_core_equivalent": True,
    "wrapper_canonical_equivalent": False,
    "issues": [
        "旧wrapper把数值层与天气层混在一起",
        "旧50断语未保存统宗/金镜与武经句读差异",
        "旧10/5分支并非当前直接条文中的独立天气特例",
        "旧默认‘视与太乙冲合而断风雨’过于泛化",
    ],
}


def _validate_c54(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError("number_result须为dict")
    if value.get("rule_id") != "C54-TAIYI-NUMBER":
        raise ValueError("number_result必须来自C54-TAIYI-NUMBER")
    if value.get("source_profile") != "tongzong_ten_essences_number":
        raise ValueError("C54 source_profile不匹配")
    n = value.get("taiyi_number")
    if not isinstance(n, int) or not 1 <= n <= 72:
        raise ValueError("C54结果缺合法taiyi_number")
    return value


def _validate_relations(value: list[str] | None) -> tuple[list[str], bool]:
    if value is None:
        return [], False
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError("relations须为字符串list或None")
    unknown = [item for item in value if item not in ALLOWED_RELATIONS]
    if unknown:
        raise ValueError(f"未知C59关系：{unknown[0]}")
    return list(dict.fromkeys(value)), True


def taiyi_number_weather_omens(
    number_result: dict[str, Any],
    *,
    relations: list[str] | None = None,
    tianmu_qi_state: str | None = None,
    flybird_palace: int | None = None,
) -> dict[str, Any]:
    """解释C54太乙数的显式天气证据，不从盘内自动生成关系。"""
    base = _validate_c54(number_result)
    number = base["taiyi_number"]
    relations_value, checked = _validate_relations(relations)

    if tianmu_qi_state not in (None, "旺相", "非旺相", "休囚"):
        raise ValueError("tianmu_qi_state须为旺相/非旺相/休囚或None")
    if flybird_palace is not None and (
        not isinstance(flybird_palace, int)
        or isinstance(flybird_palace, bool)
        or flybird_palace not in range(1, 10)
    ):
        raise ValueError("flybird_palace须为1..9或None")

    matched: list[dict[str, Any]] = []
    pending: list[str] = []

    # 数值自身直接条文
    if number in DIRECT_NUMBER_RULES:
        rule = DIRECT_NUMBER_RULES[number]
        matched.append({
            "kind": "number",
            "number": number,
            "effects": copy.deepcopy(rule["effects"]),
            "source_status": rule["status"],
        })
    elif number == 50:
        matched.append({
            "kind": "number_variant",
            "number": 50,
            "effects": None,
            "source_status": NUMBER_50_VARIANT["status"],
            "witness_variants": copy.deepcopy(NUMBER_50_VARIANT),
        })

    # 显式关系
    for relation in relations_value:
        if relation in RELATION_RULES:
            rule = RELATION_RULES[relation]
            matched.append({
                "kind": "relation",
                "relation": relation,
                "effects": copy.deepcopy(rule["effects"]),
                "source_status": rule["status"],
                "source_numbers": copy.deepcopy(rule.get("source_numbers")),
                "source_note": rule.get("source_note"),
            })
            continue

        if relation == "合天目":
            if tianmu_qi_state is None:
                pending.append("合天目须显式给tianmu_qi_state")
                continue
            if tianmu_qi_state == "旺相":
                matched.append({
                    "kind": "relation",
                    "relation": relation,
                    "effects": copy.deepcopy(TIANMU_RULE["effects"]),
                    "source_status": TIANMU_RULE["status"],
                })
            continue

        if relation == "合飞鸟":
            if flybird_palace is None:
                pending.append("合飞鸟须显式给flybird_palace")
                continue
            if flybird_palace in FLYBIRD_PALACE_RULE["required_palaces"]:
                matched.append({
                    "kind": "relation",
                    "relation": relation,
                    "flybird_palace": flybird_palace,
                    "effects": copy.deepcopy(FLYBIRD_PALACE_RULE["effects"]),
                    "source_status": FLYBIRD_PALACE_RULE["status"],
                })

    # 50 + 天目旺相的安全交集
    fifty_tianmu_safe = (
        number == 50
        and "合天目" in relations_value
        and tianmu_qi_state == "旺相"
    )
    if fifty_tianmu_safe:
        matched.append({
            "kind": "safe_variant_intersection",
            "number": 50,
            "relation": "合天目",
            "qi_state": "旺相",
            "effects": copy.deepcopy(
                NUMBER_50_VARIANT["safe_intersection_when_50_and_tianmu_wangxiang"]
            ),
            "source_status": "cross_witness_safe_intersection",
        })

    if not checked:
        pending.append("须显式检查数与太乙/天目/飞鸟/天地/主计关系；无关系时传空list")

    unresolved = [
        row for row in matched
        if row.get("source_status") == NUMBER_50_VARIANT["status"]
    ]

    return {
        "schema_version": "1.0",
        "canonical": C59_VERSION,
        "rule_id": "C59-TAIYI-NUMBER-WEATHER",
        "source_profile": "tongzong_ten_essences_number_weather",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "number_result": copy.deepcopy(base),
        "taiyi_number": number,
        "relations": relations_value,
        "relations_checked": checked,
        "tianmu_qi_state": tianmu_qi_state,
        "flybird_palace": flybird_palace,
        "matched_omens": matched,
        "number_50_variant": copy.deepcopy(NUMBER_50_VARIANT) if number == 50 else None,
        "unresolved_variant_count": len(unresolved),
        "status": "partial_explicit_evidence" if pending else "explicit_evidence_complete",
        "pending": list(dict.fromkeys(pending)),
        "auto_relation_inference_used": False,
        "legacy_audit": copy.deepcopy(LEGACY_AUDIT),
        "policy": (
            "C59只消费C54太乙数并解释显式关系；"
            "30/40可直接断，50保留句读异文。"
            "不把数值、位置和合会自动拼成关系。"
        ),
    }


def c59_catalog() -> dict[str, Any]:
    return {
        "canonical": C59_VERSION,
        "rule_id": "C59-TAIYI-NUMBER-WEATHER",
        "source_profile": "tongzong_ten_essences_number_weather",
        "direct_number_rules": copy.deepcopy(DIRECT_NUMBER_RULES),
        "number_50_variant": copy.deepcopy(NUMBER_50_VARIANT),
        "relation_rules": copy.deepcopy(RELATION_RULES),
        "flybird_palace_rule": copy.deepcopy(FLYBIRD_PALACE_RULE),
        "tianmu_rule": copy.deepcopy(TIANMU_RULE),
        "legacy_audit": copy.deepcopy(LEGACY_AUDIT),
        "auto_relation_inference_used": False,
    }
