"""C50 《太乙统宗宝鉴》卷十“明太乙历数之期术”证据聚合层。

与 C42 不同：
- C42：卷九重卦策数 / 动爻 / 历数长短结构；
- C50：卷十综合参详即位年、太阳/阴主厄会、太乙运气卦爻、
  太游/小游轨运、内外极限与囚迫击格掩挟等。

C50 不制造唯一“寿数公式”，只保存可核证证据链。
"""

from __future__ import annotations

import copy
from typing import Any

from .dayou_lishu import najia_number
from .volume9_ehui import parse_ganzhi

C50_VERSION = "taiyi-c50-lishu-evidence-bundle-v1"

SOURCE_WITNESS = {
    "work": "太乙统宗宝鉴",
    "section": "明太乙历数之期术",
    "online_witness_volume": 10,
    "source_principles": [
        "帝王应天顺人始终之期",
        "常以即位年支加大义，视太阳、阴主四神之下为厄会之期",
        "须参详太乙入运气爻卦象",
        "须参详太游、小游轨运卦爻与内外极限",
        "须参详囚迫击格掩挟之年",
    ],
    "four_spirit_explanation_status": "text_preserved_formula_not_reconstructed",
}

ALLOWED_PATTERNS = frozenset({"囚", "迫", "击", "格", "掩", "挟"})

CORONATION_CLOUD_NUMBERS = {
    "黄": {"element": "土", "number": 5},
    "白": {"element": "金", "number": 9},
    "青": {"element": "木", "number": 3},
    "黑": {"element": "水", "number": 6},
    "赤": {"element": "火", "number": 7},
}

LEGACY_BOUNDARY = {
    "c42_equivalent_formula": False,
    "c43_equivalent_formula": False,
    "reason": (
        "C42是卷九历数长短算法层；C43是厄会行限严格契约；"
        "C50把这些及其他运气/轨运/格局证据并列参详，"
        "原文未给可无损压缩成单一公式的唯一规则。"
    ),
}


def coronation_cloud_evidence(color: str | None) -> dict[str, Any]:
    """只结构化登位日旁云的颜色五行数，不解释后代兴衰。"""
    if color is None:
        return {
            "provided": False,
            "color": None,
            "element": None,
            "number": None,
            "interpretation_applied": False,
        }
    if color not in CORONATION_CLOUD_NUMBERS:
        raise ValueError("cloud_color须为黄/白/青/黑/赤或None")
    row = CORONATION_CLOUD_NUMBERS[color]
    return {
        "provided": True,
        "color": color,
        "element": row["element"],
        "number": row["number"],
        "interpretation_applied": False,
        "policy": "只保存原文颜色五行数；后续子嗣/在位长短语句OCR不稳，本层不自动解释。",
    }


def _validate_optional_rule(
    value: dict[str, Any] | None,
    *,
    rule_id: str,
    name: str,
) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError(f"{name}须为dict或None")
    if value.get("rule_id") != rule_id:
        raise ValueError(f"{name}必须来自{rule_id}")
    return value


def _patterns(value: list[str] | None) -> tuple[list[str], bool]:
    if value is None:
        return [], False
    if not isinstance(value, list):
        raise TypeError("pattern_evidence须为list或None")
    unknown = [item for item in value if item not in ALLOWED_PATTERNS]
    if unknown:
        raise ValueError(f"未知C50格局：{unknown[0]}")
    return list(value), True


