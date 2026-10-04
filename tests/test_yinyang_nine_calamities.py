import pytest

from kintaiyi.yinyang_nine_calamities import (
    CALAMITY_SEGMENTS,
    LEGACY_REFERENCE_AUDIT,
    SOURCE_WITNESS,
    TEXTUAL_NOTES,
    calamity_timeline,
    c47_catalog,
    yinyang_nine_calamities,
)


def test_c47_records_witness_volume_variant():
    assert SOURCE_WITNESS["online_witness_volume"] == 10
    assert SOURCE_WITNESS["project_legacy_volume_label"] == 9
    assert SOURCE_WITNESS["volume_status"] == "witness_volume_variant"


def test_c47_segment_lengths_sum_to_exact_yangjiu_cycle():
    assert [row["duration_years"] for row in CALAMITY_SEGMENTS] == [
        106, 374, 480, 720, 720, 600, 600, 480, 480
    ]
    assert sum(row["duration_years"] for row in CALAMITY_SEGMENTS) == 4560


def test_c47_disaster_years_sum_to_fifty_seven():
    assert [row["disaster_years"] for row in CALAMITY_SEGMENTS] == [
        9, 9, 9, 7, 7, 5, 5, 3, 3
    ]
    assert sum(row["disaster_years"] for row in CALAMITY_SEGMENTS) == 57
    assert sum(row["polarity"] == "阳" for row in CALAMITY_SEGMENTS) == 5
    assert sum(row["polarity"] == "阴" for row in CALAMITY_SEGMENTS) == 4


def test_c47_cumulative_boundaries_are_built_from_segment_lengths():
    timeline = calamity_timeline()
    assert [row["start_year"] for row in timeline] == [
        1, 107, 481, 961, 1681, 2401, 3001, 3601, 4081
    ]
    assert [row["end_year"] for row in timeline] == [
        106, 480, 960, 1680, 2400, 3000, 3600, 4080, 4560
    ]
    assert [row["disaster_start_year"] for row in timeline] == [
        98, 472, 952, 1674, 2394, 2996, 3596, 4078, 4558
    ]


def test_c47_first_segment_disaster_starts_in_last_nine_years():
    before = yinyang_nine_calamities(97 - 130 + 4560)
    start = yinyang_nine_calamities(98 - 130 + 4560)
    end = yinyang_nine_calamities(106 - 130 + 4560)

    assert before["cycle_year"] == 97
    assert before["current_segment"]["index"] == 1
    assert before["in_disaster_period"] is False

    assert start["cycle_year"] == 98
    assert start["in_disaster_period"] is True
    assert start["disaster_year_index"] == 1

    assert end["cycle_year"] == 106
    assert end["disaster_year_index"] == 9


def test_c47_second_segment_uses_374_as_length_not_absolute_threshold():
    end_second = yinyang_nine_calamities(350)
    start_third = yinyang_nine_calamities(351)

    assert end_second["cycle_year"] == 480
    assert end_second["current_segment"]["index"] == 2
    assert end_second["current_segment"]["start_year"] == 107
    assert end_second["current_segment"]["end_year"] == 480
    assert end_second["year_in_segment"] == 374
    assert end_second["in_disaster_period"] is True
    assert end_second["disaster_year_index"] == 9

    assert start_third["cycle_year"] == 481
    assert start_third["current_segment"]["index"] == 3
    assert start_third["year_in_segment"] == 1
    assert start_third["in_disaster_period"] is False


def test_c47_exact_4560_end_maps_to_ninth_segment_not_zero_year():
    data = yinyang_nine_calamities(4430)
    assert data["cycle_remainder"] == 0
    assert data["cycle_year"] == 4560
    assert data["current_segment"]["index"] == 9
    assert data["current_segment"]["name"] == "九阳三灾"
    assert data["year_in_segment"] == 480
    assert data["in_disaster_period"] is True
    assert data["disaster_year_index"] == 3


@pytest.mark.parametrize(
    "cycle_year,index,name,disaster",
    [
        (1, 1, "一阳九灾", "旱"),
        (107, 2, "二阴九灾", "水"),
        (481, 3, "三阳九灾", "旱"),
        (961, 4, "四阴七灾", "水"),
        (1681, 5, "五阳七灾", "旱"),
        (2401, 6, "六阴五灾", "水"),
        (3001, 7, "七阳五灾", "旱"),
        (3601, 8, "八阴三灾", "水"),
        (4081, 9, "九阳三灾", "旱"),
    ],
)
def test_c47_each_segment_start_is_classified_correctly(cycle_year, index, name, disaster):
    accumulated = (cycle_year - 130) % 4560
    data = yinyang_nine_calamities(accumulated)
    assert data["cycle_year"] == cycle_year
    assert data["current_segment"]["index"] == index
    assert data["current_segment"]["name"] == name
    assert data["current_segment"]["disaster"] == disaster
    assert data["year_in_segment"] == 1


def test_c47_preserves_fourth_and_ninth_ocr_conflicts():
    fourth = TEXTUAL_NOTES["fourth_label"]
    ninth = TEXTUAL_NOTES["ninth_disaster_years"]

    assert fourth["online_ocr"] == "四阳七灾水七年"
    assert fourth["normalized"] == "四阴七灾水七年"
    assert fourth["status"] == "ocr_corrected_by_internal_structure"

    assert ninth["online_ocr"] == "九阳三灾旱五年"
    assert ninth["normalized_disaster_years"] == 3
    assert "57" in ninth["reason"]
    assert ninth["status"] == "ocr_corrected_by_internal_arithmetic"


def test_c47_legacy_reference_is_not_equivalent():
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    assert any("累计阈值" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
    assert any("cumulative" in item for item in LEGACY_REFERENCE_AUDIT["issues"])


def test_c47_catalog_summarizes_internal_invariants():
    data = c47_catalog()
    assert data["segment_count"] == 9
    assert data["total_segment_years"] == 4560
    assert data["total_disaster_years"] == 57
    assert data["yang_count"] == 5
    assert data["yin_count"] == 4


def test_c47_rejects_negative_or_non_integer_accumulated_year():
    with pytest.raises(ValueError):
        yinyang_nine_calamities(-1)
    with pytest.raises(TypeError):
        yinyang_nine_calamities(True)
    with pytest.raises(TypeError):
        yinyang_nine_calamities(1.5)
