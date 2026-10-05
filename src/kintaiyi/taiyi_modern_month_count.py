"""现代 production 月计积数。

组合两条已确认规则：
1. 《统宗》卷一：所求积年减一，以十二乘之，为岁前天正十一月积月骨架；
2. 《金镜》卷一：遇闰月，以逐月节气时刻为正。

production 因此：
- 用现代天文十二节切太阳月；
- 子月=1、丑=2、…、亥=12；
- 以该太阳月所属的“月计循环年”积年定12月块；
- 闰农历月不额外加计。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .taiyi_epoch import long_accumulated_year
from .taiyi_four_counts import four_count_core_from_accumulated_count
from .taiyi_modern_solar_month import resolve_solar_month

RULE_ID = "MODERN-TAIYI-MONTH-COUNT"

MONTH_BRANCH_INDEX = {
    "子": 1,
    "丑": 2,
    "寅": 3,
    "卯": 4,
    "辰": 5,
    "巳": 6,
    "午": 7,
    "未": 8,
    "申": 9,
    "酉": 10,
    "戌": 11,
    "亥": 12,
}


def month_cycle_historical_year(solar_month: dict[str, Any]) -> int:
    """把大雪至次年立冬的12个太阳月归为一个月计循环年。

    大雪在公历Y年，属于月计循环年Y+1；
    次年小寒..立冬均属于Y+1。
    """
    start = solar_month["month_start_utc"]
    if solar_month["start_term"] == "大雪":
        return start.year + 1
    return start.year


def accumulated_month_from_cycle(
    *,
    cycle_historical_year: int,
    month_build_branch: str,
) -> dict[str, Any]:
    """月计循环年+月建 -> 连续积月。"""
    if month_build_branch not in MONTH_BRANCH_INDEX:
        raise ValueError("month_build_branch须为十二支月建")

    year_epoch = long_accumulated_year(cycle_historical_year)
    year_count = year_epoch["accumulated_year"]
    month_index = MONTH_BRANCH_INDEX[month_build_branch]

    accumulated_month = (year_count - 1) * 12 + month_index

    return {
        "rule_id": "MODERN-TAIYI-MONTH-COUNT-ARITHMETIC",
        "cycle_historical_year": cycle_historical_year,
        "year_accumulated_count": year_count,
        "month_build_branch": month_build_branch,
        "month_index_1based": month_index,
        "accumulated_month": accumulated_month,
        "formula": "(year_accumulated_count - 1) * 12 + month_index_1based",
        "policy": (
            "十二节形成固定12个太阳月；闰农历月不进入month_index。"
        ),
    }


def modern_month_count(moment: datetime) -> dict[str, Any]:
    """现代datetime -> 精确太阳月界 -> 月计积数 -> 月计G2..G7。"""
    solar_month = resolve_solar_month(moment)
    cycle_year = month_cycle_historical_year(solar_month)
    arithmetic = accumulated_month_from_cycle(
        cycle_historical_year=cycle_year,
        month_build_branch=solar_month["month_build_branch"],
    )
    count = arithmetic["accumulated_month"]

    core = four_count_core_from_accumulated_count(
        count,
        count_type="月计",
    )

    return {
        "rule_id": RULE_ID,
        "source_profile": "production_modern_astronomy_month_count",
        "calendar": solar_month,
        "arithmetic": arithmetic,
        "cycle_historical_year": cycle_year,
        "month_formula_year": cycle_year,
        "month_build_branch": solar_month["month_build_branch"],
        "accumulated_month": count,
        "result": core,
        "local_ju": core["local_ju"],
        "taiyi_palace": core["taiyi_palace"],
        "wenchang_sector": core["wenchang_sector"],
        "shiji_sector": core["shiji_sector"],
        "host_calc": core["host_calc"],
        "guest_calc": core["guest_calc"],
        "policy": (
            "production月计以现代精确十二节切月；"
            "month_formula_year仅服务积月公式，不是太乙岁标签。"
            "太乙岁仍只在冬至瞬间切换；闰月不额外推进，春节/朔日也不作为月计切换点。"
        ),
    }
