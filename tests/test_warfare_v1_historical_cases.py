from __future__ import annotations

import json
from pathlib import Path

import pytest

from rules.common.taiyi_space import (
    FIRE_TWELVE_STAGES,
    PALACE_RING as SHARED_PALACE_RING,
    SIXTEEN_RING as SHARED_SIXTEEN_RING,
    dashen_from_lushen,
    fire_stage,
    qi_state,
)
from rules.jinjing.geju import PALACE_RING as JINJING_PALACE_RING
from rules.jinjing.geju import SIXTEEN_RING as JINJING_SIXTEEN_RING
from rules.warfare_v1 import (
    attack_realm,
    calc_components,
    calc_length,
    compare_calcs,
    fierce_tiger,
    gudan_state,
    linjin_ask_way,
    lion_reversal,
    return_army,
    three_talent,
    troop_readiness,
    thunder_god_water,
    white_cloud_roll,
    white_dragon_cloud,
    wuyin_from_calc,
    yin_yang_disaster,
)

FIXTURE = Path(__file__).parent / "fixtures" / "warfare_v1_historical_cases.json"
CASES = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]


def _evaluate(case: dict) -> dict:
    values = case["inputs"]
    rule = case["rule_id"]
    if rule == "T7-01":
        return linjin_ask_way(**values)
    if rule == "T7-02":
        return lion_reversal(**values)
    if rule == "T7-03":
        return white_cloud_roll(**values)
    if rule == "T7-04":
        return fierce_tiger(**values)
    if rule == "T7-05":
        return thunder_god_water(**values)
    if rule == "T7-06":
        return white_dragon_cloud(**values)
    if rule == "T7-07":
        return return_army(**values)
    if rule == "D8-01":
        return three_talent(**values)
    if rule == "D8-02":
        n = values["n"]
        return {"算": n, "长短": calc_length(n)}
    if rule == "D8-03":
        return wuyin_from_calc(**values)
    if rule == "D8-04":
        return gudan_state(**values)
    if rule == "D8-05":
        return attack_realm(**values)
    if rule == "D8-06":
        return compare_calcs(**values)
    if rule == "D8-07":
        return yin_yang_disaster(**values)
    if rule == "D8-08":
        return troop_readiness(**values)
    raise AssertionError(f"unknown rule id: {rule}")


def _assert_subset(actual, expected, path="expected"):
    if isinstance(expected, dict):
        assert isinstance(actual, dict), path
        for key, value in expected.items():
            assert key in actual, f"{path}.{key} missing"
            _assert_subset(actual[key], value, f"{path}.{key}")
    else:
        assert actual == expected, path


@pytest.mark.parametrize("case", CASES, ids=lambda item: item["case_id"])
def test_historical_and_structural_cases(case):
    _assert_subset(_evaluate(case), case["expected"])


def test_fixture_marks_incomplete_historical_citations_instead_of_inventing_them():
    historical = [case for case in CASES if case["case_kind"] == "historical_case"]
    assert historical
    assert all(case["source"]["citation_status"] == "locator-incomplete" for case in historical)
    assert all(case["source"]["quotation"] is None for case in historical)


def test_shared_geometry_keeps_existing_jinjing_exports_unchanged():
    assert SHARED_SIXTEEN_RING == JINJING_SIXTEEN_RING
    assert SHARED_PALACE_RING == JINJING_PALACE_RING
    assert dashen_from_lushen("子") == "卯"
    assert dashen_from_lushen(3) == "巽"


def test_five_phase_direction_and_fire_stages_are_distinct_outputs():
    assert qi_state("火", "土") == "休"
    assert qi_state("火", "木") == "相"
    assert qi_state("火", "金") == "囚"
    assert fire_stage("午") == "帝旺"
    assert fire_stage("未") == "衰"
    assert fire_stage("巽") is None
    assert tuple(FIRE_TWELVE_STAGES) == tuple("寅卯辰巳午未申酉戌亥子丑")


def test_shared_ten_five_one_split_preserves_classical_category_separately():
    assert calc_components(33) == {"有十": True, "有五": False, "有一": True}
    assert three_talent(16)["典型古法三才足数"] is True
    assert three_talent(15)["天"] and three_talent(15)["地"] and three_talent(15)["人"]
    assert three_talent(15)["典型古法三才足数"] is False


def test_unknown_outcomes_and_missing_time_remain_unresolved():
    assert compare_calcs(17, 17)["古法明文断语"] is None
    assert return_army(None)["可计算"] is False
    assert white_dragon_cloud(9, 6, 3)["刑克"]["刑条件"] is None

