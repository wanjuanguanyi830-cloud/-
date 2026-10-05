import json
from pathlib import Path


CATALOG = Path("terminology/military-jingyou-v4.json")
RULESET = Path("rules/jingyou_fuying_v4_military.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_jf4m_catalog_covers_all_eleven_source_rules():
    data = _load(CATALOG)
    ids = [entry["rule_id"] for entry in data["entries"]]

    assert ids == [f"JF4M-{n:02d}" for n in range(1, 12)]
    assert data["implementation_policy"]["source_record_only"] is True
    assert data["implementation_policy"]["runtime_substitution_allowed"] is False
    assert data["implementation_policy"]["cross_source_merge"] is False


def test_jf4m_entries_match_authoritative_ruleset():
    data = _load(CATALOG)
    ruleset = _load(RULESET)
    by_id = {item["id"]: item for item in ruleset["rules"]}

    for entry in data["entries"]:
        source = by_id[entry["rule_id"]]
        assert entry["source_title"] == source["source_title"]
        assert entry["domain"] == source["domain"]
        assert entry["canonical_summary"] == source["canonical_summary"]
        assert entry["parallel_jinjing_rule"] == source["parallel_jinjing_rule"]
        assert entry["implementation_status"] == "source_record_only"
        assert entry["runtime"] is None


def test_jf4m_tail_order_is_not_forced_to_match_jinjing():
    data = _load(CATALOG)
    note = data["parallel_order_note"]

    assert note["reordered_tail"] == {
        "JF4M-10": "J4M-11",
        "JF4M-11": "J4M-10",
    }
    assert note["no_direct_jf_counterpart_for"] == ["J4M-12"]


def test_jf4m_high_risk_source_differences_remain_explicit():
    data = _load(CATALOG)
    by_id = {entry["rule_id"]: entry for entry in data["entries"]}

    assert by_id["JF4M-06"]["canonical_data"]["direction_table"]["3"] == "东北"
    assert by_id["JF4M-09"]["canonical_data"]["inner_palaces_help_host"] == [1, 8, 3, 4]
    assert any("主人败" in text for text in by_id["JF4M-10"]["notable_readings"])
    assert "奇兵必从大杀之地" in by_id["JF4M-11"]["canonical_summary"]


def test_rules_json_registers_jf4m_source_records():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-JF4M-SOURCE-RECORDS"]["rule_ids"] == [
        f"JF4M-{n:02d}" for n in range(1, 12)
    ]
    assert by_id["R-JF4M-SOURCE-RECORDS"]["runtime"] is None
