import json
from pathlib import Path

import pytest
from kintaiyi import seven_methods as t7

CASES = json.loads((Path(__file__).parent / "fixtures/seven_methods_classics.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_seven_source_examples(case):
    assert case["source_example"] and not case["derived_case"]
    data = getattr(t7, case["method"])(*case.get("args", []), **case.get("kwargs", {}))
    expected = case["expected"]
    assert data["category"] == "seven_methods"
    if case["method"] == "lijin":
        assert data["chain"] == expected["chain"]
    elif case["method"] == "lion":
        for key in ("position", "state"):
            assert data["dashen"][key] == expected[key]
        assert data["verdict"] == expected["verdict"]
        for key in ("sector", "year", "offset"):
            assert data["timing"][key] == expected[key]
        assert data["timing"]["year_number"] == 18
    elif case["method"] == "cloud":
        for side in ("home", "away"):
            assert data[side]["dashen"]["position"] == expected[side + "_position"]
            assert data[side]["dashen"]["state"] == expected[side + "_state"]
    elif case["method"] == "tiger":
        for key in ("position", "state"):
            assert data["dashen"][key] == expected[key]
        assert data["verdict"] == expected["verdict"]
    else:
        for key in ("position", "element"):
            assert data["environment"][key] == expected[key]
        for side in ("home", "away"):
            if side + "_state" in expected:
                assert data["generals"][side + "_general"]["state"] == expected[side + "_state"]
        if "enemy_verdict" in expected:
            assert data["enemy_verdict"] == expected["enemy_verdict"]


def test_derived_returnarmy_missing_arrival_never_uses_away_general():
    data = t7.returnarmy(9)
    assert data["status"] == "not_computable"
    assert "enemy_arrival_taiyi" in data["missing"]
    assert "environment" not in data


def test_derived_four_generals_model_b_and_environment_controls_general():
    data = t7.leigong(6, 8, 2, 9, 6)
    assert data["model"] == "B"
    assert [g["state"] for g in data["generals"].values()] == ["旺", "死", "相", "休"]
    assert data["missing"] == []


def test_derived_dragon_severe_control_overrides_good_qi():
    data = t7.dragon(9, 6, 3, 2, 8)
    assert data["generals"]["home_general"]["state"] == "相"
    assert data["generals"]["home_general"]["has_qi"]
    assert data["conflicts"]["home"]["severe"]
    assert data["generals"]["home_general"]["verdict"] == "出战必死"


def test_derived_explicit_xing_table_and_vassal_control():
    assert t7.general_conflict(3, 6, xing_pairs={(6, 3)})["severe"]
    assert t7.general_conflict(3, 6)["pending"]
    assert t7.general_conflict(3, 6, 9)["events"] == [{"relation": "克", "target": "home_vassal"}]


def test_derived_fire_stage_priority_cloud_and_tiger():
    assert t7.cloud(4, 8)["home"]["verdict"] == "不可触犯"
    assert t7.cloud(8, 4)["home"]["verdict"] == "强"
    # 古法冠带/临官词义，直接给十六宫anchor核对气势解释。
    assert t7._cloud_general("丑")["verdict"] == "善战/精锐"
    assert t7._cloud_general("寅")["verdict"] == "善战/精锐"
    assert t7.tiger(6)["dashen"]["stage"] == "胎"
    assert t7.tiger(6)["verdict"] == "敌营不久破/可攻"
    # 辰 anchor → 未：五态休而火阶段衰，须判破营。
    assert t7.tiger("辰")["dashen"]["state"] == "休"
    assert t7.tiger("辰")["verdict"] == "敌营不久破/可攻"


def test_derived_lion_ordinary_branch_remains_candidate():
    data = t7.lion("甲子")
    assert data["timing"]["candidate_branch"] == "卯"
    assert data["timing"]["year"] is None
    assert data["pending"]


def test_derived_missing_second_cloud_general_is_structured():
    assert t7.cloud(7)["missing"] == ["away_general"]
