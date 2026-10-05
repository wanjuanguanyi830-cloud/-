import pytest

from kintaiyi.taiyi_generals import (
    assistant_general_palace,
    generals_from_calc,
    host_guest_generals,
)


@pytest.mark.parametrize(
    ("calc_value", "big", "assistant"),
    [
        (1, 1, 3),
        (10, 1, 3),
        (20, 2, 6),
        (24, 4, 2),
        (30, 3, 9),
        (32, 2, 6),
        (40, 4, 2),
    ],
)
def test_g7_general_formula(calc_value, big, assistant):
    data = generals_from_calc(calc_value)
    assert data["blocked"] is False
    assert data["big_general_palace"] == big
    assert data["assistant_general_palace"] == assistant


@pytest.mark.parametrize("calc_value", [5, 15, 25, 35])
def test_g7_blocked_calcs_do_not_generate_fake_center_generals(calc_value):
    data = generals_from_calc(calc_value)
    assert data["blocked"] is True
    assert data["nominal_center"] == 5
    assert data["big_general_palace"] is None
    assert data["assistant_general_palace"] is None
    assert data["five_generals_released"] is False


def test_g7_assistant_general_threefold_mapping():
    assert {i: assistant_general_palace(i) for i in range(1, 10)} == {
        1: 3,
        2: 6,
        3: 9,
        4: 2,
        5: 5,
        6: 8,
        7: 1,
        8: 4,
        9: 7,
    }


def test_g7_host_guest_blockage_is_independent():
    data = host_guest_generals(25, 30)
    assert data["host"]["blocked"] is True
    assert data["guest"]["blocked"] is False
    assert data["guest"]["big_general_palace"] == 3
    assert data["guest"]["assistant_general_palace"] == 9
