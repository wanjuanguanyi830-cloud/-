"""L0 历元：金镜长积年、六纪三元、卷三五子元短积年。

核心来源：
- 《太乙金镜式经》卷一“推上元积年”：
  开元十二年甲子积 1,937,281 算；往古每年减一，未来每年加一。
- 卷一“推入六纪三元法”：
  360周内以60为纪，得六纪。
- 《太乙统宗宝鉴》卷二“明太乙入统年之法”：
  六纪元标签依次为 上、中、下、上、中、下；开元十二年为下元第三纪。
- 《太乙金镜式经》卷三“五子元积年立成法”：
  同一开元十二年甲子，短积年为30,001；仍先以360去之，再以72约之。

本模块只处理岁计年编号，不自行判断某公历日期是否已经进入下一传统岁界。
"""

from __future__ import annotations

from typing import Any

LONG_ANCHOR_YEAR_CE = 724
LONG_ANCHOR_COUNT = 1_937_281
FIVE_ZI_ANCHOR_COUNT = 30_001
EPOCH_DIFFERENCE = LONG_ANCHOR_COUNT - FIVE_ZI_ANCHOR_COUNT

J1_ACC_RULE_ID = "J1-ACC-01"
J1_SIX_JI_RULE_ID = "J1-SIX-JI-THREE-YUAN"
J3_FIVE_ZI_ACC_RULE_ID = "J3-ACC-01"
J3_FIVE_ZI_RULE_ID = "J3-FIVE-ZI-360"

JI_YUAN_LABELS = ("上元", "中元", "下元", "上元", "中元", "下元")
FIVE_ZI_NAMES = ("甲子", "丙子", "戊子", "庚子", "壬子")


