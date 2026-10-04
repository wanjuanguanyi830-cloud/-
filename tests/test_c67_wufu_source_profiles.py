import pytest

from kintaiyi.wufu_source_profiles import (
    PROFILES,
    UNSELECTED_VARIANTS,
    WUFU_PALACES,
    c67_catalog,
    wufu_position,
)


def test_c67_requires_explicit_source_profile():
    with pytest.raises(TypeError):
        wufu_position(1)
    with pytest.raises(ValueError, match="tongzong/jinjing"):
        wufu_position(1, source_profile="mixed")


def test_c67_stable_five_palace_core_is_shared():
    assert [row["position"] for row in WUFU_PALACES] == ["乾", "艮", "巽", "坤", "中"]
    assert [row["name"] for row in WUFU_PALACES] == ["黄秘", "黄始", "黄室", "黄廷", "玄室"]
    assert PROFILES["tongzong"]["years_per_palace"] == 45
    assert PROFILES["jinjing"]["years_per_palace"] == 45


def test_c67_tongzong_keeps_115_surplus_and_2250_225_layers():
    p = PROFILES["tongzong"]
    assert p["surplus"] == 115
    assert p["big_cycle"] == 2250
    assert p["small_cycle"] == 225
    assert p["rule_id"] == "C67-WUFU-TONGZONG"


def test_c67_jinjing_does_not_inherit_tongzong_surplus():
    p = PROFILES["jinjing"]
    assert p["surplus"] == 0
    assert p["big_cycle"] == 225
    assert p["small_cycle"] is None
    assert p["rule_id"] == "C67-WUFU-JINJING"


def test_c67_tongzong_position_boundaries():
    # 111 + 115 = 226；小周225余1，乾宫第1年。
    first = wufu_position(111, source_profile="tongzong")
    assert first["effective_count"] == 1
    assert first["position"] == "乾"
    assert first["palace_name"] == "黄秘"
    assert first["year_in_palace"] == 1

    end = wufu_position(155, source_profile="tongzong")
    assert end["effective_count"] == 45
    assert end["position"] == "乾"
    assert end["year_in_palace"] == 45

    next_palace = wufu_position(156, source_profile="tongzong")
    assert next_palace["effective_count"] == 46
    assert next_palace["position"] == "艮"
    assert next_palace["year_in_palace"] == 1


def test_c67_tongzong_big_cycle_zero_is_preserved():
    # 2135 + 115 = 2250。
    data = wufu_position(2135, source_profile="tongzong")
    assert data["big_cycle_remainder"] == 0
    assert data["big_cycle_count"] == 2250
    assert data["small_cycle_remainder"] == 0
    assert data["small_cycle_count"] == 225
    assert data["position"] == "中"
    assert data["year_in_palace"] == 45


def test_c67_jinjing_simple_225_cycle():
    assert wufu_position(1, source_profile="jinjing")["position"] == "乾"
    assert wufu_position(45, source_profile="jinjing")["position"] == "乾"
    assert wufu_position(46, source_profile="jinjing")["position"] == "艮"
    assert wufu_position(90, source_profile="jinjing")["position"] == "艮"
    assert wufu_position(91, source_profile="jinjing")["position"] == "巽"
    end = wufu_position(225, source_profile="jinjing")
    assert end["position"] == "中"
    assert end["year_in_palace"] == 45
    assert wufu_position(226, source_profile="jinjing")["position"] == "乾"


def test_c67_jinjing_historical_arithmetic_check_13331_is_gen_year11():
    data = wufu_position(13331, source_profile="jinjing")
    assert data["big_cycle_remainder"] == 56
    assert data["position"] == "艮"
    assert data["palace_name"] == "黄始"
    assert data["year_in_palace"] == 11


def test_c67_same_input_can_differ_by_source_profile_without_forced_merge():
    tongzong = wufu_position(1, source_profile="tongzong")
    jinjing = wufu_position(1, source_profile="jinjing")
    assert tongzong["adjusted_count"] == 116
    assert jinjing["adjusted_count"] == 1
    assert tongzong["source_profile"] != jinjing["source_profile"]


def test_c67_later_taibai_variant_remains_unselected():
    variant = UNSELECTED_VARIANTS["taibai_bingbei_later"]
    assert variant["implemented"] is False
    assert variant["canonical_selected"] is None
    assert any("二百五十" in text for text in variant["observed"])


@pytest.mark.parametrize("profile", ["tongzong", "jinjing"])
def test_c67_rejects_nonpositive_and_bool_count(profile):
    with pytest.raises(ValueError):
        wufu_position(0, source_profile=profile)
    with pytest.raises(TypeError):
        wufu_position(True, source_profile=profile)


@pytest.mark.parametrize("profile", ["tongzong", "jinjing"])
def test_c67_position_never_auto_applies_omen_or_auspicious_number_layer(profile):
    data = wufu_position(100, source_profile=profile)
    assert data["same_palace_omens_applied"] is False
    assert data["auspicious_number_layer_applied"] is False
    assert data["deferred_layer"]["auto_same_palace_inference"] is False


def test_c67_catalog_has_no_default_profile():
    data = c67_catalog()
    assert data["default_profile"] is None
    assert data["source_profile_required"] is True
    assert set(data["profiles"]) == {"tongzong", "jinjing"}
