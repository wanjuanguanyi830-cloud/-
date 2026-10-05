import json
from pathlib import Path


MIGRATION_FILE = Path(__file__).parents[1] / "terminology" / "zitingjing-migration-map.json"


def _data():
    return json.loads(MIGRATION_FILE.read_text(encoding="utf-8"))


def test_ziting_terminology_migration_map_tracks_prior_local_work():
    data = _data()
    assert data["prior_local_terminology_status"] == "preliminary_completed_locally"
    assert data["current_repository_status"] == (
        "manuscript_scan_reattached_toc_inspected_original_terminology_store_not_recovered"
    )
    assert data["manuscript_source_id"] == "shanghai_yanyilou_ming_copy"


def test_ziting_terminology_map_has_six_historical_recovery_keys():
    data = _data()
    entries = {item["key"]: item for item in data["entries"]}
    assert set(entries) == {
        "taiyi_nine_stars",
        "wenchang_nine_stars",
        "wenchang_changes",
        "shiji_changes",
        "three_banners",
        "nine_palace_nobles",
    }


def test_unknown_old_store_fields_stay_null_until_original_store_is_recovered():
    data = _data()
    for item in data["entries"]:
        assert item["manuscript_form"] is None
        assert item["source_page"] is None


def test_wenchang_migration_key_is_historical_only_and_stable_term_moved():
    data = _data()
    item = next(x for x in data["entries"] if x["key"] == "wenchang_nine_stars")

    assert item["terminology_status"] == (
        "historical_migration_key_only_stable_term_moved_to_wenchang_catalog"
    )
    assert item["current_rule_status"] == (
        "tongzong_c70_source_resolved_yanyilou_toc_not_attested"
    )
    assert item["runtime"] == (
        "kintaiyi.wenchang_nine_stars_tongzong.wenchang_nine_star_tongzong"
    )
    assert item["manuscript_form"] is None
    assert item["source_page"] is None
    assert "terminology/wenchang-nine-stars.json" in item["variant_policy"]
    assert "现代整理附篇来源未证" in item["variant_policy"]

    groups = item["external_collation_variant_groups"]
    assert ["明雄", "明维", "明維"] in groups
    assert ["阴玄", "陰玄", "阴德", "陰德"] in groups


def test_tongzong_rules_are_resolved_while_ziting_legacy_attribution_stays_recoverable():
    data = _data()
    entries = {item["key"]: item for item in data["entries"]}
    expected = {
        "three_banners": "C126-TONGZONG-THREE-BANNERS",
        "nine_palace_nobles": "C127-TONGZONG-NINE-PALACE-NOBLES",
    }
    for key, rule_id in expected.items():
        item = entries[key]
        assert item["current_rule_status"] == (
            "tongzong_volume10_direct_ziting_legacy_attribution_unverified"
        )
        assert item["current_rule_id"] == rule_id
        assert item["runtime"].startswith(
            "kintaiyi.tongzong_volume10_spirits."
        )
        assert "现行可执行公式已由《太乙统宗宝鉴》卷十直接证明" in item["source_boundary"]
        assert item["manuscript_form"] is None
        assert item["source_page"] is None


def test_recovery_order_is_for_old_store_fields_not_for_rule_source_gaps():
    data = _data()

    assert data["recovery_order"][:3] == [
        "wenchang_nine_stars",
        "three_banners",
        "nine_palace_nobles",
    ]
    assert "文昌九星现行规则来源已由C70" in data["recovery_reason"]
    assert "研易楼明钞目录未见该题" in data["recovery_reason"]
    assert "旧store身份字段" in data["recovery_reason"]
