import json
from pathlib import Path


RULESET_FILE = Path(__file__).parents[1] / "rules" / "jinjing_v4_military.json"


def _rules():
    data = json.loads(RULESET_FILE.read_text(encoding="utf-8"))
    return data, data["rules"]


def test_jinjing_v4_military_has_exact_twelve_body_heading_order():
    data, rules = _rules()
    assert data["ruleset_id"] == "jinjing-siku-v4-military-12"
    assert data["source"]["volume"] == 4
    assert len(rules) == 12
    assert [item["id"] for item in rules] == [f"J4M-{i:02d}" for i in range(1, 13)]
    assert [item["body_title"] for item in rules] == [
        "推三门具不具",
        "推五将发不发",
        "推主客相关法",
        "推主客",
        "推出师法",
        "推陈兵向背",
        "推制阵随地法",
        "推随地制变",
        "推太乙在天外地内法",
        "推奇伏法",
        "推太乙风云飞鸟助战法",
        "推阵有风云气定胜负",
    ]


def test_near_named_rules_remain_distinct():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-03"]["domain"] != by_id["J4M-04"]["domain"]
    assert by_id["J4M-03"]["target_crosswalk"]["layer"] is None
    assert by_id["J4M-04"]["target_crosswalk"]["layer"] == "C8-L3"

    assert by_id["J4M-07"]["body_title"] == "推制阵随地法"
    assert by_id["J4M-08"]["body_title"] == "推随地制变"
    assert by_id["J4M-07"]["domain"] != by_id["J4M-08"]["domain"]

    assert by_id["J4M-05"]["target_crosswalk"]["status"] == "missing_do_not_substitute_chushi_luedi"
    assert by_id["J4M-06"]["target_crosswalk"]["status"] == "missing_do_not_substitute_chenbing_chuxiang"


def test_toc_title_variants_are_aliases_not_extra_rules():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert "推主客相关" in by_id["J4M-03"]["toc_aliases"]
    assert "推障向背法" in by_id["J4M-06"]["toc_aliases"]
    assert "推置阵随地法" in by_id["J4M-07"]["toc_aliases"]
    assert "推随地置变" in by_id["J4M-08"]["toc_aliases"]
    assert "推奇兵伏兵法" in by_id["J4M-10"]["toc_aliases"]
    assert "推对阵有云气定胜负" in by_id["J4M-12"]["toc_aliases"]


def test_jinjing_and_tongzong_taiyi_inner_outer_profiles_are_not_silently_merged():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-09"]

    assert rule["canonical"]["inner_palaces_help_host"] == [8, 3, 4]
    assert rule["canonical"]["outer_palaces_help_guest"] == [9, 2, 7, 6]
    assert rule["canonical"]["palace_1"] == "not_listed_in_jinjing_siku_v4_text"

    tongzong = rule["source_variants"]["tongzong_volume5"]
    assert tongzong["inner_palaces_help_host"] == [1, 8, 3, 4]
    assert tongzong["status"] == "separate_source_variant"


