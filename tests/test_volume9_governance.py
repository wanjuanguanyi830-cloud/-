import pytest

from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.unported_catalog import catalog_unported_field
from kintaiyi.volume9_governance import (
    GOD_EFFECTS,
    LEGACY_REFERENCE_AUDIT,
    REQUIRED_GODS,
    SOURCE_VARIANTS,
    SOURCE_WITNESS,
    build_volume9_governance_source_variant,
    governance_change_from_evidence,
    parse_ganzhi,
)


def _landings():
    return {
        "太簇": "酉",
        "太阳": "辰",
        "阴主": "戌",
        "地主": "子",
        "武德": "申",
        "大义": "亥",
    }


def test_c44_records_witness_volume_variant():
    assert SOURCE_WITNESS["online_witness_volume"] == 10
    assert SOURCE_WITNESS["project_legacy_volume_label"] == 9
    assert SOURCE_WITNESS["volume_status"] == "witness_volume_variant"


def test_c44_requires_full_foundation_ganzhi():
    assert parse_ganzhi("甲子")["branch"] == "子"
    with pytest.raises(ValueError):
        parse_ganzhi("子")
    with pytest.raises(ValueError):
        parse_ganzhi("甲")
    with pytest.raises(ValueError, match="六十甲子"):
        parse_ganzhi("甲丑")
    with pytest.raises(ValueError, match="六十甲子"):
        parse_ganzhi("乙寅")


def test_c44_direct_six_god_effects_are_stable():
    assert REQUIRED_GODS == ("太簇", "太阳", "阴主", "地主", "武德", "大义")
    assert GOD_EFFECTS["太簇"] == "国政革易、法令变更、风俗改常、服色更易"
    assert GOD_EFFECTS["太阳"] == "纪律隳废、厄会兵刃"
    assert GOD_EFFECTS["阴主"] == "奸臣匿谋、凶丧祸乱"
    assert GOD_EFFECTS["地主"] == "礼仪废失、口舌谣言"
    assert GOD_EFFECTS["武德"] == "迁移易地、创营宫室"
    assert GOD_EFFECTS["大义"] == "毁折废弃"


def test_c44_preserves_six_vs_seven_god_source_variant():
    assert SOURCE_VARIANTS["tongzong"]["required_gods"] == list(REQUIRED_GODS)
    assert SOURCE_VARIANTS["tongzong"]["extra_gods"] == []
    assert SOURCE_VARIANTS["taibai_bingbei"]["extra_gods"] == ["大神"]


def test_c44_preserves_far_and_near_year_variants_without_selection():
    assert SOURCE_VARIANTS["tongzong"]["far_year_examples"] == [90, 180]
    assert SOURCE_VARIANTS["taibai_bingbei"]["far_year_examples"] == [90, 180]
    assert SOURCE_VARIANTS["tongzong"]["near_year_examples"] == [9, 28]
    assert SOURCE_VARIANTS["taibai_bingbei"]["near_year_examples"] == [9, 18]


