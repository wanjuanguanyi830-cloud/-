import pytest

from kintaiyi.tongzong_v15_observations import (
    BRANCH_TONE,
    C24_VERSION,
    c24_catalog,
    cloud_qi_direction,
    five_tone_wind,
    wind_from_bagua,
)


def test_v15_09_requires_explicit_wind_observation():
    data = five_tone_wind("卯")
    assert data["canonical"] == C24_VERSION
    assert data["source_rule_id"] == "V15-09"
    assert data["computable"] is False
    assert data["missing_inputs"] == ["wind_direction_branch"]
    assert "不得由盘面推造风音" in data["policy"]


@pytest.mark.parametrize(
    "branch,tone",
    [
        ("子", "宫"), ("午", "宫"),
        ("丑", "徵"), ("寅", "徵"), ("未", "徵"), ("申", "徵"),
        ("卯", "羽"), ("酉", "羽"),
        ("辰", "商"), ("戌", "商"),
        ("巳", "角"), ("亥", "角"),
    ],
)
def test_v15_09_branch_tone_table(branch, tone):
    data = five_tone_wind(branch, wind_direction_branch=branch)
    assert BRANCH_TONE[branch] == tone
    assert data["day_tone"]["tone"] == tone
    assert data["wind_tone"]["tone"] == tone
    assert data["relation"] == "same_element"


def test_v15_09_mother_and_child_relations_have_direct_source_effect():
    # 角木日，羽水风：水生木，母来翼子。
    mother = five_tone_wind("巳", wind_direction_branch="卯")
    assert mother["relation"] == "wind_parent_of_day"
    assert "母来翼子" in mother["direct_effect"]

    # 角木日，徵火风：木生火，子来扶母。
    child = five_tone_wind("巳", wind_direction_branch="寅")
    assert child["relation"] == "wind_child_of_day"
    assert "子来扶母" in child["direct_effect"]


def test_v15_09_does_not_turn_control_relation_into_generic_winner():
    data = five_tone_wind("卯", wind_direction_branch="寅")
    assert data["day_tone"]["element"] == "水"
    assert data["wind_tone"]["element"] == "火"
    assert data["relation"] == "day_controls_wind"
    assert data["winner"] is None
    assert data["direct_effect"] is None


def test_v15_09_ghost_wind_is_only_exact_textual_example_pattern():
    exact = five_tone_wind("巳", wind_direction_branch="辰")
    assert exact["day_tone"]["tone"] == "角"
    assert exact["wind_tone"]["tone"] == "商"
    assert exact["relation"] == "wind_controls_day"
    assert exact["ghost_wind_exact_example_match"] is True

    other = five_tone_wind("子", wind_direction_branch="辰")
    assert other["ghost_wind_exact_example_match"] is False


def test_v15_09_hour_tone_is_context_not_observation_substitute():
    data = five_tone_wind("子", hour_branch="午")
    assert data["hour_tone"]["tone"] == "宫"
    assert data["computable"] is False


@pytest.mark.parametrize(
    "palace,side_effect,movement",
    [
        (1, "利客", "客宜先举"),
        (8, "利客", "客宜先举"),
        (3, "利客", "客宜先举"),
        (4, "利主", "主宜后应"),
        (9, "利主", "主宜后应"),
        (2, "利主", "主宜后应"),
        (6, "客有伏兵", "主宜设备"),
    ],
)
def test_v15_12_bagua_wind_rules(palace, side_effect, movement):
    data = wind_from_bagua(palace)
    assert data["source_rule_id"] == "V15-12"
    assert data["computable"] is True
    assert data["side_effect"] == side_effect
    assert data["movement"] == movement


def test_v15_12_kun_ocr_uncertainty_is_not_forced_into_winner():
    data = wind_from_bagua(7)
    assert data["side_effect"] == "source_text_uncertain"
    assert data["movement"] is None
    assert "OCR" in data["source_note"]


def test_v15_12_missing_observation_is_not_computable():
    data = wind_from_bagua(None)
    assert data["computable"] is False
    assert data["missing_inputs"] == ["wind_palace"]


def test_v15_12_center_five_is_not_a_bagua_wind_direction():
    data = wind_from_bagua(5)
    assert data["computable"] is False
    assert data["status"] == "not_defined_by_source_passage"


def test_v15_13_requires_explicit_cloud_direction():
    data = cloud_qi_direction(18, 19, cloud_from_direction=None)
    assert data["source_rule_id"] == "V15-13"
    assert data["computable"] is False
    assert data["missing_inputs"] == ["cloud_from_direction"]


def test_v15_13_compares_directions_not_numeric_difference_five():
    # 主18的算向正北，云从正北来为顺。
    data = cloud_qi_direction(18, 19, cloud_from_direction="正北")
    assert data["home"] == {
        "calc": 18,
        "calc_direction": "正北",
        "opposite_direction": "正南",
        "relation": "顺",
    }
    # 客19算向东南，正北既非其算向也非对冲向。
    assert data["away"]["relation"] == "不应"


def test_v15_13_opposite_direction_is_reverse():
    data = cloud_qi_direction(18, 19, cloud_from_direction="正南")
    assert data["home"]["relation"] == "逆"


def test_v15_13_can_be_simultaneously_relevant_to_home_and_away_only_by_direction():
    data = cloud_qi_direction(18, 12, cloud_from_direction="正北")
    assert data["home"]["relation"] == "顺"
    assert data["away"]["calc_direction"] == "正南"
    assert data["away"]["relation"] == "逆"
    assert "总胜负" in data["policy"]


def test_v15_13_undefined_calc_direction_stays_explicit():
    data = cloud_qi_direction(20, 19, cloud_from_direction="东南")
    assert data["home"]["relation"] == "source_direction_undefined"
    assert data["away"]["relation"] == "顺"


def test_invalid_branch_rejected():
    with pytest.raises(ValueError):
        five_tone_wind("甲", wind_direction_branch="子")


def test_invalid_cloud_direction_rejected():
    with pytest.raises(ValueError):
        cloud_qi_direction(18, 19, cloud_from_direction="中央")


def test_c24_catalog_requires_external_observations():
    data = c24_catalog()
    assert data["implemented"] == ["V15-09", "V15-12", "V15-13"]
    assert data["all_require_external_observation"] is True
    assert data["next_dependency"] == []
    assert data["implemented_by_c25"] == ["V15-10"]
