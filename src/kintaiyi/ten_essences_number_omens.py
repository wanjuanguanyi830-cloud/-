"""C59 十精太乙数天气 / 合会断语层。

与 C54 分层：
- C54 只计算 1..72 的太乙数；
- C59 只解释显式给出的太乙数与合会证据，不自行重算积年。

直接来源：
- 《太乙统宗宝鉴》卷十八 / 卷二十“十曰太乙数”；
- 《太乙金镜式经》卷七“推太乙数法”；
- 《武经总要》后集卷十八十精太乙数条。

重要异文：
- 数30、40的天气断语跨见证稳定；
- 数50在《武经总要》读作“数得五十，日晕大风”；
  《金镜》与《统宗》转写更接近“数得五十，与天目旺相合，日晕”。
  C59 不强选，固定 source_variant_unresolved。
- 旧 yunqi.shijing_shu 把数10/5当独立天气/天地数断语，直接见证不支持这种独立规则。
"""

from __future__ import annotations

import copy
from typing import Any

C59_VERSION = "taiyi-c59-ten-essences-number-omens-v1"

ALLOWED_RELATIONS = frozenset({
    "合太乙",
    "冲太乙",
    "合天目",
    "太乙挟天目",
    "合飞鸟",
    "与天地并",
    "与天地相当",
    "合太乙飞鸟",
    "合主计",
})

QI_STATES = frozenset({"旺相", "非旺相", "休囚"})

SOURCE_WITNESS = {
    "tongzong": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [18, 20],
        "scope": "十曰太乙数及天气合会断语",
        "fifty_reading": "转写近似“数得五十，与天目旺相合，日晕”",
    },
    "jinjing": {
        "work": "太乙金镜式经",
        "volume": 7,
        "scope": "推太乙数法",
        "fifty_reading": "“数得五十与天目合旺相日晕”",
    },
    "wujing_zongyao": {
        "work": "武经总要",
        "volume": "后集卷十八",
        "scope": "十精太乙数天气断语",
        "fifty_reading": "“数得五十，日晕大风；数得天目旺相合，日晕”",
    },
}

SPECIAL_NUMBER_RULES: dict[int, dict[str, Any]] = {
    30: {
        "effects": ["日晕", "大风"],
        "status": "direct_parallel",
    },
    40: {
        "effects": ["阴雨", "黄雾"],
        "status": "direct_parallel",
    },
    50: {
        "effects": None,
        "status": "source_segmentation_variant_unresolved",
        "witness_variants": {
            "tongzong": "数得五十 + 与天目旺相合 → 日晕（转写句读近似）",
            "jinjing": "数得五十 + 与天目合旺相 → 日晕",
            "wujing_zongyao": "数得五十 → 日晕、大风；另数与天目旺相合 → 日晕",
        },
        "canonical_selected": None,
    },
}

RELATION_RULES: dict[str, dict[str, Any]] = {
    "合太乙": {
        "effects": ["日晕", "大风"],
        "status": "direct_parallel",
    },
    "冲太乙": {
        "effects": ["日晕", "风起"],
        "status": "direct_parallel",
    },
    "合天目": {
        "requires_qi_state": "旺相",
        "effects": ["日晕"],
        "status": "direct_or_segmentation_collated",
    },
    "太乙挟天目": {
        "effects": ["阴雨", "日晕", "大风"],
        "status": "direct_parallel",
    },
    "合飞鸟": {
        "requires_flybird_palaces": [6, 8, 9],
        "effects": ["日晕"],
        "status": "direct_parallel",
    },
    "与天地并": {
        "effects": ["日晕"],
        "status": "direct_parallel",
    },
    "与天地相当": {
        "effects": ["大风"],
        "status": "direct_parallel",
    },
    "合太乙飞鸟": {
        "effects": ["疾风"],
        "status": "tongzong_wujing_direct",
    },
    "合主计": {
        "requires_heaven_calculation": 10,
        "requires_earth_calculation": 9,
        "wujing_requires_main_calculation": 8,
        "effects": ["日晕"],
        "status": "source_detail_variant",
        "witness_variants": {
            "jinjing": "天十地九，数与主计合，日晕",
            "wujing_zongyao": "天十地九，数与主计八合，日晕",
        },
    },
}

LEGACY_SPECIAL_AUDIT = {
    10: {
        "legacy_statement": "天数，与计目合则大风",
        "direct_special_number_rule": False,
        "reason": (
            "直接见证只见“天十地九”作为合主计条的上下文，"
            "未见“数得十”即可独立断大风。"
        ),
    },
    5: {
        "legacy_statement": "地数",
        "direct_special_number_rule": False,
        "reason": "直接太乙数天气条未见“数得五”独立断语。",
    },
    50: {
        "legacy_statement": "黄雾尘，与天目合则旺相",
        "direct_special_number_rule": False,
        "reason": (
            "黄雾属于数40稳定断语；数50存在句读异文，"
            "旧wrapper把两层混合，不能作为canonical。"
        ),
    },
}


def _validate_number(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("taiyi_number须为整数")
    if value < 1 or value > 72:
        raise ValueError("taiyi_number须为1..72")
    return value


def _validate_optional_positive_int(name: str, value: int | None) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name}须为正整数或None")
    if value <= 0:
        raise ValueError(f"{name}须为正整数或None")
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


