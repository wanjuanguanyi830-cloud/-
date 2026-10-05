from kintaiyi.tongzong_v15_remaining import (
    anying_rishi,
    fenhe_yongbing,
    jungshi_shengfu_pan,
    qibing_fubing,
    remaining_v15_catalog,
    suidi_zhibian,
)


def test_v15_01_keeps_odd_troops_kill_positions_and_ambush_conditions_separate():
    result = qibing_fubing(
        skyeyes="巽",
        shiji="乾",
        home_cal=11,
        away_cal=22,
        pattern_evidence=["掩"],
    )

    assert result["source_rule_id"] == "V15-01"
    assert result["odd_troop_ratio"] == {"numerator": 3, "denominator": 10}
    assert result["big_kill_positions"]["host"]["position"] == "巽"
    assert result["big_kill_positions"]["guest"]["position"] == "乾"
    assert result["concealment"]["home"] is True
    assert result["concealment"]["away"] is False
    assert result["concealment"]["source_calcs"] == [1, 11, 21, 31]
    assert result["ambush_window"] == "掩迫时可发伏兵"
    assert "申酉戌" not in str(result)


def test_v15_01_missing_pattern_check_stays_partial():
    result = qibing_fubing(
        skyeyes="巽",
        shiji="乾",
        home_cal=1,
        away_cal=31,
        pattern_evidence=None,
    )

    assert result["computable"] is False
    assert result["status"] == "partial"
    assert "pattern_evidence" in result["missing_inputs"]


def test_v15_07_terrain_rule_and_formation_control_are_source_limited():
    result = suidi_zhibian(
        terrain_shape="后高前下",
        home_cal=4,
        away_cal=6,
    )

    assert result["source_rule_id"] == "V15-07"
    assert result["terrain_rule"] == {
        "formation": "锐阵",
        "element": "火",
        "effect": "利于进战溃敌",
    }
    assert result["formation_relation"]["winner"] == "主"
    assert result["formation_relation"]["relation"] == "火制金"
    assert len(result["terrain_arms_table"]) == 5


def test_v15_08_is_command_and_concentration_procedure_not_c8_formula():
    ready = fenhe_yongbing(
        battle_place_fixed=True,
        battle_time_fixed=True,
        orders_sent=True,
        arrivals={"甲将": "early", "乙将": "late"},
    )

    assert ready["source_rule_id"] == "V15-08"
    assert ready["concentration_ready"] is True
    assert ready["arrival_results"]["甲将"]["source_consequence"] == "赏"
    assert ready["arrival_results"]["乙将"]["source_consequence"] == "斩/罚"
    assert "three_doors" not in ready["prerequisites"]
    assert "five_generals" not in ready["prerequisites"]

    incomplete = fenhe_yongbing(
        battle_place_fixed=True,
        battle_time_fixed=False,
        orders_sent=True,
    )
    assert incomplete["concentration_ready"] is False
    assert incomplete["status"] == "procedure_incomplete"


def test_v15_11_requires_all_explicit_conditions_and_never_derives_eye_side_from_palace_number():
    favorable = anying_rishi(
        yin_yang_harmony=True,
        upper_eye_patterns=[],
        lower_eye_patterns=[],
        taiyi_in_yang_jue=False,
        upper_eye_in_yang_jue=False,
        lower_eye_in_yang_jue=False,
        three_doors_ready=True,
        five_generals_released=True,
    )

    assert favorable["source_rule_id"] == "V15-11"
    assert favorable["suitable"] is True
    assert favorable["status"] == "favorable"

    adverse = anying_rishi(
        yin_yang_harmony=True,
        upper_eye_patterns=["掩"],
        lower_eye_patterns=[],
        taiyi_in_yang_jue=False,
        upper_eye_in_yang_jue=False,
        lower_eye_in_yang_jue=False,
        three_doors_ready=True,
        five_generals_released=True,
    )
    assert adverse["suitable"] is False
    assert adverse["conditions"]["upper_eye_clear"] is False

    pending = anying_rishi()
    assert pending["suitable"] is None
    assert pending["status"] == "not_computable"


def test_v15_14_has_no_default_victory_without_observations():
    result = jungshi_shengfu_pan()

    assert result["source_rule_id"] == "V15-14"
    assert result["computable"] is False
    assert result["evidence"] == []
    assert result["winner"] is None
    assert result["status"] == "not_computable"
    assert "必胜" not in str(result)


def test_v15_14_wind_cloud_relation_and_external_observations_are_explicit():
    host = jungshi_shengfu_pan(
        observations={
            "wind_from_rear": True,
            "troops_vigorous": True,
            "horses_neighing": True,
            "flags_toward_enemy": True,
            "drums_clear": True,
            "command_harmonious": True,
        },
        wind_strength="strong",
        cloud_state="thin",
    )
    assert host["winner"] == "主"
    assert any(item["effect"] == "大胜之象" for item in host["evidence"])

    guest = jungshi_shengfu_pan(
        observations={"ghost_wind": True},
        wind_strength="weak",
        cloud_state="thick",
    )
    assert guest["winner"] == "客"
    assert any(item["effect"] == "兵败之象" for item in guest["evidence"])


def test_remaining_v15_catalog_closes_exact_five_rule_gap():
    data = remaining_v15_catalog()

    assert data["implemented"] == ["V15-01", "V15-07", "V15-08", "V15-11", "V15-14"]
    assert data["source_limited"] is True
    assert "V15-14" in data["old_reference_corrections"]
