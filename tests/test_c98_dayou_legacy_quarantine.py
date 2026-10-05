import pytest

import config
from kintaiyi.cycles import (
    DAYOU_PATH,
    DAYOU_TM_PATH,
    bigyo,
    bigyo_tianmu,
)


def test_c98_bigyo_default_keeps_numeric_compatibility_but_is_not_canonical():
    data = bigyo(0)
    assert data["profile"] == "jinjing_tongzong"
    assert data["offset"] == 34
    assert data["palace"] == DAYOU_PATH[0]
    assert data["canonical"] is None
    assert data["canonical_equivalent"] is False
    assert data["promotion_allowed"] is False
    assert data["quarantined"] is True
    assert "混为单一profile" in data["reason"]


def test_c98_config_bigyo_exposes_same_quarantined_compatibility_path():
    data = config.bigyo(0)
    assert data["rule_id"] == "LEGACY-DAYOU-COMPAT"
    assert data["quarantined"] is True
    assert data["canonical"] is None


def test_c98_taojin_requires_epoch_unless_explicit_compatibility_trial():
    missing = bigyo(0, profile="taojin")
    assert missing["status"] == "not_computable"
    assert missing["canonical"] is None
    assert missing["canonical_equivalent"] is False

    trial = bigyo(0, profile="taojin", epoch_offset=0)
    assert trial["palace"] == 7
    assert trial["canonical"] is None
    assert trial["promotion_allowed"] is False
    assert trial["quarantined"] is False
    assert "兼容试算" in trial["reason"]


def test_c98_tianmu_default_is_superseded_by_c104_tongzong_delegate():
    data = bigyo_tianmu(0)
    assert data["profile"] == "tongzong"
    assert data["offset"] == 214
    assert data["rule_id"] == "C106-DAYOU-TIANMU-TONGZONG"
    assert data["canonical"] == "taiyi-c106-dayou-tianmu-source-profiles-v1"
    assert data["canonical_equivalent"] is True
    assert data["promotion_allowed"] is True
    assert data["quarantined"] is False
    assert data["canonical_delegate"]["profile_key"] == "tongzong"


def test_c98_config_tianmu_default_is_c104_tongzong_delegate():
    data = config.bigyo_tianmu(0)
    assert data["rule_id"] == "C106-DAYOU-TIANMU-TONGZONG"
    assert data["quarantined"] is False
    assert data["canonical_delegate"]["surplus"] == 214


def test_c98_jinjing_tianmu_now_delegates_to_c104_without_custom_offset():
    data = bigyo_tianmu(0, profile="jinjing")
    assert data["god"] == DAYOU_TM_PATH[0]
    assert data["step_number"] == 1
    assert data["rule_id"] == "C106-DAYOU-TIANMU-JINJING"
    assert data["canonical_equivalent"] is True
    assert data["promotion_allowed"] is True
    assert data["quarantined"] is False
    assert data["profile_metadata"]["yuan"] == 72


def test_c98_non_source_tianmu_offset_remains_legacy_custom_trial():
    data = bigyo_tianmu(0, profile="jinjing", epoch_offset=1)
    assert data["rule_id"] == "LEGACY-DAYOU-TIANMU-CUSTOM-OFFSET"
    assert data["canonical"] is None
    assert data["canonical_equivalent"] is False
    assert data["promotion_allowed"] is False
    assert data["quarantined"] is False
    assert "不覆盖source-specific runtime" in data["reason"]


@pytest.mark.parametrize("func,profile", [
    (bigyo, "unknown"),
    (bigyo_tianmu, "unknown"),
])
def test_c98_unknown_profiles_are_rejected(func, profile):
    with pytest.raises(ValueError):
        func(0, profile=profile)



@pytest.mark.parametrize(
    "profile,rule_id,offset",
    [
        ("jinjing", "C107-DAYOU-JINJING", 0),
        ("tongzong", "C107-DAYOU-TONGZONG", 34),
    ],
)
def test_c98_config_bigyo_explicit_profiles_delegate_c107(profile, rule_id, offset):
    data = config.bigyo(0, profile=profile)
    assert data["rule_id"] == rule_id
    assert data["offset"] == offset
    assert data["canonical_equivalent"] is True
    assert data["promotion_allowed"] is True
    assert data["quarantined"] is False
