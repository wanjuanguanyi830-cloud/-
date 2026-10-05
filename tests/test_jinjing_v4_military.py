from kintaiyi.jinjing_v4_military import (
    chenbing_xiangbei,
    chushi_fa,
    j4m03_eye_element_from_god,
    j4m_low_dependency_catalog,
    qifu_fa,
    sanmen_jubu,
    fengyun_feiniao_zhuzhan,
    suidi_zhibian,
    taiyi_tianwai_dinei,
    wujiang_fabu,
    yunqi_dingshengfu,
    zhimen_from_cycle_count,
    zhizhen_suidi,
    zhuke_fa,
    zhuke_xiangguan,
)


def test_j4m06_chenbing_xiangbei_uses_only_source_defined_rule_numbers():
    one = chenbing_xiangbei(1)
    assert one["rule_id"] == "J4M-06"
    assert one["出军"] == "西北"
    assert one["战利"] == "东南"
    assert one["阵"] == "方阵"
    assert one["旗"] == "白旗"

    two = chenbing_xiangbei(2)
    assert two["邪道"] == "西南"
    assert two["阵"] == "直阵"
    assert two["旗"] == "青旗"

    six = chenbing_xiangbei(6)
    assert six["出军"] == "正西"
    assert six["战利"] == "正东"
    assert six["阵"] == "方阵"

    undefined = chenbing_xiangbei(3)
    assert undefined["computable"] is False
    assert undefined["status"] == "not_defined_by_source_passage"
    assert undefined["defined_rule_numbers"] == [1, 2, 4, 5, 6, 9]


def test_j4m07_terrain_formations_keep_formation_and_five_element_together():
    cases = {
        "后高前下": ("锐阵", "火"),
        "前高后下": ("直阵", "木"),
        "地洿邪": ("圆阵", "土"),
        "地高而平": ("方阵", "金"),
        "左右势高": ("曲阵", "水"),
    }
    for terrain, expected in cases.items():
        data = zhizhen_suidi(terrain)
        assert data["rule_id"] == "J4M-07"
        assert (data["宜阵"], data["五行"]) == expected
        assert data["direction_relation"] == {"顺其向": "吉", "反其向": "凶"}

    control = zhizhen_suidi(
        "后高前下",
        host_formation="直阵",
        guest_formation="方阵",
    )
    assert control["formation_contest"]["host_element"] == "木"
    assert control["formation_contest"]["guest_element"] == "金"
    assert control["formation_contest"]["winner"] == "客"
    assert control["formation_contest"]["loser"] == "主"

    reverse = zhizhen_suidi(
        "地高而平",
        host_formation="锐阵",
        guest_formation="方阵",
    )
    assert reverse["formation_contest"]["winner"] == "主"
    assert reverse["formation_contest"]["relation"] == "主阵五行克客阵五行"

    no_control = zhizhen_suidi(
        "左右势高",
        host_formation="直阵",
        guest_formation="锐阵",
    )
    assert no_control["formation_contest"]["winner"] is None
    assert no_control["formation_contest"]["relation"] == "本条无五行相克关系"

    unknown = zhizhen_suidi("未知地形")
    assert unknown["computable"] is False
    assert unknown["status"] == "not_computable"


def test_j4m09_jinjing_profile_does_not_import_tongzong_palace_one():
    inner = taiyi_tianwai_dinei(8, three_doors_ready=True, five_generals_released=True)
    assert inner["rule_id"] == "J4M-09"
    assert inner["source_profile"] == "jinjing_siku_volume4"
    assert inner["realm"] == "地内"
    assert inner["assists"] == "主"
    assert inner["decisive_ready"] is True

    outer = taiyi_tianwai_dinei(9, three_doors_ready=True, five_generals_released=True)
    assert outer["realm"] == "天外"
    assert outer["assists"] == "客"

    palace_one = taiyi_tianwai_dinei(1)
    assert palace_one["computable"] is False
    assert palace_one["realm"] is None
    assert palace_one["assists"] is None
    assert palace_one["canonical_groups"]["地内助主"] == [8, 3, 4]


def test_j4m09_does_not_declare_decisive_readiness_without_doors_and_generals():
    missing = taiyi_tianwai_dinei(3)
    assert missing["decisive_ready"] is None

    blocked = taiyi_tianwai_dinei(3, three_doors_ready=True, five_generals_released=False)
    assert blocked["decisive_ready"] is False


