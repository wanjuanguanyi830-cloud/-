"""用户指定八占测试组；算例标记derived_case，不冒充逐字古例。"""
import pytest
from kintaiyi.eight_divinations import (sancai, calc_length, wuyin_from_calc,
    gudan_state, attack_realm, suenwl, tui_danger, calc_preparedness)


@pytest.mark.parametrize("n,missing,full", [(1,["天","地"],False),(10,["地","人"],False),(16,[],True),(33,["地"],False)])
def test_sancai(n, missing, full):
    data = sancai(n)
    assert data["missing"] == missing
    assert data["sancai_full_classic"] == full
    assert data["category"] == "eight_divinations"


@pytest.mark.parametrize("n", [10,20,30,40])
def test_no_people_exact_tens(n):
    assert "人" in sancai(n)["missing"]


@pytest.mark.parametrize("n,expected", [(10,"短"),(11,"长"),(31,"长")])
def test_length_boundary(n, expected):
    assert calc_length(n)["length"] == expected


@pytest.mark.parametrize("n,tone,element,subject", [(1,"宫","土","人君"),(4,"徵","火","宗庙"),(6,"羽","水","后妃"),(8,"商","金","子孙"),(10,"角","木","疾病")])
def test_wuyin(n, tone, element, subject):
    data = wuyin_from_calc(n)
    assert (data["tone"], data["element"], data["subject"]) == (tone, element, subject)


@pytest.mark.parametrize("n,state,side,danger", [(3,"单阳","主",None),(8,"单阴","客",None),(13,"重阳","主","火厄"),(28,"重阴","客","水厄"),(10,"孤阳","主",None),(30,"孤阳","主",None),(20,"孤阴","客",None),(40,"孤阴","客",None)])
def test_gudan(n, state, side, danger):
    data = gudan_state(n)
    assert (data["state"], data["disadvantaged"], data["danger"]) == (state, side, danger)


@pytest.mark.parametrize("god,realm,verdict", [("吕申","内","内虚、宜攻外"),("大神","外","外孤、宜攻内")])
def test_fixed_attack_realm(god, realm, verdict):
    data = attack_realm(god)
    assert (data["realm"],data["verdict"]) == (realm,verdict)


@pytest.mark.parametrize("home,away,verdict", [(3,5,"主败/客胜"),(17,3,"主胜"),(17,17,"同数/无明确断语")])
def test_number_comparison(home, away, verdict):
    data = suenwl(home, away, pattern_corrections=[{"格局":"将入中"}])
    assert data["base"]["verdict"] == verdict
    assert data["pattern_corrections"] and not data["corrections_applied"]


@pytest.mark.parametrize("palace,n,state,danger", [(3,17,"重阳","厄火"),(7,28,"重阴","厄水")])
def test_yinyang(palace, n, state, danger):
    assert tui_danger(palace,n,n)["events"] == [{"side":side,"state":state,"danger":danger} for side in ("主","客")]


@pytest.mark.parametrize("palace,n", [(3,28),(7,17),(5,17)])
def test_yinyang_no_invented_other_verdict(palace,n):
    assert tui_danger(palace,n)["events"] == []


@pytest.mark.parametrize("n,missing,classic", [(7,["将军"],None),(13,["吏士"],None),(15,["兵卒"],None),(17,[],"将吏兵卒俱备")])
def test_preparedness(n,missing,classic):
    data = calc_preparedness(n)
    assert data["missing"] == missing
    assert data["classic_label"] == classic


def test_structural_all_does_not_equal_classic_full():
    assert not all(sancai(15)["components"].values())
    assert "人" in sancai(15)["missing"]
    assert not sancai(15)["sancai_full_classic"]
    assert "人" not in sancai(1)["missing"]


def test_mixed_gudan_preserves_basic_effects_without_combined_verdict():
    data = gudan_state(12)
    assert data["state"] is None and data["danger"] is None
    assert data["basic_effects"] == [{"classification":"孤阳","disadvantaged":"主"},
                                     {"classification":"单阴","disadvantaged":"客"}]