def _historical_year(value: Any) -> int:
    """历史纪年：CE为正，BCE为负，不设0年。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("historical_year须为整数")
    if value == 0:
        raise ValueError("历史纪年无0年；1 BCE请用-1，1 CE请用1")
    return value


def _to_astronomical_year(historical_year: int) -> int:
    """内部只为连续加减使用：1 BCE=0，2 BCE=-1。"""
    y = _historical_year(historical_year)
    return y if y > 0 else y + 1


def _delta_from_anchor(historical_year: int) -> int:
    return _to_astronomical_year(historical_year) - LONG_ANCHOR_YEAR_CE


def long_accumulated_year(historical_year: int) -> dict[str, Any]:
    """历史年份 -> 《金镜》卷一长积年。"""
    y = _historical_year(historical_year)
    count = LONG_ANCHOR_COUNT + _delta_from_anchor(y)
    if count < 1:
        raise ValueError("所求年份早于本长历元可表示范围")

    return {
        "rule_id": J1_ACC_RULE_ID,
        "source_profile": "jinjing_volume1_long_epoch",
        "historical_year": y,
        "year_notation": "CE_positive_BCE_negative_no_year_zero",
        "anchor_year_ce": LONG_ANCHOR_YEAR_CE,
        "anchor_count": LONG_ANCHOR_COUNT,
        "accumulated_year": count,
        "delta_from_anchor": _delta_from_anchor(y),
        "policy": (
            "724 CE开元十二年甲子=1,937,281算；"
            "向古每年减一、向未来每年加一。"
        ),
    }


def five_zi_short_accumulated_year(historical_year: int) -> dict[str, Any]:
    """历史年份 -> 《金镜》卷三五子元短积年。"""
    y = _historical_year(historical_year)
    count = FIVE_ZI_ANCHOR_COUNT + _delta_from_anchor(y)
    if count < 1:
        raise ValueError("所求年份早于卷三五子元短历元可表示范围")

    return {
        "rule_id": J3_FIVE_ZI_ACC_RULE_ID,
        "source_profile": "jinjing_volume3_five_zi_short_epoch",
        "historical_year": y,
        "year_notation": "CE_positive_BCE_negative_no_year_zero",
        "anchor_year_ce": LONG_ANCHOR_YEAR_CE,
        "anchor_count": FIVE_ZI_ANCHOR_COUNT,
        "five_zi_accumulated_year": count,
        "delta_from_anchor": _delta_from_anchor(y),
        "policy": (
            "724 CE开元十二年甲子=30,001算；"
            "此为卷三截短历元，不覆盖卷一1,937,281长积年。"
        ),
    }


def six_ji_three_yuan_from_count(accumulated_year: int) -> dict[str, Any]:
    """积年 -> 360周内六纪与三元标签。"""
    if isinstance(accumulated_year, bool) or not isinstance(accumulated_year, int):
        raise TypeError("accumulated_year须为整数")
    if accumulated_year < 1:
        raise ValueError("accumulated_year须>=1")

    r360 = accumulated_year % 360 or 360
    ji_index = (r360 - 1) // 60 + 1
    year_in_ji = (r360 - 1) % 60 + 1
    yuan = JI_YUAN_LABELS[ji_index - 1]

    return {
        "rule_id": J1_SIX_JI_RULE_ID,
        "source_profile": "jinjing_volume1_six_ji_tongzong_yuan_labels",
        "accumulated_year": accumulated_year,
        "remainder_360": r360,
        "ji_index_1based": ji_index,
        "year_in_ji": year_in_ji,
        "yuan_label": yuan,
        "yuan_sequence_index": ((ji_index - 1) % 3) + 1,
        "policy": (
            "六纪各60年；三元标签按纪循环："
            "一纪上、二纪中、三纪下、四纪上、五纪中、六纪下。"
            "不按后世玄空法把一纪再切成三个20年。"
        ),
    }


def five_zi_yuan_from_count(accumulated_year: int) -> dict[str, Any]:
    """积年 -> 360周内五子元与本元72局。"""
    if isinstance(accumulated_year, bool) or not isinstance(accumulated_year, int):
        raise TypeError("accumulated_year须为整数")
    if accumulated_year < 1:
        raise ValueError("accumulated_year须>=1")

    r360 = accumulated_year % 360 or 360
    yuan_index = (r360 - 1) // 72 + 1
    local_ju = (r360 - 1) % 72 + 1

    return {
        "rule_id": J3_FIVE_ZI_RULE_ID,
        "source_profile": "jinjing_volume3_five_zi_360",
        "accumulated_year": accumulated_year,
        "remainder_360": r360,
        "five_zi_index_1based": yuan_index,
        "five_zi_yuan": FIVE_ZI_NAMES[yuan_index - 1],
        "local_ju": local_ju,
        "yuan_size": 72,
        "outer_cycle": 360,
        "policy": "360周分五个72局元：甲子、丙子、戊子、庚子、壬子。",
    }


def epoch_context(historical_year: int) -> dict[str, Any]:
    """一次返回长积年、短积年、六纪三元、五子元，并校验360同余。"""
    long_epoch = long_accumulated_year(historical_year)
    short_epoch = five_zi_short_accumulated_year(historical_year)

    long_count = long_epoch["accumulated_year"]
    short_count = short_epoch["five_zi_accumulated_year"]
    difference = long_count - short_count

    six_ji = six_ji_three_yuan_from_count(long_count)
    five_zi_long = five_zi_yuan_from_count(long_count)
    five_zi_short = five_zi_yuan_from_count(short_count)

    congruent = (
        difference == EPOCH_DIFFERENCE
        and difference % 360 == 0
        and five_zi_long["remainder_360"] == five_zi_short["remainder_360"]
    )

    return {
        "rule_id": "L0-EPOCH-CONTEXT",
        "historical_year": historical_year,
        "long_epoch": long_epoch,
        "five_zi_short_epoch": short_epoch,
        "epoch_difference": difference,
        "epoch_difference_in_360_cycles": difference // 360,
        "equivalent_mod_360": congruent,
        "six_ji_three_yuan": six_ji,
        "five_zi_from_long": five_zi_long,
        "five_zi_from_short": five_zi_short,
        "policy": (
            "卷一长历元与卷三五子元短历元并存；"
            "二者相差整360周，只在周期层等价，不互相改名或覆盖。"
        ),
    }
