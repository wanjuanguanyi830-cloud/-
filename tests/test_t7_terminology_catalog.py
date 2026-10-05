import json
from pathlib import Path


CATALOG = Path("terminology/t7-seven-methods.json")


def _load():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_t7_terminology_catalog_covers_all_seven_methods():
    data = _load()
    method_entries = [entry for entry in data["entries"] if entry.get("rule_id")]

    assert [entry["rule_id"] for entry in method_entries] == [
        "T7-01", "T7-02", "T7-03", "T7-04", "T7-05", "T7-06", "T7-07"
    ]
    assert [entry["preferred_term"] for entry in method_entries] == [
        "临津问道", "狮子反掷", "白云卷空", "猛虎相拒",
        "雷公入水", "白龙得云", "回军无言"
    ]


def test_t7_event_input_boundaries_are_explicit():
    data = _load()
    by_rule = {
        entry["rule_id"]: entry
        for entry in data["entries"]
        if entry.get("rule_id")
    }

    assert by_rule["T7-01"]["required_inputs"] == ["enemy_start_year_branch"]
    assert by_rule["T7-04"]["required_inputs"] == ["enemy_camp_day_taiyi_palace"]
    assert "enemy_first_arrival_taiyi_palace" in by_rule["T7-07"]["required_inputs"]


def test_t7_qi_models_are_not_merged():
    data = _load()
    by_rule = {
        entry["rule_id"]: entry
        for entry in data["entries"]
        if entry.get("rule_id")
    }

    assert by_rule["T7-02"]["qi_model"] == "A"
    assert by_rule["T7-03"]["qi_model"] == "A"
    assert by_rule["T7-04"]["qi_model"] == "A"
    assert by_rule["T7-05"]["qi_model"] == "B"
    assert by_rule["T7-06"]["qi_model"] == "B"
    assert by_rule["T7-07"]["qi_model"] == "B"


def test_return_army_keeps_legacy_alias_without_input_substitution():
    data = _load()
    entry = next(e for e in data["entries"] if e.get("rule_id") == "T7-07")

    assert "回车无言" in entry["aliases"]
    assert any("不得代替" in note for note in entry["boundary_notes"])
