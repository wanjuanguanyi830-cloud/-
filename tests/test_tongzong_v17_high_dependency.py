import pytest

from kintaiyi.tongzong_v17_high_dependency import (
    c28_catalog,
    enemy_state,
    hourly_general_affairs,
    military_action_timing,
)


def test_v17_01_all_required_conditions_make_timing_usable():
    data = military_action_timing(
        half_year="冬至后",
        skyeyes_clear_of_qiupo=True,
        shiji_clear_of_yanji=True,
        calc_harmony=True,
        generals_released=True,
        taiyi_under_open_rest_life_door=False,
    )
    assert data["computable"] is True
    assert data["usable"] is True
    assert data["required_background"] == "阳局"


def test_v17_01_open_rest_life_door_is_independent_blocker():
    data = military_action_timing(
        half_year="夏至后",
        skyeyes_clear_of_qiupo=True,
        shiji_clear_of_yanji=True,
        calc_harmony=True,
        generals_released=True,
        taiyi_under_open_rest_life_door=True,
    )
    assert data["usable"] is False
    assert any("开休生门" in item["condition"] for item in data["blockers"])


def test_v17_01_missing_structured_input_is_not_computable():
    data = military_action_timing(
        half_year="冬至后",
        skyeyes_clear_of_qiupo=None,
        shiji_clear_of_yanji=True,
        calc_harmony=True,
        generals_released=True,
        taiyi_under_open_rest_life_door=False,
    )
    assert data["status"] == "not_computable"
    assert data["usable"] is None
    assert "skyeyes_clear_of_qiupo" in data["missing_inputs"]


def test_v17_01_supplemental_patterns_are_explicit_only():
    data = military_action_timing(
        half_year="冬至后",
        skyeyes_clear_of_qiupo=True,
        shiji_clear_of_yanji=True,
        calc_harmony=True,
        generals_released=True,
        taiyi_under_open_rest_life_door=False,
        obstructing_patterns=["关", "格"],
    )
    assert data["usable"] is False
    assert [item["condition"] for item in data["blockers"]] == ["见关", "见格"]


def test_v17_01_rejects_legacy_pattern_sentence():
    with pytest.raises(ValueError):
        military_action_timing(
            half_year="冬至后",
            skyeyes_clear_of_qiupo=True,
            shiji_clear_of_yanji=True,
            calc_harmony=True,
            generals_released=True,
            taiyi_under_open_rest_life_door=False,
            obstructing_patterns=["文昌囚迫不利"],
        )


@pytest.mark.parametrize("calc", [5, 15, 25, 35])
def test_v17_02_duse_is_direct_no_arrival(calc):
    data = enemy_state(
        calc,
        calc_harmony=True,
        three_doors_ready=True,
        five_generals_released=True,
        host_guest_gather_taiyi_front=True,
    )
    assert data["duse"] is True
    assert data["arrival"] == "敌不来"
    assert data["summary"] == "no_arrival_direct"


def test_v17_02_all_good_conditions_mean_surrender_not_bandit():
    data = enemy_state(
        22,
        calc_harmony=True,
        three_doors_ready=True,
        five_generals_released=True,
        host_guest_gather_taiyi_front=True,
    )
    assert data["summary"] == "surrender_not_bandit"
    assert data["arrival"] == "敌来降"
    assert data["disposition"] == "不为寇盗"


def test_v17_02_mixed_signs_are_not_overwritten():
    data = enemy_state(
        22,
        calc_harmony=True,
        three_doors_ready=True,
        five_generals_released=False,
        has_yanji=True,
        host_guest_gather_taiyi_front=True,
    )
    assert data["summary"] == "mixed_evidence"
    assert data["favorable_evidence"]
    assert data["hostile_evidence"]


def test_v17_02_all_bad_signs_are_hostile_evidence():
    data = enemy_state(
        17,
        calc_harmony=False,
        three_doors_ready=False,
        five_generals_released=False,
        has_yanji=True,
        has_poji=True,
        has_clamp_or_ge=True,
        host_guest_gather_taiyi_front=False,
    )
    assert data["summary"] == "hostile_evidence"
    assert data["arrival"] == "若入则为寇盗"


