import json
import pytest
from kintaiyi import seven_methods as s


def test_linjing_chain_and_lion_classics():
    assert s.linjin_wendao("子")["chain"] == ["子", "卯", "午", "酉", "子"]
    data = s.lion_reverse_throw("甲戌")
    assert (data["dashen"]["position"], data["dashen"]["state"], data["timing"]["sector"],
            data["timing"]["year_number"], data["timing"]["year"]) == ("丑", "休", "艮", 18, "辛卯")
    for branch, landing, god in (("丑", "辰", "太阳"), ("未", "戌", "阴主")):
        data = s.lion_reverse_throw(branch)
        assert (data["dashen"]["position"], data["dashen"]["element"], data["dashen"]["state"]) == (landing, "土", "休")
        assert data["dashen"]["landing"]["god"] == god


def test_cloud_and_tiger_canonical_examples():
    data = s.white_cloud(7, 3)
    assert (data["home"]["dashen"]["state"], data["home"]["strength"]) == ("囚", "弱")
    assert (data["away"]["dashen"]["state"], data["away"]["strength"]) == ("相", "强")
    assert data["decision"]["winner"] == "away"
    data = s.white_cloud(5, 3)
    assert not data["computable"] and not data["home"]["computable"]
    assert data["away"]["computable"]
    assert data["comparison"] == {"status": "不完整", "winner": None}
    data = s.fierce_tiger(3)
    assert (data["dashen"]["position"], data["dashen"]["state"], data["decision"]["can_attack"]) == ("巽", "相", False)
    # 囚 does not become canonical attack permission.
    assert s.fierce_tiger(7)["decision"]["can_attack"] is None


def test_thunder_dragon_and_return_examples():
    data = s.thunder_in_water(6, 8, 2, 9, 6)
    assert data["computable"]
    assert data["environment"]["position"] == "子"
    assert [g["state"] for g in data["generals"].values()] == ["旺", "死", "相", "休"]
    assert [g["death_risk"] for g in data["generals"].values()] == [False, True, False, False]
    assert data["generals"]["home_general"]["intrinsic_element"] == "金"
    assert data["generals"]["home_general"]["palace_element"] == "水"
    data = s.white_dragon(9, 6, 8, 3, 9)
    assert data["environment"]["position"] == "坤"
    assert [data["generals"][k]["state"] for k in ("home_general", "away_general")] == ["相", "旺"]
    assert all(data["generals"][k]["deployment_suitable"] for k in ("home_general", "away_general"))
    assert data["analysis"]["direct_conflict"]["home"]["pending"]
    data = s.return_army(2, 6, 9)
    assert data["environment"]["position"] == "酉"
    assert data["generals"]["away_general"]["state"] == "死"
    assert data["decision"]["enemy_has_ambush"] is False
    assert data["decision"]["enemy_self_break"] is True
    assert data["decision"]["can_attack"] is True


def test_direct_conflict_is_separate_from_deployment_qi():
    data = s.white_dragon(9, 6, 3, 2, 8)
    assert data["generals"]["home_general"]["deployment_suitable"] is True
    assert data["generals"]["home_general"]["verdict"] == "宜出军/下营/屯军"
    assert data["analysis"]["direct_conflict"]["home"]["death_risk"] is True


def test_all_methods_structured_and_events_never_substituted():
    data = s.analyze_seven_methods(home_general=7, home_assistant=8, away_general=3, away_assistant=4)
    assert set(data) == {f"T7-{i:02}" for i in range(1, 8)}
    required = {"id", "name", "computable", "missing_inputs", "reason", "inputs", "analysis", "decision", "variants", "provenance"}
    for method in data.values():
        assert required <= set(method)
        json.dumps(method, ensure_ascii=False)
    for key in ("T7-01", "T7-02", "T7-04", "T7-05", "T7-06", "T7-07"):
        assert not data[key]["computable"] and data[key]["missing_inputs"] and data[key]["reason"]
    assert data["T7-03"]["computable"]
    full = s.analyze_seven_methods(home_general=7, home_assistant=8, away_general=3, away_assistant=4,
        day_taiyi_palace=6, scenario={"enemy_start_year_branch": "子", "enemy_camp_day_taiyi_palace": 3,
                                    "enemy_first_arrival_taiyi_palace": 2})
    assert all(m["computable"] for m in full.values())
    assert not s.return_army(None, 7, 3)["computable"]
    with pytest.warns(DeprecationWarning):
        assert not s.returnarmy(9)["computable"]
