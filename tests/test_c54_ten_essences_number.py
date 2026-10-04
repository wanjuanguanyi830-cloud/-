import pytest

from kintaiyi.ten_essences_number import (
    LEGACY_AUDIT,
    OMEN_BOUNDARY,
    c54_catalog,
    taiyi_number,
)


@pytest.mark.parametrize(
    "count,expected",
    [
        (1, 1),
        (71, 71),
        (72, 72),
        (73, 1),
        (144, 72),
        (359, 71),
        (360, 72),
        (361, 1),
        (720, 72),
    ],
)
def test_c54_taiyi_number_72_cycle_boundaries(count, expected):
    data = taiyi_number(count)
    assert data["taiyi_number"] == expected
    assert 1 <= data["taiyi_number"] <= 72


def test_c54_360_cycle_boundary_is_preserved_not_zero():
    data = taiyi_number(360)
    assert data["big_cycle_remainder"] == 0
    assert data["big_cycle_count"] == 360
    assert data["small_cycle_remainder"] == 0
    assert data["taiyi_number"] == 72


def test_c54_72_boundary_inside_360_is_preserved_not_zero():
    data = taiyi_number(72)
    assert data["big_cycle_count"] == 72
    assert data["small_cycle_remainder"] == 0
    assert data["taiyi_number"] == 72


def test_c54_does_not_apply_weather_omens_for_special_numbers():
    for count in (10, 30, 40, 50):
        data = taiyi_number(count)
        assert data["taiyi_number"] == count
        assert data["cloud_omen_applied"] is False
        assert data["omen_boundary"]["number_only_in_c54"] is True
        assert data["omen_boundary"]["weather_omens_applied"] is False


def test_c54_legacy_numeric_core_can_match_without_promoting_wrapper():
    assert LEGACY_AUDIT["numeric_core_equivalent"] is True
    assert LEGACY_AUDIT["wrapper_canonical_equivalent"] is False
    assert "天气断语" in LEGACY_AUDIT["reason"]


def test_c54_rejects_nonpositive_or_bool_count():
    with pytest.raises(ValueError):
        taiyi_number(0)
    with pytest.raises(TypeError):
        taiyi_number(True)


def test_c54_catalog_keeps_number_and_omen_layers_separate():
    data = c54_catalog()
    assert data["rule_id"] == "C54-TAIYI-NUMBER"
    assert data["big_cycle"] == 360
    assert data["small_cycle"] == 72
    assert data["omen_boundary"] == OMEN_BOUNDARY
    assert data["omen_boundary"]["weather_omens_applied"] is False
