"""C42 卷九“历数长短 / 安居之代历数”结构化规则。

直接固化：
- 纳甲干支数；
- 初四单加、二五六爻纳甲数倍加、三六不倍不加；
- 一二四五历数长、三六历数短；
- 二爻正旺、五爻时已过；
- 内极（三）灾轻、外极（六）灾重。

历史算例的“策数除减后余数”存在文本/算术冲突。
因此本模块不从外卦周数自动推导 base_remainder_after_ce；
只有调用方显式提供该中间量时才计算最终历数。
"""

from __future__ import annotations

import copy
from typing import Any, Iterable

from .taiyi_rules import integer

C42_VERSION = "taiyi-c42-dayou-lishu-v1"

NAJIA_NUMBER = {
    **{ch: 9 for ch in "甲己子午"},
    **{ch: 8 for ch in "乙庚丑未"},
    **{ch: 7 for ch in "丙辛寅申"},
    **{ch: 6 for ch in "丁壬卯酉"},
    **{ch: 5 for ch in "戊癸辰戌"},
    **{ch: 4 for ch in "巳亥"},
}

NAJIA_WITNESS_NOTE = {
    "tongzong_ocr": "末组在线OCR见“己亥四”",
    "collation": "独立见证明确为“巳亥四”",
    "normalized": "巳亥",
    "status": "ocr_corrected_by_collation",
}

SOURCE_EXAMPLE_CONFLICT = {
    "wanli_jiwei": {
        "reported_outer_cycle_remainder": 146,
        "reported_after_ce": 48,
        "heavy_ce": 192,
        "arithmetic_check": "146按192除减不能直接得到48",
        "status": "source_example_arithmetic_conflict",
    },
    "hongwu": {
        "reported_outer_cycle_remainder": 535,
        "reported_after_ce": 175,
        "heavy_ce": 180,
        "arithmetic_check": "535 % 180 = 175",
        "status": "arithmetically_consistent",
    },
}


def najia_number(token: str) -> int:
    try:
        return NAJIA_NUMBER[token]
    except (KeyError, TypeError):
        raise ValueError("纳甲干支须为甲乙丙丁戊己庚辛癸或十二支单字") from None


def najia_pair_value(stem: str, branch: str) -> dict[str, Any]:
    """一爻纳甲干支数 = 天干数 + 地支数。"""
    stem_value = najia_number(stem)
    branch_value = najia_number(branch)
    return {
        "stem": stem,
        "branch": branch,
        "stem_value": stem_value,
        "branch_value": branch_value,
        "pair_value": stem_value + branch_value,
    }


def line_addition_policy(line: int) -> dict[str, Any]:
    """卷九历数加法：初四单加、二五倍六爻、三六不加。"""
    line = integer(line, 1, 6)
    if line in (1, 4):
        mode = "single_current_line"
        multiplier = 1
    elif line in (2, 5):
        mode = "double_all_six_lines"
        multiplier = 2
    else:
        mode = "no_add_at_extreme"
        multiplier = 0

    return {
        "line": line,
        "mode": mode,
        "multiplier": multiplier,
        "inner_extreme": line == 3,
        "outer_extreme": line == 6,
        "source_rule": "卷九·明历数长短，以观远近之期术",
    }


def _pair_from_value(value: Any) -> tuple[str, str]:
    if (
        not isinstance(value, (list, tuple))
        or len(value) != 2
        or not all(isinstance(item, str) for item in value)
    ):
        raise TypeError("纳甲爻须为[天干, 地支]二元组")
    return value[0], value[1]


def najia_addition(
    line: int,
    *,
    current_pair: tuple[str, str] | list[str] | None = None,
    six_line_pairs: Iterable[tuple[str, str] | list[str]] | None = None,
) -> dict[str, Any]:
    """计算历数最后的纳甲加数；不处理此前策数除减步骤。"""
    policy = line_addition_policy(line)

    if policy["mode"] == "no_add_at_extreme":
        return {
            **policy,
            "computable": True,
            "addition": 0,
            "components": [],
        }

    if policy["mode"] == "single_current_line":
        if current_pair is None:
            return {
                **policy,
                "computable": False,
                "addition": None,
                "pending": ["初/四爻须提供本爻纳甲干支"],
            }
        stem, branch = _pair_from_value(current_pair)
        pair = najia_pair_value(stem, branch)
        return {
            **policy,
            "computable": True,
            "addition": pair["pair_value"],
            "components": [pair],
        }

    if six_line_pairs is None:
        return {
            **policy,
            "computable": False,
            "addition": None,
            "pending": ["二/五爻须提供六爻全部纳甲干支后倍加"],
        }

    pairs = list(six_line_pairs)
    if len(pairs) != 6:
        raise ValueError("二/五爻倍加须恰有六爻纳甲")
    components = []
    for pair_value in pairs:
        stem, branch = _pair_from_value(pair_value)
        components.append(najia_pair_value(stem, branch))
    base_sum = sum(item["pair_value"] for item in components)

    return {
        **policy,
        "computable": True,
        "addition": base_sum * 2,
        "base_six_line_sum": base_sum,
        "components": components,
    }


