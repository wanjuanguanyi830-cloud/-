"""现代 production 日计积数。

原典锚点：
《太乙金镜式经》卷一记梁天监三年甲申岁六月八日，
日计积日为 707,501,061。

production：
- 用现代中国历法把该历史农历日转换为现代连续历日锚点；
- 当前日期按 Asia/Shanghai 民用日（00:00换日）；
- 两个历日相差几日，积日即增减几算；
- 不再使用旧实现708011105等经验常数。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from lunar_python import Lunar, Solar

from .taiyi_four_counts import four_count_core_from_accumulated_count

RULE_ID = "MODERN-TAIYI-DAY-COUNT"
CALENDAR_TIMEZONE = "Asia/Shanghai"

ANCHOR_LUNAR_YEAR = 504
ANCHOR_LUNAR_MONTH = 6
ANCHOR_LUNAR_DAY = 8
ANCHOR_ACCUMULATED_DAY = 707_501_061


def _aware_datetime(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("moment须为datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("moment必须是timezone-aware datetime")
    return value


def source_anchor_solar() -> Solar:
    """用现代中国历法重建原典梁天监三年六月八日的民用历日。"""
    return Lunar.fromYmd(
        ANCHOR_LUNAR_YEAR,
        ANCHOR_LUNAR_MONTH,
        ANCHOR_LUNAR_DAY,
    ).getSolar()


def accumulated_day_from_solar_date(solar: Solar) -> dict[str, Any]:
    anchor = source_anchor_solar()
    delta_days = solar.subtract(anchor)
    accumulated_day = ANCHOR_ACCUMULATED_DAY + delta_days

    return {
        "rule_id": "MODERN-TAIYI-DAY-COUNT-ARITHMETIC",
        "anchor_lunar": {
            "year": ANCHOR_LUNAR_YEAR,
            "month": ANCHOR_LUNAR_MONTH,
            "day": ANCHOR_LUNAR_DAY,
        },
        "anchor_solar": {
            "year": anchor.getYear(),
            "month": anchor.getMonth(),
            "day": anchor.getDay(),
        },
        "anchor_accumulated_day": ANCHOR_ACCUMULATED_DAY,
        "anchor_numeric_source_status": "primary_source_direct",
        "anchor_calendar_reconstruction": {
            "provider": "lunar_python",
            "provider_algorithm_family": "ShouXingUtil historical qi/shuo reconstruction",
            "status": "modern_historical_calendar_reconstruction",
            "not_primary_source_fact": True,
        },
        "target_solar": {
            "year": solar.getYear(),
            "month": solar.getMonth(),
            "day": solar.getDay(),
        },
        "delta_days": delta_days,
        "accumulated_day": accumulated_day,
        "policy": (
            "原典积日数作为数值锚点；历史农历到连续历日的换算由现代历法层完成。"
        ),
    }


def modern_day_count(moment: datetime) -> dict[str, Any]:
    """现代datetime -> 中国标准民用日 -> 日计积日 -> 日计G2..G7。"""
    source = _aware_datetime(moment)
    local = source.astimezone(ZoneInfo(CALENDAR_TIMEZONE))

    solar = Solar.fromYmd(local.year, local.month, local.day)
    arithmetic = accumulated_day_from_solar_date(solar)
    count = arithmetic["accumulated_day"]

    core = four_count_core_from_accumulated_count(
        count,
        count_type="日计",
    )

    return {
        "rule_id": RULE_ID,
        "source_profile": "production_modern_calendar_day_count",
        "historical_anchor_status": "primary_number_plus_modern_calendar_reconstruction",
        "calendar_timezone": CALENDAR_TIMEZONE,
        "input": source,
        "calendar_local_time": local,
        "day_boundary_local": "00:00:00",
        "accumulated_day": count,
        "arithmetic": arithmetic,
        "result": core,
        "local_ju": core["local_ju"],
        "taiyi_palace": core["taiyi_palace"],
        "wenchang_sector": core["wenchang_sector"],
        "shiji_sector": core["shiji_sector"],
        "host_calc": core["host_calc"],
        "guest_calc": core["guest_calc"],
        "policy": (
            "production日计按Asia/Shanghai民用日期00:00换日。"
            "23:00子初干支日界作为并列干支事实保留，不改变本日计积日边界。"
        ),
    }
