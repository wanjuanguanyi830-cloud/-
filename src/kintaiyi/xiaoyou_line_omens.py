"""C48 《太乙统宗宝鉴》小游统卦行爻所主灾祥。

消费 C47 小游重卦结构，但不依赖六十四卦命名。
动爻纳甲必须由上游显式给出；本模块不调用旧 najia_for_yao。
"""

from __future__ import annotations

import copy
from typing import Any

C48_VERSION = "taiyi-c48-xiaoyou-line-omens-v1"

STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
SOURCE_PATTERNS = frozenset({"关", "囚", "掩", "迫", "击", "挟", "格", "对"})

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "primary_section": "明小游统卦行爻所主灾祥术",
    "online_witness_volume": 10,
    "alternate_catalog_boundary": "部分目录/分页把本术接在卷九末",
    "volume_status": "witness_volume_boundary_variant",
    "pattern_ocr_variant": {
        "readings": ["格对", "格封"],
        "normalized": "格、对",
        "status": "ocr_or_layout_variant_preserved",
    },
}

LINE_RULES = {
    1: {"class": "初四", "base": "条件吉凶", "needs_harmony_response": True},
    2: {"class": "中道", "base": "安平", "needs_harmony_response": False},
    3: {"class": "内极", "base": "凶变", "needs_harmony_response": False, "severity": "较轻"},
    4: {"class": "初四", "base": "条件吉凶", "needs_harmony_response": True},
    5: {"class": "中道", "base": "安平", "needs_harmony_response": False},
    6: {"class": "外极", "base": "凶变", "needs_harmony_response": False, "severity": "较重"},
}

THREE_TALENT_OMENS = {
    "理天": ["天有变异", "日月失辉", "五星不经其度"],
    "理地": ["风雨不调", "禾谷不成"],
    "理人": ["人民疾疫", "时多荒俭"],
}

STEM_OMENS = {
    "甲": {
        "effects": ["疾病"],
        "witness_text": "风宣疾病",
        "uncertain_text": ["风宣"],
        "status": "partial_text_uncertain",
    },
    "乙": {
        "effects": ["疾病"],
        "witness_text": "风宣疾病",
        "uncertain_text": ["风宣"],
        "status": "partial_text_uncertain",
    },
    "丙": {
        "effects": ["大旱", "亢怪", "口舌妖言", "后宫有谋"],
        "witness_text": "大旱亢怪，口舌妖言，及后宫有谋",
        "uncertain_text": [],
        "status": "stable",
    },
    "丁": {
        "effects": ["大旱", "亢怪", "口舌妖言", "后宫有谋"],
        "witness_text": "大旱亢怪，口舌妖言，及后宫有谋",
        "uncertain_text": [],
        "status": "stable",
    },
    "戊": {
        "effects": ["飞蝗", "土工", "大丧"],
        "witness_text": "飞蝗土工，及生大丧",
        "uncertain_text": [],
        "status": "stable",
    },
    "己": {
        "effects": ["飞蝗", "土工", "大丧"],
        "witness_text": "飞蝗土工，及生大丧",
        "uncertain_text": [],
        "status": "stable",
    },
    "庚": {
        "effects": ["兵革攻战", "贼盗相伤", "国界不安"],
        "witness_text": "有兵革攻战，贼盗相伤，国界不安，甚则夭慧变现",
        "uncertain_text": ["夭慧变现"],
        "status": "partial_text_uncertain",
    },
    "辛": {
        "effects": ["兵革攻战", "贼盗相伤", "国界不安"],
        "witness_text": "有兵革攻战，贼盗相伤，国界不安，甚则夭慧变现",
        "uncertain_text": ["夭慧变现"],
        "status": "partial_text_uncertain",
    },
    "壬": {
        "effects": ["淋雨阴沉", "大水溢川", "后妃不安"],
        "witness_text": "淋雨阴沉，大水溢川，后妃不安之事",
        "uncertain_text": [],
        "status": "stable",
    },
    "癸": {
        "effects": ["淋雨阴沉", "大水溢川", "后妃不安"],
        "witness_text": "淋雨阴沉，大水溢川，后妃不安之事",
        "uncertain_text": [],
        "status": "stable",
    },
}

STEM_REGIONS = {
    "甲": "齐",
    "乙": "夷",
    "丙": "楚",
    "丁": "蛮",
    "戊": "中",
    "己": "豫",
    "庚": "秦",
    "辛": "西域",
    "壬": "燕冀",
    "癸": "北狄",
}

BRANCH_REGIONS = {
    "子": "齐",
    "丑": "吴",
    "寅": "燕",
    "卯": "宋",
    "辰": "郑",
    "巳": "楚",
    "午": "周",
    "未": "秦",
    "申": "晋",
    "酉": "赵",
    "戌": "鲁",
    "亥": "卫",
}

LEGACY_REFERENCE_AUDIT = {
    "function": "guiyun.xiaoyou_xingyao_zai",
    "canonical_equivalent": False,
    "issues": [
        "旧函数依赖六十四卦命名后再调用najia_for_yao，C47本身不要求六十四卦名",
        "旧天干分野加入东兵/宋/吴/梁益等扩展，超过当前直接正文的简表",
        "旧函数把爻位、三才、格局、纳甲灾象压成单一摘要断语",
        "未把初四爻的算和/不和与有应/无应结构化成独立输入",
    ],
}


