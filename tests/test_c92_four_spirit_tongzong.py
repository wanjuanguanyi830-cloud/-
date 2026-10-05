import pytest

from kintaiyi.four_spirit_tongzong import (
    LEGACY_RECOVERY,
    SOURCE_WITNESS,
    c92_catalog,
    four_spirit_conflict_classification,
    four_spirit_position,
)


def test_c92_four_spirit_position_uses_direct_tongzong_cycle():
    first = four_spirit_position(1)
    assert first["spirit"] == "四神"
    assert first["element"] == "水"
    assert first["big_cycle"] == 360
    assert first["small_cycle"] == 36
    assert first["years_per_palace"] == 3
    assert first["start_palace"] == 1
    assert first["palace"] == 1
    assert first["year_in_palace"] == 1


def test_c92_four_spirit_runs_all_twelve_palaces_three_years_each():
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, "绛宫", "明堂", "玉堂"]
    assert [four_spirit_position(1 + i * 3)["palace"] for i in range(12)] == expected
    assert all(
        four_spirit_position(1 + i * 3 + j)["palace"] == expected[i]
        for i in range(12)
        for j in range(3)
    )


def test_c92_cycle_zero_remainder_is_period_end_not_zero():
    y36 = four_spirit_position(36)
    assert y36["small_cycle_remainder"] == 0
    assert y36["small_cycle_year"] == 36
    assert y36["palace"] == "玉堂"
    assert y36["year_in_palace"] == 3

    y37 = four_spirit_position(37)
    assert y37["palace"] == 1
    assert y37["year_in_palace"] == 1

    y360 = four_spirit_position(360)
    assert y360["big_cycle_remainder"] == 0
    assert y360["small_cycle_year"] == 36
    assert y360["palace"] == "玉堂"


@pytest.mark.parametrize("branch,palace", [
    ("辰", 5), ("辰", 9), ("戌", 5), ("戌", 9),
    ("丑", 7), ("丑", 3), ("未", 7), ("未", 3),
])
def test_c92_direct_kezei_combinations(branch, palace):
    data = four_spirit_conflict_classification(
        year_branch=branch,
        palace=palace,
    )
    assert data["classification"] == "克贼"
    assert data["status"] == "direct_classification"
    assert data["effects"] == ["水旱", "兵盗", "饥荒"]


@pytest.mark.parametrize("branch,palace", [
    ("巳", 2), ("巳", 9), ("午", 2), ("午", 9),
])
def test_c92_direct_zhanke_combinations(branch, palace):
    data = four_spirit_conflict_classification(
        year_branch=branch,
        palace=palace,
    )
    assert data["classification"] == "战克"
    assert "上下失序" in data["effects"]


def test_c92_unlisted_conflict_combination_stays_pending():
    data = four_spirit_conflict_classification(
        year_branch="子",
        palace=8,
    )
    assert data["classification"] is None
    assert data["effects"] == []
    assert data["status"] == "source_not_listed"
    assert "不外推" in "；".join(data["pending"])


def test_c92_conflict_classifier_never_auto_reads_position():
    data = four_spirit_conflict_classification(
        year_branch="辰",
        palace=5,
    )
    assert data["auto_position_lookup_used"] is False


def test_c92_later_three_yuan_variant_is_not_restored_as_default():
    variant = SOURCE_WITNESS["later_variant"]
    assert variant["status"] == "source_variant_not_implemented"
    assert "起自玉堂宫" in "；".join(variant["observed"])
    assert "yuan" in " ".join(LEGACY_RECOVERY["not_reused"])


def test_c92_rejects_bad_inputs():
    with pytest.raises(ValueError):
        four_spirit_position(0)
    with pytest.raises(TypeError):
        four_spirit_position(True)
    with pytest.raises(ValueError, match="十二地支"):
        four_spirit_conflict_classification(year_branch="艮", palace=5)
    with pytest.raises(ValueError, match="1..9或绛宫/明堂/玉堂"):
        four_spirit_conflict_classification(year_branch="辰", palace=10)
    with pytest.raises(TypeError, match="十二运行宫"):
        four_spirit_conflict_classification(year_branch="辰", palace=True)


def test_c92_catalog_records_prior_branch_recovery_without_promoting_old_yuan():
    data = c92_catalog()
    assert data["position_rule"] == "C92-FOUR-SPIRIT-POSITION"
    assert data["classification_rule"] == "C92-FOUR-SPIRIT-CONFLICT-CLASSIFICATION"
    assert data["legacy_recovery"]["branch"] == "codex/c1-c7-canonical"
    assert "旧 four_taiyi_position(..., yuan=...) 三元起宫默认算法" in data["legacy_recovery"]["not_reused"]
