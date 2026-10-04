import pytest
from kintaiyi.cycles import (wufu,wufu_gb,bigyo,bigyo_tianmu,dayou_xiong,
                             WUFU_PATH,DAYOU_PATH,DAYOU_TAOJIN_PATH,DAYOU_TM_PATH)


def test_wufu_canonical_offset_and_source_profile_isolation():
    assert wufu(0)["offset"] == 250
    assert wufu(0,profile="source_115")["offset"] == 115
    assert wufu(0)["offset"] == 250


@pytest.mark.parametrize("i,palace", list(enumerate(WUFU_PATH)))
def test_wufu_palace_cycle(i,palace):
    year = (i*45 - 250) % 225
    data = wufu(year)
    assert (data["palace"],data["year_in_palace"],data["realm"]) == (palace,1,"理天")
    assert wufu(year+225)["palace"] == palace


@pytest.mark.parametrize("year,realm", [(1,"理天"),(15,"理天"),(16,"理地"),(30,"理地"),(31,"理人"),(45,"理人")])
def test_wufu_realms(year,realm):
    assert wufu((year-1-250)%225)["realm"] == realm


@pytest.mark.parametrize("year,subject", [(1,"君王"),(2,"王侯臣宰"),(3,"后妃"),(4,"太子"),(5,"民庶"),(6,"师帅"),(7,"上将军"),(8,"中将军"),(9,"下将军"),(10,"士卒"),(36,"师帅")])
def test_number_subjects(year,subject):
    assert dayou_xiong(year) == subject
    assert wufu_gb(year) == subject


def test_wufu_46_removed():
    with pytest.raises(ValueError):
        wufu_gb(46)


@pytest.mark.parametrize("i,palace", list(enumerate(DAYOU_PATH)))
def test_dayou_sequence(i,palace):
    year = (i*36-34)%288
    data = bigyo(year)
    assert (data["palace"],data["year_in_palace"]) == (palace,1)
    assert bigyo(year+288)["palace"] == palace
    assert palace != 5


@pytest.mark.parametrize("year,realm", [(1,"治天"),(12,"治天"),(13,"治地"),(24,"治地"),(25,"治人"),(36,"治人")])
def test_dayou_realms(year,realm):
    data = bigyo((year-1-34)%288)
    assert data["realm"] == realm
    assert data["year_in_palace"] == year
    if year == 36:
        assert data["inauspicious_subject"] == "师帅"


@pytest.mark.parametrize("i,god", list(enumerate(DAYOU_TM_PATH)))
def test_all_dayou_tianmu_steps(i,god):
    data = bigyo_tianmu((i-214)%18)
    assert data["god"] == god
    assert data["step_number"] == i+1
    assert bigyo_tianmu((i-214)%18+18)["god"] == god


def test_profile_metadata_and_pending_epoch():
    assert DAYOU_TAOJIN_PATH == (7,6,4,3,2,1,9,8)
    assert bigyo(0,profile="taojin")["status"] == "not_computable"
    assert bigyo(0,profile="taojin",epoch_offset=0)["palace"] == 7
    assert bigyo_tianmu(0)["profile_metadata"]["outer_cycle"] == 180
    assert bigyo_tianmu(0,profile="jinjing")["step_number"] == 1
    assert bigyo_tianmu(0,profile="jinjing",epoch_offset=0)["profile_metadata"]["yuan"] == 72
