"""C44 卷九/十见证“国政革易、法令变更术”严格来源模型。

不复用旧 guiyun.guozheng_bianyi(year_zhi) 的静态十六位旋转。
只消费显式的创立年干支、吕申加年后六神落点、算长短/和不和与格局证据。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C44_VERSION = "taiyi-c44-volume9-governance-change-v1"

STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
SIXTEEN_POINTS = tuple("子丑艮寅卯辰巽巳午未坤申酉戌乾亥")

REQUIRED_GODS = ("太簇", "太阳", "阴主", "地主", "武德", "大义")

GOD_EFFECTS = {
    "太簇": "国政革易、法令变更、风俗改常、服色更易",
    "太阳": "纪律隳废、厄会兵刃",
    "阴主": "奸臣匿谋、凶丧祸乱",
    "地主": "礼仪废失、口舌谣言",
    "武德": "迁移易地、创营宫室",
    "大义": "毁折废弃",
}

SOURCE_VARIANTS = {
    "tongzong": {
        "required_gods": list(REQUIRED_GODS),
        "extra_gods": [],
        "far_year_examples": [90, 180],
        "near_year_examples": [9, 28],
        "notes": "统宗当前在线见证列六神；近年数见9/28。",
    },
    "taibai_bingbei": {
        "required_gods": list(REQUIRED_GODS),
        "extra_gods": ["大神"],
        "far_year_examples": [90, 180],
        "near_year_examples": [9, 18],
        "notes": "太白兵备见证并列大神/大义；近年数见9/18。",
    },
}

LEGACY_REFERENCE_AUDIT = {
    "function": "guiyun.guozheng_bianyi",
    "canonical_equivalent": False,
    "issues": [
        "旧函数核心只收year_zhi，不能表达创立新事之完整干支年",
        "以静态吕申/六神位置作简单十六位旋转，未证等价于原式“吕申加年”",
        "未要求主客算长短与和不和的结构化输入",
        "未要求六神所临宫的关囚迫掩击格挟杜固证据",
        "要诀写90/190，与直接见证90/180不符",
        "近年数18/28存在传本差异，旧函数未保留variant",
    ],
}


def parse_ganzhi(value: str) -> dict[str, str]:
    if not isinstance(value, str) or len(value) != 2:
        raise ValueError("创立年须为两字干支")
    stem, branch = value
    if stem not in STEMS or branch not in BRANCHES:
        raise ValueError("创立年须为合法干支")
    return {"stem": stem, "branch": branch, "ganzhi": value}


def _validate_landings(
    god_landings: dict[str, str] | None,
) -> tuple[dict[str, str], list[str]]:
    if god_landings is None:
        return {}, [f"缺{god}所临" for god in REQUIRED_GODS]
    if not isinstance(god_landings, dict):
        raise TypeError("god_landings须为dict")

    unknown = sorted(set(god_landings) - set(REQUIRED_GODS) - {"大神"})
    if unknown:
        raise ValueError(f"未知国政六神字段: {', '.join(unknown)}")

    normalized = {}
    pending = []
    for god in REQUIRED_GODS:
        point = god_landings.get(god)
        if point is None:
            pending.append(f"缺{god}所临")
            continue
        if point not in SIXTEEN_POINTS:
            raise ValueError(f"{god}落点须为十六宫点")
        normalized[god] = point

    if "大神" in god_landings:
        point = god_landings["大神"]
        if point not in SIXTEEN_POINTS:
            raise ValueError("大神落点须为十六宫点")
        normalized["大神"] = point
    return normalized, pending


def _timing_state(
    calc_length: str | None,
    calc_harmonious: bool | None,
) -> dict[str, Any]:
    if calc_length not in (None, "长", "短"):
        raise ValueError("calc_length须为长/短或None")
    if calc_harmonious not in (None, True, False):
        raise TypeError("calc_harmonious须为bool或None")

    if calc_length is None or calc_harmonious is None:
        return {
            "status": "not_computable",
            "distance_class": None,
            "witness_candidates": {},
        }

    if calc_length == "长" and calc_harmonious is True:
        return {
            "status": "source_rule_matched",
            "distance_class": "远",
            "witness_candidates": {
                key: copy.deepcopy(value["far_year_examples"])
                for key, value in SOURCE_VARIANTS.items()
            },
        }

    if calc_length == "短" and calc_harmonious is False:
        return {
            "status": "source_rule_matched",
            "distance_class": "近",
            "witness_candidates": {
                key: copy.deepcopy(value["near_year_examples"])
                for key, value in SOURCE_VARIANTS.items()
            },
        }

    return {
        "status": "mixed_or_unattested_combination",
        "distance_class": None,
        "witness_candidates": {},
    }


def governance_change_from_evidence(
    *,
    foundation_ganzhi: str,
    god_landings: dict[str, str] | None = None,
    calc_length: str | None = None,
    calc_harmonious: bool | None = None,
    pattern_evidence: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    """结构化国政革易；不在本层推“吕申加年”的落点算法。"""
    gz = parse_ganzhi(foundation_ganzhi)
    landings, pending = _validate_landings(god_landings)
    timing = _timing_state(calc_length, calc_harmonious)

    if calc_length is None:
        pending.append("须提供算长/短")
    if calc_harmonious is None:
        pending.append("须提供算和/不和")
    if pattern_evidence is None:
        pending.append("须显式提供六神落宫格局证据；无格局时传空dict")
        patterns = {}
    elif not isinstance(pattern_evidence, dict):
        raise TypeError("pattern_evidence须为dict或None")
    else:
        patterns = copy.deepcopy(pattern_evidence)

    events = {
        god: {
            "landing": landings.get(god),
            "effect": GOD_EFFECTS.get(
                god,
                "大神见证只在参校本出现，所主毁折废弃类事",
            ),
            "patterns": copy.deepcopy(patterns.get(god, [])),
        }
        for god in landings
    }

    computable = not pending
    return {
        "schema_version": "1.0",
        "canonical": C44_VERSION,
        "rule_id": "C44-V9-GOV",
        "source_profile": "tongzong_volume9_governance_change",
        "foundation_year": gz,
        "landing_formula_applied": False,
        "god_landings": landings,
        "events": events,
        "timing": {
            **timing,
            "calc_length": calc_length,
            "calc_harmonious": calc_harmonious,
            "canonical_year_selected": None,
            "source_variant_unresolved": bool(timing["witness_candidates"]),
        },
        "source_variants": copy.deepcopy(SOURCE_VARIANTS),
        "pattern_evidence": patterns,
        "patterns_applied_to_base": False,
        "computable": computable,
        "status": "structured_from_explicit_source_evidence" if computable else "not_computable",
        "pending": pending,
        "policy": (
            "六神落点必须由上游原式明确给出；"
            "算长和只判远、算短不和只判近。"
            "90/180与9/18或28只作见证候选，不选单一年数。"
            "关囚迫掩击格挟杜固等格局独立保存，不覆盖基础所主。"
        ),
    }


def build_volume9_governance_source_variant(
    result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if result is None:
        result = {}
    if not isinstance(result, dict):
        raise TypeError("result须为dict或None")
    if result:
        if result.get("rule_id") != "C44-V9-GOV":
            raise ValueError("result必须来自C44-V9-GOV")
        if result.get("source_profile") != "tongzong_volume9_governance_change":
            raise ValueError("C44 source_profile不匹配")

    complete = bool(result and result.get("computable") is True)
    return {
        "schema_version": "1.0",
        "canonical": C44_VERSION,
        "result": copy.deepcopy(result),
        "legacy_replacement": (
            {"source_replacement_complete": True, "rule_id": "C44-V9-GOV"}
            if complete
            else {}
        ),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
        "cross_source_merge": False,
        "policy": "旧国政章易只有被完整C44显式来源证据替换后才清除migration gap。",
    }
