import json
from pathlib import Path

from kintaiyi.zitingjing_sources import build_zitingjing_rule_sources


RECOVERY = Path("terminology/zitingjing-legacy-scan-recovery.json")
MIGRATION = Path("terminology/zitingjing-migration-map.json")
CATALOG = Path("terminology/zitingjing.json")
INDEX = Path("terminology/catalog-index.json")
MANIFEST = Path("terminology/legacy-recovery-manifest.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_prior_ziting_scan_recovery_keeps_legacy_forms_without_promoting_primary():
    recovery = _load(RECOVERY)
    entry = recovery["entries"][0]

    assert recovery["status"] == (
        "recovered_legacy_scan_extraction_residue_direct_page_not_reattached"
    )
    assert entry["key"] == "wenchang_nine_stars"
    assert entry["recovered_star_sequence"] == [
        "文曲", "玄鳳", "明維", "昭搖", "立華", "華明", "玄武", "玄冥", "雄明"
    ]
    assert entry["current_audit"]["canonical_equivalent"] is False


def test_ziting_catalog_records_recovered_scan_evidence_but_blocks_primary_result():
    catalog = _load(CATALOG)
    entry = next(e for e in catalog["entries"] if e["key"] == "wenchang_nine_stars")

    assert entry["primary_evidence_level"] == (
        "legacy_scan_extraction_recovered_page_pending"
    )
    assert entry["primary_result_allowed"] is False
    assert entry["runtime"] is None
    assert entry["legacy_scan_recovery"]["recovered_forms"][0] == "文曲"

    wrapped = build_zitingjing_rule_sources("wenchang_nine_stars")
    assert wrapped["status"] == "primary_legacy_scan_recovered_page_pending"
    assert wrapped["primary_ready"] is False
    assert wrapped["canonical_selected"] is None


def test_migration_map_and_index_link_the_recovery_asset():
    migration = _load(MIGRATION)
    entry = next(e for e in migration["entries"] if e["key"] == "wenchang_nine_stars")
    assert entry["legacy_scan_recovery_asset"] == (
        "terminology/zitingjing-legacy-scan-recovery.json"
    )
    assert "文曲" in entry["legacy_recovered_forms"]

    index = _load(INDEX)
    assert any(
        x["path"] == "terminology/zitingjing-legacy-scan-recovery.json"
        for x in index["migration_assets"]
    )


def test_legacy_manifest_records_local_copy_without_faking_old_ids_or_pages():
    manifest = _load(MANIFEST)
    availability = manifest["original_store_availability"]
    assert availability["user_reported_local_copy"]["location"] == "local E drive"
    assert availability["user_reported_local_copy"]["status"].endswith(
        "not_mounted_in_current_runtime"
    )

    entry = next(
        x for x in manifest["stable_entries"]
        if x["stable_ref"] == {
            "catalog": "terminology/zitingjing.json",
            "key": "wenchang_nine_stars",
        }
    )
    assert entry["legacy_match_status"].startswith(
        "legacy_scan_extraction_residue_recovered"
    )
    assert entry["legacy_fields"]["old_term_record_id"] is None
    assert entry["legacy_fields"]["source_page"] is None
    assert entry["legacy_fields"]["old_aliases"] is None
    assert "文曲" in entry["recovered_scan_aliases"]
