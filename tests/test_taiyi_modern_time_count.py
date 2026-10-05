from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from kintaiyi.taiyi_modern_calendar import (
    summer_solstice_utc,
    winter_solstice_utc,
)
from kintaiyi.taiyi_modern_time_count import (
    accumulated_time_from_moment,
    modern_time_count,
    taiyi_time_unit,
)


TZ = ZoneInfo("Asia/Shanghai")


def test_time_unit_is_midnight_based_two_hour_sequence():
    samples = [
        (0, 1),
        (1, 1),
        (2, 2),
        (3, 2),
        (20, 11),
        (21, 11),
        (22, 12),
        (23, 12),
    ]
    for hour, expected in samples:
        data = taiyi_time_unit(
            datetime(2026, 3, 24, hour, 30, tzinfo=TZ)
        )
        assert data["time_unit_1based"] == expected


def test_accumulated_time_is_monotonic_across_midnight():
    before = accumulated_time_from_moment(
        datetime(2026, 3, 24, 23, 30, tzinfo=TZ)
    )
    after = accumulated_time_from_moment(
        datetime(2026, 3, 25, 0, 0, tzinfo=TZ)
    )
    assert after["accumulated_time"] == before["accumulated_time"] + 1


def test_2300_does_not_reset_taiyi_time_or_day():
    before = accumulated_time_from_moment(
        datetime(2026, 3, 24, 22, 30, tzinfo=TZ)
    )
    zi = accumulated_time_from_moment(
        datetime(2026, 3, 24, 23, 30, tzinfo=TZ)
    )
    assert zi["accumulated_day"] == before["accumulated_day"]
    assert zi["time_unit_1based"] == 12
    assert zi["accumulated_time"] == before["accumulated_time"]


def test_entry_count_and_duty_time_real_are_separate_fields_from_same_base():
    data = accumulated_time_from_moment(
        datetime(2026, 3, 24, 12, tzinfo=TZ)
    )
    assert data["entry_count"] == data["duty_time_real"]
    assert data["fields_remain_separate"] is True


def test_exact_summer_solstice_switches_to_yin_without_rewriting_time_base():
    boundary = summer_solstice_utc(2026)
    before = modern_time_count(boundary - timedelta(microseconds=1))
    exact = modern_time_count(boundary)

    assert before["dun"] == "阳"
    assert exact["dun"] == "阴"
    # 若交节未跨两小时边界，连续积时本身保持同一算；变化来自阴阳profile切换。
    assert abs(exact["entry_count"] - before["entry_count"]) <= 1


def test_exact_winter_solstice_switches_to_yang():
    boundary = winter_solstice_utc(2026)
    before = modern_time_count(boundary - timedelta(microseconds=1))
    exact = modern_time_count(boundary)

    assert before["dun"] == "阴"
    assert exact["dun"] == "阳"
    assert exact["solstice_half"] == "冬至后"


def test_same_absolute_instant_uses_same_china_standard_time_count():
    a = modern_time_count(
        datetime(2026, 3, 24, 16, 30, tzinfo=timezone.utc)
    )
    b = modern_time_count(
        datetime(2026, 3, 25, 0, 30, tzinfo=TZ)
    )
    assert a["entry_count"] == b["entry_count"]
    assert a["direct_door"] == b["direct_door"]


def test_modern_time_count_is_fully_connected_to_core_and_c119():
    data = modern_time_count(
        datetime(2026, 3, 24, 12, tzinfo=TZ)
    )
    assert data["result"]["count_type"] == "时计"
    assert data["result"]["dun"] == data["dun"]
    assert data["direct_door"] is not None
    assert data["taiyi_palace"] in {1, 2, 3, 4, 6, 7, 8, 9}
