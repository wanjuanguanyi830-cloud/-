import json
from pathlib import Path
import pytest
from kintaiyi import eight_divinations as d8

ROOT = Path(__file__).resolve().parents[1]
RECORD = json.loads((ROOT / "rules/taiyi_v1.json").read_text(encoding="utf-8"))
CASES = json.loads((ROOT / "tests/fixtures/eight_divinations_cases.json").read_text(encoding="utf-8"))


def test_categories_variants_and_source_layers_are_complete():
    assert RECORD["schema_version"] == "2.0"
    assert [row["id"] for row in RECORD["categories"]["seven_methods"]] == [f"T7-{i:02d}" for i in range(1,8)]
    assert [row["id"] for row in RECORD["categories"]["eight_divinations"]] == [f"D8-{i:02d}" for i in range(1,9)]
    assert [row["id"] for row in RECORD["variants"]] == [f"VAR-{i:03d}" for i in range(1,17)]
    assert RECORD["source_excerpts"] and RECORD["pending"]
    assert all(row["status"] == "confirmed" for row in RECORD["variants"])
    assert RECORD["derived"]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_derived_d8_records_are_callable_and_keep_category(case):
    assert case["derived_case"] and not case["source_example"]
    fn = {"D8-01":d8.sancai,"D8-02":d8.calc_length,"D8-03":d8.wuyin_from_calc,
          "D8-04":d8.gudan_state,"D8-05":d8.attack_realm,"D8-06":d8.suenwl,
          "D8-07":d8.tui_danger,"D8-08":d8.calc_preparedness}[case["rule_id"]]
    for values in case["inputs"]:
        data = fn(*values) if isinstance(values,list) else fn(values)
        assert data["rule_id"] == case["rule_id"]
        assert data["category"] == "eight_divinations"

