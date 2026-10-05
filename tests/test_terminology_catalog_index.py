import json
from pathlib import Path


INDEX = Path("terminology/catalog-index.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_catalog_index_stable_catalogs_resolve_and_match_ids():
    index = _load(INDEX)
    ids = []

    for item in index["stable_catalogs"]:
        path = Path(item["path"])
        assert path.exists(), item["path"]
        catalog = _load(path)
        assert catalog["catalog_id"] == item["catalog_id"]
        assert catalog["scope"] == item["scope"]
        ids.append(item["catalog_id"])

    assert len(ids) == len(set(ids))
    assert len(ids) == 14


def test_catalog_index_separates_stable_migration_and_supporting_assets():
    index = _load(INDEX)

    stable_paths = {item["path"] for item in index["stable_catalogs"]}
    migration_paths = {item["path"] for item in index["migration_assets"]}
    supporting_paths = {item["path"] for item in index["supporting_assets"]}

    assert not stable_paths & migration_paths
    assert not stable_paths & supporting_paths
    assert not migration_paths & supporting_paths

    for path in migration_paths | supporting_paths:
        assert Path(path).exists()
        _load(path)


def test_catalog_index_does_not_claim_legacy_master_store_is_migrated():
    index = _load(INDEX)

    assert index["legacy_terminology_json_migrated"] is False
    assert index["status"] == "repository_index_not_legacy_master_store"
    assert "不创建伪造" in index["next_merge_rule"]["master_store_creation_policy"]


def test_stable_catalogs_cover_current_core_workstreams():
    index = _load(INDEX)
    paths = {item["path"] for item in index["stable_catalogs"]}

    assert paths == {
        "terminology/common-core.json",
        "terminology/t7-seven-methods.json",
        "terminology/d8-eight-divinations.json",
        "terminology/patterns.json",
        "terminology/military-p0.json",
        "terminology/cycles.json",
        "terminology/zitingjing.json",
        "terminology/wuyun-wuyin.json",
        "terminology/volume9-10.json",
        "terminology/relations.json",
        "terminology/ritual-timing.json",
        "terminology/ten-essences.json",
        "terminology/military-jinjing-v4.json",
        "terminology/military-jingyou-v4.json",
    }
