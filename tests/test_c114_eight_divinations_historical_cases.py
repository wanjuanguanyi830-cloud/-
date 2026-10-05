import json
from pathlib import Path

import pytest

from kintaiyi import eight_divinations as d8

CASES = json.loads(
    (Path(__file__).parent / "fixtures/eight_divinations_historical_cases.json")
    .read_text(encoding="utf-8")
)


@pytest.mark.parametrize("case", CASES["cases"], ids=lambda c: c["case_id"])
def test_c114_eight_divinations_historical_cases(case):
    data = getattr(d8, case["method"])(*case["args"])
    assert data["id"] == case["rule_id"]

    for key, expected in case["expected"].items():
        assert data[key] == expected


def test_c114_fixture_keeps_historical_scope_boundaries():
    cases = {case["rule_id"]: case for case in CASES["cases"]}

    assert "不把整局军事胜负归因于单一长短规则" in cases["D8-02"]["scope_boundary"]
    assert "不把后续历史事件扩张成额外算法" in cases["D8-04"]["scope_boundary"]
    assert "16以上一律皆具" in cases["D8-08"]["scope_boundary"]

    assert d8.calc_preparedness(15)["present"] == ["将军", "吏士"]
    assert d8.calc_preparedness(15)["missing"] == ["兵卒"]
    assert d8.calc_preparedness(25)["present"] == ["将军", "吏士"]
    assert d8.calc_preparedness(35)["present"] == ["将军", "吏士"]
