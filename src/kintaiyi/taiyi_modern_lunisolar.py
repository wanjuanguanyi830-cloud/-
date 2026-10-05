"""现代中国农历/干支事实层。

用途：
- production 提供现代中国农历年月日、闰月、干支等事实；
- 与太乙岁冬至换年规则并列保存，绝不互相替代。

现代中国农历统一按 Asia/Shanghai（中国标准时间）解释。
用户输入可来自任意时区，但必须是 timezone-aware datetime。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from lunar_python import Solar

RULE_ID = "MODERN-CHINESE-LUNISOLAR-FACTS"
CALENDAR_TIMEZONE = "Asia/Shanghai"


def _aware_datetime(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("moment须为datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("moment必须是timezone-aware datetime")
    return value


def chinese_lunisolar_facts(moment: datetime) -> dict[str, Any]:
    """同一绝对瞬间 -> 中国标准时间下的现代农历/干支事实。"""
    source = _aware_datetime(moment)
    calendar_tz = ZoneInfo(CALENDAR_TIMEZONE)
    local = source.astimezone(calendar_tz)

    solar = Solar.fromYmdHms(
        local.year,
        local.month,
        local.day,
        local.hour,
        local.minute,
        local.second,
    )
    lunar = solar.getLunar()

    signed_month = lunar.getMonth()
    month = abs(signed_month)
    leap = signed_month < 0

    return {
        "rule_id": RULE_ID,
        "source_profile": "production_modern_chinese_lunisolar",
        "provider": "lunar_python",
        "calendar_timezone": CALENDAR_TIMEZONE,
        "input": source,
        "calendar_local_time": local,
        "gregorian": {
            "year": local.year,
            "month": local.month,
            "day": local.day,
            "hour": local.hour,
            "minute": local.minute,
            "second": local.second,
        },
        "lunar": {
            "year": lunar.getYear(),
            "month": month,
            "signed_month": signed_month,
            "is_leap_month": leap,
            "day": lunar.getDay(),
            "month_name": lunar.getMonthInChinese(),
            "day_name": lunar.getDayInChinese(),
        },
        "ganzhi": {
            # 农历春节年：仅作现代农历事实，不作为太乙岁换年依据。
            "lunar_year": lunar.getYearInGanZhi(),
            # 节气/立春体系的年、月干支：同样只作并列事实。
            "jieqi_year_exact": lunar.getYearInGanZhiExact(),
            "jieqi_month_exact": lunar.getMonthInGanZhiExact(),
            # 两种日界口径同时保留，暂不替太乙日计作选择。
            "day_exact": lunar.getDayInGanZhiExact(),
            "day_exact_zi": lunar.getDayInGanZhiExact2(),
            "time": lunar.getTimeInGanZhi(),
        },
        "boundary_separation": {
            "taiyi_year": "由真实冬至瞬间单独决定",
            "lunar_year": "由现代中国农历春节决定",
            "jieqi_year_exact": "节气/立春体系，只作事实展示",
        },
        "policy": (
            "现代农历事实与太乙岁并列；春节、立春均不得覆盖太乙冬至换年。"
            "日干支两种日界口径暂同时保留，待日计production规则独立定案。"
        ),
    }