def test_v17_02_guest_eye_motion_is_scoped_to_northern_enemy_example():
    north = enemy_state(
        17,
        calc_harmony=None,
        three_doors_ready=None,
        five_generals_released=None,
        host_guest_gather_taiyi_front=None,
        enemy_origin="北",
        guest_eye_motion="南",
    )
    east = enemy_state(
        17,
        calc_harmony=None,
        three_doors_ready=None,
        five_generals_released=None,
        host_guest_gather_taiyi_front=None,
        enemy_origin="东",
        guest_eye_motion="南",
    )
    assert north["motion_example"]["meaning"] == "来"
    assert east["motion_example"] is None


def test_v17_10_full_good_bundle_is_favorable():
    data = hourly_general_affairs(
        doors_ready=True,
        generals_released=True,
        calc_harmony=True,
    )
    assert data["summary"] == "favorable"
    assert data["favorable_evidence"][0]["effect"] == "百事吉"


def test_v17_10_full_bad_bundle_is_unfavorable():
    data = hourly_general_affairs(
        doors_ready=False,
        generals_released=False,
        calc_harmony=False,
    )
    assert data["summary"] == "unfavorable"
    assert data["unfavorable_evidence"][0]["effect"] == "百事凶"


def test_v17_10_partial_bundle_keeps_conditional_note():
    data = hourly_general_affairs(
        doors_ready=True,
        generals_released=False,
        calc_harmony=True,
    )
    assert data["summary"] == "undetermined"
    assert data["conditional_notes"][0]["effect"] == "当消息而推，不作全吉全凶"


def test_v17_10_masks_and_hits_are_separate_evidence():
    data = hourly_general_affairs(
        skyeyes_masks_taiyi=True,
        skyeyes_hits_taiyi=True,
        doors_ready=True,
        generals_released=True,
        calc_harmony=True,
    )
    assert data["summary"] == "mixed_evidence"
    assert len(data["unfavorable_evidence"]) == 2
    assert len(data["favorable_evidence"]) == 1


@pytest.mark.parametrize(
    "state,expected",
    [
        ("旺", "新事"),
        ("相", "相争事"),
        ("胎", "生产妇人事"),
        ("没", "溺没事"),
        ("死", "死丧事"),
        ("囚", "刑禁事"),
        ("休", "疾病；行人营事无成"),
        ("废", "废弃、改易、恐惧之事"),
    ],
)
def test_v17_10_qi_state_matter_map(state, expected):
    data = hourly_general_affairs(
        doors_ready=None,
        generals_released=None,
        calc_harmony=None,
        skyeyes_qi_state=state,
    )
    assert data["matter"] == expected


def test_v17_10_prison_opposition_adds_release_note():
    data = hourly_general_affairs(
        doors_ready=None,
        generals_released=None,
        calc_harmony=None,
        skyeyes_qi_state="囚",
        skyeyes_opposes_taiyi=True,
    )
    assert "赦释" in data["matter"]


def test_v17_10_social_roles_are_not_general_winner_signals():
    data = hourly_general_affairs(
        doors_ready=None,
        generals_released=None,
        calc_harmony=None,
        host_clamps_guest_or_blocks_guest=True,
        guest_clamps_host_or_blocks_host=True,
    )
    assert len(data["conditional_notes"]) == 2
    assert any("可言吏" in item["effect"] for item in data["conditional_notes"])
    assert any("可言民" in item["effect"] for item in data["conditional_notes"])


def test_v17_10_forbidden_directions_are_upstream_facts_only():
    data = hourly_general_affairs(
        doors_ready=None,
        generals_released=None,
        calc_harmony=None,
        forbidden_directions=["西北", "东南"],
    )
    assert data["forbidden_directions"] == ["西北", "东南"]
    assert "独立上游算法" in data["direction_policy"]


def test_c28_catalog_marks_high_structured_composite():
    data = c28_catalog()
    assert data["implemented"] == ["V17-01", "V17-02", "V17-10"]
    assert data["dependency_class"] == "high_structured_composite"
    assert data["source_limited_inputs"] is True
