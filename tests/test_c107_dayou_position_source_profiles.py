import pytest

from kintaiyi.dayou_position_source_profiles import (
    PALACE_PATH,
    RECENT_WORK_RECOVERY,
    c107_catalog,
    dayou_position,
)


@pytest.mark.parametrize(
    "n,palace,year_in_palace",
    [
        (1, 7, 1),
        (36, 7, 36),
        (37, 8, 1),
        (72, 8, 36),
        (73, 9, 1),
        (108, 9, 36),
        (109, 1, 1),
        (288, 6, 36),
        (289, 7, 1),
    ],
)
def test_c107_jinjing_288_small_cycle(n, palace, year_in_palace):
    data = dayou_position(n, source_profile="jinjing")
    assert data["outer_cycle"] == 4320
    assert data["small_cycle"] == 288
    assert data["surplus"] == 0
    assert (data["palace"], data["year_in_palace"]) == (
        palace,
        year_in_palace,
    )


def test_c107_jinjing_outer_4320_boundary_is_preserved():
    end = dayou_position(4320, source_profile="jinjing")
    reset = dayou_position(4321, source_profile="jinjing")
    assert end["outer_count"] == 4320
    assert (end["palace"], end["year_in_palace"]) == (6, 36)
    assert (reset["palace"], reset["year_in_palace"]) == (7, 1)
    assert end["secondary_cycle_metadata"] == {"纪法": 720}


def test_c107_tongzong_uses_plus34_and_288_execution_cycle():
    first = dayou_position(1, source_profile="tongzong")
    assert first["surplus"] == 34
    assert first["outer_cycle"] == 2880
    assert first["small_cycle"] == 288
    assert first["adjusted_count"] == 35
    assert (first["palace"], first["year_in_palace"]) == (7, 35)

    next_palace = dayou_position(3, source_profile="tongzong")
    assert next_palace["adjusted_count"] == 37
    assert (next_palace["palace"], next_palace["year_in_palace"]) == (8, 1)


def test_c107_tongzong_keeps_388_as_transcription_variant_not_runtime_cycle():
    data = dayou_position(1, source_profile="tongzong")
    variant = data["source_witness"]["small_cycle_transcription_variant"]
    assert variant["electronic_reading"] == "三百八十八"
    assert variant["execution_value"] == 288
    assert variant["status"] == "resolved_numeric_transcription_conflict"
    assert data["small_cycle"] == 288


def test_c107_profiles_share_route_but_not_epoch_parameters():
    jin = dayou_position(1, source_profile="jinjing")
    tong = dayou_position(1, source_profile="tongzong")
    assert jin["path"] == tong["path"] == list(PALACE_PATH)
    assert jin["rule_id"] != tong["rule_id"]
    assert jin["outer_cycle"] == 4320
    assert tong["outer_cycle"] == 2880
    assert jin["surplus"] == 0
    assert tong["surplus"] == 34


def test_c107_recent_work_is_strictly_inside_two_day_window():
    assert RECENT_WORK_RECOVERY["file_commit"] == "7f2d1b5dc74e"
    assert RECENT_WORK_RECOVERY["file_commit_date"].startswith("2026-10-04")
    assert RECENT_WORK_RECOVERY["time_window_policy"] == (
        "only_2026-10-04_and_2026-10-05_prior_work"
    )


def test_c107_relation_layers_are_not_auto_applied():
    data = dayou_position(1, source_profile="tongzong")
    assert data["same_palace_omens_applied"] is False
    assert data["boundary"]["auto_conjunction_omens"] is False
    assert "C41" in data["boundary"]["c41_relation"]


def test_c107_requires_explicit_profile_and_positive_count():
    with pytest.raises(TypeError):
        dayou_position(1)
    with pytest.raises(ValueError, match="jinjing/tongzong"):
        dayou_position(1, source_profile="mixed")
    with pytest.raises(ValueError):
        dayou_position(0, source_profile="jinjing")


def test_c107_catalog_has_no_default_profile():
    data = c107_catalog()
    assert data["source_profile_required"] is True
    assert data["default_profile"] is None
    assert data["path"] == list(PALACE_PATH)
