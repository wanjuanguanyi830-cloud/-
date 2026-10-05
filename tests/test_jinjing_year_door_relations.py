from kintaiyi.jinjing_year_door_relations import (
    year_door_meeting,
    year_door_meeting_wang_ximing,
    year_door_meeting_from_calcs,
)


def test_host_general_under_taiyi_three_good_doors_is_favorable():
    data = year_door_meeting(
        taiyi_palace=1,
        host_big_palace=8,
        guest_big_palace=4,
    )
    assert data["host"]["gate_under_taiyi_overlay"] == "休"
    assert data["host"]["meets_three_good_doors"] is True
    assert data["host"]["verdict"] == "大利"

    assert data["guest"]["gate_under_taiyi_overlay"] == "伤"
    assert data["guest"]["meets_three_good_doors"] is False


def test_same_palace_is_only_locally_open_door_favorable_not_global_override():
    data = year_door_meeting(
        taiyi_palace=1,
        host_big_palace=1,
        guest_big_palace=3,
    )
    assert data["host"]["gate_under_taiyi_overlay"] == "开"
    assert data["host"]["meets_three_good_doors"] is True
    assert "囚迫格对" in data["policy"]
    assert "最终军事判断" in data["policy"]


def test_blocked_center_general_stays_unknown_in_door_meeting():
    data = year_door_meeting(
        taiyi_palace=1,
        host_big_palace=None,
        guest_big_palace=3,
    )
    assert data["host"]["meets_three_good_doors"] is None
    assert data["host"]["status"] == "not_computable"
    assert data["guest"]["gate_under_taiyi_overlay"] == "生"
    assert data["guest"]["meets_three_good_doors"] is True



def test_wang_ximing_year_direct_door_meeting_uses_current_duty_door():
    data = year_door_meeting_wang_ximing(
        accumulated_year=91,
        taiyi_palace=1,
        host_big_palace=2,
        guest_big_palace=4,
    )
    assert data["source_status"] == "parallel_reconstruction"
    assert data["duty_door"] == "伤"
    assert data["taiyi_overlay"][1] == "伤"
    assert data["host"]["gate_under_taiyi_overlay"] == "开"
    assert data["host"]["meets_three_good_doors"] is True
    assert data["guest"]["gate_under_taiyi_overlay"] == "死"
    assert data["guest"]["meets_three_good_doors"] is False



def test_year_door_meeting_can_consume_g7_calcs_directly():
    data = year_door_meeting_from_calcs(
        taiyi_palace=1,
        host_calc=20,
        guest_calc=24,
    )
    assert data["generals"]["host"]["big_general_palace"] == 2
    assert data["generals"]["host"]["assistant_general_palace"] == 6
    assert data["meeting"]["host"]["gate_under_taiyi_overlay"] == "景"
    assert data["meeting"]["guest"]["gate_under_taiyi_overlay"] == "伤"


def test_year_door_meeting_from_calcs_preserves_blockage():
    data = year_door_meeting_from_calcs(
        taiyi_palace=1,
        host_calc=25,
        guest_calc=30,
    )
    assert data["host_blocked"] is True
    assert data["meeting"]["host"]["meets_three_good_doors"] is None
    assert data["meeting"]["host"]["status"] == "not_computable"
