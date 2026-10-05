from kintaiyi.jinjing_year_door_relations import year_door_meeting


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
    assert "囚迫格对" in data["policy"]\n    assert "最终军事判断" in data["policy"]


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
