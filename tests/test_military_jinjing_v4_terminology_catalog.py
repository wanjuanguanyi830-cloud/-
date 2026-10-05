import json
from pathlib import Path

from kintaiyi import jinjing_v4_military as runtime


CATALOG = Path("terminology/military-jinjing-v4.json")
P0 = Path("terminology/military-p0.json")
RULESET = Path("rules/jinjing_v4_military.json")
NCL = Path("terminology/ncl06604-legacy-reconciliation-map.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_j4m_extended_catalog_covers_exactly_04_through_12():
    data = _load(CATALOG)
    ids = [entry["rule_id"] for entry in data["entries"]]

    assert ids == [f"J4M-{n:02d}" for n in range(4, 13)]
    assert data["split_policy"]["p0_rule_ids"] == ["J4M-01", "J4M-02", "J4M-03"]
    assert data["split_policy"]["cross_source_merge"] is False


def test_j4m_extended_entries_match_authoritative_ruleset_titles_and_runtimes():
    data = _load(CATALOG)
    ruleset = _load(RULESET)
    by_id = {item["id"]: item for item in ruleset["rules"]}

    for entry in data["entries"]:
        source = by_id[entry["rule_id"]]
        assert entry["body_title"] == source["body_title"]
        assert entry["domain"] == source["domain"]
        assert entry["runtime"] == source["runtime"]
        assert entry["implementation_status"] == "implemented_source_specific"


def test_j4m_extended_runtime_attributes_resolve():
    data = _load(CATALOG)

    for entry in data["entries"]:
        ref = entry["runtime"]
        prefix = "kintaiyi.jinjing_v4_military."
        assert ref.startswith(prefix)
        attr = ref[len(prefix):]
        assert callable(getattr(runtime, attr))


def test_military_p0_exposes_machine_readable_source_rule_ids():
    data = _load(P0)
    by_key = {entry["key"]: entry for entry in data["entries"]}

    assert by_key["three_doors"]["rule_ids"] == ["J4M-01", "JF4M-01"]
    assert by_key["five_generals"]["rule_ids"] == ["J4M-02", "JF4M-02"]
    assert by_key["host_guest_relation"]["rule_ids"] == ["J4M-03", "JF4M-03"]


def test_ncl_reconciliation_entries_now_have_stable_rule_targets():
    catalog = _load(CATALOG)
    p0 = _load(P0)
    ncl = _load(NCL)

    stable = set()
    for entry in p0["entries"]:
        stable.update(entry.get("rule_ids", []))
        if entry.get("rule_id"):
            stable.add(entry["rule_id"])
    stable.update(entry["rule_id"] for entry in catalog["entries"])

    assert {entry["rule_id"] for entry in ncl["entries"]} <= stable


def test_high_risk_ncl_variants_remain_explicit_not_canonical_overwrites():
    data = _load(CATALOG)
    by_id = {entry["rule_id"]: entry for entry in data["entries"]}

    assert any("只见12/22" in note for note in by_id["J4M-05"]["boundary_notes"])
    assert any("1/2/3/4/6/7/8/9" in note for note in by_id["J4M-06"]["boundary_notes"])
    assert any("1宫" in note and "source variant" in note for note in by_id["J4M-09"]["boundary_notes"])
    assert any("主人刑" in note for note in by_id["J4M-11"]["boundary_notes"])
    assert any("西方白云" in note for note in by_id["J4M-12"]["boundary_notes"])


def test_rules_json_registers_j4m_extended_ids():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-J4M-EXTENDED"]["rule_ids"] == [f"J4M-{n:02d}" for n in range(4, 13)]
