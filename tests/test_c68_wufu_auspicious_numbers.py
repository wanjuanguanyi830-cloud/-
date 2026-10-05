import pytest

from kintaiyi.wufu_auspicious_numbers import (
    C67_BOUNDARY,
    NUMBER_GROUPS,
    NUMBER_TO_BENEFICIARY,
    VARIANTS,
    c68_catalog,
    wufu_auspicious_beneficiary,
)


def test_c68_direct_number_groups_cover_exactly_1_to_45_once():
    numbers = [
        number
        for group in NUMBER_GROUPS.values()
        for number in group
    ]
    assert sorted(numbers) == list(range(1, 46))
    assert len(numbers) == len(set(numbers)) == 45
    assert set(NUMBER_TO_BENEFICIARY) == set(range(1, 46))


@pytest.mark.parametrize(
    "beneficiary,numbers",
    [
        ("君王", (1, 11, 21, 31, 41)),
        ("公侯", (2, 12, 22, 32, 42)),
        ("后妃", (3, 13, 23, 33, 43)),
        ("太子", (4, 14, 24, 34, 44)),
        ("民", (5, 15, 25, 35, 45)),
        ("师帅", (6, 16, 26, 36)),
        ("上将军", (7, 17, 27, 37)),
        ("中将军", (8, 18, 28, 38)),
        ("下将军", (9, 19, 29, 39)),
        ("士卒", (10, 20, 30, 40)),
    ],
)
def test_c68_each_source_list_is_locked(beneficiary, numbers):
    assert NUMBER_GROUPS[beneficiary] == numbers
    for number in numbers:
        data = wufu_auspicious_beneficiary(number)
        assert data["beneficiary"] == beneficiary
        assert data["group_numbers"] == list(numbers)


def test_c68_45_is_people_not_an_invented_next_group():
    data = wufu_auspicious_beneficiary(45)
    assert data["beneficiary"] == "民"
    assert data["group_numbers"] == [5, 15, 25, 35, 45]


def test_c68_does_not_invent_46_to_50_from_digit_pattern():
    for value in (46, 47, 48, 49, 50):
        with pytest.raises(ValueError):
            wufu_auspicious_beneficiary(value)


@pytest.mark.parametrize("bad", [0, -1, 46])
def test_c68_rejects_out_of_range_remainder(bad):
    with pytest.raises(ValueError):
        wufu_auspicious_beneficiary(bad)


def test_c68_rejects_bool_remainder():
    with pytest.raises(TypeError):
        wufu_auspicious_beneficiary(True)


def test_c68_is_not_a_hidden_c67_position_calculator():
    data = wufu_auspicious_beneficiary(36)
    assert data["c67_boundary"] == C67_BOUNDARY
    assert data["c67_boundary"]["auto_position_lookup_used"] is False
    assert data["c67_boundary"]["auto_remainder_from_accumulated_count_used"] is False
    assert data["c67_boundary"]["accepted_input"] == "explicit_remainder_1_to_45"


def test_c68_keeps_225_vs_250_cycle_variant_outside_runtime_mapping():
    assert VARIANTS["later_250_cycle"]["cycle_years"] == 250
    assert VARIANTS["later_250_cycle"]["status"] == "source_variant_not_applied"
    assert VARIANTS["later_250_cycle"]["canonical_selected"] is None

    data = wufu_auspicious_beneficiary(1)
    assert data["beneficiary"] == "君王"


def test_c68_beneficiary_wording_variants_are_preserved():
    assert VARIANTS["beneficiary_2"]["ngj"] == "公侯"
    assert VARIANTS["beneficiary_2"]["cadal"] == "王侯臣宰"
    assert VARIANTS["beneficiary_2"]["runtime_label"] == "公侯"
    assert VARIANTS["beneficiary_5"]["runtime_label"] == "民"


def test_c68_catalog_exposes_explicit_table_not_formula_only():
    data = c68_catalog()
    assert data["rule_id"] == "C68-WUFU-AUSPICIOUS-NUMBER"
    assert len(data["number_to_beneficiary"]) == 45
    assert data["number_groups"]["士卒"] == (10, 20, 30, 40)
    assert data["c67_boundary"]["auto_position_lookup_used"] is False
