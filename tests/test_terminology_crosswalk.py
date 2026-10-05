import json
from collections import defaultdict
from pathlib import Path


INDEX = Path("terminology/catalog-index.json")
CROSSWALK = Path("terminology/crosswalk.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _stable_catalogs():
    index = _load(INDEX)
    return {
        item["path"]: _load(item["path"])
        for item in index["stable_catalogs"]
    }


def _entry_index(catalogs):
    result = {}
    for path, data in catalogs.items():
        for entry in data.get("entries", []):
            key = entry.get("key")
            if key:
                result[(path, key)] = entry
    return result


def test_no_exact_name_collision_across_distinct_entries():
    catalogs = _stable_catalogs()
    names = defaultdict(set)

    for path, data in catalogs.items():
        for entry in data.get("entries", []):
            key = entry.get("key") or entry.get("preferred_term")
            entry_id = (path, key)
            own_names = set(entry.get("aliases", []))
            if entry.get("preferred_term"):
                own_names.add(entry["preferred_term"])
            for name in own_names:
                names[name].add(entry_id)

    collisions = {
        name: sorted(refs)
        for name, refs in names.items()
        if len(refs) > 1
    }
    assert collisions == {}


def test_crosswalk_snapshot_matches_current_catalog_count_and_entry_count():
    catalogs = _stable_catalogs()
    crosswalk = _load(CROSSWALK)

    count = sum(len(data.get("entries", [])) for data in catalogs.values())
    snapshot = crosswalk["audit_snapshot"]

    assert snapshot["stable_catalog_count"] == len(catalogs)
    assert snapshot["entry_count"] == count
    assert snapshot["exact_cross_entry_name_collisions"] == 0
    assert snapshot["status"] == "clean_at_snapshot"


def test_crosswalk_key_references_resolve():
    catalogs = _stable_catalogs()
    entries = _entry_index(catalogs)
    crosswalk = _load(CROSSWALK)

    unresolved = []

    def walk(node):
        if isinstance(node, dict):
            catalog = node.get("catalog")
            key = node.get("key")
            if catalog is not None:
                if catalog not in catalogs:
                    unresolved.append((catalog, key, "missing_catalog"))
                elif key is not None and (catalog, key) not in entries:
                    unresolved.append((catalog, key, "missing_entry"))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(crosswalk["bridges"])
    assert unresolved == []


def test_crosswalk_locks_high_risk_forbidden_merges():
    crosswalk = _load(CROSSWALK)
    by_id = {item["id"]: item for item in crosswalk["bridges"]}

    assert "D8-08" in " ".join(by_id["CW-WUYIN"]["forbidden_merge"])
    assert "不得因都含“长短”" in " ".join(by_id["CW-LENGTH"]["forbidden_merge"])
    assert "C36" in " ".join(by_id["CW-YANGJIU-BAILIU"]["forbidden_merge"])
    assert "不得自动制造" in " ".join(by_id["CW-THREE-BASES"]["forbidden_merge"])
    assert by_id["CW-FOUR-TAIYI"]["name_policy"]["直符"] == "canonical"
    assert by_id["CW-FOUR-TAIYI"]["name_policy"]["值符"] == "explicit_legacy_alias_only"


def test_crosswalk_is_supporting_asset_not_master_store():
    crosswalk = _load(CROSSWALK)

    assert crosswalk["status"] == "supporting_crosswalk_not_master_store"
    assert crosswalk["legacy_terminology_json_migrated"] is False
    assert "不替代" in crosswalk["audit_policy"]["master_store_policy"]


def test_crosswalk_snapshot_tracks_military_runtime_coverage():
    snapshot = _load(CROSSWALK)["audit_snapshot"]

    assert snapshot["tongzong_military_source_runtime_coverage"] == "25/25"
    assert snapshot["jingyou_military_source_runtime_coverage"] == "11/11"
    assert snapshot["jingyou_military_text_pending"] == []
    assert snapshot["jingyou_military_resolved_collation"] == ["JF4M-02"]
