"""C48 《太乙统宗宝鉴》卷十小游统卦行爻所主灾祥术。

本层消费 C47 小游轨运结果，不重算内外卦、动爻或三才。
纳甲须由上游显式提供；不调用旧 King Wen 64 卦命名或旧 najia_for_yao。
"""

from __future__ import annotations

import copy
from typing import Any, Iterable

C48_VERSION = "taiyi-c48-xiaoyou-line-omens-v1"

STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")

BAD_PATTERNS = frozenset({"关", "囚", "掩", "迫", "击", "挟", "格", "对"})

THREE_TALENT_OMENS = {
    "理天": {
        "domain": "天",
        "omens": ["天有变异", "日月失辉", "五星不经其度"],
    },
    "理地": {
        "domain": "地",
        "omens": ["风雨不调", "禾谷不成"],
    },
    "理人": {
        "domain": "人",
        "omens": ["人民疾疫", "时多荒俭"],
    },
}

STEM_DISASTER_OMENS = {
    "甲乙": ["风雷疾病"],
    "丙丁": ["大旱", "火光亢怪", "口舌妖言", "后宫有谋"],
    "戊己": ["飞蝗", "土工兴作", "大丧"],
    "庚辛": ["兵革攻战", "盗贼相伤", "国界不安", "妖彗变现"],
    "壬癸": ["霪霖阴沉", "大水溢川", "后妃不安"],
}

# 只固化两见证都较清楚的干分野；丁、辛另存异文。
STEM_REGION_STABLE = {
    "甲": ["齐"],
    "乙": ["夷"],
    "丙": ["楚"],
    "戊": ["中"],
    "己": ["豫"],
    "庚": ["秦"],
    "壬": ["燕", "冀"],
    "癸": ["北狄"],
}

STEM_REGION_VARIANTS = {
    "丁": {
        "tongzong": ["蛮"],
        "taibai_bingbei": ["南海"],
        "canonical_selected": None,
        "status": "source_variant_unresolved",
    },
    "辛": {
        "tongzong": ["西域", "梁", "益"],
        "taibai_bingbei": ["西戎", "梁", "益"],
        "canonical_selected": None,
        "status": "source_variant_unresolved",
    },
}

BRANCH_REGION = {
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
        "旧函数依赖旧xiaoyou_chong_gua与King Wen 64卦命名链，C48不以该链为来源真值",
        "旧函数自动调用najia_for_yao；C48要求显式上游纳甲，不在本层补算",
        "旧函数把初四爻概括为‘忌关掩迫’，遗漏原文算和有应/不和无应条件",
        "旧函数仅摘要部分干灾应，未完整保存戊己、壬癸等条目",
        "旧函数静默采用单一干分野表，未保留丁与辛的见证差异",
    ],
}


def _validate_c47(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict) or result.get("rule_id") != "C47-XY-HEX":
        raise ValueError("xiaoyou_result必须来自C47-XY-HEX")
    if result.get("source_profile") != "tongzong_volume9_xiaoyou":
        raise ValueError("C47 source_profile不匹配")
    return result


def _patterns(value: Iterable[str] | None) -> tuple[list[str], bool]:
    if value is None:
        return [], False
    items = list(value)
    unknown = [item for item in items if item not in BAD_PATTERNS]
    if unknown:
        raise ValueError(f"未知小游凶格：{unknown[0]}")
    return items, True


def _najia(value: str | None) -> dict[str, Any]:
    if value is None:
        return {
            "status": "not_computable",
            "value": None,
            "stem": None,
            "branch": None,
            "stem_disaster_group": None,
            "stem_disaster_omens": [],
            "stem_region": None,
            "stem_region_variant": None,
            "branch_region": None,
        }
    if not isinstance(value, str) or len(value) != 2:
        raise ValueError("moving_line_najia须为两字纳甲干支")
    stem, branch = value
    if stem not in STEMS or branch not in BRANCHES:
        raise ValueError("moving_line_najia须为合法天干+地支组合")

    disaster_group = next(
        group for group in STEM_DISASTER_OMENS if stem in group
    )
    return {
        "status": "direct",
        "value": value,
        "stem": stem,
        "branch": branch,
        "stem_disaster_group": disaster_group,
        "stem_disaster_omens": list(STEM_DISASTER_OMENS[disaster_group]),
        "stem_region": copy.deepcopy(STEM_REGION_STABLE.get(stem)),
        "stem_region_variant": copy.deepcopy(STEM_REGION_VARIANTS.get(stem)),
        "branch_region": BRANCH_REGION[branch],
        "policy": (
            "纳甲只验证‘天干+地支’字面组合，不按六十甲子奇偶校验；"
            "纳甲如甲寅等不等同日辰六十甲子。"
        ),
    }


