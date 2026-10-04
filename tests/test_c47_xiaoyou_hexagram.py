import pytest

from kintaiyi.xiaoyou_hexagram import (
    SOURCE_WITNESS,
    XIAOYOU_TRIGRAM_PATH,
    xiaoyou_heavy_hexagram,
    xiaoyou_inner_track,
    xiaoyou_outer_track,
    xiaoyou_source_profile,
)


def test_c47_path_is_source_order():
    assert XIAOYOU_TRIGRAM_PATH == (
        "乾", "离", "艮", "震", "兑", "坤", "坎", "巽"
    )


def test_c47_inner_cycles_and_rate():
    profile = xiaoyou_source_profile()
    assert profile["inner_big_cycle"] == 1920
    assert profile["inner_small_cycle"] == 192
    assert profile["inner_rate"] == 24
    assert SOURCE_WITNESS["inner"]["years_per_trigram"] == 24


def test_c47_inner_source_example_remainder_80_is_zhen_year8():
    data = xiaoyou_inner_track(10155536)
    assert data["small_cycle_year"] == 80
    assert data["trigram_index"] == 4
    assert data["trigram"] == "震"
    assert data["year_in_trigram"] == 8
    assert data["moving_line"] == 2
    assert data["moving_line_year_range"] == [5, 8]
    assert data["moving_line_complete"] is True


@pytest.mark.parametrize(
    "year,trigram,year_in,line",
    [
        (1, "乾", 1, 1),
        (4, "乾", 4, 1),
        (5, "乾", 5, 2),
        (24, "乾", 24, 6),
        (25, "离", 1, 1),
        (48, "离", 24, 6),
        (49, "艮", 1, 1),
        (192, "巽", 24, 6),
        (193, "乾", 1, 1),
        (1920, "巽", 24, 6),
        (1921, "乾", 1, 1),
    ],
)
def test_c47_inner_boundaries(year, trigram, year_in, line):
    data = xiaoyou_inner_track(year)
    assert data["trigram"] == trigram
    assert data["year_in_trigram"] == year_in
    assert data["moving_line"] == line


def test_c47_outer_cycles_rate_and_three_talents():
    one = xiaoyou_outer_track(1)
    two = xiaoyou_outer_track(2)
    three = xiaoyou_outer_track(3)
    four = xiaoyou_outer_track(4)

    assert one["trigram"] == "乾"
    assert one["three_talent"] == "理天"
    assert two["three_talent"] == "理地"
    assert three["three_talent"] == "理人"
    assert three["trigram_complete"] is True
    assert four["trigram"] == "离"
    assert four["year_in_trigram"] == 1


def test_c47_outer_24_year_trigram_cycle_inside_360_epoch():
    end = xiaoyou_outer_track(24)
    restart = xiaoyou_outer_track(25)
    epoch_end = xiaoyou_outer_track(360)
    next_epoch = xiaoyou_outer_track(361)

    assert end["trigram"] == "巽"
    assert end["year_in_trigram"] == 3
    assert end["three_talent"] == "理人"

    assert restart["trigram"] == "乾"
    assert restart["year_in_trigram"] == 1

    assert epoch_end["epoch_cycle_year"] == 360
    assert epoch_end["trigram_cycle_year"] == 24
    assert epoch_end["trigram"] == "巽"

    assert next_epoch["epoch_cycle_year"] == 1
    assert next_epoch["trigram"] == "乾"


def test_c47_outer_profile_keeps_360_24_and_combined_192_distinct():
    profile = xiaoyou_source_profile()
    assert profile["outer_epoch_cycle"] == 360
    assert profile["outer_trigram_cycle"] == 24
    assert profile["outer_rate"] == 3
    assert profile["combined_hexagram_cycle"] == 192
    assert profile["cross_dayou_merge"] is False
    assert profile["cross_c38_merge"] is False


def test_c47_heavy_hexagram_is_outer_over_inner_and_only_inner_moves():
    data = xiaoyou_heavy_hexagram(25)
    assert data["structure"] == {
        "upper_trigram": "乾",
        "lower_trigram": "离",
        "display": "乾上离下",
    }
    assert data["inner_moving_line"] == 1
    assert data["outer_moving_line"] is None
    assert data["outer_moving_line_status"] == "not_used_by_source_rule"
    assert data["three_talent"] == "理天"


def test_c47_reuses_shared_four_image_ce_without_reusing_dayou_epoch():
    data = xiaoyou_heavy_hexagram(1)
    assert data["ce"]["inner"] == {
        "trigram": "乾",
        "four_image": "老阳",
        "per_line_ce": 36,
        "trigram_ce": 108,
        "source_dependency": "C41共享四象策数表",
    }
    assert data["ce"]["outer"]["trigram_ce"] == 108
    assert data["ce"]["total"] == 216
    assert data["c38_track_used"] is False
    assert data["dayou_epoch_offset_used"] is False


def test_c47_does_not_force_sixtyfour_hexagram_name():
    data = xiaoyou_heavy_hexagram(80)
    assert data["hexagram_name"] is None
    assert data["hexagram_name_status"] == "not_resolved_in_c46"


def test_c47_rejects_nonpositive_or_bool_year():
    with pytest.raises(ValueError):
        xiaoyou_inner_track(0)
    with pytest.raises(TypeError):
        xiaoyou_outer_track(True)
