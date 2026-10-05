from kintaiyi.unported_catalog import (
    CATALOG,
    REFERENCE_PAN_UNPORTED_FIELDS,
    catalog_unported_field,
    unported_catalog_report,
)


def test_c61_catalog_still_covers_exact_67_legacy_fields():
    assert len(REFERENCE_PAN_UNPORTED_FIELDS) == 67
    assert set(CATALOG) == set(REFERENCE_PAN_UNPORTED_FIELDS)


def test_c61_layer_counts_after_source_reclassification():
    data = unported_catalog_report(REFERENCE_PAN_UNPORTED_FIELDS)
    assert data["field_count"] == 67
    assert data["layer_counts"] == {
        "canonical": 32,
        "derived": 18,
        "source_variant": 17,
    }


def test_c61_no_strict_pending_fields_remain_after_c70():
    pending = sorted(
        key for key, item in CATALOG.items()
        if item["layer"] == "pending"
    )
    assert pending == []


def test_c61_c70_wenchang_is_source_variant_not_fake_zitingjing_canonical():
    item = catalog_unported_field("文昌九星")
    assert item["layer"] == "source_variant"
    assert item["source_scope"] == (
        "zitingjing_catalog_pending_vs_tongzong_volume6_ngj_direct"
    )
    assert item["action"] == (
        "use_c70_tongzong_profile_keep_zitingjing_primary_pending"
    )
    assert item["source_confidence"] == "high"
    assert item["migrate_whole"] is False
    assert "30年一星" in item["notes"]
    assert "紫庭primary继续pending" in item["notes"]


def test_c61_c69_current_time_is_direct_jinjing_partial_runtime():
    item = catalog_unported_field("推太乙當時法")
    assert item["layer"] == "canonical"
    assert item["source_scope"] == "jinjing_volume1_direct"
    assert item["priority"] == "P1"
    assert item["action"] == "use_c69_current_time_core_partial"
    assert item["source_confidence"] == "high"
    assert item["migrate_whole"] is False
    assert "complete_current_time_formula=False" in item["notes"]


def test_c61_c62_imperial巡狩_is_direct_volume5_and_runtime_implemented():
    item = catalog_unported_field("明天子巡狩之期術")
    assert item["layer"] == "canonical"
    assert item["source_scope"] == "tongzong_volume5_direct"
    assert item["priority"] == "P1"
    assert item["action"] == "use_c62_imperial_inspection_runtime"
    assert item["source_confidence"] == "high"
    assert item["migrate_whole"] is False
    assert item["target_hint"] == "analysis.rules.imperial_inspection"
    assert "四维" in item["notes"]
    assert "不自行造月" in item["notes"]


def test_c61_c66_c74_three_bases_use_position_and_relation_layers():
    for key in (
        "明君基太乙所主術",
        "明臣基太乙所主術",
        "明民基太乙所主術",
    ):
        item = catalog_unported_field(key)
        assert item["layer"] == "canonical"
        assert item["source_scope"] == "tongzong_volume6_7_witness_variant_direct"
        assert item["source_confidence"] == "high"
        assert item["action"] == "use_c66_c74_three_bases_layers"
        assert item["migrate_whole"] is False
        assert "邦盈差250" in item["notes"]
        assert "C74 已实现" in item["notes"]
        assert "禁止由C66位置自动制造同宫" in item["notes"]

    wufu = catalog_unported_field("明五福太乙所主術")
    assert wufu["action"] == "use_c67_c74_wufu_layers"
    assert wufu["migrate_whole"] is False
    assert "宫盈差115" in wufu["notes"]
    assert "金镜" in wufu["notes"]
    assert "C74" in wufu["notes"]
    assert "初交之始" in wufu["notes"]

    wufu_numbers = catalog_unported_field("明五福吉算所主術")
    assert wufu_numbers["action"] == "use_c68_wufu_auspicious_number_runtime"
    assert wufu_numbers["migrate_whole"] is False
    assert "1..45" in wufu_numbers["notes"]
    assert "不从积年自动调用C67" in wufu_numbers["notes"]


def test_c61_c64_tianyi_diyi_zhifu_are_direct_volume7_with_position_runtime():
    for key in (
        "明天乙太乙所主術",
        "明地乙太乙所主術",
        "明值符太乙所主術",
    ):
        item = catalog_unported_field(key)
        assert item["layer"] == "canonical"
        assert item["source_scope"] == "tongzong_volume7_direct"
        assert item["source_confidence"] == "high"
        assert item["action"] == "use_c64_c65_three_spirit_layers"
        assert item["migrate_whole"] is False
        assert "C65 已实现" in item["notes"]
        assert "same_palace显式输入" in item["notes"]


def test_c61_ten_essence_notes_no_longer_call_cloud_layer_unimplemented():
    for key in ("太尊", "飛鳥", "三風", "五風", "八風"):
        notes = catalog_unported_field(key)["notes"]
        assert "C57" in notes
        assert "C58" in notes
        assert "C59" in notes
        assert "仍属独立source unit" not in notes
