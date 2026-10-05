from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from kintaiyi.taiyi_modern_day_count import (
    ANCHOR_ACCUMULATED_DAY,
    modern_day_count,
    source_anchor_solar,
)


TZ = ZoneInfo("Asia/Shanghai")


def test_source_anchor_reconstructs_exact_accumulated_day():
    anchor = source_anchor_solar()
    moment = datetime(
        anchor.getYear(),
        anchor.getMonth(),
        anchor.getDay(),
        12,
        tzinfo=TZ,
    )
    data = modern_day_count(moment)
    assert data["accumulated_day"] == ANCHOR_ACCUMULATED_DAY
    assert data["arithmetic"]["delta_days"] == 0


def test_modern_day_count_advances_at_china_standard_midnight():
    before = modern_day_count(
        datetime(2026, 3, 24, 23, 59, 59, tzinfo=TZ)
    )
    after = modern_day_count(
        datetime(2026, 3, 25, 0, 0, 0, tzinfo=TZ)
    )
    assert after["accumulated_day"] == before["accumulated_day"] + 1


def test_2300_does_not_advance_production_day_count():
    before = modern_day_count(
        datetime(2026, 3, 24, 22, 59, 59, tzinfo=TZ)
    )
    zi_start = modern_day_count(
        datetime(2026, 3, 24, 23, 0, 0, tzinfo=TZ)
    )
    assert zi_start["accumulated_day"] == before["accumulated_day"]


def test_same_absolute_instant_uses_china_calendar_date():
    utc = ZoneInfo("UTC")
    a = modern_day_count(
        datetime(2026, 3, 24, 16, 30, tzinfo=utc)
    )
    b = modern_day_count(
        datetime(2026, 3, 25, 0, 30, tzinfo=TZ)
    )
    assert a["accumulated_day"] == b["accumulated_day"]


def test_day_count_enters_day_profile_fixed_yang():
    data = modern_day_count(
        datetime(2026, 3, 24, 12, tzinfo=TZ)
    )
    assert data["result"]["count_type"] == "日计"
    assert data["result"]["dun"] == "阳"
