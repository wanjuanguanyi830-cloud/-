import pytest

from kintaiyi.jinjing_year_eight_doors import (
    C123_VERSION,
    c123_catalog,
    year_duty_door,
)


@pytest.mark.parametrize(
    ("n", "door", "year_in_door"),
    [
        (1, "开", 1),
        (30, "开", 30),
        (31, "休", 1),
        (60, "休", 30),
        (61, "生", 1),
        (211, "惊", 1),
        (240, "惊", 30),
        (241, "开", 1),
        (720, "惊", 30),
        (721, "开", 1),
    ],
)
def test_c123_year_door_boundaries(n, door, year_in_door):
    data = year_duty_door(n)
    assert data["canonical"] == C123_VERSION
    assert data["duty_door"] == door
    assert data["year_in_door"] == year_in_door


def test_c123_kaiyuan_12_example_anchor_and_thirty_year_shift():
    # 卷一同段给上元至开元十二年甲子积1937281算。
    base = year_duty_door(1_937_281)
    later = year_duty_door(1_937_281 + 30)

    assert base["remainder_240"] == 1
    assert base["duty_door"] == "开"
    assert base["year_in_door"] == 1

    assert later["remainder_240"] == 31
    assert later["duty_door"] == "休"
    assert later["year_in_door"] == 1


def test_c123_preserves_720_outer_and_240_inner_remainders():
    data = year_duty_door(1_937_281)
    assert data["remainder_720"] == 481
    assert data["remainder_240"] == 1


def test_c123_is_explicitly_not_the_c119_time_door_formula():
    catalog = c123_catalog()
    assert catalog["years_per_door"] == 30
    assert catalog["inner_cycle"] == 240
    assert catalog["legacy_boundary"]["correct_source_scope"] == "金镜卷一推八门占岁计法"
    assert catalog["overlay_boundary"]["position_overlay_implemented"] is True
    assert catalog["overlay_boundary"]["overlay_runtime"].endswith("jinjing_year_open_door_contexts")
    assert catalog["overlay_boundary"]["meeting_runtime"].endswith("year_door_meeting")


def test_c123_rejects_zero_as_canonical_accumulated_year():
    with pytest.raises(ValueError):
        year_duty_door(0)
    with pytest.raises(TypeError):
        year_duty_door(True)
