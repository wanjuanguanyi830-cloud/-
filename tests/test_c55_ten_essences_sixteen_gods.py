import pytest

from kintaiyi.taiyi_rules import GOD_POSITION, SIXTEEN
from kintaiyi.ten_essences_sixteen_gods import (
    DIFU_REPEAT_GODS,
    DIFU_YANG_GOD_PATH,
    LEGACY_AUDIT,
    SURPLUS_REJECTION,
    TIANHUANG_REPEAT_GODS,
    TIANHUANG_YANG_GOD_PATH,
    c55_catalog,
    difu_position,
    tianhuang_position,
)


def _opposite(point):
    return SIXTEEN[(SIXTEEN.index(point) + 8) % 16]


def test_c55_tianhuang_path_is_16_gods_plus_four_corner_holds():
    assert len(TIANHUANG_YANG_GOD_PATH) == 20
    assert TIANHUANG_REPEAT_GODS == {"阴德", "和德", "大炅", "大武"}
    for god in TIANHUANG_REPEAT_GODS:
        assert TIANHUANG_YANG_GOD_PATH.count(god) == 2
    assert TIANHUANG_YANG_GOD_PATH[:5] == (
        "武德", "太簇", "阴主", "阴德", "阴德"
    )
    assert TIANHUANG_YANG_GOD_PATH[-2:] == ("大武", "大武")


def test_c55_difu_path_is_16_gods_plus_four_cardinal_holds():
    assert len(DIFU_YANG_GOD_PATH) == 20
    assert DIFU_REPEAT_GODS == {"地主", "高丛", "大威", "太簇"}
    for god in DIFU_REPEAT_GODS:
        assert DIFU_YANG_GOD_PATH.count(god) == 2
    assert DIFU_YANG_GOD_PATH[:5] == (
        "阴主", "阴德", "大义", "地主", "地主"
    )
    assert DIFU_YANG_GOD_PATH[-2:] == ("太簇", "太簇")


@pytest.mark.parametrize("func", [tianhuang_position, difu_position])
def test_c55_yin_is_stepwise_opposite_of_tongzong_yang(func):
    for count in (1, 4, 5, 10, 15, 20):
        yang = func(count, dun="阳")
        yin = func(count, dun="阴")
        assert yin["position"] == _opposite(yang["position"])
        assert yin["opposition_applied"] is True
        assert yang["opposition_applied"] is False


def test_c55_tianhuang_start_and_repeat_boundaries():
    one = tianhuang_position(1, dun="阳")
    assert one["god"] == "武德"
    assert one["position"] == "申"
    assert one["repeat_location"] is False

    four = tianhuang_position(4, dun="阳")
    five = tianhuang_position(5, dun="阳")
    assert four["god"] == five["god"] == "阴德"
    assert four["position"] == five["position"] == "乾"
    assert four["repeat_visit_ordinal"] == 1
    assert five["repeat_visit_ordinal"] == 2

    yin_one = tianhuang_position(1, dun="阴")
    assert yin_one["position"] == "寅"
    assert yin_one["god"] == "吕申"


def test_c55_difu_start_and_repeat_boundaries():
    one = difu_position(1, dun="阳")
    assert one["god"] == "阴主"
    assert one["position"] == "戌"

    four = difu_position(4, dun="阳")
    five = difu_position(5, dun="阳")
    assert four["god"] == five["god"] == "地主"
    assert four["position"] == five["position"] == "子"
    assert four["repeat_visit_ordinal"] == 1
    assert five["repeat_visit_ordinal"] == 2

    yin_one = difu_position(1, dun="阴")
    assert yin_one["position"] == "辰"
    assert yin_one["god"] == "太阳"


@pytest.mark.parametrize("func", [tianhuang_position, difu_position])
def test_c55_200_20_cycle_boundaries(func):
    twenty = func(20, dun="阳")
    twenty_one = func(21, dun="阳")
    two_hundred = func(200, dun="阳")
    two_hundred_one = func(201, dun="阳")

    assert twenty["small_cycle_year"] == 20
    assert twenty_one["small_cycle_year"] == 1
    assert two_hundred["big_cycle_remainder"] == 0
    assert two_hundred["big_cycle_year"] == 200
    assert two_hundred["small_cycle_year"] == 20
    assert two_hundred_one["small_cycle_year"] == 1


@pytest.mark.parametrize("func", [tianhuang_position, difu_position])
def test_c55_requires_explicit_valid_dun_and_positive_count(func):
    with pytest.raises(TypeError):
        func(1)
    with pytest.raises(ValueError, match="dun须为阳/阴"):
        func(1, dun="冬至")
    with pytest.raises(ValueError):
        func(0, dun="阳")
    with pytest.raises(TypeError):
        func(True, dun="阳")


def test_c55_surplus_variants_are_recorded_but_never_applied():
    tianhuang = tianhuang_position(14, dun="阳")
    difu = difu_position(17, dun="阳")
    assert tianhuang["surplus_applied"] is False
    assert difu["surplus_applied"] is False
    assert SURPLUS_REJECTION["天皇"]["witness_values"] == {
        "volume18": 14, "volume20": 14
    }
    assert SURPLUS_REJECTION["帝符"]["witness_values"] == {
        "volume18": 17, "volume20_or_ocr_variant": 70
    }
    assert SURPLUS_REJECTION["帝符"]["apply"] is False


def test_c55_old_cycle_match_does_not_promote_legacy_formula():
    assert LEGACY_AUDIT["config.tian_wang"]["canonical_equivalent"] is False
    assert LEGACY_AUDIT["config.kingfu"]["canonical_equivalent"] is False


def test_c55_catalog_keeps_tianshi_pending_and_cloud_omens_separate():
    data = c55_catalog()
    assert data["implemented"] == ["天皇", "帝符"]
    assert data["pending_position"] == ["天时"]
    assert data["repeat_counts"] == {"天皇": 4, "帝符": 4}
    assert data["cloud_omen_runtime"] is False
