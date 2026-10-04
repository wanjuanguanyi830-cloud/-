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


def test_six_p1_rules_all_use_zitingjing_primary():
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


def test_volume6_items_keep_tongzong_as_collation_only():
    for key in ("taiyi_nine_stars", "wenchang_nine_stars", "wenchang_changes", "shiji_changes"):
        data = build_zitingjing_rule_sources(
            key,
            collation_results={"tongzong_volume6": {"legacy": "参校"}},
        )
        assert data["primary_source"] == "zitingjing"
        assert data["primary_ready"] is False
        assert data["canonical_selected"] is None
        assert data["status"] == "primary_pending"
        assert data["collation_results"]["tongzong_volume6"] == {"legacy": "参校"}
        assert data["cross_source_merge"] is False


def test_volume10_items_keep_tongzong_as_collation_only():
    for key in ("three_banners", "nine_palace_nobles"):
        data = build_zitingjing_rule_sources(
            key,
            collation_results={"tongzong_volume10": {"legacy": "参校"}},
        )
        assert data["primary_ready"] is False
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


def test_legacy_fields_are_quarantined_until_zitingjing_primary_exists():
    expected = {
        "太乙九星": "source_variants.zitingjing.rules.taiyi_nine_stars.primary_result",
        "文昌九星": "source_variants.zitingjing.rules.wenchang_nine_stars.primary_result",
        "文昌變化": "source_variants.zitingjing.rules.wenchang_changes.primary_result",
        "始擊變化": "source_variants.zitingjing.rules.shiji_changes.primary_result",
        "三旗行宮": "source_variants.zitingjing.rules.three_banners.primary_result",
        "九宮貴神": "source_variants.zitingjing.rules.nine_palace_nobles.primary_result",
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


def test_collation_only_does_not_clear_primary_replacement_gaps():
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
    assert len(report["replacement_gaps"]) == 6
    assert all("primary_result" in path for path in report["replacement_gaps"])
    assert report["ready_for_v2_core_consumption"] is False


def test_zitingjing_primary_results_clear_replacement_gaps_while_collation_remains():
    results = {}
    for key, meta in RULES.items():
        collation = meta["collation_sources"][0]
        results[key] = {
            "primary_result": {"source": "太乙紫庭经", "rule_key": key},
            "collation_results": {collation: {"source": "统宗参校", "rule_key": key}},
        }

    variants = build_zitingjing_source_variants(results=results)
    snapshot = attach_v2_to_snapshot(_legacy_snapshot(), source_variants=variants)
    report = audit_legacy_snapshot(snapshot)

    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True
    assert report["quarantined_key_count"] == 6
    assert variants["zitingjing"]["rules"]["taiyi_nine_stars"]["collation_results"]


def test_legacy_flat_values_are_not_auto_promoted_into_primary_source():
    snapshot = attach_v2_to_snapshot(_legacy_snapshot())
    ziting = snapshot["v2"]["source_variants"].get("zitingjing")
    assert ziting is None
    assert snapshot["v2"]["analysis"]["patterns"] == {}
