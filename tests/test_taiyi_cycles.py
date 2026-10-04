import pytest
from kintaiyi import taiyi_cycles as c


def test_three_bases_boundaries_and_source_examples():
    for fn, stay, start in ((c.ruler_base, 30, "午"), (c.minister_base, 3, "午"), (c.people_base, 1, "戌")):
        for value in range(1, 12 * stay + 2):
            data = fn(value)
            assert 1 <= data["cycle_year"] <= 12 * stay
            assert 1 <= data["year_in_palace"] <= stay
            assert data["branch"] in c.BRANCHES
        assert fn(12 * stay - 250 % (12 * stay) + 1)["branch"] == start
    # Explicit year-accumulation adapter used by the reference project (not the movement formula).
    epoch = 10153917
    assert c.ruler_base(epoch + 714)["branch"] == "午"  # 开元二年甲寅
    assert c.minister_base(epoch + 642)["branch"] == "午"  # 贞观十六壬寅
    assert c.people_base(epoch + 627)["branch"] == "未"  # 贞观元丁亥
    assert c.ruler_base(111, profile="siku")["provenance"] == "source_variant"


@pytest.mark.parametrize("n,palace,year", [(1,1,1),(45,1,45),(46,3,1),(90,3,45),(91,9,1),(135,9,45),
    (136,7,1),(180,7,45),(181,5,1),(225,5,45),(226,1,1)])
def test_five_boundaries(n, palace, year):
    data = c.five_blessings(n, offset=0)
    assert (data["palace_id"], data["year_in_palace"]) == (palace, year)


def test_five_phase_lucky_subjects_and_domains():
    assert [c.five_blessings(n, offset=0)["phase"] for n in (15,16,30,31)] == ["理天","理地","理地","理人"]
    assert c.five_blessings_lucky_calc(5)["subject"] == "民庶"
    assert c.five_blessings_lucky_calc(10)["subject"] == "士卒"
    assert c.five_blessings(1)["offset"] == 250
    assert sum(len(s) for s in c.FIVE_DOMAINS.values()) == 16
    assert set().union(*c.FIVE_DOMAINS.values()) == set("子丑艮寅卯辰巽巳午未坤申酉戌乾亥")
    assert [c.nine_palace_to_five_domain(n) for n in (1,3,9,7,2,4,6,8)] == ["乾","艮","巽","坤","中","中","中","中"]


def test_big_wander_all_boundaries_and_skyeyes():
    for i, palace in enumerate((7,8,9,1,2,3,4,6)):
        assert c.big_wander(i*36+1)["palace_id"] == palace
        assert c.big_wander(i*36+36)["year_in_palace"] == 36
    assert c.big_wander(289)["palace_id"] == 7
    assert all(c.big_wander(n)["palace_id"] != 5 for n in range(1,290))
    assert [c.big_wander_skyeyes(n)["sector"] for n in range(1,19)] == ["未","坤","坤","申","酉","戌","乾","乾","亥","子","丑","艮","寅","卯","辰","巽","巳","午"]
    assert c.big_wander(1, profile="tongzong")["offset"] == 34
    assert c.big_wander_skyeyes(1, profile="tongzong")["offset"] == 214
    assert not c.big_wander(1, profile="taojin")["computable"]


@pytest.mark.parametrize("n,palace,year", [(1,1,1),(2,1,2),(3,1,3),(4,2,1),(6,2,3),(7,3,1),(13,6,1),(24,9,3),(25,1,1)])
def test_small_wander(n, palace, year):
    data = c.small_wander(n)
    assert (data["palace_id"], data["year_in_palace"]) == (palace, year)


def test_small_historical_and_overlap_layers():
    assert (c.small_wander(10154821)["cycle_year"], c.small_wander(10154821)["palace_id"],
            c.small_wander(10154821)["phase"]) == (13,6,"治天")
    five = c.five_blessings(181, offset=0)
    effects = c.five_blessings_wander_effect(five, big=c.big_wander(37), small=c.small_wander(4))
    assert effects[0]["fortune_fraction"] == 0.5
    assert effects[0]["disaster_palace"] == 2
    assert "fortune_fraction" not in effects[1] and "disaster_palace" not in effects[1]
    for year in range(2, 226):
        meeting = c.five_blessings_base_meeting(year, c.people_base)
        assert meeting["first_meeting"] == (meeting["same_now"] and not meeting["same_previous"])
