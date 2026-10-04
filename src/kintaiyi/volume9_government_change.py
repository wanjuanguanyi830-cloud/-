"""C44 《太乙统宗宝鉴》卷十（项目卷九层）国政革易严格来源契约。

直接来源：
- 《太乙统宗宝鉴》“明国政革易，法令变更术”
参校：
- 《太白兵备统宗宝鉴》对应条文。

本模块只实现可直接核证的：
1. 六神所主；
2. 算长而和 / 算短不和 的远近分类；
3. 当年干支数的结构化记录；
4. 关、囚、迫、掩、击、格、挟、杜固等凶证的显式并列。

不负责：
- 自动实现“吕申加即位创立新事之年”的完整盘式变换；
- 从固定十六神本位直接推六神落点；
- 把“甲子九十/一百八十、九/十八（或二十八）”例子推广成通用年限公式。
"""

from __future__ import annotations

import copy
from typing import Any, Iterable

from .dayou_lishu import najia_number
from .volume9_ehui import SIXTEEN_POINTS, parse_ganzhi

C44_VERSION = "taiyi-c44-volume9-guozheng-v1"

GOVERNMENT_GOD_SUBJECTS = {
    "太簇": ["国政革易", "法令变更", "风俗改常", "服色更易"],
    "太阳": ["纪律隳废", "厄会兵刃"],
    "阴主": ["奸臣匿谋", "凶丧祸乱"],
    "地主": ["礼仪废失", "口舌谣言"],
    "武德": ["迁移易地", "创营宫室"],
    "大义": ["毁折废弃"],
}

COLLATION_VARIANTS = {
    "destruction_subject": {
        "tongzong": ["大义"],
        "taibai_bingbei": ["大神", "大义"],
        "effect": "毁折废弃",
        "status": "source_variant_preserved",
        "canonical_selected": None,
    },
    "jiazi_near_years": {
        "tongzong_online_witness": [9, 28],
        "taibai_bingbei": [9, 18],
        "arithmetic_note": "太白兵备明示甲=9、子=9，故18与干支和数直接相合。",
        "status": "source_variant_or_ocr_conflict",
        "canonical_selected": None,
    },
}

BAD_PATTERNS = ("关", "囚", "迫", "掩", "击", "格", "挟", "杜固")

LEGACY_REFERENCE_AUDIT = {
    "function": "guiyun.guozheng_bianyi",
    "canonical_equivalent": False,
    "issues": [
        "旧函数把吕申及六神固定本位直接做十六宫offset，未证明等价于原文加法盘式",
        "旧函数未要求完整创立新事之年干支",
        "旧函数把六神落点生成与远近迟速判断揉在同一层",
        "旧函数未保留甲子近年18/28见证冲突",
        "旧函数没有把关囚迫掩击格挟杜固按神所临宫显式分开",
    ],
}


def _landing(value: str | None, name: str) -> str | None:
    if value is None:
        return None
    if value not in SIXTEEN_POINTS:
        raise ValueError(f"{name}须为十六宫点")
    return value


def _normalize_patterns(
    patterns_by_god: dict[str, Iterable[str]] | None,
) -> dict[str, list[str]]:
    if patterns_by_god is None:
        return {}
    if not isinstance(patterns_by_god, dict):
        raise TypeError("patterns_by_god须为dict")
    out: dict[str, list[str]] = {}
    for god, items in patterns_by_god.items():
        if god not in GOVERNMENT_GOD_SUBJECTS:
            raise ValueError("patterns_by_god只接受六神：太簇/太阳/阴主/地主/武德/大义")
        values = list(items)
        unknown = [item for item in values if item not in BAD_PATTERNS]
        if unknown:
            raise ValueError(f"未知凶格：{unknown[0]}")
        out[god] = values
    return out


def government_change_distance(
    *,
    calculation_length: str | None,
    calculation_harmony: bool | None,
) -> dict[str, Any]:
    """按“算和而长远 / 算短不和近”分类，不补齐未明组合。"""
    if calculation_length not in (None, "长", "短"):
        raise ValueError("calculation_length须为长/短或None")
    if calculation_harmony not in (None, True, False):
        raise TypeError("calculation_harmony须为bool或None")

    if calculation_length == "长" and calculation_harmony is True:
        status = "direct"
        distance_class = "远"
        source_rule = "算和而长，事应在远"
    elif calculation_length == "短" and calculation_harmony is False:
        status = "direct"
        distance_class = "近"
        source_rule = "算短不和，事应在近"
    elif calculation_length is None or calculation_harmony is None:
        status = "not_computable"
        distance_class = None
        source_rule = None
    else:
        status = "not_defined_by_source_passage"
        distance_class = None
        source_rule = None

    return {
        "calculation_length": calculation_length,
        "calculation_harmony": calculation_harmony,
        "distance_class": distance_class,
        "status": status,
        "source_rule": source_rule,
        "canonical": C44_VERSION,
    }