def _line_omen(
    line: int,
    *,
    calculation_harmonious: bool | None,
    has_response: bool | None,
) -> dict[str, Any]:
    if line in (2, 5):
        return {
            "status": "direct",
            "line_class": "中道",
            "summary": "安平之岁",
            "requires_calculation_response": False,
        }

    if line in (1, 4):
        if calculation_harmonious not in (None, True, False):
            raise TypeError("calculation_harmonious须为bool或None")
        if has_response not in (None, True, False):
            raise TypeError("has_response须为bool或None")

        if calculation_harmonious is None or has_response is None:
            status = "not_computable"
            summary = None
        elif calculation_harmonious is True and has_response is True:
            status = "direct"
            summary = "吉"
        elif calculation_harmonious is False and has_response is False:
            status = "direct"
            summary = "君臣失助、世不宁"
        else:
            status = "not_defined_by_source_passage"
            summary = None

        return {
            "status": status,
            "line_class": "初四条件爻",
            "summary": summary,
            "calculation_harmonious": calculation_harmonious,
            "has_response": has_response,
            "requires_calculation_response": True,
            "source_rule": "算和有应为吉；不和无应则君臣失助、世不宁",
        }

    if line == 3:
        return {
            "status": "direct",
            "line_class": "内极",
            "summary": "事多凶变",
            "severity_when_bad_patterns": "较轻",
            "requires_calculation_response": False,
        }

    if line == 6:
        return {
            "status": "direct",
            "line_class": "外极",
            "summary": "事多凶变",
            "severity_when_bad_patterns": "较重",
            "requires_calculation_response": False,
        }

    raise ValueError("moving line须为1..6")


def xiaoyou_line_omens(
    xiaoyou_result: dict[str, Any],
    *,
    calculation_harmonious: bool | None = None,
    has_response: bool | None = None,
    pattern_evidence: Iterable[str] | None = None,
    moving_line_najia: str | None = None,
) -> dict[str, Any]:
    """解释 C47 小游动爻；不重算 C47，不自动纳甲。"""
    base = _validate_c47(xiaoyou_result)
    line = base.get("inner_moving_line")
    if not isinstance(line, int) or not 1 <= line <= 6:
        raise ValueError("C47结果缺合法inner_moving_line")

    three_talent = base.get("three_talent")
    if three_talent not in THREE_TALENT_OMENS:
        raise ValueError("C47结果缺合法three_talent")

    patterns, patterns_checked = _patterns(pattern_evidence)
    line_omen = _line_omen(
        line,
        calculation_harmonious=calculation_harmonious,
        has_response=has_response,
    )
    najia = _najia(moving_line_najia)

    bad_pattern_omens = (
        ["水旱灾伤", "兵刃饥馑", "疾疫流亡"]
        if patterns
        else []
    )
    if patterns and line == 3:
        bad_pattern_severity = "内极尚轻"
    elif patterns and line == 6:
        bad_pattern_severity = "外极为重"
    else:
        bad_pattern_severity = None

    pending = []
    if not patterns_checked:
        pending.append("须显式检查关囚掩迫击挟格对；无格局时传空list")
    if line_omen["status"] == "not_computable":
        pending.append("初四爻须提供算和/不和与有应/无应")
    if najia["status"] == "not_computable":
        pending.append("须提供动爻纳甲，方可解释干灾应与干支分野")

    return {
        "schema_version": "1.0",
        "canonical": C48_VERSION,
        "rule_id": "C48-XY-OMEN",
        "source_profile": "tongzong_volume10_xiaoyou_omens",
        "upstream_rule_id": "C47-XY-HEX",
        "upstream": {
            "inner_trigram": base.get("structure", {}).get("lower_trigram"),
            "outer_trigram": base.get("structure", {}).get("upper_trigram"),
            "moving_line": line,
            "three_talent": three_talent,
        },
        "principle": {
            "hexagram": "卦主其事",
            "line": "爻主其时",
            "base_hexagram_judgement_applied": False,
        },
        "line_omen": line_omen,
        "three_talent_omen": copy.deepcopy(THREE_TALENT_OMENS[three_talent]),
        "pattern_evidence": patterns,
        "pattern_checked": patterns_checked,
        "bad_pattern_omens": bad_pattern_omens,
        "bad_pattern_severity": bad_pattern_severity,
        "najia": najia,
        "complete": not pending,
        "status": "complete_explicit_evidence" if not pending else "partial_explicit_evidence",
        "pending": pending,
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
        "policy": (
            "C48只解释C47给出的动爻与三才；纳甲、算和与有应均由上游显式给出。"
            "不同子规则并列保存，不把灾祥、分野和格局压成单一winner。"
        ),
    }


def c48_source_catalog() -> dict[str, Any]:
    return {
        "canonical": C48_VERSION,
        "rule_id": "C48-XY-OMEN",
        "source_profile": "tongzong_volume10_xiaoyou_omens",
        "bad_patterns": sorted(BAD_PATTERNS),
        "three_talent_omens": copy.deepcopy(THREE_TALENT_OMENS),
        "stem_disaster_omens": copy.deepcopy(STEM_DISASTER_OMENS),
        "stem_region_stable": copy.deepcopy(STEM_REGION_STABLE),
        "stem_region_variants": copy.deepcopy(STEM_REGION_VARIANTS),
        "branch_region": copy.deepcopy(BRANCH_REGION),
        "legacy_reference_audit": copy.deepcopy(LEGACY_REFERENCE_AUDIT),
    }