def test_j4m03_host_guest_control_follows_two_eye_five_element_examples():
    guest_wins = zhuke_xiangguan("木", "金")
    assert guest_wins["rule_id"] == "J4M-03"
    assert guest_wins["relation"] == "客关得主人"
    assert guest_wins["winner"] == "客"
    assert guest_wins["fully_computable"] is True
    assert guest_wins["calculation_scope"] == "日计"

    host_wins = zhuke_xiangguan("土", "水")
    assert host_wins["relation"] == "主人关得客"
    assert host_wins["winner"] == "主"
    assert host_wins["fully_computable"] is True

    no_control = zhuke_xiangguan("木", "水")
    assert no_control["relation"] is None
    assert no_control["winner"] is None
    assert no_control["status"] == "ok"
    assert no_control["canonical_outcome"] == "本条无相制关关系"


def test_j4m03_can_resolve_elements_from_ancient_sixteen_god_table():
    assert j4m03_eye_element_from_god("高丛") == "木"
    assert j4m03_eye_element_from_god("太簇") == "金"
    assert j4m03_eye_element_from_god("阳德") == "土"
    assert j4m03_eye_element_from_god("地主") == "水"

    source_example = zhuke_xiangguan(
        host_eye_god="高丛",
        guest_eye_god="太簇",
    )
    assert source_example["host_eye_element"] == "木"
    assert source_example["guest_eye_element"] == "金"
    assert source_example["relation"] == "客关得主人"
    assert source_example["winner"] == "客"

    second_example = zhuke_xiangguan(
        host_eye_god="地主",
        guest_eye_god="阴主",
    )
    assert second_example["host_eye_element"] == "水"
    assert second_example["guest_eye_element"] == "土"
    assert second_example["relation"] == "客关得主人"
    assert second_example["winner"] == "客"


def test_j4m03_legacy_day_nayin_input_is_quarantined_not_used():
    data = zhuke_xiangguan("木", "金", day_nayin_element="火")
    assert data["winner"] == "客"
    assert data["legacy_day_nayin"]["value"] == "火"
    assert data["legacy_day_nayin"]["status"] == "legacy_input_ignored"
    assert data["fully_computable"] is True


def test_j4m03_taojinge_same_or_generating_relation_is_collation_hint_only():
    same = zhuke_xiangguan("木", "木")
    assert same["winner"] is None
    assert same["collation_hint"]["verdict"] == "二阵平"
    assert same["collation_hint"]["canonical_override"] is False

    generating = zhuke_xiangguan("金", "土")
    assert generating["winner"] is None
    assert generating["collation_hint"]["verdict"] == "相生则和解"
    assert generating["collation_hint"]["canonical_override"] is False


def test_j4m03_requires_day_count_scope_and_disambiguates_eye_names():
    wrong_scope = zhuke_xiangguan("木", "金", calculation_scope="时计")
    assert wrong_scope["computable"] is False
    assert wrong_scope["required_scope"] == "日计"

    data = zhuke_xiangguan("木", "金")
    assert "文昌" in data["eye_role_convention"]["主"]
    assert "始击" in data["eye_role_convention"]["客"]
    assert "多义" in data["eye_role_convention"]["warning"]


def test_j4m05_campaign_requires_calc_doors_generals_and_lucky_gate():
    ready = chushi_fa(
        12,
        three_doors_ready=True,
        five_generals_released=True,
        exit_gate="开",
    )
    assert ready["rule_id"] == "J4M-05"
    assert ready["deployment_ready"] is True
    assert ready["status"] == "ready"

    pending_gate = chushi_fa(
        22,
        three_doors_ready=True,
        five_generals_released=True,
    )
    assert pending_gate["source_prerequisites_ready"] is True
    assert pending_gate["deployment_ready"] is None
    assert pending_gate["status"] == "ready_pending_gate"

    bad_calc = chushi_fa(
        13,
        three_doors_ready=True,
        five_generals_released=True,
        exit_gate="生",
    )
    assert bad_calc["deployment_ready"] is False
    assert bad_calc["calc_ready"] is False

    bad_gate = chushi_fa(
        32,
        three_doors_ready=True,
        five_generals_released=True,
        exit_gate="杜",
    )
    assert bad_gate["deployment_ready"] is False
    assert bad_gate["exit_gate_valid"] is False


