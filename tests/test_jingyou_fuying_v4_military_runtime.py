from kintaiyi.jingyou_fuying_v4_military import (
    adapt_to_terrain,
    deploy_direction,
    direct_gate_from_period_count,
    dispatch_troops,
    five_generals,
    formation_by_terrain,
    host_guest_action,
    host_guest_relation,
    odd_ambush,
    taiyi_outer_inner,
    three_doors,
    weather_bird_support,
)


def test_jf4m01_direct_gate_and_three_doors_are_fuying_specific():
    direct = direct_gate_from_period_count(31)
    assert direct["source_rule_id"] == "JF4M-01"
    assert direct["direct_gate"] == "休"
    assert direct["block_of_30"] == 2

    blocked = three_doors(taiyi_gate="休", tianmu_gate="开", period_count=31)
    assert blocked["three_doors_ready"] is False
    assert blocked["not_ready_count"] == 3
    assert blocked["direct_gate_result"]["direct_gate"] == "休"


def test_jf4m02_resolves_general_relation_from_four_general_palaces():
    ready = five_generals(
        shiji_yanji=False,
        wenchang_qiupo=False,
        home_big=1,
        home_vassal=3,
        away_big=4,
        away_vassal=6,
        three_doors_ready=True,
    )
    assert ready["five_generals_released"] is True
    assert ready["combined_ready"] is True
    assert ready["general_relation_pairs"] == []
    assert ready["normalized_reading"] == "主客大小将无相关"
    assert ready["normalized_semantics"] == "四将无同宫之关"

    blocked = five_generals(
        shiji_yanji=False,
        wenchang_qiupo=False,
        home_big=1,
        home_vassal=3,
        away_big=1,
        away_vassal=6,
        three_doors_ready=True,
    )
    assert blocked["five_generals_released"] is False
    assert ("主大", "客大") in blocked["general_relation_pairs"]
    assert "主客大小将有同宫之关" in blocked["blockers"]


def test_jf4m02_center_five_does_not_create_eight_palace_guan():
    result = five_generals(
        shiji_yanji=False,
        wenchang_qiupo=False,
        home_big=5,
        home_vassal=5,
        away_big=4,
        away_vassal=6,
    )
    assert result["general_relation_pairs"] == []
    assert result["third_condition_clear"] is True
    assert result["five_generals_released"] is True


def test_jf4m02_explicit_legacy_condition_must_not_conflict_with_structural_relation():
    conflict = five_generals(
        shiji_yanji=False,
        wenchang_qiupo=False,
        home_big=1,
        home_vassal=3,
        away_big=1,
        away_vassal=6,
        third_condition_clear=True,
    )
    assert conflict["computable"] is False
    assert conflict["status"] == "not_computable"
    assert conflict["third_condition_clear"] is True
    assert conflict["structural_third_condition_clear"] is False


def test_jf4m03_examples_follow_fuying_eye_element_control():
    guest = host_guest_relation(host_eye_god="高丛", guest_eye_god="太簇")
    assert guest["host_eye_element"] == "木"
    assert guest["guest_eye_element"] == "金"
    assert guest["winner"] == "客"

    host = host_guest_relation(host_eye_god="阴主", guest_eye_god="地主")
    assert host["host_eye_element"] == "土"
    assert host["guest_eye_element"] == "水"
    assert host["winner"] == "主"


def test_jf4m04_roles_and_favorable_triad_are_independent_of_j4m_runtime():
    field = host_guest_action(
        "陈兵原野",
        three_doors_ready=True,
        five_generals_released=True,
        yin_yang_harmonious=True,
    )
    assert field["roles"] == {"first_mover": "客", "responder": "主"}
    assert field["winner"] == "客"

    settled = host_guest_action(
        "安居之势",
        three_doors_ready=False,
        five_generals_released=False,
        yin_yang_harmonious=False,
    )
    assert settled["roles"] == {"first_mover": "主", "responder": "客"}
    assert settled["winner"] is None
    assert settled["status"] == "hold_and_defend"


