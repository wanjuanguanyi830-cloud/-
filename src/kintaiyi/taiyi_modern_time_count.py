"""现代 production 时计积时 / 时实。

来源骨架：
- 《统宗》卷一：日数减一 × 12，加所求时，为积时。
- 《金镜》卷一：积日减一 × 12，并加加时辰数，为冬/夏至时实；
  二至以后继续用“时实”推太乙、计神与八门。

production 现代化：
- 积日采用 MODERN-TAIYI-DAY-COUNT；
- 一日固定12个太乙时单位；
- 子正/午夜为日内第1单位起点：00:00–01:59=1，…，22:00–23:59=12；
- 二至阴阳切换仍使用真实天文冬至/夏至瞬间；
- 干支时辰的23:00子初口径保留为并列事实，不改变太乙连续积时。
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .taiyi_modern_calendar import resolve_time_solstice_half
from .taiyi_modern_day_count import CALENDAR_TIMEZONE
from .taiyi_time_profile import time_count_profile

RULE_ID = "MODERN-TAIYI-TIME-COUNT"
TIME_UNITS_PER_DAY = 12


def _aware_datetime(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("moment须为datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("moment必须是timezone-aware datetime")
    return value


def taiyi_time_unit(moment: datetime) -> dict[str, Any]:
    """现代production太乙日内时序：午夜起，每2小时一算。"""
    source = _aware_datetime(moment)
    local = source.astimezone(ZoneInfo(CALENDAR_TIMEZONE))

    unit = local.hour // 2 + 1
    start_hour = (unit - 1) * 2
    end_hour = start_hour + 2

    return {
        "rule_id": "MODERN-TAIYI-TIME-UNIT",
        "calendar_timezone": CALENDAR_TIMEZONE,
        "input": source,
        "calendar_local_time": local,
        "time_unit_1based": unit,
        "start_local_hour": start_hour,
        "end_local_hour_exclusive": end_hour,
        "units_per_day": TIME_UNITS_PER_DAY,
        "boundary_basis": "子正/午夜连续两小时分组",
        "policy": (
            "00:00–01:59为第1时，02:00–03:59为第2时，"
            "依次至22:00–23:59第12时。"
            "23:00干支子时不推进太乙积日或重置太乙积时。"
        ),
    }


def accumulated_time_from_moment(moment: datetime) -> dict[str, Any]:
    """现代二至半岁起算的时计积时。

    保留旧函数名以兼容调用，但语义已经纠正为：
    当前冬/夏至半岁起始民用日 -> 所求日，第1日不加12；
    再加当前日内第几时。
    """
    source = _aware_datetime(moment)
    local = source.astimezone(ZoneInfo(CALENDAR_TIMEZONE))
    half = resolve_time_solstice_half(source)

    half_start_utc = half["half_start_utc"]
    half_start_local = half_start_utc.astimezone(ZoneInfo(CALENDAR_TIMEZONE))
    unit = taiyi_time_unit(source)

    day_offset = (local.date() - half_start_local.date()).days
    if day_offset < 0:
        raise RuntimeError("所求时早于已解析的当前二至半岁起点")

    time_unit = unit["time_unit_1based"]
    entry_count = day_offset * TIME_UNITS_PER_DAY + time_unit

    return {
        "rule_id": "MODERN-TAIYI-SOLSTICE-RELATIVE-TIME",
        "source_profile": "production_modern_solstice_relative_time_count",
        "solstice_half": half["solstice_half"],
        "dun": half["dun"],
        "half_start_utc": half_start_utc,
        "half_start_local": half_start_local,
        "half_start_local_date": half_start_local.date().isoformat(),
        "target_local_date": local.date().isoformat(),
        "day_offset_0based": day_offset,
        "day_index_1based": day_offset + 1,
        "time_unit_1based": time_unit,
        "entry_count": entry_count,
        "duty_time_real": entry_count,
        "numeric_relation": (
            "production adapter currently feeds the same solstice-relative 12-time count "
            "to four-count entry_count and C119 duty_time_real"
        ),
        "fields_remain_separate": True,
        "time_unit_context": unit,
        "half_context": half,
        "formula": "(day_index_1based - 1) * 12 + time_unit_1based",
        "legacy_function_name": "accumulated_time_from_moment",
        "policy": (
            "时计从当前冬至/夏至半岁重新起算，不继承日计历史绝对积日。"
            "二至精确瞬间切换新半岁；日内仍以子正/午夜为第1时起点。"
        ),
    }

def modern_time_count(moment: datetime) -> dict[str, Any]:
    """现代datetime -> 二至阴阳 + 连续积时 -> 时计G2..G7 + C119直门。"""
    source = _aware_datetime(moment)
    half = resolve_time_solstice_half(source)
    arithmetic = accumulated_time_from_moment(source)

    profile = time_count_profile(
        entry_count=arithmetic["entry_count"],
        solstice_half=half["solstice_half"],
        duty_time_real=arithmetic["duty_time_real"],
    )

    return {
        "rule_id": RULE_ID,
        "source_profile": "production_modern_solstice_relative_time_count",
        "input": source,
        "calendar_timezone": CALENDAR_TIMEZONE,
        "solstice_half": half["solstice_half"],
        "dun": half["dun"],
        "half_context": half,
        "arithmetic": arithmetic,
        "entry_count": arithmetic["entry_count"],
        "duty_time_real": arithmetic["duty_time_real"],
        "time_unit_1based": arithmetic["time_unit_1based"],
        "result": profile,
        "taiyi_palace": profile["taiyi_palace"],
        "wenchang_sector": profile["wenchang_sector"],
        "jishen_sector": profile["jishen_sector"],
        "shiji_sector": profile["shiji_sector"],
        "host_calc": profile["host_calc"],
        "guest_calc": profile["guest_calc"],
        "direct_door": profile["direct_door"],
        "policy": (
            "现代production时计：真实二至瞬间同时切阴阳遁并建立新的半岁时计起算。"
            "半岁内按中国标准民用日午夜起12时单位编号。"
        ),
    }