def test_j4m10_qifu_keeps_each_source_condition_separate():
    hundred = qifu_fa(
        army_size=100,
        calc_value=12,
        tianmu_location="高丛",
        yanpo=True,
        terrain="山林",
    )
    assert hundred["rule_id"] == "J4M-10"
    assert hundred["odd_force_count"] == 30
    assert hundred["ambush_time"] is True
    assert hundred["concealment_time"] is False
    assert hundred["great_kill_location"] == "高丛"
    assert hundred["yanpo_status"] == "favorable_required_timing_present"

    hidden = qifu_fa(calc_value=21, enemy_urgent=True)
    assert hidden["ambush_time"] is False
    assert hidden["concealment_time"] is True
    assert "藏于山林沟涧" in hidden["recommendations"]
    assert "伏于要害" in hidden["recommendations"]

    odd_size = qifu_fa(army_size=101)
    assert odd_size["odd_force_count"] is None
    assert odd_size["odd_force_count_status"] == "ratio_known_rounding_unspecified"


def test_low_dependency_catalog_is_explicitly_partial():
    catalog = j4m_low_dependency_catalog()
    assert catalog["implemented"] == ["J4M-01", "J4M-02", "J4M-03", "J4M-04", "J4M-05", "J4M-06", "J4M-07", "J4M-08", "J4M-09", "J4M-10", "J4M-11", "J4M-12"]
    assert catalog["partial"] == []
    assert catalog["pending"] == []


def test_j4m01_direct_gate_cycle_is_240_with_30_per_gate():
    assert zhimen_from_cycle_count(1)["direct_gate"] == "开"
    assert zhimen_from_cycle_count(30)["direct_gate"] == "开"
    assert zhimen_from_cycle_count(31)["direct_gate"] == "休"
    assert zhimen_from_cycle_count(61)["direct_gate"] == "生"
    assert zhimen_from_cycle_count(240)["direct_gate"] == "惊"
    assert zhimen_from_cycle_count(241)["direct_gate"] == "开"

    bad = zhimen_from_cycle_count(0)
    assert bad["computable"] is False


def test_j4m01_three_doors_only_claims_source_explicit_cases():
    two_blocked = sanmen_jubu(taiyi_gate="开", tianmu_gate="生", direct_gate="景")
    assert two_blocked["rule_id"] == "J4M-01"
    assert two_blocked["not_ready_count"] == 2
    assert two_blocked["three_doors_ready"] is False
    assert two_blocked["direct_gate_auspice"] == "小吉"

    three_blocked = sanmen_jubu(taiyi_gate="休", tianmu_gate="开", direct_gate="死")
    assert three_blocked["not_ready_count"] == 3
    assert three_blocked["three_doors_ready"] is False
    assert three_blocked["direct_gate_auspice"] == "大凶"

    unstated = sanmen_jubu(taiyi_gate="开", tianmu_gate="开")
    assert unstated["status"] == "not_defined_by_source_passage"
    assert unstated["three_doors_ready"] is None

    missing = sanmen_jubu(taiyi_gate="开")
    assert missing["status"] == "not_computable"
    assert missing["three_doors_ready"] is None


def test_j4m02_five_generals_keeps_three_blockers_separate_from_doors():
    clear = wujiang_fabu(
        shiji_yanji=False,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        three_doors_ready=True,
    )
    assert clear["rule_id"] == "J4M-02"
    assert clear["five_generals_released"] is True
    assert clear["combined_ready"] is True
    assert clear["engagement_allowed_by_generals"] is True

    blocked = wujiang_fabu(
        shiji_yanji=True,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        three_doors_ready=True,
    )
    assert blocked["five_generals_released"] is False
    assert blocked["blockers"] == ["始击有掩击"]
    assert blocked["combined_ready"] is False

    doors_blocked = wujiang_fabu(
        shiji_yanji=False,
        wenchang_qiupo=False,
        major_minor_generals_related=False,
        three_doors_ready=False,
    )
    assert doors_blocked["five_generals_released"] is True
    assert doors_blocked["deployment_allowed_by_doors"] is False
    assert doors_blocked["combined_ready"] is False

    incomplete = wujiang_fabu(shiji_yanji=False)
    assert incomplete["computable"] is False
    assert incomplete["five_generals_released"] is None


