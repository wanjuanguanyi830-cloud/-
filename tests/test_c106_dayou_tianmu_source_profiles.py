import pytest

from kintaiyi.dayou_tianmu_source_profiles import (
    RECENT_WORK_RECOVERY,
    TIANMU_PATH,
    c106_catalog,
    dayou_tianmu_position,
)


def test_c106_path_has_two_required_repeats_and_eighteen_steps():
    assert len(TIANMU_PATH) == 18
    assert TIANMU_PATH[:4] == ("天道", "大武", "大武", "武德")
    assert TIANMU_PATH[6:9] == ("阴德", "阴德", "大义")


@pytest.mark.parametrize(
    "n,step,god",
    [
        (1, 1, "天道"),
        (2, 2, "大武"),
        (3, 3, "大武"),
        (18, 18, "大威"),
        (19, 1, "天道"),
        (72, 18, "大威"),
        (73, 1, "天道"),
    ],
)
def test_c106_jinjing_72_then_18(n, step, god):
    data = dayou_tianmu_position(n, source_profile="jinjing")
    assert data["outer_cycle"] == 72
    assert data["small_cycle"] == 18
    assert data["surplus"] == 0
    assert data["step_number"] == step
    assert data["god"] == god


def test_c106_tongzong_uses_direct_214_180_18_profile():
    first = dayou_tianmu_position(1, source_profile="tongzong")
    assert first["surplus"] == 214
    assert first["outer_cycle"] == 180
    assert first["small_cycle"] == 18
    assert first["adjusted_count"] == 215
    assert first["step_number"] == 17
    assert first["god"] == "大神"

    start = dayou_tianmu_position(3, source_profile="tongzong")
    assert start["adjusted_count"] == 217
    assert start["step_number"] == 1
    assert start["god"] == "天道"


def test_c106_profiles_remain_distinct_even_with_shared_path():
    jin = dayou_tianmu_position(3, source_profile="jinjing")
    tong = dayou_tianmu_position(3, source_profile="tongzong")
    assert jin["path"] == tong["path"]
    assert jin["rule_id"] != tong["rule_id"]
    assert jin["outer_cycle"] == 72
    assert tong["outer_cycle"] == 180
    assert jin["surplus"] == 0
    assert tong["surplus"] == 214


def test_c106_recent_work_deprecated_note_is_superseded_by_direct_recheck():
    note = RECENT_WORK_RECOVERY["old_reference_note"]
    assert "deprecated_reference" in note
    assert "确认+214/180/18本身有来源" in note
    assert RECENT_WORK_RECOVERY["file_commit_date"].startswith("2026-10-04")


def test_c106_requires_explicit_profile_and_positive_count():
    with pytest.raises(TypeError):
        dayou_tianmu_position(1)
    with pytest.raises(ValueError, match="jinjing/tongzong"):
        dayou_tianmu_position(1, source_profile="mixed")
    with pytest.raises(ValueError):
        dayou_tianmu_position(0, source_profile="jinjing")


def test_c106_catalog_has_no_default_profile():
    data = c106_catalog()
    assert data["source_profile_required"] is True
    assert data["default_profile"] is None
    assert data["path_length"] == 18