def test_runtime_status_matches_second_batch_implementation():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-03"]["implementation_status"] == "implemented_source_specific"
    assert any(path.endswith(".zhuke_xiangguan") for path in by_id["J4M-03"]["runtime"])
    assert any(path.endswith(".j4m03_eye_element_from_god") for path in by_id["J4M-03"]["runtime"])
    assert by_id["J4M-03"]["target_crosswalk"]["layer"] is None

    assert by_id["J4M-05"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-05"]["runtime"].endswith(".chushi_fa")
    assert "兵额表" in by_id["J4M-05"]["implementation_note"]

    assert by_id["J4M-10"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-10"]["runtime"].endswith(".qifu_fa")
    assert by_id["J4M-10"]["target_crosswalk"]["layer"] is None


def test_runtime_status_matches_third_batch_implementation():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-01"]["implementation_status"] == "implemented_source_specific"
    assert any(path.endswith(".sanmen_jubu") for path in by_id["J4M-01"]["runtime"])
    assert any(path.endswith(".zhimen_from_cycle_count") for path in by_id["J4M-01"]["runtime"])

    assert by_id["J4M-02"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-02"]["runtime"].endswith(".wujiang_fabu")

    assert by_id["J4M-08"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-08"]["runtime"].endswith(".suidi_zhibian")
    assert by_id["J4M-08"]["domain"] != by_id["J4M-07"]["domain"]


def test_runtime_status_matches_observation_batch_implementation():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-11"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-11"]["runtime"].endswith(".fengyun_feiniao_zhuzhan")
    assert "显式声明 phenomenon" in by_id["J4M-11"]["implementation_note"]
    assert "不做近义词扩张" in by_id["J4M-11"]["implementation_note"]
    assert "C75" in by_id["J4M-11"]["implementation_note"]

    assert by_id["J4M-12"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-12"]["runtime"].endswith(".yunqi_dingshengfu")
    assert "不以五行常识补表" in by_id["J4M-12"]["implementation_note"]


def test_j4m04_is_now_source_complete_but_c8_crosswalk_remains_roles_only():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}
    rule = by_id["J4M-04"]

    assert rule["implementation_status"] == "implemented_source_specific"
    assert rule["runtime"].endswith(".zhuke_fa")
    assert rule["target_crosswalk"]["layer"] == "C8-L3"
    assert rule["target_crosswalk"]["status"] == "source_runtime_complete_c8_roles_only"
    assert "先胜后负" in rule["implementation_note"]


def test_j4m03_ancient_collation_resolves_two_eye_nayin_without_modern_merge():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-03"]

    assert rule["implementation_status"] == "implemented_source_specific"
    assert rule["collation_status"] == "resolved_by_two_eye_nayin_collation"
    assert rule["canonical"]["scope"] == "日计"
    assert "文昌" in rule["canonical"]["host_eye"]
    assert "始击" in rule["canonical"]["guest_eye"]
    assert "日计二目纳音" in rule["collation_evidence"]["jingyou_taiyi_fuyingjing"]
    assert "二目纳音" in rule["collation_evidence"]["taiyi_taojinge"]

    quarantined = " ".join(rule["legacy_reference_quarantined"])
    assert "wc_n_sj" in quarantined
    assert "主将是否与太乙同宫" in quarantined
    assert "现代《太乙数纳音体系（修正版）》" in quarantined
    assert "不得静默回写" in quarantined


def test_all_twelve_rules_are_complete_and_have_runtime_entries():
    _, rules = _rules()
    assert len(rules) == 12
    for item in rules:
        assert item["implementation_status"] == "implemented_source_specific"
        runtime = item["runtime"]
        if isinstance(runtime, list):
            assert runtime
            assert all(path.startswith("kintaiyi.jinjing_v4_military.") for path in runtime)
        else:
            assert runtime.startswith("kintaiyi.jinjing_v4_military.")


def test_j4m_source_records_scan_witnesses_and_body_order_priority():
    data, rules = _rules()
    witnesses = {item["id"]: item for item in data["source"]["scan_witnesses"]}
    assert witnesses["CADAL06056494"]["status"] == "scan_page_locators_verified_for_j4m_01_12"
    assert witnesses["NCL-06604"]["status"] == (
        "volume4_scan_range_and_j4m_page_locators_verified_readings_in_progress"
    )
    assert "National Central Library" in witnesses["NCL-06604"]["metadata_verified"]
    assert "C86" in witnesses["NCL-06604"]["locator_policy"]
    assert "不覆盖 jinjing_siku_volume4 canonical" in witnesses["NCL-06604"]["locator_policy"]

    order = data["source"]["order_collation"]
    assert "风云飞鸟助战法" in order["siku_toc"]
    assert "先“推奇伏法”" in order["siku_body"]
    assert "J4M-10=推奇伏法" in order["canonical_policy"]

    variants = data["source"]["volume_numbering_variants"]
    assert any(item["label"] == "卷三" and item["canonical_override"] is False for item in variants)


def test_j4m08_chao_cuo_quote_variant_is_quarantined_not_silently_emended():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-08"]
    assert rule["collation_status"] == "jinjing_quote_diverges_from_jingyou_and_hanshu"
    assert any(
        "车骑三不当一" in item
        for item in rule["quotation_collation"]["jinjing_siku_volume4"]["examples"]
    )
    assert any(
        "车骑二不当一" in item
        for item in rule["quotation_collation"]["hanshu_yuanang_chaocuo_zhuan"]["examples"]
    )
    assert "不得静默改写 runtime" in rule["quotation_collation"]["policy"]


def test_j4m04_first_mover_victory_is_resolved_by_ancient_parallel_texts():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-04"]
    assert rule["collation_status"] == "resolved_first_mover_wins_in_favorable_triad"
    assert "先胜后负" in rule["collation_evidence"]["jinjing_siku_volume4"]
    assert "先起则胜" in rule["collation_evidence"]["wujing_zongyao_siku_houji_18"]
    assert "先起则胜" in rule["collation_evidence"]["taiyi_mishu"]
    assert "不自动回写" in rule["collation_evidence"]["policy"]


def test_j4m05_two_conditions_are_disambiguated_without_importing_tongzong_expansions():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-05"]
    assert rule["collation_status"] == "two_conditions_resolved_by_jingyou_parallel_and_tongzong_gloss"
    assert "出其门" in rule["collation_evidence"]["tongzong_volume5"]
    assert "用其二" in rule["collation_evidence"]["tongzong_volume5"]
    assert "兵额" in rule["collation_evidence"]["do_not_import"]


def test_j4m06_jinjing_and_tongzong_chenbing_rules_do_not_fill_each_other():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-06"]
    evidence = rule["source_boundary_evidence"]
    assert "1/2/4/5/6/9" in evidence["jinjing_siku_volume4"]
    assert "1/2/3/4/6/7/8/9" in evidence["tongzong_later_military_rule"]
    assert "不得互补缺数" in evidence["policy"]


def test_j4m07_record_includes_explicit_formation_control_layer():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-07"]
    assert "五行相克" in rule["canonical_summary"]
    assert "主阵五行克客阵则主胜" in rule["implementation_note"]
    assert "C66" in rule["completion_note"]


def test_jingyou_volume4_variants_stay_separate_from_jinjing_canonical():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    j6 = by_id["J4M-06"]["source_variants"]["jingyou_fuying_volume4"]
    assert j6["extra_vs_jinjing"] == [3, 7, 8]
    assert j6["omitted_in_variant"] == [5]
    assert j6["status"] == "separate_ancient_source_variant"

    j7 = by_id["J4M-07"]["source_variants"]["jingyou_fuying_volume4"]
    assert j7["canonical_override"] is False
    assert j7["locator_status"] == "transcription_variant_pending_scan_check"

    j9 = by_id["J4M-09"]["source_variants"]["jingyou_fuying_volume4"]
    assert j9["inner_palaces_help_host"] == [1, 8, 3, 4]
    assert by_id["J4M-09"]["canonical"]["inner_palaces_help_host"] == [8, 3, 4]


def test_j4m10_dasha_bad_character_is_not_turned_into_a_formula():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-10"]
    assert "伏兵必败大煞之地" in rule["textual_variants"]["jinjing_siku_volume4"]
    assert "奇兵必从大杀之地" in rule["textual_variants"]["jingyou_fuying_volume4"]
    assert "不把《金镜》“败”单字解释成额外动作或胜负" in rule["textual_variants"]["policy"]


def test_j4m11_conflicting_jingyou_event_readings_are_not_merged():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-11"]
    variant = rule["source_variants"]["jingyou_fuying_volume4"]
    joined = " ".join(variant["distinct_readings"])
    assert "迫击客大将宫" in joined
    assert "从主人刑上来 -> 主人败" in joined
    assert "《金镜》“从主人形上来客败”" in joined
    assert variant["canonical_override"] is False


def test_j4m12_record_forbids_symmetry_completion_and_separates_subject():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-12"]
    assert rule["collation_status"] == "source_table_audited_no_symmetry_completion"
    constraints = rule["canonical_constraints"]
    assert "基础胜负未明" in constraints["west_white"]
    assert "禁止补“大胜”" in constraints["west_white"]
    assert "subject=客" in constraints["north_red"]
    assert "云气所在阵与断语主体必须分栏" in constraints["cloud_bearer_vs_verdict_subject"]


def test_j4m11_record_requires_explicit_observation_type_and_exact_action_wording():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-11"]
    assert rule["collation_status"] == "source_event_schema_audited_strict_wording"
    constraints = rule["canonical_constraints"]
    assert "必须显式" in constraints["explicit_phenomenon_required"]
    assert "迫击大将宫" in constraints["no_synonym_expansion"]
    assert "冲击大将宫" in constraints["no_synonym_expansion"]
    assert "不生成独立胜负" in constraints["noise_event"]
    assert "JF4M" in constraints["jingyou_conflict"]


def test_c79_cadal_scan_page_locators_cover_all_twelve_rules():
    data, rules = _rules()
    assert data["source"]["scan_locator_version"] == "c79-j4m-cadal-page-locators-v1"
    expected = {
        "J4M-01": [128, 129],
        "J4M-02": [129, 130],
        "J4M-03": [130, 131],
        "J4M-04": [131, 132],
        "J4M-05": [132],
        "J4M-06": [132, 133, 134],
        "J4M-07": [134, 135],
        "J4M-08": [135, 136, 137],
        "J4M-09": [137, 138],
        "J4M-10": [138, 139],
        "J4M-11": [139, 140],
        "J4M-12": [140, 141, 142, 143],
    }
    for item in rules:
        locator = item["scan_locator"]
        assert locator["witness"] == "CADAL06056494"
        assert locator["status"] == "visual_scan_verified"
        assert locator["digital_scan_pages"] == expected[item["id"]]


def test_c79_j4m08_scan_corrects_maochui_to_maochan():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-08"]
    correction = rule["textual_correction"]
    assert correction["previous_reading"] == "矛锤"
    assert correction["corrected_reading"] == "矛鋋"
    assert correction["status"] == "corrected_scan_verified"
    assert "p.136" in correction["evidence"]
    joined = " ".join(rule["quotation_collation"]["jinjing_siku_volume4"]["examples"])
    assert "矛鋋之地，弓弩三不当一" in joined
    assert "矛锤" not in joined


def test_c80_j4m05_to_j4m10_scan_audit_locks_no_inference_boundaries():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-05"]["scan_rule_audit"]["status"] == "scan_structure_confirmed_no_expansion"
    assert "不得扩成所有尾数2" in by_id["J4M-05"]["scan_rule_audit"]["forbidden_inference"]

    assert by_id["J4M-06"]["scan_rule_audit"]["status"] == "scan_table_confirmed_no_completion"
    assert "不得对任意算数取个位" in by_id["J4M-06"]["scan_rule_audit"]["forbidden_inference"]

    assert by_id["J4M-07"]["scan_rule_audit"]["status"] == "scan_structure_confirmed"
    assert "同类或相生不补胜负" in by_id["J4M-07"]["scan_rule_audit"]["forbidden_inference"]

    assert by_id["J4M-08"]["scan_rule_audit"]["status"] == "scan_text_confirmed_after_C79_correction"
    assert "p.136矛鋋" in by_id["J4M-08"]["scan_rule_audit"]["locked_points"]

    assert by_id["J4M-09"]["scan_rule_audit"]["status"] == "scan_groups_confirmed_no_palace1_completion"
    assert any("未列1宫" in x for x in by_id["J4M-09"]["scan_rule_audit"]["forbidden_inference"])

    assert by_id["J4M-10"]["scan_rule_audit"]["status"] == "scan_nodes_confirmed_textual_uncertainty_preserved"
    assert any("不解释《金镜》‘败’字" in x for x in by_id["J4M-10"]["scan_rule_audit"]["forbidden_inference"])


def test_c83_j4m01_to_j4m04_scan_audit_and_taicu_alias_boundaries():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    j1 = by_id["J4M-01"]["scan_rule_audit"]
    assert j1["status"] == "scan_structure_confirmed_conservative_cases"
    assert any("同落开" in x for x in j1["forbidden_inference"])

    j2 = by_id["J4M-02"]["scan_rule_audit"]
    assert j2["status"] == "scan_blockers_confirmed_layers_separated"
    assert any("三门具不等于" in x for x in j2["forbidden_inference"])

    j3 = by_id["J4M-03"]
    assert j3["scan_rule_audit"]["status"] == "scan_examples_confirmed_ancient_collation_preserved"
    assert j3["terminology_aliases"]["太蔟"]["canonical"] == "太簇"
    assert "五行仍为金" in j3["terminology_aliases"]["太蔟"]["behavior"]

    j4 = by_id["J4M-04"]["scan_rule_audit"]
    assert j4["status"] == "scan_roles_confirmed_parallel_gloss_limited"
    assert any("混合条件不扩写" in x for x in j4["forbidden_inference"])


def test_c84_access_boundary_is_preserved_but_c86_supersedes_page_pending():
    data, _ = _rules()
    witnesses = {item["id"]: item for item in data["source"]["scan_witnesses"]}
    ncl = witnesses["NCL-06604"]

    assert data["source"]["witness_audit_version"] == "c84-ncl06604-access-boundary-v1"
    assert data["source"]["ncl_volume4_collation_version"] == (
        "c86-ncl06604-v4-j4m-locators-v1"
    )
    assert ncl["status"] == (
        "volume4_scan_range_and_j4m_page_locators_verified_readings_in_progress"
    )
    assert ncl["evidence_level"] == (
        "page_collated_for_volume4_j4m_locators_with_selected_readings"
    )
    assert ncl["public_scan"]["pages"] == 124
    assert ncl["public_scan"]["edition"] == "明鈔本"
    assert ncl["access_audit"]["canonical_effect"] == "none"
    assert ncl["access_audit"]["status"] == (
        "superseded_for_volume4_page_access_by_C86"
    )
    assert "C86" in ncl["access_audit"]["superseded_note"]
    assert "页级 locator 已由 C86 直接图像核验" in ncl["locator_policy"]
    assert "不覆盖 jinjing_siku_volume4 canonical" in ncl["locator_policy"]


def test_c85_j4m11_j4m12_complete_the_twelve_rule_scan_audit():
    data, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert data["source"]["full_twelve_scan_audit_version"] == "c85-j4m01-12-scan-boundary-complete-v1"
    assert all(item.get("scan_rule_audit") for item in rules)

    j11 = by_id["J4M-11"]["scan_rule_audit"]
    assert j11["cycle"] == "C85"
    assert j11["status"] == "scan_observation_schema_confirmed_no_event_inference"
    assert any("不得由盘内字段" in x for x in j11["forbidden_inference"])
    assert any("众来噪阵" in x for x in j11["forbidden_inference"])

    j12 = by_id["J4M-12"]["scan_rule_audit"]
    assert j12["cycle"] == "C85"
    assert j12["status"] == "scan_cloud_table_confirmed_no_symmetry_or_subject_inversion"
    assert any("西方白云" in x for x in j12["locked_points"])
    assert any("五行常识" in x for x in j12["forbidden_inference"])
    assert any("cloud_bearer" in x for x in j12["forbidden_inference"])


def test_c86_ncl06604_volume4_page_range_and_j4m_locators_are_verified():
    data, rules = _rules()
    witnesses = {item["id"]: item for item in data["source"]["scan_witnesses"]}
    ncl = witnesses["NCL-06604"]

    assert data["source"]["ncl_volume4_collation_version"] == "c86-ncl06604-v4-j4m-locators-and-key-readings-v2"
    assert ncl["status"] == "volume4_scan_range_and_j4m_page_locators_verified_readings_in_progress"
    assert ncl["volume_boundaries"]["volume3_end"]["digital_scan_page"] == 54
    assert ncl["volume_boundaries"]["volume4_start"]["digital_scan_page"] == 55
    assert ncl["volume_boundaries"]["volume4_end"]["digital_scan_page"] == 64

    expected = {
        "J4M-01": [55, 56],
        "J4M-02": [56],
        "J4M-03": [56, 57],
        "J4M-04": [57, 58],
        "J4M-05": [58],
        "J4M-06": [59, 60],
        "J4M-07": [60],
        "J4M-08": [60, 61],
        "J4M-09": [61, 62],
        "J4M-10": [62],
        "J4M-11": [62, 63],
        "J4M-12": [63, 64],
    }
    for item in rules:
        locator = item["ncl_scan_locator"]
        assert locator["witness"] == "NCL-06604"
        assert locator["status"] == "visual_scan_verified"
        assert locator["digital_scan_pages"] == expected[item["id"]]
        assert locator["canonical_effect"] == "none"


def test_c86_ncl06604_selected_manuscript_readings_stay_noncanonical():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-06"]["manuscript_readings"]["NCL-06604"]["body_title"] == "推陈兵向背"
    assert by_id["J4M-07"]["manuscript_readings"]["NCL-06604"]["body_title"] == "推制阵随地法"

    j8 = by_id["J4M-08"]["manuscript_readings"]["NCL-06604"]
    assert j8["body_title"] == "推随地制变"
    assert j8["weapon_reading"] == "矛鋋"
    assert j8["ratio_reading"] == "弓弩三不当一"

    j9 = by_id["J4M-09"]["manuscript_readings"]["NCL-06604"]
    assert j9["inner_palaces_help_host"] == [1, 8, 3, 4]
    assert j9["outer_palaces_help_guest"] == [9, 2, 7, 6]
    assert j9["canonical_override"] is False
    assert by_id["J4M-09"]["canonical"]["inner_palaces_help_host"] == [8, 3, 4]

    j10 = by_id["J4M-10"]["manuscript_readings"]["NCL-06604"]
    assert j10["body_title"] == "推奇兵伏兵法"
    assert j10["canonical_override"] is False

    j11 = by_id["J4M-11"]["manuscript_readings"]["NCL-06604"]
    assert j11["body_title"] == "推太乙风云飞鸟助阵法"
    assert j11["opening_phrase"] == "经曰助战之法"
    assert j11["canonical_override"] is False

    j12 = by_id["J4M-12"]["manuscript_readings"]["NCL-06604"]
    assert j12["body_title"] == "推对阵有云气定胜负"
    assert j12["west_white"]["base_verdict"] == "大胜"
    assert j12["west_white"]["day_stems_good"] == ["庚", "辛"]
    assert j12["canonical_override"] is False
    assert "基础胜负未明" in by_id["J4M-12"]["canonical_constraints"]["west_white"]
