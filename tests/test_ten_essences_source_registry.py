import pytest

from kintaiyi.pan_v2_contract import SOURCE_VARIANT_KEYS
from kintaiyi.ten_essences_source_registry import (
    CLOUD_OMEN_BOUNDARY,
    FOCUS_FORMULA_SKELETONS,
    LEGACY_FORMULA_AUDIT,
    LEGACY_NAME_AUDIT,
    SOURCE_WITNESS,
    TARGET_POLICY,
    TEN_ESSENCES,
    canonical_ten_essence_name,
    ten_essence_record,
    ten_essences_registry,
)
from kintaiyi.unported_catalog import catalog_unported_field


def test_c52_canonical_ten_essence_order_and_names():
    assert [row["name"] for row in TEN_ESSENCES] == [
        "天皇",
        "帝符",
        "天时",
        "太尊",
        "飞鸟",
        "五行",
        "八风",
        "五风",
        "三风",
        "太乙数",
    ]
    assert [row["index"] for row in TEN_ESSENCES] == list(range(1, 11))


def test_c52_direct_small_cycles_are_locked():
    assert [row["small_cycle"] for row in TEN_ESSENCES] == [
        20, 20, 12, 4, 9, 5, 9, 9, 9, 72
    ]


def test_c52_volume_boundary_is_preserved_as_variant():
    assert SOURCE_WITNESS["witness_volumes"] == [18, 20]
    assert SOURCE_WITNESS["volume_status"] == "witness_volume_variant"
    assert {row["work"] for row in SOURCE_WITNESS["independent_collation"]} == {
        "武经总要",
        "太白兵备统宗宝鉴",
    }


def test_c52_canonical_list_contains_difu_not_legacy_difu_and_ends_taiyi_number():
    names = [row["name"] for row in TEN_ESSENCES]
    assert "帝符" in names
    assert "地符" not in names
    assert "太岁" not in names
    assert "太歲" not in names
    assert names[-1] == "太乙数"


def test_c52_legacy_difu_alias_requires_explicit_compatibility_mode():
    with pytest.raises(ValueError, match="canonical"):
        canonical_ten_essence_name("地符")

    assert canonical_ten_essence_name(
        "地符",
        allow_legacy_alias=True,
    ) == "帝符"

    assert LEGACY_NAME_AUDIT["地符"]["status"] == "legacy_noncanonical_alias"
    assert LEGACY_NAME_AUDIT["地符"]["canonical_name"] == "帝符"


@pytest.mark.parametrize("name", ["太岁", "太歲"])
def test_c52_taisui_is_not_a_ten_essence(name):
    with pytest.raises(ValueError, match="canonical"):
        canonical_ten_essence_name(name)
    assert LEGACY_NAME_AUDIT[name]["status"] == "not_a_ten_essence"


@pytest.mark.parametrize(
    "source,canonical",
    [
        ("天時", "天时"),
        ("飛鳥", "飞鸟"),
        ("八風", "八风"),
        ("五風", "五风"),
        ("三風", "三风"),
        ("太乙數", "太乙数"),
    ],
)
def test_c52_traditional_aliases_normalize_without_source_loss(source, canonical):
    assert canonical_ten_essence_name(source) == canonical
    record = ten_essence_record(source)
    assert record["name"] == canonical
    expected_ready = canonical in {
        "天皇", "帝符", "天时", "飞鸟", "五风", "太尊", "八风", "三风", "五行", "太乙数"
    }
    assert record["runtime_formula_ready"] is expected_ready


def test_c52_old_flybird_cycle_conflicts_with_direct_small_cycle():
    audit = LEGACY_FORMULA_AUDIT["config.flybird"]
    assert audit["essence"] == "飞鸟"
    assert audit["legacy_cycle"] == 8
    assert audit["direct_small_cycle"] == 9
    assert audit["cycle_matches"] is False
    assert audit["runtime_ready"] is False


def test_c52_old_fivewind_cycle_conflicts_with_direct_small_cycle():
    audit = LEGACY_FORMULA_AUDIT["config.fivewind"]
    assert audit["essence"] == "五风"
    assert audit["legacy_cycle"] == 29
    assert audit["direct_small_cycle"] == 9
    assert audit["cycle_matches"] is False
    assert audit["runtime_ready"] is False


