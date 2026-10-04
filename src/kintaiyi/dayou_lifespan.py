"""C42 卷九历数长短 / 安居之代的来源限定实现。

直接来源：
- 《太乙统宗宝鉴》卷九「明历数长短，以观远近之期术」
- 「明安居之代历数之期术」
参校：
- 《太白兵备统宗宝鉴》对应条文。

本模块只实现已经校稳的：
1. 纳甲干支数；
2. 动爻位置的加数规则；
3. 安居之代的长短 / 极位 / 得位 / 有应等结构判断。

不负责：
- 从积年推内外卦；
- 六爻纳甲排法；
- +34 / +36610 等纪元差；
- C38 行限轨迹；
- 未经校稳的完整帝祚年数算法。
"""

from __future__ import annotations

from typing import Any, Iterable

from .taiyi_rules import integer

C42_VERSION = "taiyi-c42-dayou-lishu-v1"

GAN_NUMBER = {
    "甲": 9, "己": 9,
    "乙": 8, "庚": 8,
    "丙": 7, "辛": 7,
    "丁": 6, "壬": 6,
    "戊": 5, "癸": 5,
}

ZHI_NUMBER = {
    "子": 9, "午": 9,
    "丑": 8, "未": 8,
    "寅": 7, "申": 7,
    "卯": 6, "酉": 6,
    "辰": 5, "戌": 5,
    "巳": 4, "亥": 4,
}

LONG_LINES = {1, 2, 4, 5}
SHORT_LINES = {3, 6}


def najia_symbol_number(symbol: str) -> dict[str, Any]:
    """返回纳甲单个天干/地支的河图大衍数。"""
    if symbol in GAN_NUMBER:
        return {
            "symbol": symbol,
            "kind": "stem",
            "number": GAN_NUMBER[symbol],
            "canonical": C42_VERSION,
        }
    if symbol in ZHI_NUMBER:
        return {
            "symbol": symbol,
            "kind": "branch",
            "number": ZHI_NUMBER[symbol],
            "canonical": C42_VERSION,
        }
    raise ValueError("symbol须为十干或十二支")


def najia_pair_number(stem: str, branch: str) -> dict[str, Any]:
    """将本爻纳甲干、支两个数并加。

    “干支并加”来自卷九直接条文；本函数不负责决定某爻应纳何干支。
    """
    if stem not in GAN_NUMBER:
        raise ValueError("stem须为甲乙丙丁戊己庚辛壬癸")
    if branch not in ZHI_NUMBER:
        raise ValueError("branch须为十二支")
    stem_number = GAN_NUMBER[stem]
    branch_number = ZHI_NUMBER[branch]
    return {
        "stem": stem,
        "branch": branch,
        "stem_number": stem_number,
        "branch_number": branch_number,
        "pair_number": stem_number + branch_number,
        "canonical": C42_VERSION,
        "policy": "只计算显式给定的本爻纳甲干支数；不在本层推六爻纳甲。",
    }


def _normalize_six_pairs(
    six_line_najia: Iterable[tuple[str, str] | list[str]],
) -> list[tuple[str, str]]:
    pairs = list(six_line_najia)
    if len(pairs) != 6:
        raise ValueError("six_line_najia必须恰有六个爻的(干,支)")
    normalized: list[tuple[str, str]] = []
    for pair in pairs:
        if not isinstance(pair, (tuple, list)) or len(pair) != 2:
            raise ValueError("每爻纳甲须为(干,支)")
        stem, branch = pair
        if stem not in GAN_NUMBER or branch not in ZHI_NUMBER:
            raise ValueError("六爻纳甲中存在非法干支")
        normalized.append((stem, branch))
    return normalized


def moving_line_najia_adjustment(
    line: int,
    *,
    current_najia: tuple[str, str] | list[str] | None = None,
    six_line_najia: Iterable[tuple[str, str] | list[str]] | None = None,
) -> dict[str, Any]:
    """按卷九爻位规则计算应加的纳甲干支数。

    - 二、五：得中，六爻纳甲干支数皆倍加；
    - 初、四：只加本爻纳甲干支数；
    - 三、六：亢极，不倍不加。
    """
    line = integer(line, 1, 6)

    if line in (3, 6):
        return {
            "line": line,
            "line_class": "extreme",
            "addition": 0,
            "addition_rule": "不倍不加",
            "requires_current_najia": False,
            "requires_six_line_najia": False,
            "canonical": C42_VERSION,
        }

    if line in (1, 4):
        if current_najia is None:
            return {
                "line": line,
                "line_class": "initial_or_fourth",
                "status": "not_computable",
                "addition": None,
                "requires_current_najia": True,
                "requires_six_line_najia": False,
                "canonical": C42_VERSION,
            }
        if not isinstance(current_najia, (tuple, list)) or len(current_najia) != 2:
            raise ValueError("current_najia须为(干,支)")
        stem, branch = current_najia
        pair = najia_pair_number(stem, branch)
        return {
            "line": line,
            "line_class": "initial_or_fourth",
            "status": "ok",
            "addition": pair["pair_number"],
            "addition_rule": "只加本爻纳甲干支",
            "current_najia": pair,
            "requires_current_najia": True,
            "requires_six_line_najia": False,
            "canonical": C42_VERSION,
        }

    # 二、五
    if six_line_najia is None:
        return {
            "line": line,
            "line_class": "central",
            "status": "not_computable",
            "addition": None,
            "requires_current_najia": False,
            "requires_six_line_najia": True,
            "canonical": C42_VERSION,
        }
    pairs = _normalize_six_pairs(six_line_najia)
    details = [najia_pair_number(stem, branch) for stem, branch in pairs]
    raw_total = sum(item["pair_number"] for item in details)
    return {
        "line": line,
        "line_class": "central",
        "status": "ok",
        "addition": raw_total * 2,
        "raw_six_line_total": raw_total,
        "multiplier": 2,
        "addition_rule": "六爻纳甲干支数皆倍加",
        "six_line_najia": details,
        "requires_current_najia": False,
        "requires_six_line_najia": True,
        "canonical": C42_VERSION,
    }


