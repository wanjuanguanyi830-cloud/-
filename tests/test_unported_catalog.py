from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.unported_catalog import (
    REFERENCE_PAN_UNPORTED_FIELDS,
    catalog_unported_field,
    prioritize_unported_fields,
    unported_catalog_report,
)


def test_reference_pan_unported_catalog_covers_67_fields():
    assert len(REFERENCE_PAN_UNPORTED_FIELDS) == 67
    assert "十六宮分佈" in REFERENCE_PAN_UNPORTED_FIELDS
    assert "卷十二" in REFERENCE_PAN_UNPORTED_FIELDS
    assert "軍事占斷" in REFERENCE_PAN_UNPORTED_FIELDS


def test_volume2_sixteen_palaces_is_high_priority_canonical_candidate():
    item = catalog_unported_field("十六宮分佈")
    assert item["layer"] == "canonical"
    assert item["source_scope"] == "tongzong_volume2"
    assert item["priority"] == "P0"
    assert item["target_hint"] == "board.sixteen_palaces"
    assert item["migrate_whole"] is True


def test_old_pattern_wrapper_requires_source_variants():
    item = catalog_unported_field("釋格局")
    assert item["layer"] == "source_variant"
    assert item["priority"] == "P0"
    assert item["migrate_whole"] is False
    assert "tongzong_volume4" in item["source_scope"]
    assert "jinjing" in item["source_scope"]


def test_old_military_core_fields_are_not_promoted_without_source_profile():
    for key in ("推三門具不具", "推五將發不發", "推主客相闗法"):
        item = catalog_unported_field(key)
        assert item["layer"] == "source_variant"
        assert item["priority"] == "P0"
        assert item["migrate_whole"] is False


def test_weather_bird_military_rule_requires_observation_model():
    item = catalog_unported_field("推太乙風雲飛鳥助戰法")
    assert item["layer"] == "pending"
    assert item["priority"] == "P1"
    assert item["migrate_whole"] is False
    assert "observation_model" in item["action"]


def test_volume_wrappers_are_derived_and_never_migrated_wholesale():
    for key in ("卷八", "卷九", "卷十", "卷十一", "卷十二", "卷十三", "卷十四", "卷十八"):
        item = catalog_unported_field(key)
        assert item["layer"] == "derived"
        assert item["priority"] == "P3"
        assert item["migrate_whole"] is False
        assert item["action"] == "split_composite_wrapper"


def test_volume15_and_17_military_stay_separate_from_c8_and_j4m():
    v15 = catalog_unported_field("軍事應用")
    v17 = catalog_unported_field("軍事占斷")
    assert v15["layer"] == v17["layer"] == "derived"
    assert v15["source_scope"] == "tongzong_volume15"
    assert v17["source_scope"] == "tongzong_volume17"
    assert v15["migrate_whole"] is v17["migrate_whole"] is False


def test_volume6_standalone_rules_are_canonical_candidates():
    for key in ("太乙九星", "文昌九星", "文昌變化", "始擊變化"):
        item = catalog_unported_field(key)
        assert item["layer"] == "canonical"
        assert item["source_scope"] == "tongzong_volume6"
        assert item["priority"] == "P1"


def test_volume3_10_cross_volume_fields_are_source_variants():
    for key in ("五運六氣", "五音之數"):
        item = catalog_unported_field(key)
        assert item["layer"] == "source_variant"
        assert item["source_scope"] == "tongzong_volume3_and_volume10"
        assert item["migrate_whole"] is False


def test_volume1_moon_pipeline_stays_derived_modern_bridge():
    item = catalog_unported_field("朓胸定數")
    assert item["layer"] == "derived"
    assert item["source_scope"] == "tongzong_volume1_modern_astronomy_bridge"
    assert item["priority"] == "P3"
    assert item["migrate_whole"] is False


def test_unknown_new_field_stays_pending_and_low_priority():
    item = catalog_unported_field("未来新增字段")
    assert item["layer"] == "pending"
    assert item["source_scope"] == "unknown"
    assert item["priority"] == "P3"
    assert item["migrate_whole"] is False


def test_priority_queue_puts_p0_before_composite_wrappers():
    items = prioritize_unported_fields(["卷十二", "十六宮分佈", "太乙九星", "釋格局"])
    assert [item["field"] for item in items[:2]] == ["十六宮分佈", "釋格局"]
    assert items[-1]["field"] == "卷十二"


def test_catalog_report_exposes_layer_and_priority_counts():
    report = unported_catalog_report(["十六宮分佈", "釋格局", "卷十二", "推太乙當時法"])
    assert report["field_count"] == 4
    assert report["layer_counts"] == {
        "canonical": 1,
        "derived": 1,
        "pending": 1,
        "source_variant": 1,
    }
    assert report["priority_counts"] == {"P0": 2, "P2": 1, "P3": 1}
    assert {item["field"] for item in report["next_migration_candidates"]} == {
        "十六宮分佈", "釋格局"
    }


def test_c14_manifest_enriches_known_unported_field_without_changing_status():
    item = classify_legacy_field("卷十二")
    assert item["status"] == "unported"
    assert item["candidate_layer"] == "derived"
    assert item["priority"] == "P3"
    assert item["migrate_whole"] is False


def test_c13_audit_now_surfaces_next_migration_candidates():
    snapshot = attach_v2_to_snapshot({
        "太乙落宮": 1,
        "太乙": "乾",
        "十六宮分佈": {"legacy": True},
        "釋格局": {"legacy": True},
        "卷十二": {"legacy": True},
    })
    report = audit_legacy_snapshot(snapshot)
    assert report["unported_priority_counts"] == {"P0": 2, "P3": 1}
    assert report["unported_layer_counts"] == {
        "canonical": 1,
        "derived": 1,
        "source_variant": 1,
    }
    assert [item["field"] for item in report["next_migration_candidates"]] == [
        "十六宮分佈",
        "釋格局",
    ]
