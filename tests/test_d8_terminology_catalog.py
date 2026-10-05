import json
from pathlib import Path


CATALOG = Path("terminology/d8-eight-divinations.json")


def _load():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_d8_terminology_catalog_covers_all_eight_rules():
    data = _load()
    entries = data["entries"]
    method_entries = [entry for entry in entries if entry.get("rule_id")]

    assert [entry["rule_id"] for entry in method_entries] == [
        "D8-01", "D8-02", "D8-03", "D8-04",
        "D8-05", "D8-06", "D8-07", "D8-08",
    ]
    assert len({entry["key"] for entry in entries}) == len(entries)


def test_d8_terminology_catalog_contains_requested_core_terms():
    data = _load()
    by_term = {entry["preferred_term"]: entry for entry in data["entries"]}

    assert "三才" in by_term
    assert "五音" in by_term
    assert "孤单" in by_term
    assert "阴阳厄会" in by_term

    assert by_term["三才"]["classic_tags"]["杜塞"] == [5, 15, 25, 35]
    assert by_term["五音"]["tone_kind"]["正音"] == [1, 3, 5, 7, 9]
    assert by_term["孤单"]["classes"]["重阳"]["danger"] == "火厄"
    assert by_term["阴阳厄会"]["palaces"]["中五"] == "不参与"


def test_d8_terminology_keeps_wuyin_and_number_subject_separate():
    data = _load()
    by_rule = {
        entry["rule_id"]: entry
        for entry in data["entries"]
        if entry.get("rule_id")
    }

    assert by_rule["D8-03"]["preferred_term"] == "五音"
    assert by_rule["D8-08"]["preferred_term"] == "数有所主"
    assert by_rule["D8-03"]["runtime"].endswith("wuyin_from_calc")
    assert by_rule["D8-08"]["runtime"].endswith("calc_preparedness")
