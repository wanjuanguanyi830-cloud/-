import pytest

from kintaiyi.taiyi_epoch import (
    EPOCH_DIFFERENCE,
    epoch_context,
    five_zi_short_accumulated_year,
    five_zi_yuan_from_count,
    long_accumulated_year,
    six_ji_three_yuan_from_count,
)


def test_l0_kaiyuan_12_dual_epoch_anchors():
    long_epoch = long_accumulated_year(724)
    short_epoch = five_zi_short_accumulated_year(724)
    assert long_epoch["accumulated_year"] == 1_937_281
    assert short_epoch["five_zi_accumulated_year"] == 30_001
    assert EPOCH_DIFFERENCE == 1_907_280
    assert EPOCH_DIFFERENCE == 360 * 5_298


def test_l0_each_historical_year_moves_exactly_one_count():
    assert long_accumulated_year(725)["accumulated_year"] == 1_937_282
    assert long_accumulated_year(723)["accumulated_year"] == 1_937_280

    # 无0年：1 BCE(-1) -> 1 CE(1)只前进一年。
    bce1 = long_accumulated_year(-1)["accumulated_year"]
    ce1 = long_accumulated_year(1)["accumulated_year"]
    assert ce1 - bce1 == 1


def test_l0_year_zero_is_rejected():
    with pytest.raises(ValueError):
        long_accumulated_year(0)


def test_l0_kaiyuan_12_is_lower_yuan_third_ji():
    data = six_ji_three_yuan_from_count(1_937_281)
    assert data["remainder_360"] == 121
    assert data["ji_index_1based"] == 3
    assert data["year_in_ji"] == 1
    assert data["yuan_label"] == "下元"


@pytest.mark.parametrize(
    ("r360", "ji", "yuan", "year_in_ji"),
    [
        (1, 1, "上元", 1),
        (60, 1, "上元", 60),
        (61, 2, "中元", 1),
        (120, 2, "中元", 60),
        (121, 3, "下元", 1),
        (181, 4, "上元", 1),
        (241, 5, "中元", 1),
        (301, 6, "下元", 1),
        (360, 6, "下元", 60),
    ],
)
def test_l0_six_ji_three_yuan_boundaries(r360, ji, yuan, year_in_ji):
    data = six_ji_three_yuan_from_count(r360)
    assert data["ji_index_1based"] == ji
    assert data["yuan_label"] == yuan
    assert data["year_in_ji"] == year_in_ji


def test_l0_kaiyuan_12_five_zi_is_bingzi_yuan_ju_49():
    long_data = five_zi_yuan_from_count(1_937_281)
    short_data = five_zi_yuan_from_count(30_001)
    for data in (long_data, short_data):
        assert data["remainder_360"] == 121
        assert data["five_zi_yuan"] == "丙子"
        assert data["local_ju"] == 49


def test_l0_long_and_short_epochs_are_mod360_equivalent_for_multiple_years():
    for year in (1, 724, 2026, -1, -1000):
        data = epoch_context(year)
        assert data["equivalent_mod_360"] is True
        assert data["epoch_difference"] == 1_907_280
        assert data["epoch_difference_in_360_cycles"] == 5_298
        assert (
            data["five_zi_from_long"]["local_ju"]
            == data["five_zi_from_short"]["local_ju"]
        )


def test_l0_2026_context_is_consistent():
    data = epoch_context(2026)
    assert data["long_epoch"]["accumulated_year"] == 1_938_583
    assert data["five_zi_short_epoch"]["five_zi_accumulated_year"] == 31_303
    assert data["six_ji_three_yuan"]["remainder_360"] == 343
    assert data["six_ji_three_yuan"]["ji_index_1based"] == 6
    assert data["six_ji_three_yuan"]["yuan_label"] == "下元"
    assert data["five_zi_from_long"]["five_zi_yuan"] == "壬子"
    assert data["five_zi_from_long"]["local_ju"] == 55
