import pytest

from kintaiyi.taiyi_taisui import (
    CYCLE_60,
    FIVE_YUAN,
    taisui_from_accumulated_year,
    taisui_from_ju,
    year_entry_from_accumulated_year,
)


def test_g1_sexagenary_cycle_boundaries():
    first = taisui_from_accumulated_year(1)
    assert first["taisui_ganzhi"] == "甲子"
    assert first["remainder_60"] == 1

    last = taisui_from_accumulated_year(60)
    assert last["taisui_ganzhi"] == "癸亥"
    assert last["remainder_60"] == 60

    repeat = taisui_from_accumulated_year(61)
    assert repeat["taisui_ganzhi"] == "甲子"


def test_g1_360_zero_remainder_is_cycle_end_not_cycle_start():
    data = taisui_from_accumulated_year(360)
    assert data["remainder_360"] == 360
    assert data["remainder_60"] == 60
    assert data["taisui_ganzhi"] == "癸亥"


def test_g1_kaiyuan_anchor_1937281_is_jiazi():
    data = year_entry_from_accumulated_year(1_937_281)
    assert data["remainder_360"] == 121
    assert data["remainder_60"] == 1
    assert data["taisui_ganzhi"] == "甲子"
    assert data["five_yuan"] == "丙子"
    assert data["local_ju"] == 49


@pytest.mark.parametrize(
    ("n", "yuan", "ju"),
    [
        (1, "甲子", 1),
        (72, "甲子", 72),
        (73, "丙子", 1),
        (144, "丙子", 72),
        (145, "戊子", 1),
        (217, "庚子", 1),
        (289, "壬子", 1),
        (360, "壬子", 72),
        (361, "甲子", 1),
    ],
)
def test_five_yuan_72_boundaries(n, yuan, ju):
    data = year_entry_from_accumulated_year(n)
    assert data["five_yuan"] == yuan
    assert data["local_ju"] == ju


def test_72ju_helper_branch_matches_each_local_ju_branch():
    for ju in range(1, 73):
        assert taisui_from_ju(ju)["taisui_branch"] == CYCLE_60[(ju - 1) % 12][1]


def test_five_yuan_names_are_source_order():
    assert FIVE_YUAN == ("甲子", "丙子", "戊子", "庚子", "壬子")
