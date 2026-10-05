import json
from pathlib import Path


INDEX = Path("terminology/catalog-index.json")
MANIFEST = Path("terminology/legacy-recovery-manifest.json")
ZITING = Path("terminology/zitingjing-migration-map.json")
NCL = Path("terminology/ncl06604-legacy-reconciliation-map.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _stable_refs():
    index = _load(INDEX)
    refs = set()
    for item in index["stable_catalogs"]:
        catalog = _load(item["path"])
        for entry in catalog.get("entries", []):
            refs.add((item["path"], entry["key"]))
    return refs


def test_manifest_covers_every_stable_entry_exactly_once():
    manifest = _load(MANIFEST)
    expected = _stable_refs()
    actual = [
        (entry["stable_ref"]["catalog"], entry["stable_ref"]["key"])
        for entry in manifest["stable_entries"]
    ]

    assert len(actual) == len(set(actual))
    assert set(actual) == expected
    assert manifest["generated_from"]["stable_entry_count"] == len(expected)


def test_manifest_never_synthesizes_legacy_fields():
    manifest = _load(MANIFEST)

    assert manifest["legacy_field_policy"]["synthetic_ids_allowed"] is False
    for entry in manifest["stable_entries"]:
        legacy = entry["legacy_fields"]
        assert legacy["old_term_record_id"] is None
        assert legacy["manuscript_form"] is None
        assert legacy["source_page"] is None
        assert legacy["source_section"] is None
        assert legacy["old_definition"] is None
        assert legacy["old_notes"] is None
        assert legacy["old_aliases"] is None


def test_ziting_migration_entries_resolve_to_stable_refs():
    manifest = _load(MANIFEST)
    ziting = _load(ZITING)

    linked = {
        link["asset_entry_key"]
        for entry in manifest["stable_entries"]
        for link in entry["migration_links"]
        if link["asset"] == "terminology/zitingjing-migration-map.json"
    }

    assert linked == {entry["key"] for entry in ziting["entries"]}


def test_ncl_reconciliation_entries_all_resolve_after_j4m_catalog():
    manifest = _load(MANIFEST)
    ncl = _load(NCL)

    linked = {
        link["asset_entry_key"]
        for entry in manifest["stable_entries"]
        for link in entry["migration_links"]
        if link["asset"] == "terminology/ncl06604-legacy-reconciliation-map.json"
    }

    assert linked == {entry["key"] for entry in ncl["entries"]}
    assert manifest["migration_only_candidates"] == []


def test_original_legacy_store_still_remains_unrecovered():
    manifest = _load(MANIFEST)
    availability = manifest["original_store_availability"]

    assert manifest["status"] == "blocked_missing_original_store_with_reversible_mapping"
    assert availability["expected_name"] == "terminology.json"
    assert availability["schema_recovered"] is False
    assert availability["original_bytes_recovered"] is False
    assert "不生成合成old_term_record_id" in availability["policy"]
