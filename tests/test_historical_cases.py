from __future__ import annotations

import json
from pathlib import Path

import pytest

from rules.jinjing.geju import GejuContext, analyze_geju


CASE_FILE = Path(__file__).parent / "fixtures" / "historical_cases.json"
HISTORICAL_CASES = json.loads(CASE_FILE.read_text(encoding="utf-8"))["cases"]


@pytest.mark.parametrize("case", HISTORICAL_CASES, ids=lambda case: f"{case['year']}年-{case['kook']}局")
def test_historical_case_positions(case):
    detail = analyze_geju(GejuContext(**case["context"]))
    legacy_keys = set(detail["舊式"])
    for expected in case.get("expected_keys", []):
        assert expected in legacy_keys
    for prefix in case.get("expected_absent_prefixes", []):
        assert not any(key.startswith(prefix) for key in legacy_keys)

