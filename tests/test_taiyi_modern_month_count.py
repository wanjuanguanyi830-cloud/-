from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from kintaiyi.taiyi_modern_calendar import winter_solstice_utc
from kintaiyi.taiyi_modern_month_count import (
    MONTH_BRANCH_INDEX,
    accumulated_month_from_cycle,
    modern_month_count,
)
from kintaiyi.taiyi_modern_solar_month import jie_instant_utc


def test_month_count_uses_source_12_month_arithmetic():
    data = accumulated_month_from_cycle(
        cycle_historical_year=724,
        month_build_branch="子",
    )
    assert data["year_accumulated_count"] == 1_937_281
    assert data["month_index_1based"] == 1
    assert data["accumulated_month"] == (1_937_281 - 1) * 12 + 1


def test_month_branch_index_is_zi_through_hai():
    assert MONTH_BRANCH_INDEX == {
        "子": 1, "丑": 2, "寅": 3, "卯": 4, "辰": 5, "巳": 6,
        "午": 7, "未": 8, "申": 9, "酉": 10, "戌": 11, "亥": 12,
    }


def test_month_count_advances_exactly_at_jie_boundary():
    lichun = jie_instant_utc(2026, "立春")
    before = modern_month_count(lichun - timedelta(microseconds=1))
    exact = modern_month_count(lichun)

    assert before["month_build_branch"] == "丑"
    assert exact["month_build_branch"] == "寅"
    assert exact["accumulated_month"] == before["accumulated_month"] + 1


def test_winter_solstice_changes_year_count_but_not_month_count():
    boundary = winter_solstice_utc(2026)
    before = modern_month_count(boundary - timedelta(microseconds=1))
    exact = modern_month_count(boundary)

    assert before["month_build_branch"] == "子"
    assert exact["month_build_branch"] == "子"
    assert before["accumulated_month"] == exact["accumulated_month"]


def test_chinese_new_year_does_not_advance_month_count():
    tz = ZoneInfo("Asia/Shanghai")
    before = modern_month_count(datetime(2027, 2, 5, 12, tzinfo=tz))
    new_year = modern_month_count(datetime(2027, 2, 6, 12, tzinfo=tz))

    assert before["accumulated_month"] == new_year["accumulated_month"]
    assert before["month_build_branch"] == new_year["month_build_branch"]


def test_leap_lunar_month_does_not_advance_month_count():
    tz = ZoneInfo("Asia/Shanghai")
    before = modern_month_count(datetime(2025, 7, 24, 12, tzinfo=tz))
    leap_start = modern_month_count(datetime(2025, 7, 25, 12, tzinfo=tz))

    assert before["accumulated_month"] == leap_start["accumulated_month"]
    assert leap_start["month_build_branch"] == "未"


def test_daxue_starts_next_month_cycle_year():
    daxue = jie_instant_utc(2026, "大雪")
    exact = modern_month_count(daxue)
    assert exact["cycle_historical_year"] == 2027
    assert exact["month_build_branch"] == "子"
    assert exact["arithmetic"]["month_index_1based"] == 1
