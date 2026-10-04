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
        "canonical": 31,
        "derived": 18,
        "pending": 2,
        "source_variant": 16,
    }


def test_c61_only_two_strict_pending_fields_remain():
    pending = sorted(
        key for key, item in CATALOG.items()
        if item["layer"] == "pending"
    )
    assert pending == ["推太乙當時法", "文昌九星"]


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


def test_c61_c66_three_bases_use_runtime_and_preserve_volume_variant():
    for key in (
        "明君基太乙所主術",
        "明臣基太乙所主術",
        "明民基太乙所主術",
    ):
        item = catalog_unported_field(key)
        assert item["layer"] == "canonical"
        assert item["source_scope"] == "tongzong_volume6_7_witness_variant_direct"
        assert item["source_confidence"] == "high"
        assert item["action"] == "use_c66_three_bases_cycle_runtime"
        assert item["migrate_whole"] is False
        assert "邦盈差250" in item["notes"]

    wufu = catalog_unported_field("明五福太乙所主術")
    assert wufu["action"] == "use_c67_wufu_tongzong_profile"
    assert wufu["migrate_whole"] is False
    assert "宫盈差115" in wufu["notes"]
    assert "金镜" in wufu["notes"]

    wufu_numbers = catalog_unported_field("明五福吉算所主術")
    assert wufu_numbers["action"] == "source_verified_split_runtime_next"
    assert wufu_numbers["migrate_whole"] is False
    assert "独立于C67" in wufu_numbers["notes"]


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


def test_c61_remaining_source_verified_fields_are_not_yet_runtime_implemented():
    fields = ("明五福吉算所主術",)
    for key in fields:
        item = catalog_unported_field(key)
        assert item["action"] == "source_verified_split_runtime_next"
        assert item["migrate_whole"] is False


def test_c61_ten_essence_notes_no_longer_call_cloud_layer_unimplemented():
    for key in ("太尊", "飛鳥", "三風", "五風", "八風"):
        notes = catalog_unported_field(key)["notes"]
        assert "C57" in notes
        assert "C58" in notes
        assert "C59" in notes
        assert "仍属独立source unit" not in notes
