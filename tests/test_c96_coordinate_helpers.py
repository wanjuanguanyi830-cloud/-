import pytest

from kintaiyi.taiyi_rules import (
    OPPOSITE_PALACES,
    SECTOR_GODS,
    SECTOR_TO_NINE_PALACE,
    general_palace_qi,
    nine_palace_opposition,
    nine_palace_representative_sector,
    nine_palace_to_trigram,
    qi_relation,
    rotate_sixteen,
    sector_detail,
    sector_opposition,
    sector_to_nine_palace,
)


def test_c96_sector_to_nine_palace_recovered_mapping():
    assert sector_to_nine_palace("子") == 8
    assert sector_to_nine_palace("亥") == 8
    assert sector_to_nine_palace("丑") == 3
    assert sector_to_nine_palace("艮") == 3
    assert sector_to_nine_palace("巳") == 2
    assert sector_to_nine_palace("午") == 2
    assert sector_to_nine_palace("戌") == 1
    assert sector_to_nine_palace("乾") == 1
    assert len(SECTOR_TO_NINE_PALACE) == 16


def test_c96_sector_gods_is_inverse_of_current_god_position():
    assert SECTOR_GODS["子"] == "地主"
    assert SECTOR_GODS["巽"] == "大炅"
    assert SECTOR_GODS["酉"] == "太簇"
    assert SECTOR_GODS["乾"] == "阴德"


def test_c96_sector_detail_keeps_sector_and_palace_elements_separate():
    data = sector_detail("辰")
    assert data["sector"] == "辰"
    assert data["god"] == "太阳"
    assert data["sector_element"] == "土"
    assert data["nine_palace"] == 9
    assert data["nine_palace_trigram"] == "巽"
    assert data["nine_palace_element"] == "木"
    assert data["projection_lossy"] is True


def test_c96_generic_sixteen_rotation_accepts_negative_steps():
    assert rotate_sixteen("子", 1) == "丑"
    assert rotate_sixteen("子", -1) == "亥"
    assert rotate_sixteen("子", 16) == "子"
    assert sector_opposition("子") == "午"
    assert sector_opposition("乾") == "巽"


def test_c96_nine_palace_helpers_preserve_center_boundary():
    assert nine_palace_to_trigram(1) == "乾"
    assert nine_palace_to_trigram(5) == "中"
    assert nine_palace_representative_sector(9) == "巽"
    with pytest.raises(ValueError, match="中五无十六宫代表点"):
        nine_palace_representative_sector(5)

    center = nine_palace_opposition(5)
    assert center["computable"] is False
    assert center["status"] == "pending"
    assert center["reason"] == "中宫对冲来源待校"

    assert nine_palace_opposition(1)["opposite_palace_id"] == 9
    assert nine_palace_opposition(2)["opposite_palace_id"] == 8
    assert OPPOSITE_PALACES[4] == 6


@pytest.mark.parametrize(
    "subject,environment,relation,state",
    [
        ("木", "木", "比和", "旺"),
        ("木", "水", "生我", "相"),
        ("木", "金", "克我", "死"),
        ("木", "土", "我克", "囚"),
        ("木", "火", "我生", "休"),
    ],
)
def test_c96_qi_relation_wraps_existing_five_state_formula(
    subject, environment, relation, state
):
    data = qi_relation(subject, environment)
    assert data == {
        "subject": subject,
        "environment": environment,
        "relation": relation,
        "state": state,
    }


def test_c96_general_palace_qi_is_explicit_coordinate_relation_only():
    data = general_palace_qi(1, "辰")
    assert data["palace_id"] == 1
    assert data["palace_element"] == "金"
    assert data["landing"]["sector"] == "辰"
    assert data["landing"]["nine_palace"] == 9
    assert data["model"] == "B"


def test_c96_rejects_bad_coordinate_inputs():
    with pytest.raises(ValueError, match="十六宫位置"):
        sector_to_nine_palace("中")
    with pytest.raises(TypeError):
        rotate_sixteen("子", True)
    with pytest.raises(ValueError):
        nine_palace_to_trigram(10)