def lifespan_term_from_remainder(
    remainder_after_four_image_ce: int,
    line: int,
    *,
    current_najia: tuple[str, str] | list[str] | None = None,
    six_line_najia: Iterable[tuple[str, str] | list[str]] | None = None,
) -> dict[str, Any]:
    """对“以四象策除之不尽”的余数应用动爻纳甲加数。

    本函数故意要求调用方提供“除策后的余数”，不从积年或帝王即位年重算，
    从而隔离尚有纪元差异的上游公式。
    """
    remainder = integer(remainder_after_four_image_ce, 0)
    if remainder == 0:
        return {
            "canonical": C42_VERSION,
            "status": "exact_division_source_not_expanded",
            "computable": False,
            "remainder_after_four_image_ce": 0,
            "lifespan_term": None,
            "policy": "正文只说明‘不尽者’再加动爻纳甲干支；整除情形不擅自补断。",
        }

    adjustment = moving_line_najia_adjustment(
        line,
        current_najia=current_najia,
        six_line_najia=six_line_najia,
    )
    if adjustment.get("addition") is None:
        return {
            "canonical": C42_VERSION,
            "status": "not_computable",
            "computable": False,
            "remainder_after_four_image_ce": remainder,
            "line": integer(line, 1, 6),
            "adjustment": adjustment,
        }

    return {
        "canonical": C42_VERSION,
        "status": "ok",
        "computable": True,
        "remainder_after_four_image_ce": remainder,
        "line": integer(line, 1, 6),
        "adjustment": adjustment,
        "lifespan_term": remainder + adjustment["addition"],
        "formula_scope": "post_four_image_ce_remainder_plus_moving_line_najia",
        "epoch_formula_applied": False,
        "policy": "只实现正文‘不尽者，加太游动爻纳甲干支，并加于上’这一后置步骤。",
    }


def settled_reign_assessment(
    line: int,
    *,
    scope: str | None = None,
    yin_yang_in_position: bool | None = None,
    line_is_yang: bool | None = None,
    has_response: bool | None = None,
    ruler_minister_relation: str | None = None,
) -> dict[str, Any]:
    """结构化“明安居之代历数之期术”的直接判断。

    scope 只接受“内卦/外卦”；不从积年自行推断。
    """
    line = integer(line, 1, 6)
    if scope not in (None, "内卦", "外卦"):
        raise ValueError("scope须为内卦/外卦或None")
    if yin_yang_in_position not in (None, True, False):
        raise TypeError("yin_yang_in_position须为bool或None")
    if line_is_yang not in (None, True, False):
        raise TypeError("line_is_yang须为bool或None")
    if has_response not in (None, True, False):
        raise TypeError("has_response须为bool或None")
    if ruler_minister_relation not in (None, "合", "格"):
        raise ValueError("ruler_minister_relation须为合/格或None")

    if line in LONG_LINES:
        length_class = "长"
    else:
        length_class = "短"

    phase = {
        1: "长位",
        2: "正旺",
        3: "内极",
        4: "长位",
        5: "时已过",
        6: "外极",
    }[line]

    position_judgment = None
    if yin_yang_in_position is True:
        position_judgment = "政治安"
    elif yin_yang_in_position is False:
        position_judgment = "政治乱"

    response_judgment = None
    if line_is_yang is True and has_response is True:
        response_judgment = "君得臣之助"
    elif line_is_yang is True and has_response is False:
        response_judgment = "君失臣之辅"
    elif line_is_yang is False and has_response is not None:
        response_judgment = "source_not_expanded_for_yin_line_response"

    relation_judgment = None
    if ruler_minister_relation == "合":
        relation_judgment = "政道亨"
    elif ruler_minister_relation == "格":
        relation_judgment = "政道乖"

    scope_length = None
    if scope == "内卦":
        scope_length = "历数应长"
    elif scope == "外卦":
        scope_length = "历数应短"

    extreme_severity = None
    if line == 3:
        extreme_severity = "内极灾轻"
    elif line == 6:
        extreme_severity = "外极灾重"

    return {
        "canonical": C42_VERSION,
        "rule_id": "C42-ANJU",
        "line": line,
        "length_class": length_class,
        "phase": phase,
        "scope": scope,
        "scope_length": scope_length,
        "extreme_severity": extreme_severity,
        "yin_yang_in_position": yin_yang_in_position,
        "position_judgment": position_judgment,
        "line_is_yang": line_is_yang,
        "has_response": has_response,
        "response_judgment": response_judgment,
        "ruler_minister_relation": ruler_minister_relation,
        "relation_judgment": relation_judgment,
        "policy": (
            "本层只解释显式爻位/内外/得位/有应/君臣合格；"
            "不从旧guiyun的积年偏移、外卦动爻或其他盘内字段反推。"
        ),
    }