def _validate_c47(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError("xiaoyou_hexagram须为dict")
    if value.get("rule_id") != "C47-XY-HEX":
        raise ValueError("xiaoyou_hexagram必须来自C47-XY-HEX")
    if value.get("source_profile") != "tongzong_volume9_xiaoyou":
        raise ValueError("C47 source_profile不匹配")
    return value


def _line_assessment(
    line: int,
    *,
    calc_harmonious: bool | None,
    has_response: bool | None,
) -> dict[str, Any]:
    if line not in LINE_RULES:
        raise ValueError("动爻须为1..6")
    if calc_harmonious not in (None, True, False):
        raise TypeError("calc_harmonious须为bool或None")
    if has_response not in (None, True, False):
        raise TypeError("has_response须为bool或None")

    rule = copy.deepcopy(LINE_RULES[line])
    pending = []
    verdict = rule["base"]

    if rule["needs_harmony_response"]:
        if calc_harmonious is None:
            pending.append("初四爻须提供算和/不和")
        if has_response is None:
            pending.append("初四爻须提供有应/无应")
        if not pending:
            if calc_harmonious and has_response:
                verdict = "吉"
            elif (not calc_harmonious) and (not has_response):
                verdict = "君臣失助、世不宁"
            else:
                verdict = "mixed_evidence"
    elif line in (2, 5):
        verdict = "安平"
    elif line == 3:
        verdict = "凶变，内极尚轻"
    else:
        verdict = "凶变，外极为重"

    return {
        "line": line,
        **rule,
        "calc_harmonious": calc_harmonious,
        "has_response": has_response,
        "verdict": verdict,
        "computable": not pending,
        "pending": pending,
    }


def _patterns(value: list[str] | None) -> tuple[list[str], bool]:
    if value is None:
        return [], False
    if not isinstance(value, list):
        raise TypeError("pattern_evidence须为list或None")
    unknown = [item for item in value if item not in SOURCE_PATTERNS]
    if unknown:
        raise ValueError(f"未知小游格局: {', '.join(unknown)}")
    return list(value), True


def _najia(value: tuple[str, str] | list[str] | None) -> dict[str, Any]:
    if value is None:
        return {
            "provided": False,
            "stem": None,
            "branch": None,
            "stem_omens": [],
            "stem_region": None,
            "branch_region": None,
        }
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise TypeError("moving_line_najia须为[天干, 地支]")
    stem, branch = value
    if stem not in STEMS:
        raise ValueError("纳甲天干须为十天干")
    if branch not in BRANCHES:
        raise ValueError("纳甲地支须为十二地支")
    return {
        "provided": True,
        "stem": stem,
        "branch": branch,
        "stem_omens": copy.deepcopy(STEM_OMENS[stem]),
        "stem_region": STEM_REGIONS[stem],
        "branch_region": BRANCH_REGIONS[branch],
    }


def xiaoyou_line_omens(
    xiaoyou_hexagram: dict[str, Any],
    *,
    calc_harmonious: bool | None = None,
    has_response: bool | None = None,
    pattern_evidence: list[str] | None = None,
    moving_line_najia: tuple[str, str] | list[str] | None = None,
) -> dict[str, Any]:
    """结构化小游行爻灾祥，不从重卦名反推纳甲。"""
    x47 = _validate_c47(xiaoyou_hexagram)
    line = x47.get("inner_moving_line")
    if not isinstance(line, int):
        raise ValueError("C47结果缺inner_moving_line")
    talent = x47.get("three_talent")
    if talent not in THREE_TALENT_OMENS:
        raise ValueError("C47结果缺有效three_talent")

    line_result = _line_assessment(
        line,
        calc_harmonious=calc_harmonious,
        has_response=has_response,
    )
    patterns, patterns_checked = _patterns(pattern_evidence)
    najia = _najia(moving_line_najia)

    pending = list(line_result["pending"])
    if not patterns_checked:
        pending.append("须显式检查关囚掩迫击挟格对；无格局时传空list")
    if not najia["provided"]:
        pending.append("须由上游显式提供动爻纳甲干支；C48不强制命名六十四卦")

    pattern_omen = (
        ["水旱灾伤", "兵刃饥馑", "疾疫流亡"]
        if patterns
        else []
    )

    return {
        "schema_version": "1.0",
        "canonical": C48_VERSION,
        "rule_id": "C48-XY-OMEN",
        "source_profile": "tongzong_volume10_xiaoyou_line_omens",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "c47": {
            "rule_id": x47["rule_id"],
            "accumulated_year": x47.get("accumulated_year"),
            "structure": copy.deepcopy(x47.get("structure")),
            "inner_moving_line": line,
            "three_talent": talent,
        },
        "line_assessment": line_result,
        "three_talent": {
            "state": talent,
            "omens": copy.deepcopy(THREE_TALENT_OMENS[talent]),
        },
        "pattern_evidence": patterns,
        "pattern_omens": pattern_omen,
        "patterns_aggravate_only": True,
        "najia": najia,
        "computable": not pending,
        "status": "structured_from_explicit_source_evidence" if not pending else "partial",
        "pending": pending,
        "legacy_sixtyfour_hexagram_lookup_used": False,
        "legacy_fenye_extensions_used": False,
        "policy": (
            "卦主其事、爻主其时；爻位、三才、格局、纳甲四层并列保存。"
            "格局只加重灾象，不覆盖基础爻位判断。"
            "纳甲必须显式输入，不因C47未命名六十四卦而伪造。"
        ),
    }


def c48_catalog() -> dict[str, Any]:
    return {
        "canonical": C48_VERSION,
        "rule_id": "C48-XY-OMEN",
        "source_profile": "tongzong_volume10_xiaoyou_line_omens",
        "stem_regions": copy.deepcopy(STEM_REGIONS),
        "branch_regions": copy.deepcopy(BRANCH_REGIONS),
        "source_patterns": sorted(SOURCE_PATTERNS),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
    }
