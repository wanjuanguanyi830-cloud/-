"""《太乙金镜式经》卷一“推八门占岁计法”兼容入口。

canonical 数值实现已迁至：
    kintaiyi.jinjing_year_eight_doors.year_duty_door

本文件保留旧 `eight_door(accumulated_year) -> str` API。
旧API继续输出既有繁体门名（開/傷/驚），避免破坏格局引擎契约；
C123 canonical runtime 使用项目当前规范简体门名。
旧API允许0，并把0按240年周期末处理；C123 canonical积年要求>=1。
"""

from __future__ import annotations

from kintaiyi.jinjing_year_eight_doors import (
    INNER_CYCLE as DOOR_CYCLE,
    YEARS_PER_DOOR as DOOR_PERIOD,
    year_duty_door,
)

DOOR_ORDER = ("開", "休", "生", "傷", "杜", "景", "死", "驚")
_CANONICAL_TO_LEGACY = {
    "开": "開",
    "休": "休",
    "生": "生",
    "伤": "傷",
    "杜": "杜",
    "景": "景",
    "死": "死",
    "惊": "驚",
}


def eight_door(accumulated_year: int) -> str:
    """Compatibility wrapper returning the legacy traditional-character door name."""
    if isinstance(accumulated_year, bool) or not isinstance(accumulated_year, int):
        raise TypeError("accumulated_year must be an integer")
    if accumulated_year < 0:
        raise ValueError("accumulated_year must be non-negative")

    canonical_year = DOOR_CYCLE if accumulated_year == 0 else accumulated_year
    canonical_door = year_duty_door(canonical_year)["duty_door"]
    return _CANONICAL_TO_LEGACY[canonical_door]