def test_c44_legacy_reference_is_not_equivalent():
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    assert any("year_zhi" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
    assert any("90/190" in item for item in LEGACY_REFERENCE_AUDIT["issues"])


def test_c44_missing_explicit_inputs_stays_not_computable():
    data = governance_change_from_evidence(foundation_ganzhi="甲子")
    assert data["computable"] is False
    assert data["status"] == "not_computable"
    assert data["landing_formula_applied"] is False
    assert len(data["pending"]) == 9


def test_c44_long_harmonious_only_selects_far_class_not_specific_year():
    data = governance_change_from_evidence(
        foundation_ganzhi="甲子",
        god_landings=_landings(),
        calc_length="长",
        calc_harmonious=True,
        pattern_evidence={},
    )
    assert data["computable"] is True
    assert data["foundation_ganzhi_numbers"] == {
        "stem": 9,
        "branch": 9,
        "sum": 18,
        "source_dependency": "C42纳甲干支数表",
        "used_to_auto_select_year": False,
    }
    assert data["timing"]["distance_class"] == "远"
    assert data["timing"]["witness_candidates"] == {
        "tongzong": [90, 180],
        "taibai_bingbei": [90, 180],
    }
    assert data["timing"]["canonical_year_selected"] is None
    assert data["timing"]["source_variant_unresolved"] is True


def test_c44_short_unharmonious_keeps_9_28_vs_9_18_variant():
    data = governance_change_from_evidence(
        foundation_ganzhi="丙寅",
        god_landings=_landings(),
        calc_length="短",
        calc_harmonious=False,
        pattern_evidence={},
    )
    assert data["timing"]["distance_class"] == "近"
    assert data["timing"]["witness_candidates"]["tongzong"] == [9, 28]
    assert data["timing"]["witness_candidates"]["taibai_bingbei"] == [9, 18]
    assert data["timing"]["canonical_year_selected"] is None


def test_c44_mixed_length_harmony_combo_does_not_invent_rule():
    data = governance_change_from_evidence(
        foundation_ganzhi="甲子",
        god_landings=_landings(),
        calc_length="长",
        calc_harmonious=False,
        pattern_evidence={},
    )
    assert data["computable"] is True
    assert data["timing"]["status"] == "mixed_or_unattested_combination"
    assert data["timing"]["distance_class"] is None
    assert data["timing"]["witness_candidates"] == {}


def test_c44_pattern_evidence_stays_separate_from_base_effect():
    data = governance_change_from_evidence(
        foundation_ganzhi="甲子",
        god_landings=_landings(),
        calc_length="长",
        calc_harmonious=True,
        pattern_evidence={
            "太簇": ["关"],
            "太阳": ["掩", "格"],
        },
    )
    assert data["events"]["太簇"]["effect"] == GOD_EFFECTS["太簇"]
    assert data["events"]["太簇"]["patterns"] == ["关"]
    assert data["events"]["太阳"]["patterns"] == ["掩", "格"]
    assert data["patterns_applied_to_base"] is False


def test_c44_optional_taibai_dasheng_is_kept_as_variant_not_required_core():
    landings = _landings()
    landings["大神"] = "巳"
    data = governance_change_from_evidence(
        foundation_ganzhi="甲子",
        god_landings=landings,
        calc_length="长",
        calc_harmonious=True,
        pattern_evidence={},
    )
    assert data["computable"] is True
    assert data["events"]["大神"]["landing"] == "巳"
    assert "参校本" in data["events"]["大神"]["effect"]


def test_c44_requires_explicit_pattern_check_even_when_no_pattern():
    data = governance_change_from_evidence(
        foundation_ganzhi="甲子",
        god_landings=_landings(),
        calc_length="长",
        calc_harmonious=True,
    )
    assert data["computable"] is False
    assert data["pending"] == ["须显式提供六神落宫格局证据；无格局时传空dict"]


def test_c44_rejects_unknown_god_or_invalid_landing():
    with pytest.raises(ValueError, match="未知"):
        governance_change_from_evidence(
            foundation_ganzhi="甲子",
            god_landings={**_landings(), "天游太乙": "子"},
        )
    bad = _landings()
    bad["太簇"] = "中"
    with pytest.raises(ValueError, match="太簇"):
        governance_change_from_evidence(
            foundation_ganzhi="甲子",
            god_landings=bad,
        )


def test_c44_catalog_and_legacy_policy():
    item = catalog_unported_field("國政章易")
    assert item["layer"] == "canonical"
    assert item["action"] == "use_c44_explicit_evidence_contract"
    assert item["migrate_whole"] is False
    assert "90/190" in item["notes"]

    legacy = classify_legacy_field("國政章易")
    assert legacy["status"] == "quarantined"
    assert legacy["replacement"] == (
        "source_variants.volume9.governance_change.legacy_replacement"
    )


def _legacy_snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "國政章易": {"旧": "year_zhi静态旋转"},
    }


def test_c44_old_flat_never_auto_promotes():
    snapshot = attach_v2_to_snapshot(_legacy_snapshot())
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.volume9.governance_change.legacy_replacement"
    ]
    assert "國政章易" in snapshot["v2"]["compat"]["quarantined_legacy_keys"]


def test_c44_incomplete_profile_does_not_clear_gap():
    result = governance_change_from_evidence(foundation_ganzhi="甲子")
    wrapped = build_volume9_governance_source_variant(result)
    assert wrapped["legacy_replacement"] == {}

    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants={
            "volume9": {
                "governance_change": wrapped,
            }
        },
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.volume9.governance_change.legacy_replacement"
    ]


def test_c44_complete_profile_clears_gap():
    result = governance_change_from_evidence(
        foundation_ganzhi="甲子",
        god_landings=_landings(),
        calc_length="长",
        calc_harmonious=True,
        pattern_evidence={},
    )
    wrapped = build_volume9_governance_source_variant(result)
    assert wrapped["legacy_replacement"]["rule_id"] == "C44-V9-GOV"

    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants={
            "volume9": {
                "governance_change": wrapped,
            }
        },
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True


def test_c44_wrapper_rejects_wrong_rule_identity():
    with pytest.raises(ValueError, match="C44"):
        build_volume9_governance_source_variant({
            "rule_id": "wrong",
            "source_profile": "tongzong_volume9_governance_change",
            "computable": True,
        })
