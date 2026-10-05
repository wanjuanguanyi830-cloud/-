import pytest

from kintaiyi.tongzong_volume10_spirits import (
    FOUR_MENG_REVERSE,
    REVERSE_BRANCHES_FROM_HAI,
    haiqi_red_banner,
    nine_palace_nobles,
    qinglong_banner,
    taiyin_black_banner,
    three_banners,
    volume10_spirit_catalog,
)


def test_c126_qinglong_uses_one_based_suanwai_boundary():
    assert qinglong_banner(1)["branch"] == "子"
    assert qinglong_banner(12)["branch"] == "亥"
    assert qinglong_banner(13)["branch"] == "子"
    assert qinglong_banner(60)["branch"] == "亥"
    assert qinglong_banner(61)["branch"] == "子"


def test_c126_taiyin_keeps_three_full_years_in_each_branch():
    first = taiyin_black_banner(12)
    third = taiyin_black_banner(14)
    next_branch = taiyin_black_banner(15)

    assert first["small_count"] == 1
    assert (first["branch"], first["year_in_branch"]) == ("亥", 1)
    assert (third["branch"], third["year_in_branch"]) == ("亥", 3)
    assert (next_branch["branch"], next_branch["year_in_branch"]) == ("戌", 1)
    assert REVERSE_BRANCHES_FROM_HAI[:3] == ("亥", "戌", "酉")


def test_c126_haiqi_is_one_based_reverse_four_meng():
    assert FOUR_MENG_REVERSE == ("亥", "申", "巳", "寅")
    assert haiqi_red_banner(4)["branch"] == "亥"
    assert haiqi_red_banner(5)["branch"] == "申"
    assert haiqi_red_banner(6)["branch"] == "巳"
    assert haiqi_red_banner(7)["branch"] == "寅"
    assert haiqi_red_banner(8)["branch"] == "亥"


def test_c126_source_cycle_has_three_flag_meeting_at_count_3():
    data = three_banners(3)
    assert data["rule_id"] == "C126-TONGZONG-THREE-BANNERS"
    assert data["flags"] == {
        "太岁青龙旗": "寅",
        "太阴黑旗": "寅",
        "害气赤旗": "寅",
    }
    assert data["meeting"] == "三神会合"
    assert data["meeting_branches"] == ["寅"]
    assert data["source_omen"] == "灾急"
    assert data["taiyi_meeting_applied"] is False


def test_c127_source_example_remainder_three_is_taiyin():
    # accumulated_year=9 -> 周纪余9；+3 -> 12；九除余3
    data = nine_palace_nobles(9)

    assert data["rule_id"] == "C127-TONGZONG-NINE-PALACE-NOBLES"
    assert data["small_count"] == 3
    assert data["direct_god_number"] == 8
    assert data["direct_god"] == "太阴"
    assert data["direct_palace"] == "中"


def test_c127_taiyin_example_reproduces_tongzong_flying_distribution():
    data = nine_palace_nobles(9)
    assert data["distribution"] == {
        "坎": "招摇",
        "坤": "天符",
        "震": "青龙",
        "巽": "咸池",
        "中": "太阴",
        "乾": "天乙",
        "兑": "太乙",
        "艮": "摄提",
        "离": "轩辕",
    }
    assert data["god_locations"]["天乙"] == "乾"
    assert data["god_locations"]["太乙"] == "兑"
    assert data["god_locations"]["摄提"] == "艮"
    assert data["god_locations"]["轩辕"] == "离"


def test_c127_cycle_boundary_preserves_remainder_three_at_360():
    data = nine_palace_nobles(360)
    assert data["cycle_360_count"] == 360
    assert data["small_count"] == 3
    assert data["direct_god"] == "太阴"


def test_c126_c127_require_positive_accumulated_year():
    for func in (qinglong_banner, taiyin_black_banner, haiqi_red_banner, three_banners, nine_palace_nobles):
        with pytest.raises(ValueError):
            func(0)


def test_volume10_spirit_catalog_forbids_ziting_backfill():
    data = volume10_spirit_catalog()
    assert data["rule_ids"] == [
        "C126-TONGZONG-THREE-BANNERS",
        "C127-TONGZONG-NINE-PALACE-NOBLES",
    ]
    assert data["cross_source_merge"] is False
    assert data["ziting_backfill_allowed"] is False