def test_jf4m05_and_06_preserve_fuying_calcs_and_direction_table():
    ready = dispatch_troops(
        32,
        three_doors_ready=True,
        five_generals_released=True,
        exit_gate="生",
    )
    assert ready["deployment_ready"] is True
    assert ready["eligible_calcs"] == [12, 22, 32]

    assert deploy_direction(3)["direction"] == "东北"
    assert deploy_direction(8)["direction"] == "正北"
    assert deploy_direction(5)["computable"] is False


def test_jf4m07_formation_control_and_terrain_table_are_fuying_native():
    result = formation_by_terrain(
        host_formation="锐阵",
        guest_formation="方阵",
        terrain_shape="后高前低",
    )
    assert result["formation_contest"]["winner"] == "主"
    assert result["formation_contest"]["relation"] == "火制金"
    assert result["terrain_status"] == "ok"
    assert result["terrain_rule"]["formation"] == "锐阵"
    assert result["terrain_table"]["地形跨斜"]["formation"] == "圆阵"
    assert result["terrain_table"]["左右势高岗"]["formation"] == "曲阵"


def test_jf4m08_preserves_fuying_specific_ratios():
    result = adapt_to_terrain(
        "步兵地",
        soldiers_trained=False,
        equipment_serviceable=True,
        general_inspects_troops=False,
    )
    assert result["terrain_rule"]["source_ratio_text"] == "车骑二不当一"
    assert len(result["source_facts"]["terrain_rules"]) == 6
    assert any(
        item["source_ratio_text"] == "长戟二不当一"
        for item in result["source_facts"]["terrain_rules"]
    )
    assert any("百不当十" in warning for warning in result["warnings"])
    assert any("五不当一" in warning for warning in result["warnings"])


def test_jf4m09_one_palace_is_explicitly_inner_and_helps_host():
    result = taiyi_outer_inner(
        1,
        three_doors_ready=True,
        five_generals_released=True,
    )
    assert result["realm"] == "地内"
    assert result["assists"] == "主"
    assert result["decisive_ready"] is True
    assert 1 in result["canonical_groups"]["地内助主"]


def test_jf4m10_keeps_fuying_punishment_reading_and_wing_outcomes():
    result = weather_bird_support([
        {
            "phenomenon": "飞鸟",
            "source_anchor": "主人刑",
            "action": "上来",
        },
        {
            "phenomenon": "云",
            "wing_target": "主人阵前",
        },
        {
            "phenomenon": "众鸟",
            "action": "冲阵",
            "crowd_noisy": True,
        },
    ])
    assert result["computable"] is True
    assert result["judgments"][0]["loser"] == "主"
    assert result["judgments"][1]["winner"] == "主"
    assert result["judgments"][2]["omen"] == "凶"


def test_jf4m11_odd_ambush_keeps_fuying_great_kill_reading():
    result = odd_ambush(
        army_size=100,
        tianmu_location="巽",
        calc_value=21,
        yanpo=True,
        enemy_near=True,
    )
    assert result["odd_force_count"] == 30
    assert result["great_kill_location"] == "巽"
    assert result["concealment_time"] is True
    assert "掩迫时发" in result["recommendations"]
    assert "伏于要害" in result["recommendations"]
    assert "奇兵必从大杀之地" in result["divergence_from_jinjing"]
    assert "12" not in str(result["concealment_calcs"])


def test_jf4m10_extended_source_transcription_cases():
    result = weather_bird_support([
        {
            "phenomenon": "云",
            "action": "冲格迫击",
            "target": "太乙宫",
        },
        {
            "phenomenon": "飞鸟",
            "source_anchor": "主目",
            "action": "去击",
            "target": "客大将宫",
        },
        {
            "phenomenon": "风",
            "source_anchor": "太岁",
            "action": "击",
            "target": "主人阵",
        },
        {
            "phenomenon": "飞鸟",
            "returning_wind": True,
            "birds_circling": True,
        },
        {
            "phenomenon": "众鸟",
            "action": "冲阵",
            "target": "客阵",
            "crowd_noisy": True,
        },
    ])

    assert result["judgments"][0]["omen"] == "大败"
    assert result["judgments"][1]["loser"] == "客"
    assert result["judgments"][2]["loser"] == "主"
    assert result["judgments"][3]["omen"] == "大败之兆"
    assert result["judgments"][4]["loser"] == "客"
    assert result["judgments"][4]["omen"] == "凶"
