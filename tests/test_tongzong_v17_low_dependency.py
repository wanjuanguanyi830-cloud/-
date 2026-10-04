import pytest

from kintaiyi.tongzong_v17_low_dependency import (
    C26_VERSION,
    c26_catalog,
    enemy_arrival_scale,
    enemy_envoy_truth,
    enemy_spy_state,
    traveler_arrival,
)


def test_v17_03_outer_shiji_marks_foreign_spy_envoy_without_claiming_absence_elsewhere():
    data = enemy_spy_state(
        shiji_realm="外",
        away_general_realm="内",
    )
    assert data["canonical"] == C26_VERSION
    assert data["source_rule_id"] == "V17-03"
    assert any(item["event"] == "foreign_spy_envoy" for item in data["events"])
    assert data["no_positive_condition"] is False


def test_v17_03_all_guest_factors_outer_marks_enemy_forces_entering():
    data = enemy_spy_state(
        shiji_realm="外",
        away_general_realm="外",
        away_vassal_realm="外",
    )
    assert any(item["event"] == "enemy_forces_entering" for item in data["events"])


def test_v17_03_skyeyes_outer_with_guest_general_same_place_marks_spy_entered():
    data = enemy_spy_state(
        shiji_realm="内",
        away_general_realm="外",
        skyeyes_realm="外",
        away_general_at_skyeyes=True,
    )
    assert any(item["event"] == "spy_entered_our_border" for item in data["events"])


def test_v17_03_no_matching_condition_does_not_invent_no_spy_verdict():
    data = enemy_spy_state(
        shiji_realm="内",
        away_general_realm="内",
    )
    assert data["events"] == []
    assert data["no_positive_condition"] is True
    assert "不反推“绝无间谍”" in data["policy"]


def test_v17_03_depth_is_explicit_not_geometrically_rebuilt():
    near = enemy_spy_state(
        shiji_realm="外",
        away_general_realm="内",
        shiji_depth="近",
    )
    far = enemy_spy_state(
        shiji_realm="外",
        away_general_realm="内",
        shiji_depth="远",
    )
    assert near["depth_meaning"] == "已入境"
    assert far["depth_meaning"] == "始发之期"


def test_v17_04_taiyi_controls_guest_factor_is_real_evidence():
    data = enemy_envoy_truth(
        taiyi_element="金",
        shiji_element="水",
        away_general_element="木",
    )
    assert data["source_rule_id"] == "V17-04"
    assert data["verdict"] == "实"
    assert data["real_evidence"] == ["太乙金制客大将木"]
    assert data["false_evidence"] == []


def test_v17_04_guest_controls_taiyi_is_false_evidence():
    data = enemy_envoy_truth(
        taiyi_element="木",
        shiji_element="金",
        away_general_element="水",
    )
    assert data["verdict"] == "虚"
    assert any("反制太乙木" in item for item in data["false_evidence"])


def test_v17_04_mixed_evidence_is_not_overwritten_by_order():
    data = enemy_envoy_truth(
        taiyi_element="土",
        shiji_element="木",
        away_general_element="水",
    )
    # 木克土=虚证；土克水=实证。
    assert data["verdict"] == "mixed_evidence"
    assert data["real_evidence"]
    assert data["false_evidence"]


def test_v17_04_no_control_relation_stays_undetermined():
    data = enemy_envoy_truth(
        taiyi_element="土",
        shiji_element="土",
        away_general_element="火",
    )
    assert data["verdict"] == "未定"


@pytest.mark.parametrize("calc", [5, 15, 25, 35])
def test_v17_05_duse_calculations_do_not_arrive(calc):
    data = enemy_arrival_scale(
        calc,
        time_yinyang="阳",
        calc_harmony=True,
        shiji_relative_position="左",
    )
    assert data["duse_no_arrival"] is True
    assert data["arrival"] == "不来"
    assert data["force_scale"] == "八门杜塞"


