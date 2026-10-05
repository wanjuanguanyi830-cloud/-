from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest

from kintaiyi.taiyi_modern_lunisolar import (
    CALENDAR_TIMEZONE,
    chinese_lunisolar_facts,
)


def test_modern_lunisolar_uses_china_standard_calendar_timezone():
    data = chinese_lunisolar_facts(
        datetime(2027, 1, 1, 12, tzinfo=timezone.utc)
    )
    assert data["calendar_timezone"] == "Asia/Shanghai"
    assert data["calendar_local_time"].tzinfo == ZoneInfo(CALENDAR_TIMEZONE)


def test_2027_new_year_day_is_still_lunar_2026():
    data = chinese_lunisolar_facts(
        datetime(2027, 1, 1, 12, tzinfo=timezone.utc)
    )
    assert data["lunar"]["year"] == 2026
    assert data["lunar"]["is_leap_month"] is False


def test_2027_chinese_new_year_starts_lunar_year_2027():
    data = chinese_lunisolar_facts(
        datetime(2027, 2, 6, 12, tzinfo=ZoneInfo("Asia/Shanghai"))
    )
    assert data["lunar"]["year"] == 2027
    assert data["lunar"]["month"] == 1
    assert data["lunar"]["day"] == 1
    assert data["lunar"]["is_leap_month"] is False


def test_2025_leap_sixth_month_is_preserved_as_explicit_fact():
    data = chinese_lunisolar_facts(
        datetime(2025, 7, 25, 12, tzinfo=ZoneInfo("Asia/Shanghai"))
    )
    assert data["lunar"]["year"] == 2025
    assert data["lunar"]["month"] == 6
    assert data["lunar"]["day"] == 1
    assert data["lunar"]["is_leap_month"] is True
    assert data["lunar"]["signed_month"] == -6


def test_lunisolar_facts_keep_multiple_ganzhi_conventions_separate():
    data = chinese_lunisolar_facts(
        datetime(2027, 1, 1, 12, tzinfo=timezone.utc)
    )
    assert len(data["ganzhi"]["lunar_year"]) == 2
    assert len(data["ganzhi"]["jieqi_year_exact"]) == 2
    assert len(data["ganzhi"]["jieqi_month_exact"]) == 2
    assert len(data["ganzhi"]["day_exact"]) == 2
    assert len(data["ganzhi"]["day_exact_zi"]) == 2
    assert len(data["ganzhi"]["time"]) == 2
    assert "冬至" in data["boundary_separation"]["taiyi_year"]


def test_modern_lunisolar_rejects_naive_datetime():
    with pytest.raises(ValueError):
        chinese_lunisolar_facts(datetime(2027, 1, 1, 12))
