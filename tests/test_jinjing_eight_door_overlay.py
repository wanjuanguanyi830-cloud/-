from kintaiyi.jinjing_eight_door_overlay import (
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
