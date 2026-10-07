from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from kintaiyi.taiyi_modern_calendar import summer_solstice_utc, winter_solstice_utc
from kintaiyi.taiyi_modern_minute_count import (
    accumulated_minute_from_moment,
    modern_minute_count,
)


TZ = ZoneInfo("Asia/Shanghai")


def test_consecutive_absolute_minutes_advance_exactly_one_count():
    a = accumulated_minute_from_moment(datetime(2026, 10, 8, 12, 0, tzinfo=TZ))
    b = accumulated_minute_from_moment(datetime(2026, 10, 8, 12, 1, tzinfo=TZ))
    assert b["entry_count"] == a["entry_count"] + 1


def test_same_absolute_instant_is_timezone_invariant():
    utc = datetime(2026, 10, 8, 4, 17, tzinfo=timezone.utc)
    sh = utc.astimezone(TZ)
    a = modern_minute_count(utc)
    b = modern_minute_count(sh)
    assert a["entry_count"] == b["entry_count"]
    assert a["dun"] == b["dun"]
    assert a["result"]["local_ju"] == b["result"]["local_ju"]
    assert a["host_calc"] == b["host_calc"]
    assert a["guest_calc"] == b["guest_calc"]


def test_exact_summer_solstice_resets_to_first_yin_minute():
    boundary = summer_solstice_utc(2026)
    before = modern_minute_count(boundary - timedelta(microseconds=1))
    exact = modern_minute_count(boundary)
    assert before["dun"] == "阳"
    assert exact["dun"] == "阴"
    assert exact["entry_count"] == 1


def test_exact_winter_solstice_resets_to_first_yang_minute():
    boundary = winter_solstice_utc(2026)
    before = modern_minute_count(boundary - timedelta(microseconds=1))
    exact = modern_minute_count(boundary)
    assert before["dun"] == "阴"
    assert exact["dun"] == "阳"
    assert exact["entry_count"] == 1


def test_sixty_prematch_minutes_have_sixty_distinct_entry_counts():
    kickoff = datetime(2026, 10, 8, 20, 0, tzinfo=TZ)
    counts = [
        modern_minute_count(kickoff - timedelta(minutes=offset))["entry_count"]
        for offset in range(60, 0, -1)
    ]
    assert len(counts) == 60
    assert len(set(counts)) == 60
    assert counts == list(range(counts[0], counts[0] + 60))


def test_minute_core_keeps_c119_direct_door_unset():
    data = modern_minute_count(datetime(2026, 10, 8, 12, 30, tzinfo=TZ))
    assert data["result"]["count_type"] == "分计"
    assert data["direct_door"] is None
    assert data["taiyi_palace"] in {1, 2, 3, 4, 6, 7, 8, 9}
    assert 1 <= data["host_calc"] <= 40
    assert 1 <= data["guest_calc"] <= 40
