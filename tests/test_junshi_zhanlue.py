from kintaiyi.junshi_zhanlue import (
    jiangshuai_xianfou_layer,
    junshi_zhanlue,
    three_doors_five_generals_layer,
    zhuke_dongjing_layer,
)


def test_c8_reuses_eight_divinations_and_keeps_wuyin_separate_from_preparedness():
    data = junshi_zhanlue(home_cal=15, away_cal=25)
    home = data["layers"]["eight_divinations"]["home"]

    assert home["wuyin"]["rule_id"] == "D8-03"
    assert home["preparedness"]["rule_id"] == "D8-08"
    assert home["preparedness"]["present"] == ["将军", "吏士"]
    assert home["preparedness"]["missing"] == ["兵卒"]

    legacy = data["legacy_projection"]
    assert legacy["数有所主"]["主算"]["rule_id"] == "D8-08"
    assert legacy["五音"]["主算"]["rule_id"] == "D8-03"


def test_c8_five_is_only_ground_component():
    data = junshi_zhanlue(home_cal=5, away_cal=15)
    home = data["layers"]["eight_divinations"]["home"]["preparedness"]
    assert home["present"] == ["吏士"]
    assert home["missing"] == ["将军", "兵卒"]


def test_three_doors_and_five_generals_are_upstream_facts_not_recomputed():
    layer = three_doors_five_generals_layer("三門具。", "五將發。")
    assert layer["three_doors"]["ready"] is True
    assert layer["five_generals"]["released"] is True
    assert layer["joint_ready"] is True

    blocked = three_doors_five_generals_layer("三門具。", "主將主參不出中門，杜塞無門。")
    assert blocked["joint_ready"] is False


def test_host_guest_movement_does_not_declare_winner():
    ready = three_doors_five_generals_layer(True, True)
    layer = zhuke_dongjing_layer(ready)
    assert layer["roles"]["field_battle"]["first_mover"] == "客"
    assert layer["roles"]["field_battle"]["responder"] == "主"
    assert layer["roles"]["settled_context"]["first_mover"] == "主"
    assert layer["winner"] is None


def test_commander_rest_state_is_not_forced_into_good_or_bad():
    layer = jiangshuai_xianfou_layer(home_state="休", away_state="死")
    assert layer["home"]["status"] == "pending"
    assert layer["home"]["capable"] is None
    assert layer["away"]["status"] == "unfavorable"
    assert layer["away"]["capable"] is False


def test_cross_volume_rules_are_explicitly_excluded_from_default_composition():
    data = junshi_zhanlue(
        home_cal=17,
        away_cal=13,
        taiyi=8,
        skyeyes="地主",
        three_doors=True,
        five_generals=True,
        home_general_state="旺",
        away_general_state="囚",
    )
    excluded = {item["name"] for item in data["excluded_from_default"]}
    assert "孤虚对照" in excluded
    assert "太乙助主客" in excluded
    assert data["layers"]["eight_divinations"]["comparison"]["rule_id"] == "D8-06"
    assert data["layers"]["host_guest_movement"]["winner"] is None
