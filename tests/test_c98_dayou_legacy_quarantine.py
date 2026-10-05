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


def test_c98_tianmu_default_deprecated_plus214_is_quarantined():
    data = bigyo_tianmu(0)
    assert data["profile"] == "tongzong"
    assert data["offset"] == 214
    assert data["canonical"] is None
    assert data["canonical_equivalent"] is False
    assert data["promotion_allowed"] is False
    assert data["quarantined"] is True
    assert "deprecated_reference" in data["reason"]


def test_c98_config_tianmu_default_is_same_quarantined_path():
    data = config.bigyo_tianmu(0)
    assert data["rule_id"] == "LEGACY-DAYOU-TIANMU-COMPAT"
    assert data["quarantined"] is True
    assert data["canonical"] is None


def test_c98_jinjing_tianmu_requires_explicit_epoch_and_remains_noncanonical():
    missing = bigyo_tianmu(0, profile="jinjing")
    assert missing["status"] == "not_computable"
    assert missing["canonical"] is None
    assert missing["quarantined"] is False

    data = bigyo_tianmu(0, profile="jinjing", epoch_offset=0)
    assert data["god"] == DAYOU_TM_PATH[0]
    assert data["step_number"] == 1
    assert data["canonical"] is None
    assert data["canonical_equivalent"] is False
    assert data["promotion_allowed"] is False
    assert data["quarantined"] is False
    assert "72→18" in data["reason"]


@pytest.mark.parametrize("func,profile", [
    (bigyo, "unknown"),
    (bigyo_tianmu, "unknown"),
])
def test_c98_unknown_profiles_are_rejected(func, profile):
    with pytest.raises(ValueError):
        func(0, profile=profile)
