import pytest

from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.unported_catalog import catalog_unported_field
from kintaiyi.volume9_disaster_timing import (
    BRANCH_MONTH,
    LEGACY_REFERENCE_AUDIT,
    SOURCE_WITNESS,
    build_volume9_disaster_source_variant,
    disaster_day_from_evidence,
    disaster_month_from_evidence,
    disaster_timing_from_evidence,
    month_for_point,
    opposite_point,
)


def test_c45_records_witness_volume_variant():
    assert SOURCE_WITNESS["online_witness_volume"] == 10
    assert SOURCE_WITNESS["project_legacy_volume_label"] == 9
    assert SOURCE_WITNESS["volume_status"] == "witness_volume_variant"


def test_c45_branch_month_mapping():
    assert BRANCH_MONTH == {
        "寅": 1, "卯": 2, "辰": 3, "巳": 4, "午": 5, "未": 6,
        "申": 7, "酉": 8, "戌": 9, "亥": 10, "子": 11, "丑": 12,
    }
    assert month_for_point("辰") == 3
    assert month_for_point("戌") == 9
    assert month_for_point("艮") is None


def test_c45_opposite_uses_sixteen_point_ring():
    assert opposite_point("辰") == "戌"
    assert opposite_point("戌") == "辰"
    assert opposite_point("艮") == "坤"
    assert opposite_point("乾") == "巽"


def test_c45_source_example_wenchang_chen_means_march_and_opposite_september():
    data = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )
    assert data["wenchang_landing"] == "辰"
    assert data["disaster_month"] == 3
    assert data["opposite_landing"] == "戌"
    assert data["opposite_disaster_month"] == 9
    assert data["water_drought"] == "旱"
    assert data["tianmu_disaster_month"] == 8
    assert data["tianmu_opposite_disaster_month"] == 2
    assert data["computable"] is True


def test_c45_does_not_guess_palace_polarity_from_point():
    data = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )
    assert data["palace_polarity"] is None
    assert data["water_drought"] is None
    assert data["legacy_yang_palace_guess_used"] is False
    assert data["computable"] is False
    assert "阳宫或阴宫" in data["pending"][0]


def test_c45_yang_means_drought_yin_means_water_only_when_explicit():
    dry = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )
    wet = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阴",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )
    assert dry["water_drought"] == "旱"
    assert wet["water_drought"] == "水"


def test_c45_same_taiyi_or_source_pattern_marks_annual_disorder_but_not_month():
    same = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阳",
        wenchang_same_as_taiyi=True,
        pattern_evidence=[],
    )
    assert same["annual_disorder_triggered"] is True
    assert same["annual_disorder"] == "君臣不协、岁不丰稔"
    assert same["disaster_month"] == 3

    pattern = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
        pattern_evidence=["格", "挟"],
    )
    assert pattern["annual_disorder_triggered"] is True
    assert pattern["disaster_month"] == 3


def test_c45_no_taiyi_same_palace_and_no_patterns_means_no_disorder_trigger():
    data = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )
    assert data["annual_disorder_triggered"] is False
    assert data["annual_disorder"] is None


def test_c45_four_corner_landing_does_not_invent_month():
    data = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="艮",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )
    assert data["disaster_month"] is None
    assert data["opposite_landing"] == "坤"
    assert data["opposite_disaster_month"] is None
    assert data["computable"] is False
    assert len(data["pending"]) == 2


def test_c45_requires_explicit_pattern_check():
    data = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
    )
    assert data["computable"] is False
    assert data["annual_disorder_triggered"] is None
    assert data["pending"] == ["须显式检查格掩迫击挟提；无格局时传空list"]


def test_c45_day_stage_returns_branch_and_opposite_not_fake_calendar_day():
    data = disaster_day_from_evidence(
        month_branch="辰",
        month_hegod_anchor="午",
        wenchang_landing_after_month_addition="酉",
        tianmu_landing_after_month_addition="子",
    )
    assert data["disaster_day_branch"] == "酉"
    assert data["opposite_day_branch"] == "卯"
    assert data["specific_calendar_day"] is None
    assert data["specific_calendar_day_status"] == "source_gives_sixteen_point_period_not_calendar_day_number"
    assert data["tianmu_day_branch"] == "子"
    assert data["tianmu_opposite_day_branch"] == "午"
    assert data["addition_formula_applied"] is False


def test_c45_day_four_dimension_point_is_not_mislabeled_as_branch():
    data = disaster_day_from_evidence(
        month_branch="辰",
        month_hegod_anchor="午",
        wenchang_landing_after_month_addition="艮",
        tianmu_landing_after_month_addition="巽",
    )
    assert data["disaster_day_point"] == "艮"
    assert data["disaster_day_branch"] is None
    assert data["opposite_day_point"] == "坤"
    assert data["opposite_day_branch"] is None
    assert data["tianmu_day_point"] == "巽"
    assert data["tianmu_day_branch"] is None
    assert data["computable"] is True


