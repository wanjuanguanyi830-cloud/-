import pytest

from kintaiyi.ten_essences_tianshi import (
    LEGACY_AUDIT,
    SOURCE_WITNESS,
    SURPLUS_REJECTION,
    TIANSHI_PATHS,
    c56_catalog,
    tianshi_position,
)


def test_c56_tianshi_paths_are_yang_yin_opposites_and_both_forward():
    assert TIANSHI_PATHS["阳"] == (
        "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"
    )
    assert TIANSHI_PATHS["阴"] == (
        "申", "酉", "戌", "亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未"
    )


@pytest.mark.parametrize(
    "count,yang_branch,yin_branch",
    [
        (1, "寅", "申"),
        (2, "卯", "酉"),
        (6, "未", "丑"),
        (12, "丑", "未"),
        (13, "寅", "申"),
        (120, "丑", "未"),
        (121, "寅", "申"),
    ],
)
def test_c56_tianshi_120_12_boundaries(count, yang_branch, yin_branch):
    yang = tianshi_position(count, dun="阳")
    yin = tianshi_position(count, dun="阴")
    assert yang["branch"] == yang_branch
    assert yin["branch"] == yin_branch
    assert yang["small_cycle"] == yin["small_cycle"] == 12


def test_c56_zero_remainders_mean_cycle_end_not_zero():
    data = tianshi_position(120, dun="阳")
    assert data["big_cycle_remainder"] == 0
    assert data["big_cycle_year"] == 120
    assert data["small_cycle_remainder"] == 0
    assert data["small_cycle_year"] == 12
    assert data["path_index"] == 12
    assert data["branch"] == "丑"


def test_c56_preserves_taibai_internal_summary_variant_without_overriding_detail():
    witness = SOURCE_WITNESS["taibai_bingbei"]
    assert "阳遁起寅" in witness["detailed_formula"]
    assert "阴遁起申" in witness["detailed_formula"]
    assert "阳起申、阴起寅" in witness["intro_summary_variant"]
    assert "internal_witness_conflict" in witness["status"]

    data = tianshi_position(1, dun="阳")
    assert data["branch"] == "寅"
    assert "内部异文保留" in data["policy"]


def test_c56_wujing_supports_lushen_start_and_preserves_yin_detail():
    witness = SOURCE_WITNESS["wujing_zongyao"]
    assert "命起吕申" in witness["main"]
    assert "阴起武德" in witness["variant_addition"]


def test_c56_rejects_bang_surplus_two():
    data = tianshi_position(2, dun="阳")
    assert data["surplus_applied"] is False
    assert data["surplus_policy"]["witness_value"] == 2
    assert data["surplus_policy"]["apply"] is False
    assert "古经无此" in data["surplus_policy"]["reason"]


def test_c56_old_cycle_match_does_not_promote_legacy_formula():
    assert LEGACY_AUDIT["legacy_small_cycle"] == 12
    assert LEGACY_AUDIT["direct_small_cycle"] == 12
    assert LEGACY_AUDIT["canonical_equivalent"] is False


def test_c56_requires_explicit_valid_dun_and_positive_count():
    with pytest.raises(TypeError):
        tianshi_position(1)
    with pytest.raises(ValueError, match="dun须为阳/阴"):
        tianshi_position(1, dun="冬至")
    with pytest.raises(ValueError):
        tianshi_position(0, dun="阳")
    with pytest.raises(TypeError):
        tianshi_position(True, dun="阳")


def test_c56_catalog_keeps_cloud_omens_separate():
    data = c56_catalog()
    assert data["implemented"] == ["天时"]
    assert data["big_cycle"] == 120
    assert data["small_cycle"] == 12
    assert data["cloud_omen_runtime"] is False
    assert data["surplus_rejection"] == SURPLUS_REJECTION
