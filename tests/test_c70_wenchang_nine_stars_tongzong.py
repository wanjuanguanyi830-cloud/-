import pytest

from kintaiyi.wenchang_nine_stars_tongzong import (
    DYNAMIC_DISTRIBUTION_BOUNDARY,
    LEGACY_AUDIT,
    NAME_VARIANTS,
    STAR_TABLE,
    STEM_LANDING,
    c70_catalog,
    wenchang_nine_star_tongzong,
)


def test_c70_ngj_star_table_is_source_specific():
    assert [row["star"] for row in STAR_TABLE] == [
        "文昌", "玄凤", "明维", "阴德", "招摇",
        "华明", "玄武", "玄冥", "维明",
    ]
    assert [row["palace"] for row in STAR_TABLE] == [
        "乾", "离", "艮", "震", "中", "兑", "坤", "坎", "巽"
    ]


def test_c70_30_year_star_boundaries():
    first = wenchang_nine_star_tongzong(1)
    assert first["direct_star"] == "文昌"
    assert first["year_in_star"] == 1

    end = wenchang_nine_star_tongzong(30)
    assert end["direct_star"] == "文昌"
    assert end["year_in_star"] == 30

    next_star = wenchang_nine_star_tongzong(31)
    assert next_star["direct_star"] == "玄凤"
    assert next_star["year_in_star"] == 1


def test_c70_source_example_structure_xuanfeng_year11_then_year12():
    # 31..60 为玄凤；41 = 玄凤第11年。
    jiachen = wenchang_nine_star_tongzong(41, year_stem="甲")
    assert jiachen["direct_star"] == "玄凤"
    assert jiachen["year_in_star"] == 11
    assert jiachen["direct_star_landing"]["palace"] == "艮"
    assert jiachen["direct_star_landing"]["region"] == "青州"

    yisi = wenchang_nine_star_tongzong(42, year_stem="乙")
    assert yisi["direct_star"] == "玄凤"
    assert yisi["year_in_star"] == 12
    assert yisi["direct_star_landing"]["palace"] == "震"
    assert yisi["direct_star_landing"]["region"] == "徐州"


def test_c70_corrects_legacy_ding_and_ren_stem_landings():
    ding = wenchang_nine_star_tongzong(1, year_stem="丁")
    ren = wenchang_nine_star_tongzong(1, year_stem="壬")
    assert ding["direct_star_landing"] == {
        "palace": "离", "region": "荆州", "table_index": 2
    }
    assert ren["direct_star_landing"] == {
        "palace": "乾", "region": "冀州", "table_index": 1
    }
    assert STEM_LANDING["丁"]["table_index"] == 2
    assert STEM_LANDING["壬"]["table_index"] == 1


def test_c70_stem_disaster_groups_are_direct_and_explicit():
    assert wenchang_nine_star_tongzong(
        1, year_stem="甲"
    )["stem_disaster_effects"] == ["疾疫", "风雷"]
    assert wenchang_nine_star_tongzong(
        1, year_stem="丙"
    )["stem_disaster_effects"] == ["火旱", "口舌妖言"]
    assert wenchang_nine_star_tongzong(
        1, year_stem="壬"
    )["stem_disaster_effects"] == ["霪沉淋雨", "大水", "后妃不安"]


def test_c70_270_and_2700_zero_remainders_are_preserved():
    small_end = wenchang_nine_star_tongzong(270)
    assert small_end["small_cycle_remainder"] == 0
    assert small_end["small_cycle_count"] == 270
    assert small_end["direct_star"] == "维明"
    assert small_end["year_in_star"] == 30

    big_end = wenchang_nine_star_tongzong(2700)
    assert big_end["large_cycle_remainder"] == 0
    assert big_end["large_cycle_count"] == 2700
    assert big_end["small_cycle_count"] == 270
    assert big_end["direct_star"] == "维明"


def test_c70_next_cycle_restarts_at_wenchang():
    data = wenchang_nine_star_tongzong(2701)
    assert data["small_cycle_count"] == 1
    assert data["direct_star"] == "文昌"
    assert data["year_in_star"] == 1


def test_c70_year_stem_is_optional_but_if_present_must_be_valid():
    data = wenchang_nine_star_tongzong(1)
    assert data["year_stem"] is None
    assert data["direct_star_landing"] is None

    with pytest.raises(ValueError, match="十天干"):
        wenchang_nine_star_tongzong(1, year_stem="甲子")


@pytest.mark.parametrize("bad", [0, -1])
def test_c70_rejects_nonpositive_counts(bad):
    with pytest.raises(ValueError):
        wenchang_nine_star_tongzong(bad)


def test_c70_rejects_bool_count():
    with pytest.raises(TypeError):
        wenchang_nine_star_tongzong(True)


def test_c70_preserves_cross_source_name_variants():
    assert NAME_VARIANTS["third"] == ["明维", "明雄"]
    assert NAME_VARIANTS["fourth"] == ["阴德", "阴玄"]
    assert NAME_VARIANTS["ninth"] == ["维明", "雄明"]


def test_c70_does_not_invent_full_dynamic_distribution():
    data = wenchang_nine_star_tongzong(41, year_stem="甲")
    assert data["full_dynamic_distribution"] is None
    assert data["dynamic_distribution_boundary"] == DYNAMIC_DISTRIBUTION_BOUNDARY
    assert data["dynamic_distribution_boundary"]["supported"] is False


def test_c70_legacy_function_is_not_canonical_equivalent():
    assert LEGACY_AUDIT["identifier"] == "config.wenchang_nine_stars"
    assert LEGACY_AUDIT["canonical_equivalent"] is False
    assert LEGACY_AUDIT["promotion_allowed"] is False
    assert any("丁" in item for item in LEGACY_AUDIT["problems"])
    assert any("壬" in item for item in LEGACY_AUDIT["problems"])
    assert any("gong变量" in item for item in LEGACY_AUDIT["problems"])


def test_c70_catalog_keeps_zitingjing_primary_unselected():
    data = c70_catalog()
    assert data["source_profile"] == "tongzong_volume6_ngj_wenchang_nine_stars"
    assert data["cross_source_canonical_selected"] == (
        "tongzong_volume6_ngj_wenchang_nine_stars"
    )
    assert data["source_witness"]["variants_not_merged"]["zitingjing_appendix"][
        "direct_text_available"
    ] is False
