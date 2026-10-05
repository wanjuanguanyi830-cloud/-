"""C123 《太乙金镜式经》卷一“推八门占岁计法”。

本层只实现王希明“别立新术”的岁计直门：
- 上元甲子以来积年；
- 先以720去之；
- 再以240除之；
- 余数按30年一门；
- 起开门，依次休、生、伤、杜、景、死、惊，左行八门周而复始。

与C119时计八门严格分层：
- C119：30时一移门；
- C123：30年一移门。
"""

from __future__ import annotations

import copy
from typing import Any

C123_VERSION = "taiyi-c123-jinjing-volume1-year-eight-doors-v1"

YEAR_DOOR_ORDER = ("开", "休", "生", "伤", "杜", "景", "死", "惊")
OUTER_CYCLE = 720
INNER_CYCLE = 240
YEARS_PER_DOOR = 30

SOURCE_WITNESS = {
    "work": "太乙金镜式经",
    "volume": 1,
    "section": "推八门占岁计法",
    "direct_formula": [
        "置上元甲子以来距所求积年",
        "以大游纪法七百二十去之",
        "不尽以三分纪法二百四十除之",
        "余以三十约之为直门数",
        "不尽即直门所入年",
        "命起开门以次休生门左行八门周而复始",
    ],
    "example": (
        "开元十二年甲子开门为直使；自该年起至第三十一年甲午，休门为直使。"
    ),
    "policy": "只实现岁计直门，不自动把开门加太乙/主客大将的位置叠加写成新公式。",
}

LEGACY_BOUNDARY = {
    "legacy_file": "rules/jinjing/eight_door.py",
    "legacy_previous_docstring_scope": "卷四",
    "correct_source_scope": "金镜卷一推八门占岁计法",
    "compatibility_zero_input": (
        "旧API允许0并把它当240周期末；C123 canonical积年要求>=1。"
    ),
}

OVERLAY_BOUNDARY = {
    "source_statements": [
        "常以开门加太乙，即太乙之八门",
        "开门加主大将、客大将、定计大将，各立其八门",
        "客主八门与太乙八门开休生三门合者大利",
    ],
    "position_overlay_implemented": False,
    "reason": "这些语句涉及各自八门的空间叠加；C123只先锁定岁计直门周期。",
}


def _accumulated_year(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("accumulated_year须为整数")
    if value < 1:
        raise ValueError("accumulated_year须>=1")
    return value


def year_duty_door(accumulated_year: int) -> dict[str, Any]:
    n = _accumulated_year(accumulated_year)
    remainder_720 = n % OUTER_CYCLE or OUTER_CYCLE
    remainder_240 = remainder_720 % INNER_CYCLE or INNER_CYCLE
    door_index = (remainder_240 - 1) // YEARS_PER_DOOR
    year_in_door = (remainder_240 - 1) % YEARS_PER_DOOR + 1
    return {
        "schema_version": "1.0",
        "canonical": C123_VERSION,
        "rule_id": "C123-YEAR-DUTY-DOOR",
        "source_profile": "jinjing_volume1_year_eight_doors",
        "accumulated_year": n,
        "remainder_720": remainder_720,
        "remainder_240": remainder_240,
        "door_index": door_index,
        "duty_door": YEAR_DOOR_ORDER[door_index],
        "year_in_door": year_in_door,
        "years_per_door": YEARS_PER_DOOR,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_boundary": copy.deepcopy(LEGACY_BOUNDARY),
        "overlay_boundary": copy.deepcopy(OVERLAY_BOUNDARY),
    }


def c123_catalog() -> dict[str, Any]:
    return {
        "canonical": C123_VERSION,
        "rule_id": "C123-YEAR-DUTY-DOOR",
        "door_order": list(YEAR_DOOR_ORDER),
        "outer_cycle": OUTER_CYCLE,
        "inner_cycle": INNER_CYCLE,
        "years_per_door": YEARS_PER_DOOR,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_boundary": copy.deepcopy(LEGACY_BOUNDARY),
        "overlay_boundary": copy.deepcopy(OVERLAY_BOUNDARY),
    }
