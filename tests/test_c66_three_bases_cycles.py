import pytest

from kintaiyi.three_bases_cycles import (
    BANG_SURPLUS,
    DEFERRED_LAYER,
    THREE_BASES,
    c66_catalog,
    chenji_position,
    junji_position,
    minji_position,
    three_base_position,
)


def test_c66_common_surplus_is_250():
    assert BANG_SURPLUS == 250
    for func in (junji_position, chenji_position, minji_position):
        assert func(1)["surplus"] == 250


def test_c66_direct_cycle_constants():
    assert THREE_BASES["君基"]["big_cycle"] == 3600
    assert THREE_BASES["君基"]["small_cycle"] == 360
    assert THREE_BASES["君基"]["years_per_state"] == 30
    assert THREE_BASES["君基"]["start_branch"] == "午"

    assert THREE_BASES["臣基"]["big_cycle"] == 360
    assert THREE_BASES["臣基"]["small_cycle"] == 36
    assert THREE_BASES["臣基"]["years_per_state"] == 3
    assert THREE_BASES["臣基"]["start_branch"] == "午"

    assert THREE_BASES["民基"]["big_cycle"] == 360
    assert THREE_BASES["民基"]["small_cycle"] == 12
    assert THREE_BASES["民基"]["years_per_state"] == 1
    assert THREE_BASES["民基"]["start_branch"] == "戌"


def test_c66_junji_source_arithmetic_remainder_200_means_zi_year20():
    # 310 + 邦盈差250 = 560；小周360余200。
    data = junji_position(310)
    assert data["adjusted_count"] == 560
    assert data["small_cycle_remainder"] == 200
    assert data["small_cycle_count"] == 200
    assert data["branch"] == "子"
    assert data["year_in_state"] == 20
    assert data["state_number"] == 7


def test_c66_chenji_source_arithmetic_remainder_2_means_wu_year2():
    # 4 + 250 = 254；小周36余2。
    data = chenji_position(4)
    assert data["small_cycle_remainder"] == 2
    assert data["branch"] == "午"
    assert data["year_in_state"] == 2
    assert data["state_number"] == 1


def test_c66_minji_one_year_each_state_and_xu_start():
    # 3 + 250 = 253；12余1，回到戌邦第一年。
    data = minji_position(3)
    assert data["small_cycle_remainder"] == 1
    assert data["branch"] == "戌"
    assert data["year_in_state"] == 1

    assert [minji_position(3 + i)["branch"] for i in range(12)] == [
        "戌", "亥", "子", "丑", "寅", "卯",
        "辰", "巳", "午", "未", "申", "酉",
    ]


def test_c66_junji_each_state_lasts_30_years():
    # 111 + 250 = 361 -> small360余1，午邦第一年。
    assert junji_position(111)["branch"] == "午"
    assert junji_position(111)["year_in_state"] == 1
    assert junji_position(140)["branch"] == "午"
    assert junji_position(140)["year_in_state"] == 30
    assert junji_position(141)["branch"] == "未"
    assert junji_position(141)["year_in_state"] == 1


def test_c66_chenji_each_state_lasts_3_years():
    # 111 + 250 = 361 -> 小周36余1。
    assert chenji_position(111)["branch"] == "午"
    assert chenji_position(113)["branch"] == "午"
    assert chenji_position(113)["year_in_state"] == 3
    assert chenji_position(114)["branch"] == "未"
    assert chenji_position(114)["year_in_state"] == 1


@pytest.mark.parametrize(
    "func,big,small",
    [
        (junji_position, 3600, 360),
        (chenji_position, 360, 36),
        (minji_position, 360, 12),
    ],
)
def test_c66_zero_remainder_is_cycle_end_not_zero(func, big, small):
    # 使 adjusted_count 恰为对应大周。
    count = big - BANG_SURPLUS
    data = func(count)
    assert data["big_cycle_remainder"] == 0
    assert data["big_cycle_count"] == big
    assert data["small_cycle_remainder"] == 0
    assert data["small_cycle_count"] == small
    assert data["state_number"] == 12
    assert data["year_in_state"] == data["years_per_state"]


@pytest.mark.parametrize("func", [junji_position, chenji_position, minji_position])
def test_c66_rejects_nonpositive_and_bool_counts(func):
    with pytest.raises(ValueError):
        func(0)
    with pytest.raises(TypeError):
        func(True)


def test_c66_rejects_unknown_base_name():
    with pytest.raises(ValueError, match="君基/臣基/民基"):
        three_base_position("五福", 1)


def test_c66_never_auto_applies_same_palace_omens():
    data = chenji_position(1)
    assert data["same_palace_omens_applied"] is False
    assert data["deferred_layer"] == DEFERRED_LAYER
    assert data["deferred_layer"]["auto_same_palace_inference"] is False


def test_c66_catalog_locks_three_distinct_scales():
    data = c66_catalog()
    assert data["surplus"] == 250
    assert data["rule_ids"] == {
        "君基": "C66-JUNJI",
        "臣基": "C66-CHENJI",
        "民基": "C66-MINJI",
    }
    assert data["bases"]["君基"]["years_per_state"] == 30
    assert data["bases"]["臣基"]["years_per_state"] == 3
    assert data["bases"]["民基"]["years_per_state"] == 1
