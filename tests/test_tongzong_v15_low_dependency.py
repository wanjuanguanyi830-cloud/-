import pytest

from kintaiyi.tongzong_v15_low_dependency import (
    C23_VERSION,
    FORMATION_TEXT_VARIANT,
    c23_catalog,
    deity_march,
    deity_march_from_calc,
    five_formations_and_flags,
    formation_flag_from_calc,
    general_selection_principles,
    march_direction_from_calc,
    march_directions,
    troop_training_principles,
)


@pytest.mark.parametrize(
    "calc,formation,element,flag,direction",
    [
        (1, "曲阵", "水", "黑旗", "北方"),
        (8, "曲阵", "水", "黑旗", "北方"),
        (3, "直阵", "木", "青旗", "东方"),
        (4, "锐阵", "火", "赤旗", "南方"),
        (9, "锐阵", "火", "赤旗", "南方"),
        (2, "圆阵", "土", "黄旗", "中央"),
        (5, "圆阵", "土", "黄旗", "中央"),
        (6, "方阵", "金", "白旗", "西方"),
        (7, "方阵", "金", "白旗", "西方"),
    ],
)
def test_v15_02_formation_flag_source_mapping(calc, formation, element, flag, direction):
    data = formation_flag_from_calc(calc)
    assert data["canonical"] == C23_VERSION
    assert data["source_rule_id"] == "V15-02"
    assert data["formation"] == formation
    assert data["element"] == element
    assert data["flag"] == flag
    assert data["direction"] == direction
    assert data["cross_j4m_merge"] is False


def test_v15_02_explicitly_corrects_reference_digit_seven_mapping():
    data = formation_flag_from_calc(7)
    assert data["formation"] == "方阵"
    assert data["flag"] == "白旗"
    assert FORMATION_TEXT_VARIANT["reference_code_conflict"] == (
        "参考仓库旧表曾写3/7直阵、6方阵"
    )
    assert FORMATION_TEXT_VARIANT["resolution"] == (
        "preserve_variant_note_use_coherent_source_reading"
    )


def test_v15_02_exact_tens_are_not_invented():
    data = formation_flag_from_calc(20)
    assert data["computable"] is False
    assert data["digit"] == 10
    assert data["status"] == "not_defined_by_source_passage"


def test_v15_02_home_and_away_are_separate_not_a_winner():
    data = five_formations_and_flags(18, 27)
    assert data["home"]["formation"] == "曲阵"
    assert data["away"]["formation"] == "方阵"
    assert "winner" not in data
    assert "不由本条自动推出主客胜负" in data["policy"]


@pytest.mark.parametrize(
    "calc,order,tempo,cloth",
    [
        (1, "步卒在前、车骑次之、大将居中", "肃静缓行", "皂帛"),
        (4, "步卒在前、车骑次之、大将居中", "肃静缓行", "赤帛"),
        (6, "车骑在前、步卒次之、大将居中", "鼓噪急行", "白帛"),
        (9, "车骑在前、步卒次之、大将居中", "鼓噪急行", "赤帛"),
    ],
)
def test_v15_03_deity_march_regular_cases(calc, order, tempo, cloth):
    data = deity_march_from_calc(calc, side="主")
    assert data["source_rule_id"] == "V15-03"
    assert data["computable"] is True
    assert data["order"] == order
    assert data["tempo"] == tempo
    assert data["cloth"] == cloth
    assert "咒" not in data


def test_v15_03_five_is_not_filled_from_legacy_guess():
    data = deity_march_from_calc(5, side="客")
    assert data["computable"] is False
    assert data["status"] == "not_regularly_enumerated_by_source"
    assert data["digit"] == 5
    assert "不据参考代码扩写" in data["source_note"]


def test_v15_03_home_away_wrapper_preserves_side():
    data = deity_march(3, 7)
    assert data["home"]["side"] == "主"
    assert data["away"]["side"] == "客"
    assert data["home"]["cloth"] == "青帛"
    assert data["away"]["cloth"] == "白帛"


@pytest.mark.parametrize(
    "calc,direction",
    [
        (1, "西北"),
        (2, "正南"),
        (3, "东北"),
        (4, "正东"),
        (6, "正西"),
        (7, "西南"),
        (8, "正北"),
        (9, "东南"),
        (19, "东南"),
    ],
)
def test_v15_04_march_direction(calc, direction):
    data = march_direction_from_calc(calc, side="主")
    assert data["source_rule_id"] == "V15-04"
    assert data["direction"] == direction
    assert data["j4m_equivalent"] is False


def test_v15_04_five_and_ten_are_left_undefined():
    assert march_direction_from_calc(5, side="主")["computable"] is False
    assert march_direction_from_calc(10, side="客")["computable"] is False


def test_v15_04_wrapper_never_imports_j4m_06_extra_fields():
    data = march_directions(3, 6)
    assert data["home"]["direction"] == "东北"
    assert data["away"]["direction"] == "正西"
    for side in ("home", "away"):
        assert "formation" not in data[side]
        assert "flag" not in data[side]
        assert "背地" not in data[side]


def test_v15_05_selection_uses_eight_examinations():
    data = general_selection_principles()
    assert data["source_rule_id"] == "V15-05"
    assert data["method"] == "八征"
    assert len(data["checks"]) == 8
    assert data["checks"][0] == {"test": "问之以言", "observe": "辞"}
    assert data["checks"][-1] == {"test": "醉之以酒", "observe": "态"}
    assert "不宣称太乙独有" in data["policy"]


def test_v15_06_training_is_progressive_and_non_calculational():
    data = troop_training_principles()
    assert data["source_rule_id"] == "V15-06"
    assert data["progression"][0] == {"from": 1, "to": 10}
    assert data["progression"][-1] == {"from": 10000, "to": "三军"}
    assert len(data["discipline"]) == 3
    assert data["computable"] is True


def test_c23_catalog_stops_before_external_observation_rules():
    data = c23_catalog()
    assert data["implemented"] == ["V15-02", "V15-03", "V15-04", "V15-05", "V15-06"]
    assert data["pending_low_dependency"] == ["V15-09", "V15-12", "V15-13"]


@pytest.mark.parametrize("bad", [0, 41, -1])
def test_calc_out_of_range_rejected(bad):
    with pytest.raises(ValueError):
        formation_flag_from_calc(bad)


@pytest.mark.parametrize("bad", [1.5, "3", True])
def test_calc_type_rejected(bad):
    with pytest.raises(TypeError):
        formation_flag_from_calc(bad)


def test_side_validation_is_strict():
    with pytest.raises(ValueError):
        deity_march_from_calc(3, side="中")
    with pytest.raises(ValueError):
        march_direction_from_calc(3, side="中")
