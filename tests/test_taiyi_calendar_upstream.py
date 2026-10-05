import pytest

from kintaiyi.taiyi_calendar_upstream import (
    calendar_automation_status,
    calendar_upstream_requirements,
    run_resolved_calendar_count,
)


def test_calendar_contract_year_requires_resolved_historical_year():
    req = calendar_upstream_requirements("岁计")
    assert req["required_facts"] == ["resolved_historical_year"]
    assert req["automatic_gregorian_resolution"] is True

    data = run_resolved_calendar_count(
        count_type="岁计",
        resolved_historical_year=724,
    )
    assert data["result"]["dun"] == "阳"
    assert data["result"]["taisui_ganzhi"] == "甲子"
    assert data["result"]["local_ju"] == 49


def test_calendar_contract_month_and_day_accept_only_resolved_accumulated_count():
    month = run_resolved_calendar_count(
        count_type="月计",
        accumulated_count=121,
    )
    day = run_resolved_calendar_count(
        count_type="日计",
        accumulated_count=121,
    )
    assert month["result"]["dun"] == "阳"
    assert day["result"]["dun"] == "阳"
    assert month["result"]["local_ju"] == 49
    assert day["result"]["local_ju"] == 49

    with pytest.raises(ValueError):
        run_resolved_calendar_count(count_type="月计", accumulated_count=None)


def test_calendar_contract_time_requires_explicit_solstice_half():
    winter = run_resolved_calendar_count(
        count_type="时计",
        entry_count=1,
        solstice_half="冬至后",
        duty_time_real=0,
    )
    summer = run_resolved_calendar_count(
        count_type="时计",
        entry_count=1,
        solstice_half="夏至后",
        duty_time_real=0,
    )
    assert winter["result"]["dun"] == "阳"
    assert winter["result"]["direct_door"] == "开"
    assert summer["result"]["dun"] == "阴"
    assert summer["result"]["direct_door"] == "杜"

    with pytest.raises(ValueError):
        run_resolved_calendar_count(count_type="时计", entry_count=1)


def test_calendar_contract_rejects_cross_layer_convenience_inputs():
    with pytest.raises(ValueError):
        run_resolved_calendar_count(
            count_type="岁计",
            resolved_historical_year=724,
            solstice_half="夏至后",
        )

    with pytest.raises(ValueError):
        run_resolved_calendar_count(
            count_type="日计",
            accumulated_count=121,
            solstice_half="夏至后",
        )


def test_calendar_automation_status_keeps_datetime_boundary_pending():
    status = calendar_automation_status()
    assert status["automatic_gregorian_resolution"] is False
    assert not any("岁计历史年边界" in item for item in status["pending"])
    assert not any("冬至/夏至气应时刻" in item for item in status["pending"])
    assert not any("月计" in item for item in status["pending"])
    assert not any("日计" in item for item in status["pending"])
    assert any("时计" in item for item in status["pending"])