def test_v17_05_sixteen_plus_requires_harmony_for_large_force():
    ok = enemy_arrival_scale(
        22,
        time_yinyang="阳",
        calc_harmony=True,
        shiji_relative_position="右",
    )
    assert ok["arrival"] == "有贼"
    assert ok["force_scale"] == "兵众、有将有卒"
    assert ok["direction"] == "西方"

    no = enemy_arrival_scale(
        22,
        time_yinyang="阳",
        calc_harmony=False,
        shiji_relative_position="右",
    )
    assert "条件不成立" in no["force_scale"]


def test_v17_05_fifteen_below_is_small_force_when_not_duse():
    data = enemy_arrival_scale(
        14,
        time_yinyang="阳",
        calc_harmony=None,
        shiji_relative_position="前",
    )
    assert data["force_scale"] == "兵寡、无将"
    assert data["direction"] == "南方"


def test_v17_05_yin_time_does_not_force_scale_from_number():
    data = enemy_arrival_scale(
        22,
        time_yinyang="阴",
        calc_harmony=True,
        shiji_relative_position="后",
    )
    assert data["arrival"] == "无贼"
    assert data["force_scale"] == "不据兵数扩断"


@pytest.mark.parametrize(
    "position,direction",
    [("左", "东方"), ("右", "西方"), ("前", "南方"), ("后", "北方"), ("四维", "四维")],
)
def test_v17_05_direction_comes_from_explicit_shiji_relative_position(position, direction):
    data = enemy_arrival_scale(
        22,
        time_yinyang="阳",
        calc_harmony=True,
        shiji_relative_position=position,
    )
    assert data["direction"] == direction


@pytest.mark.parametrize(
    "direction,calc,expected",
    [
        ("北", 3, "不来"),
        ("北", 8, "不来"),
        ("北", 2, "来"),
        ("北", 7, "来"),
        ("东", 4, "不来"),
        ("东", 9, "不来"),
        ("东", 1, "来"),
        ("东", 6, "来"),
        ("西", 1, "不来"),
        ("西", 6, "不来"),
        ("西", 4, "来"),
        ("西", 9, "来"),
        ("南", 2, "不来"),
        ("南", 7, "不来"),
    ],
)
def test_v17_11_stable_number_rules(direction, calc, expected):
    data = traveler_arrival(direction, calc)
    assert data["base_verdict"] == expected
    assert data["effective_verdict"] == expected


@pytest.mark.parametrize("calc", [1, 6, 3, 8])
def test_v17_11_south_come_numbers_preserve_variant_conflict(calc):
    data = traveler_arrival("南", calc)
    assert data["base_verdict"] == "variant_conflict"
    assert data["source_variant"] is not None
    assert data["number_rule_status"] == "variant_conflict"


def test_v17_11_yanji_and_guange_are_explicit_modifiers():
    yanji = traveler_arrival("北", 2, has_yanji=True)
    assert yanji["base_verdict"] == "来"
    assert yanji["effective_verdict"] == "虽发未至"

    guange = traveler_arrival("北", 2, has_yanji=True, has_guange=True)
    assert guange["effective_verdict"] == "尚未发"


def test_v17_11_arrival_day_count_uses_guest_calc_without_extra_guessing():
    data = traveler_arrival("北", 23)
    assert data["arrival_day_count_method"]["days"] == 23
    assert "第23日" in data["arrival_day_count_method"]["source_example"]


def test_invalid_v17_inputs_rejected():
    with pytest.raises(ValueError):
        enemy_spy_state(shiji_realm="中", away_general_realm="外")
    with pytest.raises(ValueError):
        enemy_envoy_truth(
            taiyi_element="风",
            shiji_element="木",
            away_general_element="土",
        )
    with pytest.raises(ValueError):
        enemy_arrival_scale(
            22,
            time_yinyang="中",
            calc_harmony=True,
        )
    with pytest.raises(ValueError):
        traveler_arrival("中", 2)


def test_c26_catalog_lists_four_rules_and_known_variant():
    data = c26_catalog()
    assert data["implemented"] == ["V17-03", "V17-04", "V17-05", "V17-11"]
    assert data["source_limited_inputs"] is True
    assert data["known_variants"] == ["V17-11_south_come_numbers"]
