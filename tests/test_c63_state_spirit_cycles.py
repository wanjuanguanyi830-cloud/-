import pytest

from kintaiyi.state_spirit_cycles import (
    DEFERRED_LAYER,
    LEGACY_NAME_AUDIT,
    SPIRITS,
    TWELVE_PALACES,
    c63_catalog,
    canonical_spirit_name,
    diyi_position,
    spirit_position,
    tianyi_position,
    zhifu_position,
)


def test_c63_twelve_palace_order_is_explicit():
    assert TWELVE_PALACES == (
        1, 2, 3, 4, 5, 6, 7, 8, 9, "绛宫", "明堂", "玉堂"
    )


@pytest.mark.parametrize(
    "func,start",
    [
        (tianyi_position, 6),
        (diyi_position, 9),
        (zhifu_position, 5),
    ],
)
def test_c63_first_three_years_stay_in_start_palace(func, start):
    assert [func(i)["palace"] for i in (1, 2, 3)] == [start, start, start]
    assert [func(i)["year_in_palace"] for i in (1, 2, 3)] == [1, 2, 3]


def test_c63_tianyi_full_36_year_route():
    expected = [6, 7, 8, 9, "绛宫", "明堂", "玉堂", 1, 2, 3, 4, 5]
    actual = [tianyi_position(1 + i * 3)["palace"] for i in range(12)]
    assert actual == expected
    assert tianyi_position(36)["palace"] == 5
    assert tianyi_position(37)["palace"] == 6


def test_c63_diyi_full_36_year_route():
    expected = [9, "绛宫", "明堂", "玉堂", 1, 2, 3, 4, 5, 6, 7, 8]
    actual = [diyi_position(1 + i * 3)["palace"] for i in range(12)]
    assert actual == expected
    assert diyi_position(36)["palace"] == 8
    assert diyi_position(37)["palace"] == 9


def test_c63_zhifu_full_36_year_route():
    expected = [5, 6, 7, 8, 9, "绛宫", "明堂", "玉堂", 1, 2, 3, 4]
    actual = [zhifu_position(1 + i * 3)["palace"] for i in range(12)]
    assert actual == expected
    assert zhifu_position(36)["palace"] == 4
    assert zhifu_position(37)["palace"] == 5


@pytest.mark.parametrize("func", [tianyi_position, diyi_position, zhifu_position])
def test_c63_360_big_cycle_boundary_is_preserved(func):
    end = func(360)
    restart = func(361)
    assert end["big_cycle_remainder"] == 0
    assert end["big_cycle_year"] == 360
    assert end["small_cycle_remainder"] == 0
    assert end["small_cycle_year"] == 36
    assert restart["small_cycle_year"] == 1
    assert restart["year_in_palace"] == 1


def test_c63_yuan_checkpoints_match_later_collation():
    assert tianyi_position(1)["palace"] == 6
    assert tianyi_position(61)["palace"] == 2
    assert tianyi_position(121)["palace"] == "绛宫"

    assert diyi_position(1)["palace"] == 9
    assert diyi_position(61)["palace"] == 5
    assert diyi_position(121)["palace"] == 1

    assert zhifu_position(1)["palace"] == 5
    assert zhifu_position(61)["palace"] == 1
    assert zhifu_position(121)["palace"] == 9


def test_c63_generic_name_and_legacy_zhifu_title_boundary():
    assert canonical_spirit_name("直符") == "直符"
    with pytest.raises(ValueError, match="canonical"):
        canonical_spirit_name("值符")

    assert canonical_spirit_name("值符", allow_legacy_alias=True) == "直符"
    alias = spirit_position("值符", 1, allow_legacy_alias=True)
    assert alias["spirit"] == "直符"
    assert alias["palace"] == 5
    assert LEGACY_NAME_AUDIT["值符"]["canonical_name"] == "直符"


@pytest.mark.parametrize(
    "name,element,rule_id",
    [
        ("天乙", "金", "C63-TIANYI"),
        ("地乙", "土", "C63-DIYI"),
        ("直符", "火", "C63-ZHIFU"),
    ],
)
def test_c63_identity_and_rule_ids(name, element, rule_id):
    data = spirit_position(name, 1)
    assert data["element"] == element
    assert data["rule_id"] == rule_id
    assert SPIRITS[name]["rule_id"] == rule_id


@pytest.mark.parametrize("func", [tianyi_position, diyi_position, zhifu_position])
def test_c63_rejects_nonpositive_and_bool_count(func):
    with pytest.raises(ValueError):
        func(0)
    with pytest.raises(TypeError):
        func(True)


def test_c63_never_auto_applies_same_palace_omens():
    data = tianyi_position(1)
    assert data["same_palace_omens_applied"] is False
    assert data["deferred_layer"] == DEFERRED_LAYER
    assert data["deferred_layer"]["auto_same_palace_inference"] is False


def test_c63_catalog_locks_common_cycle_without_merging_omen_layer():
    data = c63_catalog()
    assert data["big_cycle"] == 360
    assert data["small_cycle"] == 36
    assert data["years_per_palace"] == 3
    assert data["palace_order"] == list(TWELVE_PALACES)
    assert data["rule_ids"] == {
        "天乙": "C63-TIANYI",
        "地乙": "C63-DIYI",
        "直符": "C63-ZHIFU",
    }
    assert data["deferred_layer"]["same_palace_omens"] == (
        "deferred_explicit_evidence_layer"
    )
