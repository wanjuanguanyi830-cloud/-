"""现代 production 天文历法事实层。

硬约束：
- 太乙岁唯一换年边界：真实天文冬至瞬间；
- 公历年Y的冬至瞬间，太乙岁标签 Y -> Y+1；
- 元旦、春节、立春、春分均不触发太乙换年；
- 时计半岁：冬至瞬间起阳局，夏至瞬间起阴局。

天文引擎只负责提供季节瞬间；太乙边界语义属于本项目规则。
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import astronomy

from .taiyi_core_chain import year_count_from_historical_year
from .taiyi_modern_lunisolar import chinese_lunisolar_facts
from .taiyi_modern_solar_month import resolve_solar_month
from .taiyi_modern_month_count import modern_month_count
from .taiyi_modern_day_count import modern_day_count

RULE_ID = "MODERN-TAIYI-ASTRONOMICAL-CALENDAR"
YEAR_BOUNDARY_RULE_ID = "MODERN-TAIYI-YEAR-WINTER-SOLSTICE"
TIME_HALF_RULE_ID = "MODERN-TAIYI-TIME-SOLSTICE-HALF"


def _aware_datetime(value: datetime) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("moment须为datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("moment必须是timezone-aware datetime")
    return value


def _astronomy_time_to_utc(value: Any) -> datetime:
    dt = value.Utc()
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _calendar_year(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("year须为整数")
    if not 2 <= value <= 9998:
        raise ValueError("现代datetime天文层当前要求year在2..9998")
    return value


def season_instants_utc(year: int) -> dict[str, datetime]:
    """返回现代天文季节点UTC瞬间。"""
    y = _calendar_year(year)
    seasons = astronomy.Seasons(y)
    return {
        "march_equinox": _astronomy_time_to_utc(seasons.mar_equinox),
        "june_solstice": _astronomy_time_to_utc(seasons.jun_solstice),
        "september_equinox": _astronomy_time_to_utc(seasons.sep_equinox),
        "december_solstice": _astronomy_time_to_utc(seasons.dec_solstice),
    }


def winter_solstice_utc(year: int) -> datetime:
    return season_instants_utc(year)["december_solstice"]


def summer_solstice_utc(year: int) -> datetime:
    return season_instants_utc(year)["june_solstice"]


def resolve_taiyi_year(moment: datetime) -> dict[str, Any]:
    """按唯一冬至边界，把现代时间解析为太乙岁标签。

    公历Y年冬至前：太乙Y岁。
    公历Y年冬至瞬间及其后：太乙Y+1岁。
    """
    local = _aware_datetime(moment)
    utc = local.astimezone(timezone.utc)
    y = _calendar_year(utc.year)

    boundary = winter_solstice_utc(y)
    if utc >= boundary:
        taiyi_year = y + 1
        start = boundary
        next_boundary = winter_solstice_utc(y + 1)
        relation = "at_or_after_current_year_winter_solstice"
    else:
        taiyi_year = y
        start = winter_solstice_utc(y - 1)
        next_boundary = boundary
        relation = "before_current_year_winter_solstice"

    return {
        "rule_id": YEAR_BOUNDARY_RULE_ID,
        "source_profile": "production_modern_astronomy",
        "input": local,
        "input_utc": utc,
        "taiyi_historical_year": taiyi_year,
        "taiyi_year_start_utc": start,
        "next_taiyi_year_start_utc": next_boundary,
        "current_gregorian_year_winter_solstice_utc": boundary,
        "boundary_relation": relation,
        "boundary_operator": "moment < winter_solstice => Y; moment >= winter_solstice => Y+1",
        "ignored_year_boundaries": ["元旦", "春节", "立春", "春分"],
        "policy": (
            "太乙岁只在真实天文冬至交节瞬间换年；"
            "公历Y年冬至瞬间起进入太乙Y+1岁。"
        ),
    }


def resolve_time_solstice_half(moment: datetime) -> dict[str, Any]:
    """按真实二至瞬间判断时计阳/阴半岁。"""
    local = _aware_datetime(moment)
    utc = local.astimezone(timezone.utc)
    y = _calendar_year(utc.year)

    june = summer_solstice_utc(y)
    december = winter_solstice_utc(y)

    if utc < june:
        half = "冬至后"
        dun = "阳"
        start = winter_solstice_utc(y - 1)
        next_boundary = june
        boundary_name = "夏至"
    elif utc < december:
        half = "夏至后"
        dun = "阴"
        start = june
        next_boundary = december
        boundary_name = "冬至"
    else:
        half = "冬至后"
        dun = "阳"
        start = december
        next_boundary = summer_solstice_utc(y + 1)
        boundary_name = "夏至"

    return {
        "rule_id": TIME_HALF_RULE_ID,
        "source_profile": "production_modern_astronomy",
        "input": local,
        "input_utc": utc,
        "solstice_half": half,
        "dun": dun,
        "half_start_utc": start,
        "next_half_boundary_utc": next_boundary,
        "next_half_boundary_name": boundary_name,
        "policy": (
            "冬至瞬间起为冬至后/阳局；夏至瞬间起为夏至后/阴局。"
            "不用固定公历日期近似。"
        ),
    }


def modern_year_count(moment: datetime) -> dict[str, Any]:
    """现代datetime -> 冬至换年 -> source-specific岁计G1..G7。"""
    resolved = resolve_taiyi_year(moment)
    core = year_count_from_historical_year(
        historical_year=resolved["taiyi_historical_year"]
    )
    return {
        "rule_id": "MODERN-YEAR-COUNT-G1-G7",
        "source_profile": "production_modern_astronomy",
        "calendar": resolved,
        "result": core,
        "taiyi_historical_year": resolved["taiyi_historical_year"],
        "accumulated_year": core["accumulated_year"],
        "taisui_ganzhi": core["taisui_ganzhi"],
        "local_ju": core["local_ju"],
        "policy": (
            "现代生产岁计由真实冬至瞬间先解析太乙岁标签，"
            "再进入既有L0/G1-G7；元旦春节立春春分不改岁。"
        ),
    }


def production_calendar_context(moment: datetime) -> dict[str, Any]:
    """一次返回现代production四计所需的统一日历事实与计数结果。"""
    # lazy import 避免 taiyi_modern_time_count -> taiyi_modern_calendar 的循环导入
    from .taiyi_modern_time_count import modern_time_count

    return {
        "rule_id": RULE_ID,
        "source_profile": "production_modern_calendar",
        "year_boundary": resolve_taiyi_year(moment),
        "year_count": modern_year_count(moment),
        "time_half": resolve_time_solstice_half(moment),
        "lunisolar": chinese_lunisolar_facts(moment),
        "solar_month": resolve_solar_month(moment),
        "month_count": modern_month_count(moment),
        "day_count": modern_day_count(moment),
        "time_count": modern_time_count(moment),
        "astronomy_provider": "astronomy-engine",
        "lunisolar_provider": "lunar_python",
        "policy": (
            "天文引擎提供冬夏至与十二节精确交节；现代农历库提供农历/干支事实。"
            "production已自动生成岁/月/日/时四计所需计数；"
            "太乙岁由冬至决定，月界由十二节决定，日界/连续时序由中国标准民用日决定。"
        ),
    }