@pytest.mark.parametrize(
    "func,cycle",
    [
        ("config.tian_wang", 20),
        ("config.kingfu", 20),
        ("config.tian_shi", 12),
        ("config.taijun", 4),
        ("config.wuxing", 5),
        ("config.eightwind", 9),
        ("config.threewind", 9),
    ],
)
def test_c52_matching_legacy_cycle_still_does_not_make_formula_ready(func, cycle):
    audit = LEGACY_FORMULA_AUDIT[func]
    assert audit["direct_small_cycle"] == cycle
    assert audit["cycle_matches"] is True
    assert audit["runtime_ready"] is False


def test_c52_old_ten_jing_function_map_has_name_set_error():
    audit = LEGACY_FORMULA_AUDIT["yunqi._TEN_JING_FN"]
    assert audit["cycle_matches"] is False
    assert audit["runtime_ready"] is False
    assert "帝符" in audit["reason"]
    assert "太乙数" in audit["reason"]


def test_c52_cloud_omens_remain_separate_source_unit():
    assert CLOUD_OMEN_BOUNDARY["status"] == "separate_source_unit"
    assert CLOUD_OMEN_BOUNDARY["runtime_in_c52"] is False
    assert "旺相休囚" in CLOUD_OMEN_BOUNDARY["reason"]


def test_c52_does_not_extend_pan_contract_or_cycles_root():
    assert TARGET_POLICY["suggested_future_target"] == "source_variants.ten_essences"
    assert TARGET_POLICY["pan_contract_extended_in_c52"] is False
    assert TARGET_POLICY["cycles_root_used"] is False
    assert "ten_essences" not in SOURCE_VARIANT_KEYS


def test_c52_registry_tracks_completed_position_runtime_without_becoming_formula_layer():
    data = ten_essences_registry()
    assert data["rule_id"] == "C52-TEN-ESSENCES-REGISTRY"
    assert data["position_runtime_ready"] is True
    assert data["all_position_runtime_ready"] is True
    assert data["implemented_position_runtimes"] == [
        "飞鸟", "五风", "太尊", "八风", "三风", "五行", "天皇", "帝符", "天时"
    ]
    assert data["pending_position_runtimes"] == []
    assert data["cloud_runtime_ready"] is False
    assert data["target_policy"]["legacy_top_level_promoted"] is False

    status = {row["name"]: row["formula_status"] for row in data["essences"]}
    for name in ("飞鸟", "五风", "太尊", "八风", "三风", "五行"):
        assert status[name] == "implemented_c53"
    assert status["天皇"] == "implemented_c55"
    assert status["帝符"] == "implemented_c55"
    assert status["天时"] == "implemented_c56"
    assert status["太乙数"] == "implemented_c54"


def test_c52_c53_reclassify_old_pan_fields_by_actual_runtime_status():
    difu = catalog_unported_field("帝符")
    assert difu["layer"] == "canonical"
    assert difu["source_scope"] == "tongzong_ten_essences_volume18_20_variant"
    assert difu["action"] == "use_c55_sixteen_god_runtime"
    assert difu["migrate_whole"] is False
    assert difu["source_confidence"] == "high"
    assert difu["target_hint"] == "source_variants.ten_essences.positions"

    for field in ("太尊", "飛鳥", "三風", "五風", "八風"):
        item = catalog_unported_field(field)
        assert item["layer"] == "canonical"
        assert item["source_scope"] == "tongzong_ten_essences_volume18_20_variant"
        assert item["action"] == "use_c53_position_runtime"
        assert item["migrate_whole"] is False
        assert item["source_confidence"] == "high"
        assert item["target_hint"] == "source_variants.ten_essences.positions"
        assert "旧flat值不直接搬运" in item["notes"]


def test_c52_registry_never_introduces_tianyou_taiyi():
    serialized = repr(ten_essences_registry())
    assert "天游太乙" not in serialized


