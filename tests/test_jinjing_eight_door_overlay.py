from kintaiyi.jinjing_eight_door_overlay import (
    duty_door_overlay,
    jinjing_year_open_door_contexts,
    open_door_overlay,
    taiyi_eight_door_context,
)


def test_open_door_overlay_anchor_one_matches_jinjing_volume2_fixed_directions():
    data = open_door_overlay(1)
    assert data["palace_to_door"] == {
        1: "开",
        8: "休",
        3: "生",
        4: "伤",
        9: "杜",
        2: "景",
        7: "死",
        6: "惊",
    }


def test_open_door_overlay_rotates_with_taiyi_anchor():
    data = open_door_overlay(8)
    assert data["palace_to_door"][8] == "开"
    assert data["palace_to_door"][3] == "休"
    assert data["palace_to_door"][4] == "生"
    assert data["palace_to_door"][1] == "惊"


def test_taiyi_overlay_projects_tianmu_interstitial_sector_to_palace():
    data = taiyi_eight_door_context(1, tianmu="丑")
    assert data["tianmu_palace"] == 3
    assert data["tianmu_gate"] == "生"

    same_palace_interstitial = taiyi_eight_door_context(1, tianmu="戌")
    assert same_palace_interstitial["tianmu_palace"] == 1
    assert same_palace_interstitial["tianmu_gate"] == "开"



def test_duty_door_overlay_places_current_direct_gate_at_anchor():
    data = duty_door_overlay(1, "伤")
    assert data["palace_to_door"] == {
        1: "伤",
        8: "杜",
        3: "景",
        4: "死",
        9: "惊",
        2: "开",
        7: "休",
        6: "生",
    }

    context = taiyi_eight_door_context(1, tianmu="卯", anchor_door="伤")
    assert context["taiyi_gate"] == "伤"
    assert context["tianmu_palace"] == 4
    assert context["tianmu_gate"] == "死"



def test_jinjing_year_four_open_door_overlays_are_independent():
    data = jinjing_year_open_door_contexts(
        taiyi_palace=1,
        host_big_palace=8,
        guest_big_palace=3,
        dingji_big_palace=4,
    )
    assert data["contexts"]["taiyi"]["palace_to_door"][1] == "开"
    assert data["contexts"]["host_big"]["palace_to_door"][8] == "开"
    assert data["contexts"]["guest_big"]["palace_to_door"][3] == "开"
    assert data["contexts"]["dingji_big"]["palace_to_door"][4] == "开"
    assert data["good_door_palaces"]["taiyi"] != data["good_door_palaces"]["host_big"]


def test_jinjing_year_four_overlays_do_not_fake_center_general():
    data = jinjing_year_open_door_contexts(
        taiyi_palace=1,
        host_big_palace=None,
        guest_big_palace=3,
        dingji_big_palace=None,
    )
    assert data["contexts"]["host_big"]["computable"] is False
    assert data["contexts"]["dingji_big"]["computable"] is False