def taiyi_lishu_evidence_bundle(
    *,
    enthronement_ganzhi: str,
    ehui_result: dict[str, Any] | None = None,
    dayou_hexagram: dict[str, Any] | None = None,
    xiaoyou_hexagram: dict[str, Any] | None = None,
    taiyi_yunqi_hexagram_evidence: dict[str, Any] | None = None,
    pattern_evidence: list[str] | None = None,
    cloud_color: str | None = None,
) -> dict[str, Any]:
    """构建卷十历数之期证据束；即使证据齐全也不伪造最终寿数。"""
    gz = parse_ganzhi(enthronement_ganzhi)
    ehui = _validate_optional_rule(
        ehui_result, rule_id="C43-V9-EHUI", name="ehui_result"
    )
    dayou = _validate_optional_rule(
        dayou_hexagram, rule_id="C41-DY-HEX", name="dayou_hexagram"
    )
    xiaoyou = _validate_optional_rule(
        xiaoyou_hexagram, rule_id="C47-XY-HEX", name="xiaoyou_hexagram"
    )
    if taiyi_yunqi_hexagram_evidence is not None and not isinstance(
        taiyi_yunqi_hexagram_evidence, dict
    ):
        raise TypeError("taiyi_yunqi_hexagram_evidence须为dict或None")

    patterns, patterns_checked = _patterns(pattern_evidence)
    cloud = coronation_cloud_evidence(cloud_color)

    pending = []
    if ehui is None:
        pending.append("缺太阳/阴主厄会证据（可由C43提供）")
    if dayou is None:
        pending.append("缺太游轨运卦爻证据（C41）")
    if xiaoyou is None:
        pending.append("缺小游轨运卦爻证据（C47）")
    if taiyi_yunqi_hexagram_evidence is None:
        pending.append("缺太乙入运气爻卦象显式证据")
    if not patterns_checked:
        pending.append("须显式检查囚迫击格掩挟；无格局时传空list")

    stem_num = najia_number(gz["stem"])
    branch_num = najia_number(gz["branch"])

    return {
        "schema_version": "1.0",
        "canonical": C50_VERSION,
        "rule_id": "C50-LISHU-EVIDENCE",
        "source_profile": "tongzong_volume10_lishu_evidence",
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "enthronement_year": gz,
        "enthronement_ganzhi_numbers": {
            "stem": stem_num,
            "branch": branch_num,
            "sum": stem_num + branch_num,
            "source_dependency": "C42纳甲干支数表",
            "used_as_final_lifespan_formula": False,
        },
        "ehui": copy.deepcopy(ehui) if ehui is not None else {},
        "dayou": copy.deepcopy(dayou) if dayou is not None else {},
        "xiaoyou": copy.deepcopy(xiaoyou) if xiaoyou is not None else {},
        "taiyi_yunqi_hexagram_evidence": copy.deepcopy(
            taiyi_yunqi_hexagram_evidence
        ) if taiyi_yunqi_hexagram_evidence is not None else {},
        "pattern_evidence": patterns,
        "pattern_checked": patterns_checked,
        "cloud": cloud,
        "evidence_bundle_complete": not pending,
        "status": "evidence_bundle_complete" if not pending else "evidence_bundle_partial",
        "pending": pending,
        "final_lifespan_years": None,
        "final_lifespan_status": "source_requires_composite_judgement_not_unique_formula",
        "four_spirit_formula_reconstructed": False,
        "c42_formula_reused_as_c50": False,
        "c43_formula_reused_as_c50": False,
        "legacy_boundary": copy.deepcopy(LEGACY_BOUNDARY),
        "policy": (
            "C50是参详证据聚合层，不把C42、C43、C41、C47静默合成唯一寿数。"
            "登位日旁云只保存颜色五行数；OCR不稳的子嗣/在位解释不自动结构化。"
        ),
    }


def c50_catalog() -> dict[str, Any]:
    return {
        "canonical": C50_VERSION,
        "rule_id": "C50-LISHU-EVIDENCE",
        "source_profile": "tongzong_volume10_lishu_evidence",
        "required_evidence_classes": [
            "即位年",
            "太阳/阴主厄会",
            "太乙入运气爻卦象",
            "太游轨运卦爻",
            "小游轨运卦爻",
            "囚迫击格掩挟检查",
        ],
        "cloud_numbers": copy.deepcopy(CORONATION_CLOUD_NUMBERS),
        "legacy_boundary": copy.deepcopy(LEGACY_BOUNDARY),
        "final_lifespan_formula": None,
    }