def test_c52_focus_formula_skeletons_lock_direct_source_boundaries():
    tianhuang = FOCUS_FORMULA_SKELETONS["天皇"]
    assert tianhuang["big_cycle"] == 200
    assert tianhuang["small_cycle"] == 20
    assert tianhuang["route"]["start"] == "武德（申）"
    assert tianhuang["route"]["repeat_on_gods"] == ["阴德", "和德", "大炅", "大武"]
    assert tianhuang["route"]["repeat_on_positions"] == ["乾", "艮", "巽", "坤"]
    assert tianhuang["route"]["repeat_count"] == 4
    assert tianhuang["runtime_rule_id"] == "C55-TIANHUANG"

    difu = FOCUS_FORMULA_SKELETONS["帝符"]
    assert difu["big_cycle"] == 200
    assert difu["small_cycle"] == 20
    assert difu["route"]["start"] == "阴主（戌）"
    assert difu["route"]["repeat_on_gods"] == ["地主", "高丛", "大威", "太簇"]
    assert difu["route"]["repeat_on_positions"] == ["子", "卯", "午", "酉"]
    assert difu["route"]["repeat_count"] == 4
    assert difu["surplus_variant"]["witness_values"] == {
        "volume18": 17, "volume20_or_ocr_variant": 70
    }
    assert difu["surplus_variant"]["apply"] is False
    assert difu["runtime_rule_id"] == "C55-DIFU"

    taizun = FOCUS_FORMULA_SKELETONS["太尊"]
    assert taizun["big_cycle"] == 40
    assert taizun["small_cycle"] == 4
    assert taizun["route"]["tongzong_sequence"] == [8, 6, 2, 4]
    assert taizun["route"]["taibai_yin_path"] == [2, 4, 8, 6]
    assert taizun["runtime_formula_ready"] is True
    assert taizun["runtime_rule_id"] == "C53-TAIZUN"

    bird = FOCUS_FORMULA_SKELETONS["飞鸟"]
    assert bird["big_cycle"] == 90
    assert bird["small_cycle"] == 9
    assert bird["surplus_variant"]["value"] == 3
    assert bird["surplus_variant"]["apply"] is False
    assert bird["same_name_boundary"]["j4m11_external_bird_observation"] is False

    five = FOCUS_FORMULA_SKELETONS["五风"]
    assert five["route"]["tongzong_sequence"] == [1, 3, 5, 7, 9, 2, 4, 6, 8]
    assert five["route"]["jingyou_sequence"] == [1, 3, 5, 7, 9, 2, 4, 6, 8]
    assert five["route"]["jinjing_volume7_sequence"] == [1, 3, 5, 7, 9, 2, 4, 6, 8]
    assert five["route"]["wujing_zongyao_variant_sequence"] == [1, 3, 5, 9, 7, 2, 4, 6, 8]
    assert five["route"]["status"] == "implemented_c53_profile_selection"
    assert five["route"]["canonical_route_for_tongzong_profile"] == [
        1, 3, 5, 7, 9, 2, 4, 6, 8
    ]
    assert five["route"]["cross_source_canonical_selected"] is None

    eight = FOCUS_FORMULA_SKELETONS["八风"]
    assert eight["route"]["tongzong_yang_path"] == [2, 3, 4, 5, 6, 7, 8, 9, 1]
    assert eight["route"]["taibai_yin_path"] == [8, 7, 6, 5, 4, 3, 2, 1, 9]
    assert eight["runtime_formula_ready"] is True

    three = FOCUS_FORMULA_SKELETONS["三风"]
    assert three["route"]["tongzong_sequence"] == [3, 7, 2, 6, 1, 5, 9, 4, 8]
    assert three["route"]["taibai_yin_path"] == [7, 3, 8, 4, 9, 5, 1, 6, 2]
    assert "起五宫" in three["route"]["wujing_zongyao_variant_text"]
    assert three["runtime_formula_ready"] is True
    assert three["runtime_rule_id"] == "C53-THREEWIND"


