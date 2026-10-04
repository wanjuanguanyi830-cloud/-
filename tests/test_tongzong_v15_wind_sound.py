import pytest

from kintaiyi.tongzong_v15_wind_sound import (
    C25_VERSION,
    WIND_SOUND_CLASSES,
    c25_catalog,
    observe_general_from_wind_sound,
)


def test_v15_10_requires_explicit_wind_sound_observation():
    data = observe_general_from_wind_sound(None)
    assert data["canonical"] == C25_VERSION
    assert data["source_rule_id"] == "V15-10"
    assert data["computable"] is False
    assert data["missing_inputs"] == ["wind_sound_class"]
    assert data["v15_09_direction_tone_substitute_allowed"] is False
    assert "不得由风向五音" in data["policy"]


@pytest.mark.parametrize(
    "sound,tone,element,character",
    [
        ("宫风", "宫", "土", "宽和、有信"),
        ("商风", "商", "金", "威猛、好杀"),
        ("角风", "角", "木", "仁恕、不易欺诈"),
        ("徵风", "徵", "火", "猛烈、难争锋"),
        ("羽风", "羽", "水", "贪暴、多奸诈"),
    ],
)
def test_v15_10_five_wind_sound_classes(sound, tone, element, character):
    data = observe_general_from_wind_sound(sound)
    assert data["computable"] is True
    assert data["wind_sound_class"] == sound
    assert data["tone"] == tone
    assert data["element"] == element
    assert data["general_character"] == character
    assert data["winner"] is None


def test_v15_10_sound_profiles_are_descriptive_not_directional():
    for sound, item in WIND_SOUND_CLASSES.items():
        data = observe_general_from_wind_sound(sound)
        assert "wind_direction_branch" not in data
        assert "wind_palace" not in data
        assert data["sound_profile"] == item["sound_profile"]


def test_v15_10_does_not_auto_create_military_winner():
    data = observe_general_from_wind_sound("商风")
    assert data["winner"] is None
    assert "不自动推成军事胜负" in data["policy"]


def test_invalid_wind_sound_class_rejected():
    with pytest.raises(ValueError):
        observe_general_from_wind_sound("东北风")


def test_non_string_wind_sound_class_rejected():
    with pytest.raises(TypeError):
        observe_general_from_wind_sound(3)


def test_c25_catalog_separates_wind_sound_from_wind_direction():
    data = c25_catalog()
    assert data["implemented"] == ["V15-10"]
    assert data["external_observation"] == "wind_sound_class"
    assert data["direction_rule_separate"] == "V15-09"
    assert data["policy"] == "风声与风向分层。"
