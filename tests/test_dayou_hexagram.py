import pytest

from kintaiyi.dayou_hexagram import (
    EPOCH_VARIANTS,
    FOUR_IMAGE_CE,
    compose_dayou_heavy_hexagram,
    dayou_epoch_variants,
    four_image_ce,
    inner_moving_line,
)


def test_c41_four_image_ce_table():
    assert FOUR_IMAGE_CE["乾"] == {"four_image": "老阳", "ce": 36}
    assert FOUR_IMAGE_CE["坤"] == {"four_image": "老阴", "ce": 24}
    for trigram in ("震", "坎", "艮"):
        assert FOUR_IMAGE_CE[trigram] == {"four_image": "少阳", "ce": 28}
    for trigram in ("巽", "离", "兑"):
        assert FOUR_IMAGE_CE[trigram] == {"four_image": "少阴", "ce": 32}


def test_c41_traditional_aliases_are_representation_only():
    assert four_image_ce("離")["trigram"] == "离"
    assert four_image_ce("兌")["trigram"] == "兑"


@pytest.mark.parametrize(
    "year,line,name,span",
    [
        (1, 1, "初爻", [1, 6]),
        (6, 1, "初爻", [1, 6]),
        (7, 2, "二爻", [7, 12]),
        (12, 2, "二爻", [7, 12]),
        (13, 3, "三爻", [13, 18]),
        (19, 4, "四爻", [19, 24]),
        (25, 5, "五爻", [25, 30]),
        (31, 6, "上爻", [31, 36]),
        (36, 6, "上爻", [31, 36]),
    ],
)
def test_c41_inner_moving_line_every_six_years(year, line, name, span):
    data = inner_moving_line(year)
    assert data["line"] == line
    assert data["line_name"] == name
    assert data["year_range"] == span


def test_c41_line_complete_only_on_each_sixth_year():
    assert inner_moving_line(5)["line_complete"] is False
    assert inner_moving_line(6)["line_complete"] is True
    assert inner_moving_line(35)["line_complete"] is False
    assert inner_moving_line(36)["line_complete"] is True


def test_c41_invalid_inner_year_rejected():
    with pytest.raises(ValueError):
        inner_moving_line(0)
    with pytest.raises(ValueError):
        inner_moving_line(37)
    with pytest.raises(TypeError):
        inner_moving_line(True)


def test_c41_heavy_hexagram_structure_is_outer_over_inner():
    data = compose_dayou_heavy_hexagram(
        inner_trigram="坤",
        outer_trigram="乾",
        year_in_inner_trigram=13,
    )
    assert data["rule_id"] == "C41-DY-HEX"
    assert data["structure"] == {
        "upper_trigram": "乾",
        "lower_trigram": "坤",
        "display": "乾上坤下",
    }
    assert data["inner"]["four_image"] == "老阴"
    assert data["outer"]["four_image"] == "老阳"
    assert data["inner_moving_line"]["line"] == 3
    assert data["ce"] == {
        "inner": 24,
        "outer": 36,
        "total": 60,
        "total_status": "derived_sum_of_inner_outer_trigram_ce",
    }


def test_c41_does_not_invent_outer_moving_line():
    data = compose_dayou_heavy_hexagram(
        inner_trigram="震",
        outer_trigram="巽",
        year_in_inner_trigram=20,
    )
    assert data["outer_moving_line"] is None
    assert data["outer_moving_line_status"] == "not_attested_in_direct_c41_rule"


def test_c41_does_not_use_c38_or_epoch_offsets():
    data = compose_dayou_heavy_hexagram(
        inner_trigram="坎",
        outer_trigram="离",
        year_in_inner_trigram=6,
    )
    assert data["epoch_formula_applied"] is False
    assert data["c38_track_used"] is False
    assert "+34/+50" in data["policy"]


def test_c41_epoch_variants_preserve_offset_conflict_without_selection():
    data = dayou_epoch_variants()
    assert data["canonical_selected"] is None
    assert data["cross_source_merge"] is False
    assert data["runtime_uses_epoch_variant"] is False

    variants = data["variants"]
    assert variants["tongzong_offset34_witness"]["inner_offset"] == 34
    assert variants["taibai_bingbei_epoch_correction"]["inner_offset"] == 36610
    assert variants["legacy_guiyun_outer_offset50"]["status"] == "unsupported_legacy_offset"
    assert variants["legacy_guiyun_outer_offset50"]["outer_offset"] == 50


def test_c41_invalid_trigram_rejected():
    with pytest.raises(ValueError):
        four_image_ce("中")
    with pytest.raises(ValueError):
        compose_dayou_heavy_hexagram(
            inner_trigram="乾",
            outer_trigram="坤宫",
            year_in_inner_trigram=1,
        )


def test_c41_total_ce_is_marked_as_derived_convenience():
    data = compose_dayou_heavy_hexagram(
        inner_trigram="艮",
        outer_trigram="兑",
        year_in_inner_trigram=24,
    )
    assert data["ce"]["inner"] == 28
    assert data["ce"]["outer"] == 32
    assert data["ce"]["total"] == 60
    assert data["ce"]["total_status"] == "derived_sum_of_inner_outer_trigram_ce"
    assert "正文未另立“总策”公式" in data["policy"]
