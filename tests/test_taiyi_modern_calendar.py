from datetime import timedelta, timezone

import pytest

from kintaiyi.taiyi_modern_calendar import (
    modern_year_count,
    production_calendar_context,
    resolve_taiyi_year,
    resolve_time_solstice_half,
    season_instants_utc,
    summer_solstice_utc,
    winter_solstice_utc,
)


def test_season_instants_are_timezone_aware_and_plausible():
    data = season_instants_utc(2026)
    for value in data.values():
        assert value.tzinfo == timezone.utc

    assert data["june_solstice"].month == 6
    assert 19 <= data["june_solstice"].day <= 22
    assert data["december_solstice"].month == 12
    assert 20 <= data["december_solstice"].day <= 23


def test_taiyi_year_switches_exactly_at_winter_solstice():
    boundary = winter_solstice_utc(2026)

    before = resolve_taiyi_year(boundary - timedelta(microseconds=1))
    exact = resolve_taiyi_year(boundary)
    after = resolve_taiyi_year(boundary + timedelta(microseconds=1))

    assert before["taiyi_historical_year"] == 2026
    assert exact["taiyi_historical_year"] == 2027
    assert after["taiyi_historical_year"] == 2027
    assert exact["taiyi_year_start_utc"] == boundary


def test_new_year_day_does_not_trigger_taiyi_year_change():
    from datetime import datetime

    dec31 = datetime(2026, 12, 31, 12, tzinfo=timezone.utc)
    jan1 = datetime(2027, 1, 1, 12, tzinfo=timezone.utc)

    assert resolve_taiyi_year(dec31)["taiyi_historical_year"] == 2027
    assert resolve_taiyi_year(jan1)["taiyi_historical_year"] == 2027


def test_spring_equinox_does_not_trigger_taiyi_year_change():
    from datetime import timedelta

    spring = season_instants_utc(2027)["march_equinox"]
    before = resolve_taiyi_year(spring - timedelta(seconds=1))
    after = resolve_taiyi_year(spring + timedelta(seconds=1))
    assert before["taiyi_historical_year"] == 2027
    assert after["taiyi_historical_year"] == 2027


def test_time_half_switches_exactly_at_summer_and_winter_solstice():
    june = summer_solstice_utc(2026)
    december = winter_solstice_utc(2026)

    assert resolve_time_solstice_half(june - timedelta(microseconds=1))["dun"] == "阳"
    assert resolve_time_solstice_half(june)["dun"] == "阴"
    assert resolve_time_solstice_half(december - timedelta(microseconds=1))["dun"] == "阴"
    assert resolve_time_solstice_half(december)["dun"] == "阳"


def test_modern_year_count_enters_next_taiyi_year_at_boundary():
    boundary = winter_solstice_utc(2026)

    before = modern_year_count(boundary - timedelta(microseconds=1))
    exact = modern_year_count(boundary)

    assert before["taiyi_historical_year"] == 2026
    assert exact["taiyi_historical_year"] == 2027
    assert exact["accumulated_year"] == before["accumulated_year"] + 1


def test_modern_calendar_rejects_naive_datetime():
    boundary = winter_solstice_utc(2026)
    naive = boundary.replace(tzinfo=None)

    with pytest.raises(ValueError):
        resolve_taiyi_year(naive)


def test_production_context_keeps_year_and_time_boundaries_separate():
    boundary = winter_solstice_utc(2026)
    data = production_calendar_context(boundary)
    assert data["year_boundary"]["taiyi_historical_year"] == 2027
    assert data["time_half"]["solstice_half"] == "冬至后"
    assert data["time_half"]["dun"] == "阳"



def test_production_context_keeps_taiyi_year_separate_from_lunar_new_year():
    from datetime import datetime

    data = production_calendar_context(
        datetime(2027, 1, 1, 12, tzinfo=timezone.utc)
    )
    assert data["year_boundary"]["taiyi_historical_year"] == 2027
    assert data["lunisolar"]["lunar"]["year"] == 2026
    assert data["lunisolar"]["boundary_separation"]["taiyi_year"] == "由真实冬至瞬间单独决定"


def test_production_context_chinese_new_year_changes_lunar_year_not_taiyi_year():
    from datetime import datetime
    from zoneinfo import ZoneInfo

    before = production_calendar_context(
        datetime(2027, 2, 5, 12, tzinfo=ZoneInfo("Asia/Shanghai"))
    )
    new_year = production_calendar_context(
        datetime(2027, 2, 6, 12, tzinfo=ZoneInfo("Asia/Shanghai"))
    )
    assert before["year_boundary"]["taiyi_historical_year"] == 2027
    assert new_year["year_boundary"]["taiyi_historical_year"] == 2027
    assert before["lunisolar"]["lunar"]["year"] == 2026
    assert new_year["lunisolar"]["lunar"]["year"] == 2027