def test_j4m08_terrain_arm_mapping_preserves_source_ratio_text():
    infantry = suidi_zhibian("沟堑山林川泽丘阜草木")
    assert infantry["rule_id"] == "J4M-08"
    assert infantry["favored"] == "步兵"
    assert infantry["disfavored"] == "车骑"
    assert infantry["source_ratio_text"] == "车骑三不当一步兵"

    cavalry = suidi_zhibian("平陵平原广野")
    assert cavalry["favored"] == "车骑"
    assert cavalry["source_ratio_text"] == "步兵十不当一车骑"

    missile = suidi_zhibian("平阳相远山谷幽涧仰高临下")
    assert missile["favored"] == "弓弩"
    assert missile["source_ratio_text"] == "短兵百不当一弓弩"

    reeds = suidi_zhibian("萑苇竹萧蒙笼草木")
    assert reeds["favored"] == "矛鋋"
    assert reeds["source_ratio_text"] == "弓弩三不当一矛鋋"
    assert reeds["quotation_collation"]["do_not_silent_emend"] is True
    assert "汉书" in reeds["quotation_collation"]["external_witness"]

    unknown = suidi_zhibian("未知地形")
    assert unknown["computable"] is False
    assert unknown["favored"] is None


def test_j4m08_training_and_command_warnings_do_not_become_fake_combat_scores():
    data = suidi_zhibian(
        "两阵相近平地浅草",
        soldiers_trained=False,
        equipment_serviceable=False,
        general_knows_warfare=False,
        ruler_selects_generals=False,
    )
    assert data["favored"] == "长戟"
    assert len(data["warnings"]) == 4
    assert "士卒服习" in data["urgent_requirements"]
    assert data["doctrine_chain"][-1] == "君不择将，以其国与敌"


def test_j4m11_requires_external_observation_and_maps_explicit_cases():
    missing = fengyun_feiniao_zhuzhan([])
    assert missing["computable"] is False
    assert missing["status"] == "not_computable"

    data = fengyun_feiniao_zhuzhan([
        {
            "phenomenon": "风云飞鸟",
            "source_anchor": "太乙所在宫",
            "action": "冲格迫击",
            "target": "太乙",
        },
        {
            "phenomenon": "飞鸟",
            "source_anchor": "主目",
            "action": "去击",
            "target": "客",
        },
        {
            "phenomenon": "云",
            "action": "扶",
            "target": "客阵",
        },
    ])
    assert data["rule_id"] == "J4M-11"
    assert data["computable"] is True
    assert data["judgments"][0]["omen"] == "大败之兆"
    assert data["judgments"][1]["loser"] == "客"
    assert data["judgments"][2]["winner"] == "客"


def test_j4m11_requires_explicit_phenomenon_for_every_observation():
    missing = fengyun_feiniao_zhuzhan([
        {"action": "扶", "target": "主人阵"}
    ])
    assert missing["computable"] is False
    assert missing["status"] == "not_defined_by_source_passage"
    assert missing["judgments"][0]["matched"] is False
    assert missing["judgments"][0]["source_case"] == "缺失或未知观测类型"


def test_j4m11_does_not_expand_po_ji_into_chong_ji_synonym():
    unsupported = fengyun_feiniao_zhuzhan([
        {
            "phenomenon": "风",
            "action": "冲击",
            "target": "大将宫",
        }
    ])
    assert unsupported["computable"] is False
    assert unsupported["judgments"][0]["matched"] is False
    assert unsupported["judgments"][0]["source_case"] == "正文未覆盖该观测组合"

    supported = fengyun_feiniao_zhuzhan([
        {
            "phenomenon": "风",
            "action": "迫击",
            "target": "大将宫",
        }
    ])
    assert supported["computable"] is True
    assert supported["judgments"][0]["matched"] is True
    assert supported["judgments"][0]["loser"] == "主"
    assert supported["judgments"][0]["source_case"] == "迫击大将宫"


