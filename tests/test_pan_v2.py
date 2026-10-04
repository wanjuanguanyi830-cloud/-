import json
from collections import Counter

import pytest
from kintaiyi import Taiyi
from kintaiyi.kintaiyi import collect_core_snapshot
from kintaiyi.pan_v2 import build_pan_v2_from_snapshot, validate_pan_v2


def snapshot(**updates):
    return {"accumulated_year": 10154821, "year_accumulated_year": 10154821,
            "ji_style": 0, "taiyi_acumyear": 0, "taiyi_palace": 7,
            "wenchang_sector": "辰", "shiji_sector": "戌", "dingmu_sector": "巳",
            "home_cal": 15, "away_cal": 26, "fixed_cal": 40,
            "home_general": 7, "home_assistant": 8, "away_general": 3, "away_assistant": 4,
            "day_taiyi_palace": 6, "four_taiyi_yuan": 1, **updates}


def test_canonical_builder_complete_shape_and_json():
    v2 = build_pan_v2_from_snapshot(snapshot())
    assert set(v2) == {"schema_version","meta","calendar","board","cycles","analysis","modern","source_variants","compat"}
    assert v2["schema_version"] == "2.0" and v2["modern"] == {}
    assert validate_pan_v2(v2)["valid"]
    assert json.loads(json.dumps(v2, ensure_ascii=False)) == v2
    board = v2["board"]
    assert board["taiyi"]["palace_id"] == 7
    assert (board["eyes"]["skyeyes"]["element"], board["eyes"]["skyeyes"]["nine_palace_element"]) == ("土","木")
    assert (board["eyes"]["shiji"]["element"], board["eyes"]["shiji"]["nine_palace_element"]) == ("土","金")
    assert board["calculations"]["home"]["missing_components"] == ["人"]
    assert board["calculations"]["fixed"]["parity"] == "even"
    assert board["calculations"]["fixed"]["last_digit"] == 0
    assert (board["generals"]["home_general"]["intrinsic_element"], board["generals"]["home_general"]["palace_element"]) == ("金","土")
    assert (board["generals"]["home_assistant"]["intrinsic_element"], board["generals"]["home_assistant"]["palace_element"]) == ("水","水")
    assert set(v2["cycles"]["three_bases"]) == {"ruler","minister","people"}
    assert set(v2["cycles"]["four_taiyi"]) == {"天乙","地乙","直符","四神"}
    assert v2["cycles"]["small_wander"]["palace_id"] == 6
    assert set(v2["analysis"]["eight_divinations"]) == {f"D8-{i:02}" for i in range(1,9)}
    assert set(v2["analysis"]["seven_methods"]) == {f"T7-{i:02}" for i in range(1,8)}


def test_scenarios_and_day_taiyi_are_explicit():
    core = snapshot(ji_style=1)
    core.pop("day_taiyi_palace")
    v2 = build_pan_v2_from_snapshot(core)
    methods = v2["analysis"]["seven_methods"]
    for key in ("T7-01","T7-02","T7-04","T7-05","T7-06","T7-07"):
        assert not methods[key]["computable"]
        assert methods[key]["reason"] and methods[key]["missing_inputs"]
    assert methods["T7-03"]["computable"]
    core["day_taiyi_palace"] = 6
    scenario = {"enemy_start_year_branch": "甲戌", "enemy_camp_day_taiyi_palace": 3,
                "enemy_first_arrival_taiyi_palace": 2}
    full = Taiyi(core).pan(1,0, scenario=scenario)["v2"]
    assert all(m["computable"] for m in full["analysis"]["seven_methods"].values())
    assert full["analysis"]["seven_methods"]["T7-05"]["environment"]["position"] == "子"
    assert full["board"]["taiyi"]["palace_id"] == 7


