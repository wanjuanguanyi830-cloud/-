"""《太乙金镜式经》卷一“推八门占岁计法”兼容入口。

canonical 数值实现已迁至：
    kintaiyi.jinjing_year_eight_doors.year_duty_door

本文件保留旧 `eight_door(accumulated_year) -> str` API。
旧API允许0，并把0按240年周期末处理；新 canonical C123 要求1-based积年 >=1。
"""

from __future__ import annotations

from kintaiyi.jinjing_year_eight_doors import (
    INNER_CYCLE as DOOR_CYCLE,
    YEARS_PER_DOOR as DOOR_PERIOD,
    YEAR_DOOR_ORDER as DOOR_ORDER,
    year_duty_door,
)


def eight_door(accumulated_year: int) -> str:
    """Compatibility wrapper returning only the duty-door name."""
    if isinstance(accumulated_year, bool) or not isinstance(accumulated_year, int):
        raise TypeError("accumulated_year must be an integer")
    if accumulated_year < 0:
        raise ValueError("accumulated_year must be non-negative")

    canonical_year = DOOR_CYCLE if accumulated_year == 0 else accumulated_year
    return year_duty_door(canonical_year)["duty_door"]
