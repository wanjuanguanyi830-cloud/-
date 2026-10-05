import pytest

from kintaiyi.jinjing_time_eight_doors import (
    C119_VERSION,
    c119_catalog,
    movement_rates,
    summer_solstice_duty_door,
    time_duty_door,
    winter_solstice_duty_door,
)


@pytest.mark.parametrize(
    ("time_real", "door"),
    [
        (0, "开"),
        (29, "开"),
        (30, "生"),
        (59, "生"),
        (60, "惊"),
        (89, "惊"),
        (90, "休"),
        (119, "休"),
        (120, "开"),
        (239, "休"),
        (240, "开"),
    ],
)
def test_c119_winter_thirty_time_blocks(time_real, door):
    data = winter_solstice_duty_door(time_real)
    assert data["canonical"] == C119_VERSION
    assert data["duty_door"] == door
    assert data["block_size"] == 30


@pytest.mark.parametrize(
    ("time_real", "door"),
    [
        (0, "杜"),
        (29, "杜"),
        (30, "死"),
        (60, "伤"),
        (90, "景"),
        (120, "杜"),
    ],
)
def test_c119_summer_thirty_time_blocks(time_real, door):
    data = summer_solstice_duty_door(time_real)
    assert data["duty_door"] == door
    assert data["source_status"] == "cross_section_direct_sequence_with_local_lacuna"


def test_c119_generic_dispatch_keeps_yin_yang_sequences_separate():
    assert time_duty_door("阳遁", 30)["duty_door"] == "生"
    assert time_duty_door("阴遁", 30)["duty_door"] == "死"


def test_c119_movement_rates_are_direct_but_overlay_formula_stays_unimplemented():
    data = movement_rates()
    assert data["rates"]["太乙"]["time_units_per_move"] == 3
    assert data["rates"]["大将"]["time_units_per_move"] == 1
    assert data["overlay_boundary"]["implemented_position_overlay"] is False


def test_c119_explicitly_separates_time_doors_from_existing_year_cycle():
    catalog = c119_catalog()
    boundary = catalog["separation_boundary"]
    assert boundary["same_formula"] is False
    assert boundary["c119_semantics"] == "time-count / 30-time-unit duty-door cycle"
    assert "30-year" in boundary["existing_file_semantics"]


def test_c119_zhangliang_anchor_tables_preserved_as_source_metadata():
    catalog = c119_catalog()
    assert [x["door"] for x in catalog["zhangliang_anchors"]["阳遁"]] == [
        "开", "生", "惊", "休"
    ]
    assert [x["door"] for x in catalog["zhangliang_anchors"]["阴遁"]] == [
        "杜", "死", "伤", "景"
    ]


def test_c119_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        time_duty_door("未知", 0)
    with pytest.raises(ValueError):
        winter_solstice_duty_door(-1)
    with pytest.raises(TypeError):
        summer_solstice_duty_door(True)
