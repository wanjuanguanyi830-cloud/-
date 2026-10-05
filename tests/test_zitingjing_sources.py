import pytest

from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.zitingjing_sources import (
    RULES,
    build_zitingjing_p1_sources,
    build_zitingjing_rule_sources,
    build_zitingjing_source_variants,
    PRIMARY_SOURCE_TITLE,
)


def test_full_primary_source_title_is_taiyi_zitingjing():
    assert PRIMARY_SOURCE_TITLE == "太乙紫庭经"


def test_six_legacy_source_slots_record_current_evidence_role():
    assert set(RULES) == {
        "taiyi_nine_stars",
        "wenchang_nine_stars",
        "wenchang_changes",
        "shiji_changes",
        "three_banners",
        "nine_palace_nobles",
    }
    for meta in RULES.values():
        assert meta["primary_source"] == "zitingjing"

    assert RULES["taiyi_nine_stars"]["primary_evidence_level"] == "direct_text_verified"
    assert RULES["wenchang_changes"]["primary_evidence_level"] == "direct_text_verified"
    assert RULES["shiji_changes"]["primary_evidence_level"] == "direct_text_verified"
    assert RULES["wenchang_nine_stars"]["primary_evidence_level"] == "prior_scan_confirmed_page_record_pending"
    assert RULES["three_banners"]["primary_evidence_level"] == "ziting_not_attested_cross_source_only"
    assert RULES["nine_palace_nobles"]["primary_evidence_level"] == "ziting_not_attested_cross_source_only"
    assert RULES["three_banners"]["known_source_rule_id"] == "C126-TONGZONG-THREE-BANNERS"
    assert RULES["nine_palace_nobles"]["known_source_rule_id"] == "C127-TONGZONG-NINE-PALACE-NOBLES"


def test_volume6_items_keep_tongzong_as_collation_only():
    expected_status = {
        "taiyi_nine_stars": "primary_pending",
        "wenchang_nine_stars": "primary_prior_scan_confirmed_page_record_pending",
        "wenchang_changes": "primary_pending",
        "shiji_changes": "primary_pending",
    }
    for key, status in expected_status.items():
        data = build_zitingjing_rule_sources(
            key,
            collation_results={"tongzong_volume6": {"legacy": "参校"}},
        )
        assert data["primary_source"] == "zitingjing"
        assert data["primary_ready"] is False
        assert data["canonical_selected"] is None
        assert data["status"] == status
        assert data["collation_results"]["tongzong_volume6"] == {"legacy": "参校"}
        assert data["cross_source_merge"] is False


def test_volume10_items_are_legacy_recovery_pointers_with_resolved_tongzong_rules():
    expected = {
        "three_banners": "C126-TONGZONG-THREE-BANNERS",
        "nine_palace_nobles": "C127-TONGZONG-NINE-PALACE-NOBLES",
    }
    for key, rule_id in expected.items():
        data = build_zitingjing_rule_sources(
            key,
            collation_results={"tongzong_volume10": {"legacy": "兼容迁移值"}},
        )
        assert data["primary_ready"] is False
        assert data["primary_result_allowed"] is False
        assert data["primary_evidence_level"] == "ziting_not_attested_cross_source_only"
        assert data["status"] == "legacy_cross_source_recovery_pointer"
        assert data["known_source_rule_id"] == rule_id
        assert data["canonical_selected"] is None
        assert data["collation_sources"] == ["tongzong_volume10"]


def test_primary_result_can_coexist_with_collation_without_merge():
    data = build_zitingjing_rule_sources(
        "taiyi_nine_stars",
        primary_result={"source": "太乙紫庭经", "table": [1, 2, 3]},
        collation_results={"tongzong_volume6": {"source": "统宗", "table": [1, 2, 4]}},
    )
    assert data["primary_ready"] is True
    assert data["canonical_selected"] == "zitingjing"
    assert data["primary_result"]["table"] == [1, 2, 3]
    assert data["collation_results"]["tongzong_volume6"]["table"] == [1, 2, 4]
    assert data["cross_source_merge"] is False


def test_wrong_collation_volume_is_rejected():
    with pytest.raises(ValueError):
        build_zitingjing_rule_sources(
            "taiyi_nine_stars",
            collation_results={"tongzong_volume10": {"wrong": True}},
        )

    with pytest.raises(ValueError):
        build_zitingjing_rule_sources(
            "three_banners",
            collation_results={"tongzong_volume6": {"wrong": True}},
        )


def test_batch_source_variants_keep_primary_pending_by_default():
    data = build_zitingjing_source_variants()
    assert set(data) == {"zitingjing"}
    rules = data["zitingjing"]["rules"]
    assert all(item["primary_source"] == "zitingjing" for item in rules.values())
    assert all(item["primary_ready"] is False for item in rules.values())
    assert all(item["canonical_selected"] is None for item in rules.values())


