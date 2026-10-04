import json
import pytest
from kintaiyi import four_taiyi as f


def test_twelve_coordinates_and_independent_extra_palaces():
    assert set(f.TWELVE_PALACES) == set(range(1,13))
    assert [(f.TWELVE_PALACES[i]["name"], f.TWELVE_PALACES[i]["sector"]) for i in (10,11,12)] == [("绛宫","巳"),("明堂","申"),("玉堂","寅")]
    for name in f.FOUR_ATTRIBUTES:
        data = [f.four_taiyi_position(name, n) for n in range(1,37)]
        assert len({x["palace_id"] for x in data}) == 12
        assert all("phase" not in x for x in data)
        assert [x["year_in_palace"] for x in data[:3]] == [1,2,3]
        assert f.four_taiyi_position(name, 37)["palace_id"] == data[0]["palace_id"]
    json.dumps(f.four_taiyi_positions(17))


def test_yuan_start_profiles():
    expected = {"四神": [1,9,5], "天乙": [6,2,10], "地乙": [9,5,1], "直符": [5,1,9]}
    for name, starts in expected.items():
        assert [f.four_taiyi_position(name, 1, yuan=y)["palace_id"] for y in (1,2,3)] == starts
    assert f.rotate_twelve(12, 1) == 1
    assert f.rotate_twelve(1, -1) == 12


@pytest.mark.parametrize("year,name,palace", [(622,"天乙",12),(934,"地乙",11),(907,"四神",6)])
def test_historical_year_adapter(year, name, palace):
    data = f.four_taiyi_position(name, 10153917 + year, yuan=1)
    assert data["palace_id"] == palace


def test_six_pairs_compare_only_palace12_ids():
    all_same = {name: {"palace_id": 10} for name in f.FOUR_ATTRIBUTES}
    effects = f.same_palace_effects(all_same)
    assert len(effects) == 6
    assert len({frozenset(x["pair"]) for x in effects}) == 6
    assert f.same_palace_effects({"天乙": {"palace_id": 10, "sector": "午"},
                                  "地乙": {"palace_id": 2, "sector": "午"}}) == []
    json.dumps(effects)


def test_five_domain_effects_separate_from_positions():
    positions = {"天乙": f.four_taiyi_position("天乙", 13)}  # Palace12 10/巳 belongs to 巽 domain.
    assert positions["天乙"]["palace_id"] == 10
    assert f.five_blessings_four_taiyi_effects({"domain": "巽"}, positions)[0]["effects"] == ["兵","盗"]
    assert f.five_blessings_four_taiyi_effects({"domain": "中"}, positions) == []
    assert "effects" not in positions["天乙"]


def test_partial_source_tables_never_invent_remaining_cases():
    for branch, palaces in (("辰", (5,9)), ("戌", (5,9)), ("丑", (7,3)), ("未", (7,3))):
        assert all(f.four_gods_water_special(branch, palace)["classification"] == "克贼" for palace in palaces)
    for branch in "巳午":
        assert all(f.four_gods_water_special(branch, palace)["classification"] == "战克" for palace in (2,9))
    assert f.four_gods_water_special("子", 8)["status"] == "pending"
    assert not f.four_gods_water_special(None, 8)["computable"]
    assert [f.zhifu_known_state(p)["state"] for p in (2,3,4)] == ["旺","长生","败"]
    assert f.zhifu_known_state(12)["status"] == "source_pending"