def taiyi_number_omens(
    taiyi_number: int,
    *,
    relations: list[str] | None = None,
    tianmu_qi_state: str | None = None,
    flybird_palace: int | None = None,
    heaven_calculation: int | None = None,
    earth_calculation: int | None = None,
    main_calculation: int | None = None,
) -> dict[str, Any]:
    """解释显式太乙数和合会证据；不从积年或其他runtime自动推关系。"""
    number = _validate_number(taiyi_number)
    relation_list, relations_checked = _validate_relations(relations)

    if tianmu_qi_state is not None and tianmu_qi_state not in QI_STATES:
        raise ValueError("tianmu_qi_state须为旺相/非旺相/休囚或None")
    if flybird_palace is not None and (
        not isinstance(flybird_palace, int)
        or isinstance(flybird_palace, bool)
        or flybird_palace not in range(1, 10)
    ):
        raise ValueError("flybird_palace须为1..9或None")

    heaven_calculation = _validate_optional_positive_int(
        "heaven_calculation", heaven_calculation
    )
    earth_calculation = _validate_optional_positive_int(
        "earth_calculation", earth_calculation
    )
    main_calculation = _validate_optional_positive_int(
        "main_calculation", main_calculation
    )

    matched: list[dict[str, Any]] = []
    pending: list[str] = []
    unresolved: list[dict[str, Any]] = []

    special = SPECIAL_NUMBER_RULES.get(number)
    if special is not None:
        if special["effects"] is None:
            unresolved.append({
                "kind": "special_number",
                "taiyi_number": number,
                "source_status": special["status"],
                "witness_variants": copy.deepcopy(special["witness_variants"]),
                "canonical_selected": None,
            })
        else:
            matched.append({
                "kind": "special_number",
                "taiyi_number": number,
                "effects": copy.deepcopy(special["effects"]),
                "source_status": special["status"],
            })

    for relation in relation_list:
        rule = RELATION_RULES[relation]

        if relation == "合天目":
            if tianmu_qi_state is None:
                pending.append("数与天目合：须显式给tianmu_qi_state")
                continue
            if tianmu_qi_state != "旺相":
                continue

        if relation == "合飞鸟":
            if flybird_palace is None:
                pending.append("数与飞鸟合：须显式给flybird_palace")
                continue
            if flybird_palace not in rule["requires_flybird_palaces"]:
                continue

        if relation == "合主计":
            if heaven_calculation is None or earth_calculation is None:
                pending.append("数与主计合：须显式给heaven_calculation与earth_calculation")
                continue
            if (
                heaven_calculation != rule["requires_heaven_calculation"]
                or earth_calculation != rule["requires_earth_calculation"]
            ):
                continue
            if main_calculation is None:
                pending.append(
                    "数与主计合：武经明见主计八，金镜仅见主计合；"
                    "须给main_calculation以保存见证边界"
                )
                continue
            if main_calculation != rule["wujing_requires_main_calculation"]:
                unresolved.append({
                    "kind": "relation",
                    "relation": relation,
                    "source_status": "source_detail_variant_unresolved",
                    "witness_variants": copy.deepcopy(rule["witness_variants"]),
                    "canonical_selected": None,
                    "provided_main_calculation": main_calculation,
                })
                continue

        matched.append({
            "kind": "relation",
            "relation": relation,
            "effects": copy.deepcopy(rule["effects"]),
            "source_status": rule["status"],
            "witness_variants": copy.deepcopy(rule.get("witness_variants")),
        })

    if not relations_checked:
        pending.append("合会关系未检查；如确认无关系请显式传空list")

    status = "explicit_evidence_complete"
    if unresolved:
        status = "explicit_evidence_with_unresolved_variants"
    elif pending:
        status = "partial_explicit_evidence"

    return {
        "schema_version": "1.0",
        "canonical": C59_VERSION,
        "rule_id": "C59-TAIYI-NUMBER-OMEN",
        "source_profile": "tongzong_ten_essences_number_omens",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "taiyi_number": number,
        "relations": relation_list,
        "relations_checked": relations_checked,
        "tianmu_qi_state": tianmu_qi_state,
        "flybird_palace": flybird_palace,
        "heaven_calculation": heaven_calculation,
        "earth_calculation": earth_calculation,
        "main_calculation": main_calculation,
        "matched_omens": matched,
        "unresolved_variants": unresolved,
        "unresolved_variant_count": len(unresolved),
        "pending": list(dict.fromkeys(pending)),
        "status": status,
        "legacy_special_audit": copy.deepcopy(LEGACY_SPECIAL_AUDIT),
        "auto_number_lookup_used": False,
        "auto_relation_inference_used": False,
        "policy": (
            "C59只解释调用方显式给出的1..72太乙数与关系证据；"
            "不调用C54自动重算积年，也不从盘面位置自动制造合冲。"
            "数50跨见证句读冲突保持unresolved；旧数10/5独立断语不采用。"
        ),
    }


def c59_catalog() -> dict[str, Any]:
    return {
        "canonical": C59_VERSION,
        "rule_id": "C59-TAIYI-NUMBER-OMEN",
        "source_profile": "tongzong_ten_essences_number_omens",
        "special_number_rules": copy.deepcopy(SPECIAL_NUMBER_RULES),
        "relation_rules": copy.deepcopy(RELATION_RULES),
        "legacy_special_audit": copy.deepcopy(LEGACY_SPECIAL_AUDIT),
        "auto_number_lookup_used": False,
        "auto_relation_inference_used": False,
    }