def test_legacy_ziting_fields_route_to_matching_tongzong_collation_profiles():
    expected = {
        "太乙九星": "source_variants.zitingjing.rules.taiyi_nine_stars.collation_results.tongzong_volume6",
        "文昌九星": "source_variants.zitingjing.rules.wenchang_nine_stars.collation_results.tongzong_volume6",
        "文昌變化": "source_variants.zitingjing.rules.wenchang_changes.collation_results.tongzong_volume6",
        "始擊變化": "source_variants.zitingjing.rules.shiji_changes.collation_results.tongzong_volume6",
        "三旗行宮": "source_variants.zitingjing.rules.three_banners.collation_results.tongzong_volume10",
        "九宮貴神": "source_variants.zitingjing.rules.nine_palace_nobles.collation_results.tongzong_volume10",
    }
    for key, replacement in expected.items():
        item = classify_legacy_field(key)
        assert item["status"] == "quarantined"
        assert item["replacement"] == replacement


def _legacy_snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "太乙九星": {"旧": "统宗实现"},
        "文昌九星": {"旧": "统宗实现"},
        "文昌變化": {"旧": "统宗实现"},
        "始擊變化": {"旧": "统宗实现"},
        "三旗行宮": {"旧": "统宗实现"},
        "九宮貴神": {"旧": "统宗实现"},
    }


def test_matching_tongzong_collations_clear_legacy_flat_replacement_gaps():
    variants = build_zitingjing_source_variants(results={
        "taiyi_nine_stars": {
            "collation_results": {"tongzong_volume6": {"old": True}},
        },
        "wenchang_nine_stars": {
            "collation_results": {"tongzong_volume6": {"old": True}},
        },
        "wenchang_changes": {
            "collation_results": {"tongzong_volume6": {"old": True}},
        },
        "shiji_changes": {
            "collation_results": {"tongzong_volume6": {"old": True}},
        },
        "three_banners": {
            "collation_results": {"tongzong_volume10": {"old": True}},
        },
        "nine_palace_nobles": {
            "collation_results": {"tongzong_volume10": {"old": True}},
        },
    })
    snapshot = attach_v2_to_snapshot(_legacy_snapshot(), source_variants=variants)
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True


def test_primary_completion_is_independent_from_legacy_collation_replacement():
    results = {
        "taiyi_nine_stars": {
            "primary_result": {"source": "太乙紫庭经", "rule_key": "taiyi_nine_stars"},
            "collation_results": {"tongzong_volume6": {"source": "统宗参校"}},
        },
        "wenchang_changes": {
            "primary_result": {"source": "太乙紫庭经", "rule_key": "wenchang_changes"},
            "collation_results": {"tongzong_volume6": {"source": "统宗参校"}},
        },
        "shiji_changes": {
            "primary_result": {"source": "太乙紫庭经", "rule_key": "shiji_changes"},
            "collation_results": {"tongzong_volume6": {"source": "统宗参校"}},
        },
        "wenchang_nine_stars": {
            "collation_results": {"tongzong_volume6": {"source": "统宗参校"}},
        },
        "three_banners": {
            "collation_results": {"tongzong_volume10": {"source": "统宗参校"}},
        },
        "nine_palace_nobles": {
            "collation_results": {"tongzong_volume10": {"source": "统宗参校"}},
        },
    }

    variants = build_zitingjing_source_variants(results=results)
    snapshot = attach_v2_to_snapshot(_legacy_snapshot(), source_variants=variants)
    report = audit_legacy_snapshot(snapshot)

    # legacy flat字段已经由同源统宗collation profile替代；
    # 紫庭primary是否完成是另一条证据状态，不属于legacy replacement gap。
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True

    rules = variants["zitingjing"]["rules"]
    assert rules["taiyi_nine_stars"]["primary_ready"] is True
    assert rules["wenchang_changes"]["primary_ready"] is True
    assert rules["shiji_changes"]["primary_ready"] is True
    assert rules["wenchang_nine_stars"]["primary_ready"] is False
    assert rules["three_banners"]["primary_ready"] is False
    assert rules["nine_palace_nobles"]["primary_ready"] is False


def test_pending_or_unverified_ziting_items_reject_primary_result_injection():
    for key in ("wenchang_nine_stars", "three_banners", "nine_palace_nobles"):
        with pytest.raises(ValueError, match="不得注入primary_result"):
            build_zitingjing_rule_sources(
                key,
                primary_result={"fake": True},
            )

def test_legacy_flat_values_are_not_auto_promoted_into_primary_source():
    snapshot = attach_v2_to_snapshot(_legacy_snapshot())
    ziting = snapshot["v2"]["source_variants"].get("zitingjing")
    assert ziting is None
    assert snapshot["v2"]["analysis"]["patterns"] == {}
