from datetime import timedelta

from kintaiyi.taiyi_modern_solar_month import (
    jie_instant_utc,
    resolve_solar_month,
)


def test_lichun_exact_instant_switches_chou_to_yin_month():
    lichun = jie_instant_utc(2026, "立春")
    before = resolve_solar_month(lichun - timedelta(microseconds=1))
    exact = resolve_solar_month(lichun)

    assert before["month_build_branch"] == "丑"
    assert before["start_term"] == "小寒"
    assert exact["month_build_branch"] == "寅"
    assert exact["start_term"] == "立春"


def test_daxue_exact_instant_switches_hai_to_zi_month():
    daxue = jie_instant_utc(2026, "大雪")
    before = resolve_solar_month(daxue - timedelta(microseconds=1))
    exact = resolve_solar_month(daxue)

    assert before["month_build_branch"] == "亥"
    assert before["start_term"] == "立冬"
    assert exact["month_build_branch"] == "子"
    assert exact["start_term"] == "大雪"


def test_january_before_xiaohan_belongs_previous_daxue_zi_month():
    xiaohan = jie_instant_utc(2027, "小寒")
    data = resolve_solar_month(xiaohan - timedelta(days=1))
    assert data["start_term"] == "大雪"
    assert data["month_build_branch"] == "子"


def test_2025_leap_sixth_lunar_month_does_not_create_extra_solar_month():
    from datetime import datetime
    from zoneinfo import ZoneInfo

    data = resolve_solar_month(
        datetime(2025, 7, 25, 12, tzinfo=ZoneInfo("Asia/Shanghai"))
    )
    assert data["start_term"] == "小暑"
    assert data["month_build_branch"] == "未"
    assert data["leap_month_effect"] == "none"


def test_each_solar_month_has_known_next_jie():
    from datetime import timedelta

    for year, term, branch in (
        (2026, "小寒", "丑"),
        (2026, "立春", "寅"),
        (2026, "惊蛰", "卯"),
        (2026, "清明", "辰"),
        (2026, "立夏", "巳"),
        (2026, "芒种", "午"),
        (2026, "小暑", "未"),
        (2026, "立秋", "申"),
        (2026, "白露", "酉"),
        (2026, "寒露", "戌"),
        (2026, "立冬", "亥"),
        (2026, "大雪", "子"),
    ):
        instant = jie_instant_utc(year, term)
        data = resolve_solar_month(instant + timedelta(seconds=1))
        assert data["start_term"] == term
        assert data["month_build_branch"] == branch
