import json
from pathlib import Path


MIGRATION_FILE = Path(__file__).parents[1] / "terminology" / "zitingjing-migration-map.json"


def _data():
    return json.loads(MIGRATION_FILE.read_text(encoding="utf-8"))


def test_ziting_terminology_migration_map_tracks_prior_local_work():
    data = _data()
    assert data["prior_local_terminology_status"] == "preliminary_completed_locally"
    assert data["current_repository_status"] == (
        "prior_manuscript_scan_confirmed_original_store_and_pages_not_reattached"
    )
    assert data["manuscript_source_id"] == "shanghai_yanyilou_ming_copy"


def test_ziting_terminology_map_has_six_core_entries():
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


def test_unknown_manuscript_fields_stay_null_until_old_store_or_scan_is_recovered():
    data = _data()
    for item in data["entries"]:
        assert item["manuscript_form"] is None
        assert item["source_page"] is None


def test_wenchang_external_variants_do_not_become_manuscript_reading():
    data = _data()
    item = next(x for x in data["entries"] if x["key"] == "wenchang_nine_stars")
    assert item["manuscript_form"] is None
    groups = item["external_collation_variant_groups"]
    assert ["明雄", "明维", "明維"] in groups
    assert ["阴玄", "陰玄", "阴德", "陰德"] in groups
    assert "不选canonical" in item["variant_policy"]


def test_unverified_ziting_attributions_remain_unverified_in_terminology_map():
    data = _data()
    entries = {item["key"]: item for item in data["entries"]}
    for key in ("three_banners", "nine_palace_nobles"):
        item = entries[key]
        assert item["current_rule_status"] == "zitingjing_attribution_unverified"
        assert item["runtime"] is None
        assert "不能" in item["source_boundary"] or "未证" in item["source_boundary"]


def test_recovery_order_prioritizes_current_source_gaps():
    data = _data()
    assert data["recovery_order"][:3] == [
        "wenchang_nine_stars",
        "three_banners",
        "nine_palace_nobles",
    ]
