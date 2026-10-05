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


def test_derived_explicit_xing_pairs_are_external_extension_only():
    general = t7.general_conflict(3, 6, 9, xing_pairs={(6, 3)})
    assert {
        "relation": "刑",
        "target": "home_general",
        "source_role": "explicit_external_extension",
    } in general["external_xing_events"]
    assert all(item["relation"] == "克" for item in general["events"])
    assert general["external_extension_severe"] is True
    assert general["xing_evidence_status"] == (
        "explicit_external_extension_not_canonical"
    )
    assert general["pending"] == []

    vassal = t7.general_conflict(3, 6, 9, xing_pairs={(6, 9)})
    assert {
        "relation": "刑",
        "target": "home_vassal",
        "source_role": "explicit_external_extension",
    } in vassal["external_xing_events"]
    assert {"relation": "克", "target": "home_vassal"} in vassal["events"]
    assert vassal["severe"] is True


def test_derived_external_xing_does_not_change_dragon_canonical_verdict():
    base = t7.dragon(9, home_general=3, away_general=6)
    extended = t7.dragon(
        9, home_general=3, away_general=6, xing_pairs={(6, 3)}
    )

    assert extended["conflicts"]["home"]["external_extension_severe"] is True
    assert base["conflicts"]["home"]["severe"] == extended["conflicts"]["home"]["severe"]
    assert (
        base["generals"]["home_general"]["verdict"]
        == extended["generals"]["home_general"]["verdict"]
    )


def test_derived_t7_06_has_no_independent_xing_operator_pending():
    data = t7.general_conflict(3, 6)
    assert data["xing_evidence_status"] == "no_independent_xing_operator_from_source"
    assert data["pending"] == []
    assert data["canonical_relation"] == "五行克"
    assert data["external_xing_events"] == []
    assert "四库本" in data["source_interpretation"]
    assert data["collation_record"] == "sources/t7-06-white-dragon-xing-collation.md"

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


def test_derived_lion_ordinary_full_year_is_resolved():
    data = t7.lion("甲子")
    assert data["timing"]["mode"] == "direct_break_year"
    assert data["timing"]["source_marker"] == "卯"
    assert data["timing"]["break_year_branch"] == "卯"
    assert data["timing"]["candidate_branch"] == "卯"
    assert data["timing"]["offset"] == 3
    assert data["timing"]["year_number"] == 4
    assert data["timing"]["year"] == "丁卯"
    assert data["timing"]["year_resolution"] == "full_ganzhi"
    assert data["pending"] == []


def test_derived_lion_branch_only_input_keeps_stem_unknown_without_research_pending():
    data = t7.lion("子")
    assert data["timing"]["mode"] == "direct_break_year"
    assert data["timing"]["break_year_branch"] == "卯"
    assert data["timing"]["year"] is None
    assert data["timing"]["year_resolution"] == "branch_only_input_no_stem"
    assert data["pending"] == []


def test_lion_all_sexagenary_years_follow_plus3_or_plus17_source_split():
    cycle = [
        t7.STEMS[i % 10] + t7.BRANCHES[i % 12]
        for i in range(60)
    ]
    cardinal = {"子", "卯", "午", "酉"}

    for index, start in enumerate(cycle):
        data = t7.lion(start)
        branch = start[1]
        expected_offset = 3 if branch in cardinal else 17
        expected_year = cycle[(index + expected_offset) % 60]

        assert data["timing"]["offset"] == expected_offset
        assert data["timing"]["year_number"] == expected_offset + 1
        assert data["timing"]["year"] == expected_year
        assert data["timing"]["break_year_branch"] == expected_year[1]
        assert data["pending"] == []

        if branch in cardinal:
            assert data["timing"]["mode"] == "direct_break_year"
            assert data["timing"]["sector"] is None
        else:
            assert data["timing"]["mode"] == "corner_18_year"
            assert data["timing"]["sector"] in {"艮", "巽", "坤", "乾"}


def test_derived_missing_second_cloud_general_is_structured():
    assert t7.cloud(7)["missing"] == ["away_general"]