def test_c52_formula_skeleton_marks_all_position_runtimes_ready_after_c56():
    data = ten_essences_registry()
    assert data["position_runtime_ready"] is True
    assert data["all_position_runtime_ready"] is True

    for name, skeleton in data["focus_formula_skeletons"].items():
        assert skeleton["runtime_formula_ready"] is (
            name in {
                "天皇", "帝符", "天时", "飞鸟", "五风", "太尊", "八风", "三风", "五行", "太乙数"
            }
        ), name

    five = ten_essence_record("五風")
    assert five["formula_skeleton"]["route"]["status"] == "implemented_c53_profile_selection"
    assert five["formula_skeleton"]["route"]["canonical_route_for_tongzong_profile"] == [
        1, 3, 5, 7, 9, 2, 4, 6, 8
    ]
    assert five["runtime_formula_ready"] is True
    assert five["formula_skeleton"]["runtime_rule_id"] == "C53-FIVEWIND"


def test_c52_ten_essence_flying_bird_is_not_j4m_external_observation():
    bird = ten_essence_record("飛鳥")
    boundary = bird["formula_skeleton"]["same_name_boundary"]
    assert boundary["j4m11_external_bird_observation"] is False
    assert "不得互相代替" in boundary["policy"]


def test_c52_rejected_surplus_variants_are_not_applied():
    for name in ("天皇", "帝符", "天时", "飞鸟", "八风", "五风", "三风"):
        variant = FOCUS_FORMULA_SKELETONS[name]["surplus_variant"]
        assert variant["apply"] is False
        assert "古" in variant["note"] or "经旨" in variant["note"]


def test_c52_fivewind_preserves_collation_variant_without_overriding_primary():
    five = FOCUS_FORMULA_SKELETONS["五风"]
    assert five["route"]["tongzong_sequence"][3:5] == [7, 9]
    assert five["route"]["wujing_zongyao_variant_sequence"][3:5] == [9, 7]
    assert five["route"]["wujing_zongyao_parallel_sequence"][3:5] == [7, 9]
    assert five["runtime_formula_ready"] is True
    assert five["runtime_rule_id"] == "C53-FIVEWIND"
    assert five["runtime_profile"] == "tongzong_primary_taibai_collation"



def test_c52_wuxing_and_tianshi_runtime_boundaries_are_locked():
    wuxing = FOCUS_FORMULA_SKELETONS["五行"]
    assert wuxing["big_cycle"] == 50
    assert wuxing["small_cycle"] == 5
    assert wuxing["route"]["tongzong_yang_path"] == [1, 8, 3, 9, 7]
    assert wuxing["route"]["taibai_yin_path"] == [9, 2, 7, 1, 3]
    assert wuxing["runtime_formula_ready"] is True
    assert wuxing["runtime_rule_id"] == "C53-WUXING"

    tianshi = FOCUS_FORMULA_SKELETONS["天时"]
    assert tianshi["big_cycle"] == 120
    assert tianshi["small_cycle"] == 12
    assert tianshi["route"]["tongzong_yang_path"] == [
        "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"
    ]
    assert tianshi["route"]["tongzong_yin_path"] == [
        "申", "酉", "戌", "亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未"
    ]
    assert "阳寅阴申" in tianshi["route"]["taibai_detailed_formula"]
    assert "阳申阴寅" in tianshi["route"]["taibai_intro_summary_variant"]
    assert tianshi["route"]["status"] == "implemented_c56_primary_with_internal_variant_preserved"
    assert tianshi["surplus_variant"]["value"] == 2
    assert tianshi["surplus_variant"]["apply"] is False
    assert tianshi["runtime_formula_ready"] is True
    assert tianshi["runtime_rule_id"] == "C56-TIANSHI"



def test_c52_taiyi_number_is_implemented_as_number_not_position():
    data = ten_essences_registry()
    assert data["implemented_number_runtimes"] == ["太乙数"]
    assert data["number_runtime_pending"] == []

    record = ten_essence_record("太乙數")
    assert record["kind"] == "number"
    assert record["formula_status"] == "implemented_c54"
    assert record["runtime_formula_ready"] is True
    assert record["formula_skeleton"]["runtime_rule_id"] == "C54-TAIYI-NUMBER"
    assert record["formula_skeleton"]["route"]["range"] == [1, 72]
