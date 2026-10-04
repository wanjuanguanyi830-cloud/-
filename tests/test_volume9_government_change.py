import pytest

from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.volume9_government_change import (
    BAD_PATTERNS,
    COLLATION_VARIANTS,
    GOVERNMENT_GOD_SUBJECTS,
    LEGACY_REFERENCE_AUDIT,
    build_volume9_government_change_source_variant,
    government_change_distance,
    government_change_from_evidence,
)


def _landings():
    return {
        "太簇": "子",
        "太阳": "丑",
        "阴主": "寅",
        "地主": "卯",
        "武德": "辰",
        "大义": "巽",
    }


def test_c44_six_god_subjects_stay_separate():
    assert GOVERNMENT_GOD_SUBJECTS["太簇"] == [
        "国政革易", "法令变更", "风俗改常", "服色更易"
    ]
    assert GOVERNMENT_GOD_SUBJECTS["太阳"] == ["纪律隳废", "厄会兵刃"]
    assert GOVERNMENT_GOD_SUBJECTS["阴主"] == ["奸臣匿谋", "凶丧祸乱"]
    assert GOVERNMENT_GOD_SUBJECTS["地主"] == ["礼仪废失", "口舌谣言"]
    assert GOVERNMENT_GOD_SUBJECTS["武德"] == ["迁移易地", "创营宫室"]
    assert GOVERNMENT_GOD_SUBJECTS["大义"] == ["毁折废弃"]


def test_c44_preserves_destruction_and_jiazi_year_variants():
    destruction = COLLATION_VARIANTS["destruction_subject"]
    assert destruction["tongzong"] == ["大义"]
    assert destruction["taibai_bingbei"] == ["大神", "大义"]
    assert destruction["canonical_selected"] is None

    near = COLLATION_VARIANTS["jiazi_near_years"]
    assert near["tongzong_online_witness"] == [9, 28]
    assert near["taibai_bingbei"] == [9, 18]
    assert near["canonical_selected"] is None


@pytest.mark.parametrize(
    "length,harmony,distance,status",
    [
        ("长", True, "远", "direct"),
        ("短", False, "近", "direct"),
        ("长", False, None, "not_defined_by_source_passage"),
        ("短", True, None, "not_defined_by_source_passage"),
        (None, True, None, "not_computable"),
        ("长", None, None, "not_computable"),
    ],
)
def test_c44_distance_only_uses_explicit_source_combinations(
    length, harmony, distance, status
):
    data = government_change_distance(
        calculation_length=length,
        calculation_harmony=harmony,
    )
    assert data["distance_class"] == distance
    assert data["status"] == status


def test_c44_requires_real_sexagenary_event_ganzhi():
    with pytest.raises(ValueError, match="六十甲子"):
        government_change_from_evidence(
            event_ganzhi="甲丑",
            god_landings=_landings(),
            calculation_length="长",
            calculation_harmony=True,
        )


def test_c44_incomplete_landings_do_not_compute():
    data = government_change_from_evidence(
        event_ganzhi="甲子",
        god_landings={"太簇": "子"},
        calculation_length="长",
        calculation_harmony=True,
    )
    assert data["computable"] is False
    assert "须提供吕申加创立新事之年后六神所临" in data["pending"]
    assert data["automatic_lvshen_transform_used"] is False
    assert data["legacy_fixed_offset_formula_used"] is False


def test_c44_complete_evidence_records_ganzhi_numbers_and_manifestations():
    data = government_change_from_evidence(
        event_ganzhi="甲子",
        god_landings=_landings(),
        calculation_length="长",
        calculation_harmony=True,
        patterns_by_god={
            "太阳": ["格"],
            "大义": ["杜固"],
        },
    )
    assert data["computable"] is True
    assert data["status"] == "computed_from_explicit_source_evidence"
    assert data["ganzhi_numbers"] == {
        "stem": 9,
        "branch": 9,
        "sum": 18,
        "source_dependency": "C42纳甲干支数表",
    }
    assert data["distance"]["distance_class"] == "远"
    assert data["bad_change_evidence"] is True

    rows = {row["god"]: row for row in data["manifestations"]}
    assert rows["太阳"]["landing"] == "丑"
    assert rows["太阳"]["bad_patterns"] == ["格"]
    assert rows["大义"]["bad_patterns"] == ["杜固"]


def test_c44_bad_patterns_are_explicit_per_god():
    assert set(BAD_PATTERNS) == {"关", "囚", "迫", "掩", "击", "格", "挟", "杜固"}

    with pytest.raises(ValueError, match="未知凶格"):
        government_change_from_evidence(
            event_ganzhi="甲子",
            god_landings=_landings(),
            calculation_length="长",
            calculation_harmony=True,
            patterns_by_god={"太簇": ["旺"]},
        )


def test_c44_legacy_reference_is_not_canonical_equivalent():
    assert LEGACY_REFERENCE_AUDIT["function"] == "guiyun.guozheng_bianyi"
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    joined = "；".join(LEGACY_REFERENCE_AUDIT["issues"])
    assert "offset" in joined
    assert "18/28" in joined


def test_c44_variant_only_completes_with_full_evidence():
    incomplete = government_change_from_evidence(
        event_ganzhi="甲子",
        god_landings={"太簇": "子"},
        calculation_length="长",
        calculation_harmony=True,
    )
    assert build_volume9_government_change_source_variant(incomplete)[
        "legacy_replacement"
    ] == {}

    complete = government_change_from_evidence(
        event_ganzhi="甲子",
        god_landings=_landings(),
        calculation_length="短",
        calculation_harmony=False,
    )
    wrapped = build_volume9_government_change_source_variant(complete)
    assert wrapped["legacy_replacement"] == {
        "source_replacement_complete": True,
        "rule_id": "C44-V9-GUOZHENG",
    }


def test_c44_rejects_unknown_god_landing_and_bad_shapes():
    bad = _landings()
    bad["天乙"] = "午"
    with pytest.raises(ValueError, match="未知神"):
        government_change_from_evidence(
            event_ganzhi="甲子",
            god_landings=bad,
            calculation_length="长",
            calculation_harmony=True,
        )
    with pytest.raises(TypeError):
        government_change_from_evidence(
            event_ganzhi="甲子",
            god_landings=[],
        )


def test_c44_migration_gap_clears_only_for_complete_contract():
    legacy = {
        "太乙落宮": 1,
        "太乙": "乾",
        "國政章易": {"旧": True},
    }

    incomplete = build_volume9_government_change_source_variant(
        government_change_from_evidence(
            event_ganzhi="甲子",
            god_landings={"太簇": "子"},
            calculation_length="长",
            calculation_harmony=True,
        )
    )
    snapshot = attach_v2_to_snapshot(
        legacy,
        source_variants={"volume9": {"government_change": incomplete}},
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.volume9.government_change.legacy_replacement"
    ]

    complete = build_volume9_government_change_source_variant(
        government_change_from_evidence(
            event_ganzhi="甲子",
            god_landings=_landings(),
            calculation_length="短",
            calculation_harmony=False,
        )
    )
    snapshot = attach_v2_to_snapshot(
        legacy,
        source_variants={"volume9": {"government_change": complete}},
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