def test_legacy_projection_same_values_and_types_without_mutating_input():
    legacy = {"太乙落宮": 2, "主算": [99,"旧错值"], "大游": {"宫": 5}, "八門分佈": {1:"開"}}
    core = snapshot()
    pan = Taiyi(core, legacy_snapshot=legacy).pan(0,0)
    assert legacy["主算"][0] == 99 and core["home_cal"] == 15
    assert {"太乙落宮","主算","客算","文昌","大游","小游"} <= set(pan)
    v2 = pan["v2"]
    assert pan["太乙落宮"] == v2["board"]["taiyi"]["palace_id"]
    assert pan["主算"][0] == v2["board"]["calculations"]["home"]["value"]
    assert pan["客算"][0] == v2["board"]["calculations"]["away"]["value"]
    assert pan["文昌"][0] == v2["board"]["eyes"]["skyeyes"]["sector"]
    assert isinstance(pan["大游"], dict)
    assert pan["大游"]["宫"] == v2["cycles"]["big_wander"]["palace_id"]
    assert pan["小游"] == v2["cycles"]["small_wander"]["palace_id"]
    assert pan["君基"] == v2["cycles"]["three_bases"]["ruler"]["branch"]
    assert pan["天乙"] == v2["cycles"]["four_taiyi"]["天乙"]["palace_id"]


def test_center_does_not_create_sector_and_cloud_is_partial():
    v2 = Taiyi(snapshot(taiyi_palace=5, home_general=5)).pan(0,0)["v2"]
    assert v2["board"]["taiyi"]["sector"] is None
    general = v2["board"]["generals"]["home_general"]
    assert general["representative_sector"] is None and general["palace_element"] == "土"
    cloud = v2["analysis"]["seven_methods"]["T7-03"]
    assert not cloud["computable"] and cloud["decision"]["status"] == "不完整"
    assert cloud["decision"]["winner"] is None


def test_annual_cycle_does_not_borrow_monthly_accumulation():
    core = snapshot(ji_style=1, accumulated_year=888, year_accumulated_year=111)
    v2 = build_pan_v2_from_snapshot(core)
    big = v2["cycles"]["big_wander"]
    assert big["accumulated_year"] == big["year_accumulated_year"] == 111
    assert big["selected_accumulated_year"] == 888
    core.pop("year_accumulated_year")
    missing = build_pan_v2_from_snapshot(core)["cycles"]["big_wander"]
    assert not missing["computable"] and missing["missing_inputs"] == ["year_accumulated_year"]


def test_partial_snapshot_returns_structured_unavailable_sections():
    v2 = Taiyi({}).pan(0,0)["v2"]
    assert not v2["board"]["taiyi"]["computable"]
    assert not v2["board"]["calculations"]["home"]["computable"]
    assert not v2["cycles"]["five_blessings"]["computable"]
    assert all(not m["computable"] for m in v2["analysis"]["seven_methods"].values())
    assert all(not d["computable"] for d in v2["analysis"]["eight_divinations"].values())
    json.dumps(v2)


def test_engine_collector_calls_each_primitive_once_and_uses_actual_day_style():
    calls = Counter()
    class Engine:
        def __getattr__(self, name):
            def method(style, profile):
                calls[(name, style)] += 1
                if name == "accnum":
                    return 10154821 if style == 0 else 999
                if name in ("skyeyes","sf","se"):
                    return "辰"
                return 3 if name == "ty" and style == 2 else 7
            return method
    core = collect_core_snapshot(Engine(), 1, 0)
    assert max(calls.values()) == 1
    assert core["accumulated_year"] == 999 and core["year_accumulated_year"] == 10154821
    assert core["day_taiyi_palace"] == 3 and core["taiyi_palace"] == 7


def test_modern_projection_is_added_only_when_enabled():
    pan = Taiyi(snapshot()).pan(0,0, True)
    assert pan["v2"]["schema_version"] == "2.0"
    assert pan["運籌博弈分析"]["derived_modern_feature"] is True
    assert pan["v2"]["modern"]["game_theory"] == pan["運籌博弈分析"]
    json.dumps(pan)


def test_invalid_scenario_rejected_instead_of_silently_ignored():
    with pytest.raises(ValueError):
        Taiyi(snapshot()).pan(0,0, scenario={"current_date_as_enemy_arrival": 7})
