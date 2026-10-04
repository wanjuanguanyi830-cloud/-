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
    assert record["runtime_formula_ready"] is False


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


def test_c52_registry_is_metadata_only():
    data = ten_essences_registry()
    assert data["rule_id"] == "C52-TEN-ESSENCES-REGISTRY"
    assert data["position_runtime_ready"] is False
    assert data["cloud_runtime_ready"] is False
    assert data["target_policy"]["legacy_top_level_promoted"] is False
    assert all(
        row["formula_status"] == "pending_source_formula_audit"
        for row in data["essences"]
    )


@pytest.mark.parametrize("field", ["帝符", "太尊", "飛鳥", "三風", "五風", "八風"])
def test_c52_reclassifies_old_pan_fields_as_source_verified_formula_pending(field):
    item = catalog_unported_field(field)
    assert item["layer"] == "canonical"
    assert item["source_scope"] == "tongzong_ten_essences_volume18_20_variant"
    assert item["action"] == "use_c52_source_registry_formula_pending"
    assert item["migrate_whole"] is False
    assert item["source_confidence"] == "high"
    assert item["target_hint"] == "source_variants.ten_essences"
    assert "不得进入cycles真源" in item["notes"]


def test_c52_registry_never_introduces_tianyou_taiyi():
    serialized = repr(ten_essences_registry())
    assert "天游太乙" not in serialized


def test_c52_focus_formula_skeletons_lock_direct_source_boundaries():
    difu = FOCUS_FORMULA_SKELETONS["帝符"]
    assert difu["big_cycle"] == 200
    assert difu["small_cycle"] == 20
    assert difu["route"]["start"] == "阴主"
    assert difu["route"]["repeat_on"] == [
        "地主", "高丛", "大威", "太簇", "坎", "离", "震", "兑"
    ]
    assert difu["surplus_variant"]["value"] == 70
    assert difu["surplus_variant"]["apply"] is False

    taizun = FOCUS_FORMULA_SKELETONS["太尊"]
    assert taizun["big_cycle"] == 40
    assert taizun["small_cycle"] == 4
    assert taizun["route"]["canonical_route"] is None
    assert taizun["runtime_formula_ready"] is False

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
    assert five["route"]["status"] == "primary_direct_collated_with_preserved_variant"
    assert five["route"]["canonical_route_for_tongzong_profile"] == [
        1, 3, 5, 7, 9, 2, 4, 6, 8
    ]
    assert five["route"]["cross_source_canonical_selected"] is None

    three = FOCUS_FORMULA_SKELETONS["三风"]
    assert three["route"]["source_sequence"] == [3, 7, 2, 6, 1, 5, 4, 8]
    assert len(three["route"]["source_sequence"]) == 8
    assert three["route"]["canonical_route"] is None
    assert "不得自行补第九项" in three["route"]["note"]


def test_c52_formula_skeleton_never_promotes_runtime_readiness():
    data = ten_essences_registry()
    assert data["position_runtime_ready"] is False
    for name, skeleton in data["focus_formula_skeletons"].items():
        assert skeleton["runtime_formula_ready"] is False, name

    five = ten_essence_record("五風")
    assert five["formula_skeleton"]["route"]["status"] == (
        "primary_direct_collated_with_preserved_variant"
    )
    assert five["formula_skeleton"]["route"]["canonical_route_for_tongzong_profile"] == [
        1, 3, 5, 7, 9, 2, 4, 6, 8
    ]
    assert five["runtime_formula_ready"] is False


def test_c52_ten_essence_flying_bird_is_not_j4m_external_observation():
    bird = ten_essence_record("飛鳥")
    boundary = bird["formula_skeleton"]["same_name_boundary"]
    assert boundary["j4m11_external_bird_observation"] is False
    assert "不得互相代替" in boundary["policy"]


def test_c52_rejected_surplus_variants_are_not_applied():
    for name in ("帝符", "飞鸟", "八风", "五风", "三风"):
        variant = FOCUS_FORMULA_SKELETONS[name]["surplus_variant"]
        assert variant["apply"] is False
        assert "古" in variant["note"] or "经旨" in variant["note"]


def test_c52_fivewind_preserves_collation_variant_without_overriding_primary():
    five = FOCUS_FORMULA_SKELETONS["五风"]
    assert five["route"]["tongzong_sequence"][3:5] == [7, 9]
    assert five["route"]["wujing_zongyao_variant_sequence"][3:5] == [9, 7]
    assert five["route"]["wujing_zongyao_parallel_sequence"][3:5] == [7, 9]
    assert five["runtime_formula_ready"] is False
    assert "C53" in five["runtime_blocker"]