def test_c45_missing_tianmu_keeps_each_stage_incomplete():
    month = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )
    assert month["computable"] is False
    assert "天目所临" in "；".join(month["pending"])

    day = disaster_day_from_evidence(
        month_branch="辰",
        month_hegod_anchor="午",
        wenchang_landing_after_month_addition="酉",
    )
    assert day["computable"] is False
    assert "天目所临" in "；".join(day["pending"])


def _month():
    return disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="丑",
        wenchang_landing_after_year_addition="辰",
        tianmu_landing_after_year_addition="酉",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )


def _day():
    return disaster_day_from_evidence(
        month_branch="辰",
        month_hegod_anchor="午",
        wenchang_landing_after_month_addition="酉",
        tianmu_landing_after_month_addition="子",
    )


def test_c45_month_only_is_partial_not_complete_rule():
    data = disaster_timing_from_evidence(_month())
    assert data["computable"] is False
    assert data["status"] == "partial_month_only"
    assert data["day_stage"] == {}


def test_c45_month_and_day_stages_complete_rule_without_merging_inputs():
    month = _month()
    day = _day()
    data = disaster_timing_from_evidence(month, day)
    assert data["computable"] is True
    assert data["status"] == "complete_month_day_timing"
    assert data["month_stage"]["disaster_month"] == 3
    assert data["day_stage"]["disaster_day_branch"] == "酉"
    assert data["cross_stage_merge"] is False


def test_c45_rejects_bad_stage_identity():
    with pytest.raises(ValueError):
        disaster_timing_from_evidence({"rule_id": "wrong"})
    with pytest.raises(ValueError):
        disaster_timing_from_evidence(_month(), {"rule_id": "wrong"})


def test_c45_rejects_unknown_pattern_or_invalid_branch():
    with pytest.raises(ValueError, match="未知"):
        disaster_month_from_evidence(
            year_branch="子",
            year_hegod_anchor="丑",
            wenchang_landing_after_year_addition="辰",
            tianmu_landing_after_year_addition="酉",
            palace_polarity="阳",
            wenchang_same_as_taiyi=False,
            pattern_evidence=["杜"],
        )
    with pytest.raises(ValueError, match="地支"):
        disaster_month_from_evidence(
            year_branch="艮",
            year_hegod_anchor="丑",
            wenchang_landing_after_year_addition="辰",
        )


def test_c45_legacy_reference_is_not_equivalent():
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    assert any("_YANG_GONG" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
    assert any("月层" in item for item in LEGACY_REFERENCE_AUDIT["issues"])


def test_c45_catalog_and_legacy_policy():
    item = catalog_unported_field("歲中災發")
    assert item["layer"] == "canonical"
    assert item["action"] == "use_c45_two_stage_explicit_evidence"
    assert item["migrate_whole"] is False
    assert "两" in item["notes"] or "兩" in item["notes"]

    legacy = classify_legacy_field("歲中災發")
    assert legacy["status"] == "quarantined"
    assert legacy["replacement"] == (
        "source_variants.volume9.disaster_timing.legacy_replacement"
    )


def _legacy_snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "歲中災發": {"旧": "单层月份offset"},
    }


def test_c45_old_flat_never_auto_promotes():
    snapshot = attach_v2_to_snapshot(_legacy_snapshot())
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.volume9.disaster_timing.legacy_replacement"
    ]
    assert "歲中災發" in snapshot["v2"]["compat"]["quarantined_legacy_keys"]


def test_c45_month_only_profile_does_not_clear_gap():
    partial = disaster_timing_from_evidence(_month())
    wrapped = build_volume9_disaster_source_variant(partial)
    assert wrapped["legacy_replacement"] == {}

    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants={
            "volume9": {
                "disaster_timing": wrapped,
            }
        },
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.volume9.disaster_timing.legacy_replacement"
    ]


def test_c45_complete_month_day_profile_clears_gap():
    complete = disaster_timing_from_evidence(_month(), _day())
    wrapped = build_volume9_disaster_source_variant(complete)
    assert wrapped["legacy_replacement"]["rule_id"] == "C45-V9-DISASTER"

    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants={
            "volume9": {
                "disaster_timing": wrapped,
            }
        },
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True


def test_c45_wrapper_rejects_wrong_rule_identity():
    with pytest.raises(ValueError, match="C45"):
        build_volume9_disaster_source_variant({
            "rule_id": "wrong",
            "source_profile": "tongzong_volume9_disaster_timing",
            "computable": True,
        })
