import pytest
from kintaiyi.cycles import (wufu,wufu_gb,bigyo,bigyo_tianmu,dayou_xiong,
                             WUFU_PATH,DAYOU_PATH,DAYOU_TAOJIN_PATH,DAYOU_TM_PATH)
from kintaiyi.wufu_source_profiles import wufu_position


def test_wufu_legacy_project_250_is_quarantined_not_canonical():
    data = wufu(0)
    assert data["offset"] == 250
    assert data["canonical"] is None
    assert data["canonical_equivalent"] is False
    assert data["quarantined"] is True
    assert data["promotion_allowed"] is False
    assert data["replacement_rule_ids"] == [
        "C67-WUFU-TONGZONG", "C67-WUFU-JINJING"
    ]


@pytest.mark.parametrize("year", [0, 1, 44, 45, 224, 225, 13330])
def test_wufu_source115_zero_based_adapter_delegates_to_c67_tongzong(year):
    legacy = wufu(year, profile="source_115")
    direct = wufu_position(year + 1, source_profile="tongzong")
    palace_by_position = {"乾": 1, "艮": 3, "巽": 9, "坤": 7, "中": 5}
    assert legacy["rule_id"] == "C67-WUFU-TONGZONG"
    assert legacy["canonical_equivalent"] is True
    assert legacy["quarantined"] is False
    assert legacy["offset"] == 115
    assert legacy["palace"] == palace_by_position[direct["position"]]
    assert legacy["year_in_palace"] == direct["year_in_palace"]


@pytest.mark.parametrize("year", [0, 44, 45, 224, 225, 13330])
def test_wufu_jinjing_zero_based_adapter_delegates_to_c67_jinjing(year):
    legacy = wufu(year, profile="jinjing")
    direct = wufu_position(year + 1, source_profile="jinjing")
    palace_by_position = {"乾": 1, "艮": 3, "巽": 9, "坤": 7, "中": 5}
    assert legacy["rule_id"] == "C67-WUFU-JINJING"
    assert legacy["offset"] == 0
    assert legacy["palace"] == palace_by_position[direct["position"]]
    assert legacy["year_in_palace"] == direct["year_in_palace"]


@pytest.mark.parametrize("i,palace", list(enumerate(WUFU_PATH)))
def test_wufu_legacy_project_cycle_is_preserved_only_for_compatibility(i,palace):
    year = (i*45 - 250) % 225
    data = wufu(year)
    assert data["quarantined"] is True
    assert (data["palace"],data["year_in_palace"],data["realm"]) == (palace,1,"理天")
    assert wufu(year+225)["palace"] == palace


@pytest.mark.parametrize("year,realm", [(1,"理天"),(15,"理天"),(16,"理地"),(30,"理地"),(31,"理人"),(45,"理人")])
def test_wufu_legacy_realms_are_marked_compatibility_derived(year,realm):
    data = wufu((year-1-250)%225)
    assert data["realm"] == realm
    assert data["realm_status"] == "legacy_compatibility_derived"


@pytest.mark.parametrize("year,subject", [(1,"君王"),(2,"公侯"),(3,"后妃"),(4,"太子"),(5,"民"),(6,"师帅"),(7,"上将军"),(8,"中将军"),(9,"下将军"),(10,"士卒"),(36,"师帅")])
def test_wufu_gb_delegates_to_c68_labels(year,subject):
    assert wufu_gb(year) == subject


@pytest.mark.parametrize("year,subject", [(1,"君王"),(2,"王侯臣宰"),(5,"民庶"),(6,"师帅"),(10,"士卒"),(36,"师帅")])
def test_dayou_number_subject_legacy_labels_remain_separate(year,subject):
    assert dayou_xiong(year) == subject


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
    tongzong = bigyo_tianmu(0)
    assert tongzong["profile_metadata"]["outer_cycle"] == 180
    assert tongzong["rule_id"] == "C106-DAYOU-TIANMU-TONGZONG"
    assert tongzong["canonical_equivalent"] is True
    jinjing = bigyo_tianmu(0, profile="jinjing")
    assert jinjing["rule_id"] == "C106-DAYOU-TIANMU-JINJING"
    assert jinjing["canonical_equivalent"] is True
    assert jinjing["profile_metadata"]["yuan"] == 72
    assert bigyo_tianmu(0,profile="jinjing",epoch_offset=0)["profile_metadata"]["yuan"] == 72
