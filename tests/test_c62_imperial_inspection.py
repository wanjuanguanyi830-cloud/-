import pytest

from kintaiyi.imperial_inspection import (
    CORNER_POSITIONS,
    DIRECTION_BY_TIANMU,
    MONTH_PATTERNS,
    SOURCE_WITNESS,
    c62_catalog,
    imperial_inspection,
)


@pytest.mark.parametrize("taiyi", ["乾", "艮", "巽", "坤"])
@pytest.mark.parametrize(
    "tianmu,direction",
    [
        ("乾", "东方"),
        ("艮", "南方"),
        ("巽", "西方"),
        ("坤", "北方"),
    ],
)
def test_c62_both_in_four_corners_make_inspection_year(taiyi, tianmu, direction):
    data = imperial_inspection(
        taiyi_position=taiyi,
        tianmu_position=tianmu,
        month_patterns=[],
    )
    assert data["inspection_year"] is True
    assert data["direction"] == direction
    assert data["direction_basis"] == DIRECTION_BY_TIANMU[tianmu]


@pytest.mark.parametrize(
    "taiyi,tianmu",
    [
        ("子", "乾"),
        ("乾", "子"),
        ("午", "卯"),
        ("申", "巽"),
    ],
)
def test_c62_requires_both_taiyi_and_tianmu_in_four_corners(taiyi, tianmu):
    data = imperial_inspection(
        taiyi_position=taiyi,
        tianmu_position=tianmu,
        month_patterns=[],
    )
    assert data["inspection_year"] is False
    assert data["direction"] is None
    assert "遣使按行风俗" in data["fallback_if_not_inspection"]


def test_c62_accepts_source_god_names_via_canonical_position_normalization():
    data = imperial_inspection(
        taiyi_position="阴德",
        tianmu_position="和德",
        month_patterns=[],
    )
    assert data["taiyi_position"] == "乾"
    assert data["tianmu_position"] == "艮"
    assert data["inspection_year"] is True
    assert data["direction"] == "南方"


@pytest.mark.parametrize("pattern", ["囚", "挟", "挾", "格", "对", "對"])
def test_c62_month_patterns_are_explicit_conditions_not_month_numbers(pattern):
    data = imperial_inspection(
        taiyi_position="乾",
        tianmu_position="巽",
        month_patterns=[pattern],
    )
    assert data["month_patterns_checked"] is True
    assert data["month_condition_met"] is True
    assert data["month_number"] is None
    assert data["month_number_computation_supported"] is False


def test_c62_missing_month_pattern_check_stays_pending():
    data = imperial_inspection(
        taiyi_position="乾",
        tianmu_position="坤",
    )
    assert data["inspection_year"] is True
    assert data["month_patterns_checked"] is False
    assert data["month_condition_met"] is False
    assert "行期之月" in "；".join(data["pending"])
    assert data["status"] == "inspection_year_month_condition_unchecked"


def test_c62_explicit_no_month_pattern_does_not_invent_month():
    data = imperial_inspection(
        taiyi_position="艮",
        tianmu_position="乾",
        month_patterns=[],
    )
    assert data["month_patterns_checked"] is True
    assert data["month_condition_met"] is False
    assert data["month_number"] is None
    assert "不自行给出行月" in "；".join(data["pending"])


def test_c62_west_direction_uses_stable_position_not_ocr_god_name():
    west = SOURCE_WITNESS["west_name_witness"]
    assert west["stable_position"] == "巽"
    assert west["stable_direction"] == "西方"
    assert west["jinjing_name"] == "大炅"
    assert set(west["tongzong_online_ocr_variants"]) == {"太昊", "太靈"}

    data = imperial_inspection(
        taiyi_position="乾",
        tianmu_position="巽",
        month_patterns=[],
    )
    assert data["direction"] == "西方"


def test_c62_never_auto_infers_board_or_month():
    data = imperial_inspection(
        taiyi_position="乾",
        tianmu_position="乾",
        month_patterns=["囚"],
    )
    assert data["auto_taiyi_lookup_used"] is False
    assert data["auto_tianmu_lookup_used"] is False
    assert data["auto_pattern_inference_used"] is False
    assert data["month_number"] is None


def test_c62_rejects_unknown_position_and_pattern():
    with pytest.raises(ValueError):
        imperial_inspection(
            taiyi_position="中",
            tianmu_position="乾",
            month_patterns=[],
        )
    with pytest.raises(ValueError, match="囚/挟/格/对"):
        imperial_inspection(
            taiyi_position="乾",
            tianmu_position="艮",
            month_patterns=["击"],
        )
    with pytest.raises(TypeError):
        imperial_inspection(
            taiyi_position="乾",
            tianmu_position="艮",
            month_patterns="囚",
        )


def test_c62_catalog_locks_source_boundaries():
    data = c62_catalog()
    assert set(data["corner_positions"]) == CORNER_POSITIONS
    assert data["direction_by_tianmu"]["乾"]["direction"] == "东方"
    assert data["direction_by_tianmu"]["坤"]["direction"] == "北方"
    assert set(data["month_patterns"]) == MONTH_PATTERNS
    assert data["month_number_computation_supported"] is False