def test_j4m11_keeps_unstated_noise_outcome_unscored():
    data = fengyun_feiniao_zhuzhan([
        {"phenomenon": "飞鸟", "action": "噪阵", "crowd_noisy": True}
    ])
    assert data["computable"] is False
    assert data["status"] == "not_defined_by_source_passage"
    assert data["judgments"][0]["matched"] is False
    assert "未单独明示" in data["judgments"][0]["note"]


def test_j4m11_handles_flag_break_and_formation_collision():
    data = fengyun_feiniao_zhuzhan([
        {
            "phenomenon": "风云飞鸟",
            "returning_wind": True,
            "birds_circling": True,
            "flag_broken": True,
        },
        {
            "phenomenon": "风云",
            "action": "冲突",
            "target": "主人阵",
        },
    ])
    assert data["judgments"][0]["omen"] == "大败之兆"
    assert data["judgments"][1]["loser"] == "主"


def test_j4m12_cloud_color_table_and_day_stem_modifiers():
    north = yunqi_dingshengfu(
        formation_direction="北",
        cloud_color="黑",
        observed_formation="敌",
        day_stem="壬",
    )
    assert north["rule_id"] == "J4M-12"
    assert north["base_verdict"] == "大胜"
    assert north["qi_class"] == "胜气"
    assert north["day_modifier"] == "弥佳"
    assert north["verdict_subject"] == "敌"
    assert "敌阵" in north["perspective_note"]

    south_bad = yunqi_dingshengfu(
        formation_direction="南",
        cloud_color="黑",
        day_stem="丙",
    )
    assert south_bad["base_verdict"] == "大败"
    assert south_bad["day_modifier"] == "弥恶"

    east_delay = yunqi_dingshengfu(
        formation_direction="东",
        cloud_color="赤",
    )
    assert east_delay["base_verdict"] == "将迟钝，然不可击"


def test_j4m12_explicit_guest_role_is_not_rewritten_by_cloud_bearer():
    enemy = yunqi_dingshengfu(
        formation_direction="北",
        cloud_color="红",
        observed_formation="敌",
    )
    ours = yunqi_dingshengfu(
        formation_direction="北",
        cloud_color="红",
        observed_formation="我",
    )
    assert enemy["base_verdict"] == "客胜"
    assert ours["base_verdict"] == "客胜"
    assert enemy["verdict_subject"] == "客"
    assert ours["verdict_subject"] == "客"
    assert ours["cloud_bearer"] == "我"
    assert ours["subject_mode"] == "guest_role"


def test_j4m12_west_white_does_not_invent_big_victory_from_table_symmetry():
    data = yunqi_dingshengfu(
        formation_direction="西",
        cloud_color="白",
        observed_formation="敌",
        day_stem="庚",
    )
    assert data["base_verdict"] is None
    assert data["effective_verdict"] is None
    assert data["qi_class"] == "基础胜负未明"
    assert data["day_modifier"] == "弥佳"
    assert "未明写基础胜负" in data["source_note"]


def test_j4m12_unknown_color_is_not_filled_by_five_elements():
    east_white = yunqi_dingshengfu(
        formation_direction="东",
        cloud_color="白",
    )
    assert east_white["computable"] is False
    assert east_white["status"] == "not_defined_by_source_passage"
    assert "白" not in east_white["defined_colors"]


def test_j4m12_morphology_modifies_only_source_explicit_cases():
    broken_victory = yunqi_dingshengfu(
        formation_direction="北",
        cloud_color="黑",
        continuity="断续",
    )
    assert broken_victory["base_verdict"] == "大胜"
    assert broken_victory["effective_verdict"] == "败"
    assert any("反败" in x for x in broken_victory["morphology_modifiers"])

    weakened_defeat = yunqi_dingshengfu(
        formation_direction="西",
        cloud_color="赤",
        disorder="溃乱",
        over_general="大将",
    )
    assert weakened_defeat["qi_class"] == "败气"
    assert any("不至全恶" in x for x in weakened_defeat["morphology_modifiers"])
    assert "原文曰反此" in weakened_defeat["general_modifier"]


def test_j4m12_no_cloud_returns_no_war_or_balance_note():
    data = yunqi_dingshengfu(cloud_present=False)
    assert data["status"] == "no_cloud"
    assert data["computable"] is True
    assert data["verdict"] is None
    assert "无战或复相匀" in data["source_note"]


