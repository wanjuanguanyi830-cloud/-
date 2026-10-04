import pytest

from kintaiyi import eight_divinations as d


@pytest.mark.parametrize("n,components", [(5, (False, True, False)), (10, (True, False, False)),
    (15, (True, True, False)), (25, (True, True, False)), (35, (True, True, False)),
    (16, (True, True, True)), (26, (True, True, True)), (36, (True, True, True)), (40, (True, False, False))])
def test_component_structure_and_preparedness(n, components):
    assert tuple(d.calc_components(n).values()) == components
    assert d.calc_preparedness(n)["components_all"] == all(components)
    if n in (5, 15, 25, 35):
        assert "杜塞" in d.sancai_analysis(n)["classic_tags"]
        assert "无人" not in d.sancai_analysis(n)["classic_tags"]
        assert "人" in d.sancai_analysis(n)["missing_components"]


def test_classic_sets_all_40_numbers():
    data = {n: d.sancai_analysis(n)["classic_tags"] for n in range(1, 41)}
    assert {n for n, tags in data.items() if "无天" in tags} == set(range(1, 10))
    assert {n for n, tags in data.items() if "无地" in tags} == {1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34}
    assert {n for n, tags in data.items() if "无人" in tags} == {10, 20, 30, 40}
    assert {n for n, tags in data.items() if "三才俱足" in tags} == {16, 17, 18, 19, 26, 27, 28, 29, 36, 37, 38, 39}


@pytest.mark.parametrize("n,tone,kind,subject", [(23, "徵", "正音", "宗庙"), (15, "羽", "正音", "后妃"),
    (16, "羽", "比音", "后妃"), (39, "角", "正音", "疾病"), (40, "角", "比音", "疾病")])
def test_wuyin_pairs(n, tone, kind, subject):
    data = d.wuyin_from_calc(n)
    assert (data["tone"], data["tone_kind"], data["subject"]) == (tone, kind, subject)
    assert data["judges_fortune"] is False


def test_explicit_gudan_sets_and_independent_adversity():
    expected = {"单阳": {1, 3, 7, 9}, "单阴": {2, 4, 6, 8}, "孤阳": {10, 30},
                "孤阴": {20, 40}, "重阳": {11, 13, 17, 19, 31, 33, 37, 39}, "重阴": {22, 24, 26, 28}}
    for label, numbers in expected.items():
        assert {n for n in range(1, 41) if d.gudan_analysis(n)["state"] == label} == numbers
    assert d.gudan_analysis(33)["state"] == "重阳"
    assert d.yinyang_adversity(7, 33)["events"] == []
    assert d.gudan_analysis(26)["state"] == "重阴"
    assert d.yinyang_adversity(7, 26)["events"][0]["state"] == "重阴"
    assert d.calc_amount_victory(3, 15)["winner"] == "away"
    assert d.calc_amount_victory(15, 15)["winner"] is None


def test_fixed_realms_and_independent_entry_points():
    for sector in "乾亥子丑艮寅卯辰":
        assert d.neiwai_attack(sector)["attack"] == "外"
    for sector in "巽巳午未坤申酉戌":
        assert d.neiwai_attack(sector)["attack"] == "内"
    assert d.calc_length(10)["variants"][0]["status"] == "source_ambiguous"
    data = d.analyze_eight_divinations(7, "辰", 15, 26)
    assert set(data) == {f"D8-{i:02}" for i in range(1, 9)}
    assert data["D8-03"]["home"]["subject"] == "后妃"
    assert data["D8-08"]["home"]["missing"] == ["兵卒"]
