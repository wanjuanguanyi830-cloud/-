import pytest

from kintaiyi.xiaoyou_position import (
    PALACE_PATH,
    RECENT_WORK_RECOVERY,
    c103_catalog,
    xiaoyou_position,
)


@pytest.mark.parametrize(
    "n,palace,year_in_palace",
    [
        (1, 1, 1),
        (3, 1, 3),
        (4, 2, 1),
        (6, 2, 3),
        (7, 3, 1),
        (12, 4, 3),
        (13, 6, 1),
        (18, 7, 3),
        (19, 8, 1),
        (24, 9, 3),
        (25, 1, 1),
    ],
)
@pytest.mark.parametrize("profile", ["jinjing", "tongzong"])
def test_c103_shared_24_year_eight_palace_core(profile, n, palace, year_in_palace):
    data = xiaoyou_position(n, source_profile=profile)
    assert data["palace"] == palace
    assert data["year_in_palace"] == year_in_palace
    assert data["path"] == list(PALACE_PATH)
    assert 5 not in data["path"]


def test_c103_jinjing_preserves_240_outer_cycle():
    end = xiaoyou_position(240, source_profile="jinjing")
    reset = xiaoyou_position(241, source_profile="jinjing")
    assert end["outer_cycle"] == 240
    assert end["outer_count"] == 240
    assert end["small_count"] == 24
    assert (end["palace"], end["year_in_palace"]) == (9, 3)
    assert (reset["palace"], reset["year_in_palace"]) == (1, 1)


def test_c103_tongzong_preserves_360_outer_cycle():
    end = xiaoyou_position(360, source_profile="tongzong")
    reset = xiaoyou_position(361, source_profile="tongzong")
    assert end["outer_cycle"] == 360
    assert end["outer_count"] == 360
    assert end["small_count"] == 24
    assert (end["palace"], end["year_in_palace"]) == (9, 3)
    assert (reset["palace"], reset["year_in_palace"]) == (1, 1)


def test_c103_profiles_are_not_silently_merged():
    jin = xiaoyou_position(1, source_profile="jinjing")
    tong = xiaoyou_position(1, source_profile="tongzong")
    assert jin["outer_cycle_name"] == "大周"
    assert jin["outer_cycle"] == 240
    assert tong["outer_cycle_name"] == "纪元周"
    assert tong["outer_cycle"] == 360
    assert jin["rule_id"] != tong["rule_id"]


def test_c103_keeps_position_separate_from_c47_hexagram_layer():
    data = xiaoyou_position(1, source_profile="tongzong")
    assert "C47" in data["boundary"]["c47_relation"]
    assert data["boundary"]["auto_conjunction_omens"] is False
    assert data["same_palace_omens_applied"] is False


def test_c103_recent_work_recovery_is_inside_two_day_window():
    assert RECENT_WORK_RECOVERY["file_commit"] == "3c9161b5e7b3"
    assert RECENT_WORK_RECOVERY["file_commit_date"].startswith("2026-10-04")
    assert RECENT_WORK_RECOVERY["time_window_policy"] == (
        "only_2026-10-04_and_2026-10-05_prior_work"
    )


def test_c103_requires_explicit_source_profile_and_positive_count():
    with pytest.raises(TypeError):
        xiaoyou_position(1)
    with pytest.raises(ValueError, match="jinjing/tongzong"):
        xiaoyou_position(1, source_profile="mixed")
    with pytest.raises(ValueError):
        xiaoyou_position(0, source_profile="jinjing")


def test_c103_catalog_has_no_default_profile():
    data = c103_catalog()
    assert data["source_profile_required"] is True
    assert data["default_profile"] is None
    assert set(data["profiles"]) == {"jinjing", "tongzong"}
