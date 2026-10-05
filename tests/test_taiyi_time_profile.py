from kintaiyi.taiyi_time_profile import time_count_profile, time_profile_contract


def test_winter_time_profile_is_yang_and_open_first_duty_door():
    data = time_count_profile(
        entry_count=1,
        solstice_half="冬至后",
        duty_time_real=0,
    )
    assert data["dun"] == "阳"
    assert data["taiyi_palace"] == 1
    assert data["wenchang_sector"] == "申"
    assert data["jishen_sector"] == "寅"
    assert data["direct_door"] == "开"


def test_summer_time_profile_is_yin_and_du_first_duty_door():
    data = time_count_profile(
        entry_count=1,
        solstice_half="夏至后",
        duty_time_real=0,
    )
    assert data["dun"] == "阴"
    assert data["taiyi_palace"] == 9
    assert data["wenchang_sector"] == "寅"
    assert data["jishen_sector"] == "申"
    assert data["direct_door"] == "杜"


def test_time_profile_keeps_entry_count_and_duty_time_real_separate():
    data = time_count_profile(
        entry_count=31,
        solstice_half="冬至后",
        duty_time_real=91,
    )
    assert data["entry_count"] == 31
    assert data["duty_time_real"] == 91
    assert data["direct_door"] == "休"


def test_time_profile_contract_requires_calendar_upstream():
    winter = time_profile_contract("冬至后")
    summer = time_profile_contract("夏至后")
    assert winter["dun"] == "阳"
    assert winter["time_duty_doors"] == ["开", "生", "惊", "休"]
    assert summer["dun"] == "阴"
    assert summer["time_duty_doors"] == ["杜", "死", "伤", "景"]
    assert winter["calendar_upstream_required"] is True