def lishu_base_status() -> dict[str, Any]:
    """记录策数除减中间量的算例冲突，不猜公式。"""
    return {
        "canonical": C42_VERSION,
        "status": "source_example_conflict_requires_explicit_base",
        "examples": copy.deepcopy(SOURCE_EXAMPLE_CONFLICT),
        "automatic_remainder_formula": None,
        "policy": (
            "洪武算例与取余相合，但万历己未算例文字/数字不相合；"
            "在校勘解决前，不由外卦周数自动算base_remainder_after_ce。"
        ),
    }


def compose_lishu(
    heavy_hexagram: dict[str, Any],
    *,
    line: int | None = None,
    current_pair: tuple[str, str] | list[str] | None = None,
    six_line_pairs: Iterable[tuple[str, str] | list[str]] | None = None,
    base_remainder_after_ce: int | None = None,
) -> dict[str, Any]:
    """组装历数；base_remainder_after_ce 必须显式给出才产最终值。"""
    if not isinstance(heavy_hexagram, dict):
        raise TypeError("heavy_hexagram须为C41结果dict")
    if heavy_hexagram.get("rule_id") != "C41-DY-HEX":
        raise ValueError("heavy_hexagram必须来自C41-DY-HEX")

    heavy_ce = heavy_hexagram.get("ce", {}).get("total")
    if not isinstance(heavy_ce, int):
        raise ValueError("C41结果缺重卦总策")

    if line is None:
        line = heavy_hexagram.get("inner_moving_line", {}).get("line")
    line = integer(line, 1, 6)

    addition = najia_addition(
        line,
        current_pair=current_pair,
        six_line_pairs=six_line_pairs,
    )

    if base_remainder_after_ce is None:
        final_value = None
        final_status = "not_computable_base_remainder_unresolved"
    else:
        base_remainder_after_ce = integer(base_remainder_after_ce)
        final_value = (
            base_remainder_after_ce + addition["addition"]
            if addition["computable"]
            else None
        )
        final_status = "computed_from_explicit_base" if final_value is not None else "not_computable_najia"

    return {
        "schema_version": "1.0",
        "canonical": C42_VERSION,
        "rule_id": "C42-DY-LISHU",
        "source_profile": "tongzong_volume9_dayou_lishu",
        "heavy_hexagram_ce": heavy_ce,
        "line": line,
        "najia_addition": addition,
        "base_remainder_after_ce": base_remainder_after_ce,
        "base_remainder_evidence": lishu_base_status(),
        "final_lishu": final_value,
        "status": final_status,
        "automatic_outer_cycle_remainder_used": False,
        "policy": (
            "C42不自行重算C41重卦，也不从C38/旧guiyun取得周数；"
            "只有显式base_remainder_after_ce与足够纳甲输入齐备时才给最终历数。"
        ),
    }


def anju_line_assessment(line: int) -> dict[str, Any]:
    """安居之代：一二四五历数长，三六历数短。"""
    line = integer(line, 1, 6)
    long = line in (1, 2, 4, 5)
    phase = "正旺" if line == 2 else "时已过" if line == 5 else None
    extreme = "内极" if line == 3 else "外极" if line == 6 else None
    severity = "较轻" if line == 3 else "较重" if line == 6 else None

    return {
        "rule_id": "C42-DY-ANJU",
        "canonical": C42_VERSION,
        "line": line,
        "base_length": "长" if long else "短",
        "phase": phase,
        "extreme": extreme,
        "extreme_severity": severity,
        "base_result": "历数长" if long else "历数短",
        "corrections_applied": False,
        "policy": "一二四五为长，三六为短；后续阴阳得位、应与不应、君臣合格均另列证据，不覆盖基础爻位分类。",
    }


def anju_governance_assessment(
    line: int,
    *,
    yin_yang_in_position: bool | None = None,
    yang_line_has_response: bool | None = None,
    ruler_minister_relation: str | None = None,
    extra_patterns: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """把安居术的附加政治证据与基础历数长短分开。"""
    base = anju_line_assessment(line)
    evidence = []

    if yin_yang_in_position is True:
        evidence.append({"condition": "阴阳得位", "effect": "政治安"})
    elif yin_yang_in_position is False:
        evidence.append({"condition": "阴阳失位", "effect": "政治乱"})

    if yang_line_has_response is True:
        evidence.append({"condition": "阳爻有应", "effect": "君得臣助"})
    elif yang_line_has_response is False:
        evidence.append({"condition": "阳爻无应", "effect": "君失臣辅"})

    if ruler_minister_relation is not None:
        if ruler_minister_relation not in {"合", "格"}:
            raise ValueError("ruler_minister_relation须为合/格或None")
        evidence.append({
            "condition": f"君臣{ruler_minister_relation}",
            "effect": "政亨" if ruler_minister_relation == "合" else "政乖",
        })

    return {
        **base,
        "governance_evidence": evidence,
        "extra_patterns": copy.deepcopy(extra_patterns or []),
        "corrections_applied": False,
        "policy": (
            "附加证据与掩迫囚击格挟、阳九百六首尾等条件并列；"
            "不得回写或覆盖一二四五长、三六短的基础分类。"
        ),
    }
