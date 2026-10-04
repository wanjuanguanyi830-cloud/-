from kintaiyi.migration_audit import audit_legacy_snapshot, audit_snapshot_collection
from kintaiyi.pan_adapter import attach_v2_to_snapshot


def _legacy():
    return {
        "太乙計": "年計",
        "公元日期": "2026-10-05",
        "太乙落宮": 1,
        "太乙": "乾",
        "主算": [17, ["旧描述"]],
        "客算": [13, ["旧描述"]],
        "軍事戰略": {"旧": True},
        "推猛虎相拒": "旧断语",
        "推孤單以占成敗": "旧断语",
        "運籌博弈分析": {"旧": True},
        "卷十二": {"legacy": True},
    }


def test_legacy_only_status_and_rates():
    report = audit_legacy_snapshot(_legacy())
    assert report["status"] == "legacy_only"
    assert report["v2_present"] is False
    assert report["ready_for_v2_core_consumption"] is False
    assert "軍事戰略" in report["quarantined_legacy_keys"]
    assert "卷十二" in report["unported_legacy_keys"]
    assert report["replacement_gaps"] == ["v2"]


def test_v2_without_structured_replacements_is_partial():
    snapshot = attach_v2_to_snapshot(_legacy())
    report = audit_legacy_snapshot(snapshot)
    assert report["v2_valid"] is True
    assert report["status"] == "v2_partial_replacements"
    assert report["replacement_gaps"] == [
        "analysis.military",
        "analysis.seven_methods",
        "analysis.eight_divinations",
        "modern.game_theory",
    ]


def test_explicit_replacements_make_core_ready_even_with_unported_legacy():
    snapshot = attach_v2_to_snapshot(
        _legacy(),
        analysis={
            "military": {"source_profile": "volume5_strict"},
            "seven_methods": {"tiger": {"rule_id": "T7-04"}},
            "eight_divinations": {"home": {"rule_id": "D8-01"}},
        },
        modern={
            "game_theory": {
                "derived_modern_feature": True,
                "cross_system_palace_mapping": False,
            },
        },
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True
    assert report["status"] == "v2_core_ready_with_unported_legacy"
    assert "卷十二" in report["unported_legacy_keys"]


def test_no_unported_fields_can_reach_v2_core_ready():
    snapshot = {
        "太乙計": "年計",
        "公元日期": "2026-10-05",
        "太乙落宮": 1,
        "太乙": "乾",
        "主算": [17],
    }
    snapshot = attach_v2_to_snapshot(snapshot)
    report = audit_legacy_snapshot(snapshot)
    assert report["unported_legacy_keys"] == []
    assert report["replacement_gaps"] == []
    assert report["status"] == "v2_core_ready"


def test_invalid_v2_is_reported_separately():
    snapshot = _legacy()
    snapshot["v2"] = {"schema_version": "1.0"}
    report = audit_legacy_snapshot(snapshot)
    assert report["status"] == "v2_invalid"
    assert report["v2_valid"] is False
    assert any("schema_version" in item for item in report["v2_errors"])


def test_collection_aggregates_status_and_field_frequencies():
    legacy = _legacy()
    ready = attach_v2_to_snapshot(
        _legacy(),
        analysis={
            "military": {"ok": True},
            "seven_methods": {"ok": True},
            "eight_divinations": {"ok": True},
        },
        modern={"game_theory": {"derived_modern_feature": True}},
    )
    data = audit_snapshot_collection([legacy, ready])
    assert data["snapshot_count"] == 2
    assert data["status_counts"]["legacy_only"] == 1
    assert data["status_counts"]["v2_core_ready_with_unported_legacy"] == 1
    assert data["ready_for_v2_core_count"] == 1
    assert data["quarantined_field_frequency"]["軍事戰略"] == 2
    assert data["unported_field_frequency"]["卷十二"] == 2


def test_empty_collection_is_well_defined():
    data = audit_snapshot_collection([])
    assert data["snapshot_count"] == 0
    assert data["ready_for_v2_core_count"] == 0
    assert data["average_migrated_fact_rate"] == 0.0
    assert data["reports"] == []
