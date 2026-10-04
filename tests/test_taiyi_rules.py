import pytest
import config
from kintaiyi.taiyi_rules import (SIXTEEN, SIXTEEN_GOD_WX, PALACE_POINT, FIRE_STAGES,
    dashen_from_lushen, dashen_qi, qi_state, calc_components)


@pytest.mark.parametrize("anchor,landing", list(zip(tuple("子丑寅卯辰巳午未申酉戌亥"),tuple("卯辰巳午未申酉戌亥子丑寅"))))
def test_all_twelve_branch_mappings(anchor,landing):
    assert dashen_from_lushen(anchor) == landing


@pytest.mark.parametrize("palace,landing", [(1,"艮"),(2,"酉"),(3,"巽"),(4,"午"),(6,"子"),(7,"乾"),(8,"卯"),(9,"坤")])
def test_all_palace_mappings(palace,landing):
    assert dashen_from_lushen(palace) == landing


def test_corrected_elements_and_aliases():
    assert [SIXTEEN_GOD_WX[g] for g in ("和德","大炅","大武")] == ["土","木","土"]
    assert dashen_from_lushen("太炅") == dashen_from_lushen("大炅")
    assert dashen_from_lushen("太神") == dashen_from_lushen("大神")
    assert FIRE_STAGES["午"] == "帝旺"
    for palace in (1,3,7,9):
        assert dashen_qi(palace)["stage"] is None


@pytest.mark.parametrize("environment,state", [("火","旺"),("木","相"),("水","死"),("金","囚"),("土","休")])
def test_fire_qi(environment,state):
    assert qi_state("火",environment) == state


@pytest.mark.parametrize("invalid", [True,1.5,"17",0,41])
def test_invalid_calcs(invalid):
    with pytest.raises((TypeError,ValueError)):
        calc_components(invalid)


def test_center_cannot_be_forced_to_sixteen_ring():
    with pytest.raises(ValueError):
        dashen_from_lushen(5)


def test_compatibility_delegates_to_canonical():
    assert config.lijin("甲子")["chain"] == ["子","卯","午","酉","子"]
    assert config.gudan(13) == config.gudan_zhanlue(13)
    assert config._calc_jianbei(11)["length"]["length"] == "长"
    assert config.junshi_zhanlue(17)["數有所主"]["主"]["rule_id"] == "D8-08"
    assert config.returnarmy(9)["status"] == "not_computable"
