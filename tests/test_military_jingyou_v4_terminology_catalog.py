import importlib
import json
from pathlib import Path

from kintaiyi.jingyou_fuying_v4_military import jf4m_runtime_catalog


CATALOG = Path("terminology/military-jingyou-v4.json")
RULESET = Path("rules/jingyou_fuying_v4_military.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _resolve(ref):
    module_name, attr = ref.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), attr)


def test_jf4m_catalog_covers_all_eleven_source_rules():
    data = _load(CATALOG)
    ids = [entry["rule_id"] for entry in data["entries"]]

    assert ids == [f"JF4M-{n:02d}" for n in range(1, 12)]
    assert data["implementation_policy"]["source_record_only"] is False
    assert data["implementation_policy"]["runtime_substitution_allowed"] is False
    assert data["implementation_policy"]["cross_source_merge"] is False
    assert data["implementation_policy"]["implemented_rule_ids"] == ids


def test_jf4m_entries_match_authoritative_ruleset_and_have_independent_runtime():
    data = _load(CATALOG)
    ruleset = _load(RULESET)
    by_id = {item["id"]: item for item in ruleset["rules"]}

    for entry in data["entries"]:
        source = by_id[entry["rule_id"]]
        assert entry["source_title"] == source["source_title"]
        assert entry["domain"] == source["domain"]
        assert entry["canonical_summary"] == source["canonical_summary"]
        assert entry["parallel_jinjing_rule"] == source["parallel_jinjing_rule"]
        assert entry["implementation_status"] == "implemented_source_specific"
        assert entry["runtime"].startswith("kintaiyi.jingyou_fuying_v4_military.")
        assert callable(_resolve(entry["runtime"]))


def test_jf4m_runtime_catalog_covers_exact_eleven_rules():
    data = jf4m_runtime_catalog()
    assert data["implemented"] == [f"JF4M-{n:02d}" for n in range(1, 12)]
    assert data["cross_source_merge"] is False
    assert data["source_limited"] is True
    assert data["pending_textual_uncertainty"] == {}
    assert data["resolved_collation"]["JF4M-02"]["normalized_semantics"] == "四将无同宫之关"


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
    assert by_id["JF4M-02"]["textual_uncertainty"] == []
    assert by_id["JF4M-02"]["canonical_data"]["normalized_semantics"] == "四将无同宫之关"


def test_rules_json_registers_jf4m_runtime_coverage():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}
    record = by_id["R-JF4M-SOURCE-RECORDS"]

    assert record["rule_ids"] == [f"JF4M-{n:02d}" for n in range(1, 12)]
    assert record["implemented_rule_ids"] == [f"JF4M-{n:02d}" for n in range(1, 12)]
    assert record["runtime"] is None
    assert record["runtime_catalog"] == (
        "kintaiyi.jingyou_fuying_v4_military.jf4m_runtime_catalog"
    )


def test_jf4m_resolved_transcription_data_is_machine_readable():
    data = _load(CATALOG)
    by_id = {entry["rule_id"]: entry for entry in data["entries"]}

    assert by_id["JF4M-07"]["canonical_data"]["terrain_table"]["后高前低"]["formation"] == "锐阵"
    assert by_id["JF4M-07"]["textual_uncertainty"] == []
    assert by_id["JF4M-08"]["canonical_data"]["terrain_rule_count"] == 6
    assert "太岁/太阴/月建击主客阵" in by_id["JF4M-10"]["canonical_data"]["event_families"]


def test_jf4m02_source_form_is_preserved_while_semantics_are_normalized():
    data = _load(CATALOG)
    by_id = {entry["rule_id"]: entry for entry in data["entries"]}
    item = by_id["JF4M-02"]

    assert item["canonical_data"]["source_form"] == "大小将不相开"
    assert item["canonical_data"]["normalized_reading"] == "主客大小将无相关"
    assert item["canonical_data"]["normalized_semantics"] == "四将无同宫之关"
    assert item["canonical_data"]["center_5_excluded"] is True
    assert item["textual_uncertainty"] == []