def test_j4m04_host_guest_roles_and_favorable_triad_are_separate():
    data = zhuke_fa(
        "陈兵原野",
        three_doors_ready=True,
        five_generals_released=True,
        yin_yang_harmonious=True,
        direction="东",
        host_calc=17,
        guest_calc=13,
    )
    assert data["rule_id"] == "J4M-04"
    assert data["roles"] == {"first_mover": "客", "responder": "主"}
    assert data["action_status"] == "raise_forces_favorable"
    assert data["action_advice"] == "称兵"
    assert data["source_campaign_verdict"] == "所向必克"
    assert data["source_temporal_outcome"] == "先起者胜，后起者负"
    assert data["winner"] == "客"
    assert data["loser"] == "主"
    assert "先起则胜" in data["winner_basis"]
    assert data["start_deity"] == "阴德"
    assert data["cross_side_calc_reference"]["客欲知主"]["target_calc"] == "主算"
    assert data["cross_side_calc_reference"]["客欲知主"]["value"] == 17
    assert data["cross_side_calc_reference"]["主人欲知客"]["target_calc"] == "客算"
    assert data["cross_side_calc_reference"]["主人欲知客"]["value"] == 13


def test_j4m04_settled_context_reverses_roles_and_all_bad_means_hold():
    data = zhuke_fa(
        "安居之势",
        three_doors_ready=False,
        five_generals_released=False,
        yin_yang_harmonious=False,
        direction="北",
    )
    assert data["roles"] == {"first_mover": "主", "responder": "客"}
    assert data["action_status"] == "hold_and_defend"
    assert data["action_advice"] == "不利举兵，宜固守吉"
    assert data["source_combination_status"] == "explicit_unfavorable_triad"
    assert data["start_deity"] == "大武"


def test_j4m04_mixed_conditions_are_not_silently_promoted_to_full_source_verdict():
    data = zhuke_fa(
        "陈兵原野",
        three_doors_ready=False,
        five_generals_released=True,
        yin_yang_harmonious=True,
    )
    assert data["action_status"] == "blocked_or_mixed"
    assert data["source_combination_status"] == "mixed_combination_not_fully_expanded_by_j4m04"
    assert data["source_campaign_verdict"] is None
    assert data["source_temporal_outcome"] is None
    assert data["winner"] is None
    assert data["blockers"] == ["三门不具：不可出兵"]


def test_j4m04_unknown_context_is_not_inferred():
    data = zhuke_fa(
        "城守",
        three_doors_ready=True,
        five_generals_released=True,
        yin_yang_harmonious=True,
    )
    assert data["computable"] is False
    assert data["status"] == "not_computable"


def test_j4m12_same_source_table_can_apply_to_our_formation_without_side_inversion():
    ours = yunqi_dingshengfu(
        formation_direction="北",
        cloud_color="黑",
        observed_formation="我",
        day_stem="壬",
    )
    assert ours["base_verdict"] == "大胜"
    assert ours["verdict_subject"] == "我"
    assert "我阵" in ours["perspective_note"]

    invalid = yunqi_dingshengfu(
        formation_direction="北",
        cloud_color="黑",
        observed_formation="未知",
    )
    assert invalid["computable"] is False
    assert invalid["status"] == "not_computable"
    assert invalid["valid_observed_formations"] == ["敌", "我"]


def test_j4m04_favorable_settled_context_makes_host_the_first_mover_winner():
    data = zhuke_fa(
        "安居之势",
        three_doors_ready=True,
        five_generals_released=True,
        yin_yang_harmonious=True,
    )
    assert data["roles"] == {"first_mover": "主", "responder": "客"}
    assert data["winner"] == "主"
    assert data["loser"] == "客"
    assert data["source_temporal_outcome"] == "先起者胜，后起者负"


def test_j4m04_unfavorable_triad_does_not_import_other_books_reverse_winner():
    data = zhuke_fa(
        "陈兵原野",
        three_doors_ready=False,
        five_generals_released=False,
        yin_yang_harmonious=False,
    )
    assert data["action_status"] == "hold_and_defend"
    assert data["winner"] is None
    assert data["loser"] is None
    assert "不自动回写" in data["temporal_outcome_policy"]