def government_change_from_evidence(
    *,
    event_ganzhi: str,
    god_landings: dict[str, str | None] | None = None,
    calculation_length: str | None = None,
    calculation_harmony: bool | None = None,
    patterns_by_god: dict[str, Iterable[str]] | None = None,
) -> dict[str, Any]:
    """根据显式六神落点与算长短/和不和证据组装国政革易结果。

    god_landings 是“吕申加创立新事之年”之后的上游盘式结果；
    C44 不在此处用固定十六神本位重算。
    """
    gz = parse_ganzhi(event_ganzhi)
    if god_landings is None:
        god_landings = {}
    if not isinstance(god_landings, dict):
        raise TypeError("god_landings须为dict")

    normalized_landings: dict[str, str | None] = {}
    for god in GOVERNMENT_GOD_SUBJECTS:
        normalized_landings[god] = _landing(god_landings.get(god), god)

    unknown_gods = set(god_landings) - set(GOVERNMENT_GOD_SUBJECTS)
    if unknown_gods:
        raise ValueError(f"god_landings含未知神：{sorted(unknown_gods)[0]}")

    patterns = _normalize_patterns(patterns_by_god)
    distance = government_change_distance(
        calculation_length=calculation_length,
        calculation_harmony=calculation_harmony,
    )

    manifestations = []
    for god, subjects in GOVERNMENT_GOD_SUBJECTS.items():
        landing = normalized_landings[god]
        god_patterns = patterns.get(god, [])
        manifestations.append({
            "god": god,
            "landing": landing,
            "subjects": list(subjects),
            "bad_patterns": list(god_patterns),
            "bad_change_evidence": bool(god_patterns),
        })

    pending = []
    if not all(normalized_landings.values()):
        pending.append("须提供吕申加创立新事之年后六神所临")
    if distance["status"] == "not_computable":
        pending.append("须提供算长短与和不和")
    elif distance["status"] == "not_defined_by_source_passage":
        pending.append("当前长短/和不和组合原文未直接定远近")

    stem_number = najia_number(gz["stem"])
    branch_number = najia_number(gz["branch"])

    return {
        "schema_version": "1.0",
        "canonical": C44_VERSION,
        "rule_id": "C44-V9-GUOZHENG",
        "source_profile": "tongzong_volume9_government_change",
        "event_ganzhi": gz,
        "ganzhi_numbers": {
            "stem": stem_number,
            "branch": branch_number,
            "sum": stem_number + branch_number,
            "source_dependency": "C42纳甲干支数表",
        },
        "god_landings": normalized_landings,
        "manifestations": manifestations,
        "distance": distance,
        "patterns_by_god": patterns,
        "bad_change_evidence": any(patterns.values()),
        "collation_variants": copy.deepcopy(COLLATION_VARIANTS),
        "automatic_lvshen_transform_used": False,
        "legacy_fixed_offset_formula_used": False,
        "computable": not pending,
        "status": "computed_from_explicit_source_evidence" if not pending else "not_computable",
        "pending": pending,
        "policy": (
            "六神落点必须来自上游对‘吕申加创立新事之年’的真实盘式结果；"
            "C44不以十六神固定本位offset代替。远近只按原文明示的两种组合判断，"
            "甲子90/180与9/18(28)只保存为算例见证，不推广为通用年限公式。"
        ),
    }


def build_volume9_government_change_source_variant(
    result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """构建 source_variants.volume9.government_change。"""
    if result is None:
        result = {}
    if not isinstance(result, dict):
        raise TypeError("result须为dict或None")
    if result:
        if result.get("rule_id") != "C44-V9-GUOZHENG":
            raise ValueError("result必须来自C44-V9-GUOZHENG")
        if result.get("source_profile") != "tongzong_volume9_government_change":
            raise ValueError("C44 source_profile不匹配")

    complete = bool(result and result.get("computable") is True)
    return {
        "schema_version": "1.0",
        "canonical": C44_VERSION,
        "result": copy.deepcopy(result),
        "legacy_replacement": (
            {
                "source_replacement_complete": True,
                "rule_id": "C44-V9-GUOZHENG",
            }
            if complete
            else {}
        ),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
        "cross_rule_merge": False,
        "policy": (
            "国政革易独立于C43厄会行限与后续岁中灾发；"
            "只有六神落点和远近证据齐备的C44结果才清除旧字段migration gap。"
        ),
    }
