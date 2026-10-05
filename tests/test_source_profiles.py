import pytest

from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.jinjing_v4_military import fengyun_feiniao_zhuzhan
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.source_profiles import (
    MILITARY_P0_CROSSWALK,
    build_military_p0_source_variants,
    build_p0_source_variants,
    build_pattern_source_variants,
    build_weather_bird_source_variant,
)


def test_pattern_profiles_are_kept_separate_without_canonical_selection():
    data = build_pattern_source_variants(profiles={
        "tongzong_volume4": {"events": ["統宗格"]},
        "jinjing_geju": {"事件": [{"格局": "掩"}]},
    })
    assert data["cross_source_merge"] is False
    assert data["canonical_selected"] is None
    assert set(data["profiles"]) == {"tongzong_volume4", "jinjing_geju"}
    assert data["profiles"]["tongzong_volume4"] != data["profiles"]["jinjing_geju"]


def test_pattern_profile_rejects_unknown_source_name():
    with pytest.raises(ValueError):
        build_pattern_source_variants(profiles={"merged_best_guess": {"x": 1}})


def test_military_crosswalk_never_claims_c8_formula_equivalence():
    assert MILITARY_P0_CROSSWALK["three_doors"]["jinjing_rule_id"] == "J4M-01"
    assert MILITARY_P0_CROSSWALK["five_generals"]["jinjing_rule_id"] == "J4M-02"
    assert MILITARY_P0_CROSSWALK["host_guest_relation"]["jinjing_rule_id"] == "J4M-03"
    assert MILITARY_P0_CROSSWALK["three_doors"]["c8_equivalent_formula"] is False
    assert MILITARY_P0_CROSSWALK["five_generals"]["c8_equivalent_formula"] is False
    assert MILITARY_P0_CROSSWALK["host_guest_relation"]["c8_equivalent_formula"] is False


def test_three_doors_and_five_generals_can_store_c8_as_upstream_role_only():
    data = build_military_p0_source_variants(
        three_doors_profiles={
            "jinjing_siku_volume4": {"rule_id": "J4M-01", "status": "pending"},
            "c8_upstream": {"layer_id": "C8-L2", "value": True},
        },
        five_generals_profiles={
            "tongzong_volume5": {"value": "發"},
            "c8_upstream": {"layer_id": "C8-L2", "value": False},
        },
    )
    assert data["cross_source_merge"] is False
    assert data["three_doors"]["canonical_selected"] is None
    assert data["five_generals"]["canonical_selected"] is None
    assert data["three_doors"]["profiles"]["c8_upstream"]["layer_id"] == "C8-L2"


def test_host_guest_relation_rejects_c8_as_direct_replacement():
    with pytest.raises(ValueError):
        build_military_p0_source_variants(
            host_guest_relation_profiles={
                "c8_upstream": {"layer_id": "C8-L3"},
            }
        )


def test_c14_quarantines_source_sensitive_legacy_fields_with_specific_paths():
    expected = {
        "釋格局": "source_variants.patterns.profiles",
        "推三門具不具": "source_variants.military.three_doors.profiles",
        "推五將發不發": "source_variants.military.five_generals.profiles",
        "推主客相闗法": "source_variants.military.host_guest_relation.profiles",
    }
    for key, replacement in expected.items():
        item = classify_legacy_field(key)
        assert item["status"] == "quarantined"
        assert item["replacement"] == replacement


def _legacy_source_sensitive_snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "釋格局": {"格(始擊)": "旧统宗结果"},
        "推三門具不具": "旧三门断语",
        "推五將發不發": "旧五将断语",
        "推主客相闗法": "旧主客相关断语",
    }


def test_empty_source_profile_container_does_not_satisfy_replacement():
    snapshot = attach_v2_to_snapshot(
        _legacy_source_sensitive_snapshot(),
        source_variants=build_p0_source_variants(),
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.patterns.profiles",
        "source_variants.military.three_doors.profiles",
        "source_variants.military.five_generals.profiles",
        "source_variants.military.host_guest_relation.profiles",
    ]
    assert report["ready_for_v2_core_consumption"] is False


def test_explicit_source_profiles_clear_all_c17_replacement_gaps():
    source_variants = build_p0_source_variants(
        pattern_profiles={
            "tongzong_volume4": {"events": ["旧统宗结构化结果"]},
            "jinjing_geju": {"事件": [{"格局": "掩"}]},
        },
        three_doors_profiles={
            "tongzong_volume5": {"value": "具"},
            "jinjing_siku_volume4": {"rule_id": "J4M-01", "status": "pending"},
        },
        five_generals_profiles={
            "tongzong_volume5": {"value": "發"},
            "jinjing_siku_volume4": {"rule_id": "J4M-02", "status": "pending"},
        },
        host_guest_relation_profiles={
            "tongzong_volume5": {"value": "主客相关"},
            "jinjing_siku_volume4": {"rule_id": "J4M-03", "status": "pending"},
        },
    )
    snapshot = attach_v2_to_snapshot(
        _legacy_source_sensitive_snapshot(),
        source_variants=source_variants,
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True
    assert report["quarantined_key_count"] == 4


def test_legacy_source_sensitive_values_never_enter_analysis_implicitly():
    snapshot = attach_v2_to_snapshot(_legacy_source_sensitive_snapshot())
    v2 = snapshot["v2"]
    assert v2["analysis"]["patterns"] == {}
    assert v2["analysis"]["military"] == {}
    assert "釋格局" in v2["compat"]["quarantined_legacy_keys"]
    assert "推三門具不具" in v2["compat"]["quarantined_legacy_keys"]


def test_c35_weather_bird_legacy_field_requires_explicit_j4m11_profile():
    item = classify_legacy_field("推太乙風雲飛鳥助戰法")
    assert item["status"] == "quarantined"
    assert item["replacement"] == (
        "source_variants.military.weather_bird_support.profiles.jinjing_siku_volume4"
    )


def test_c35_weather_bird_profile_accepts_only_valid_j4m11_result():
    result = fengyun_feiniao_zhuzhan([
        {
            "phenomenon": "飞鸟",
            "action": "扶",
            "target": "主人阵",
        }
    ])
    wrapped = build_weather_bird_source_variant(jinjing_result=result)
    profile = wrapped["profiles"]["jinjing_siku_volume4"]
    assert profile["rule_id"] == "J4M-11"
    assert profile["computable"] is True
    assert wrapped["observation_required"] is True
    assert wrapped["legacy_flat_auto_promoted"] is False


def test_c35_weather_bird_profile_rejects_wrong_rule():
    with pytest.raises(ValueError, match="J4M-11"):
        build_weather_bird_source_variant(jinjing_result={
            "source_profile": "jinjing_siku_volume4",
            "ruleset": "jinjing-siku-v4-military-12",
            "rule_id": "J4M-12",
        })


def test_c35_weather_bird_structured_profile_clears_legacy_gap():
    result = fengyun_feiniao_zhuzhan([
        {
            "phenomenon": "飞鸟",
            "action": "扶",
            "target": "主人阵",
        }
    ])
    source_variants = {
        "military": {
            "weather_bird_support": build_weather_bird_source_variant(
                jinjing_result=result
            )
        }
    }
    snapshot = attach_v2_to_snapshot(
        {
            "太乙落宮": 1,
            "太乙": "乾",
            "推太乙風雲飛鳥助戰法": "旧flybird_wl断语",
        },
        source_variants=source_variants,
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert "推太乙風雲飛鳥助戰法" in report["quarantined_legacy_keys"]
    assert report["ready_for_v2_core_consumption"] is True


def test_c35_legacy_weather_bird_flat_value_never_auto_promotes():
    snapshot = attach_v2_to_snapshot({
        "太乙落宮": 1,
        "太乙": "乾",
        "推太乙風雲飛鳥助戰法": "旧flybird_wl断语",
    })
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.military.weather_bird_support.profiles.jinjing_siku_volume4"
    ]
    assert snapshot["v2"]["analysis"]["military"] == {}


def test_jingyou_p0_profiles_are_allowed_but_never_merged_with_jinjing():
    data = build_military_p0_source_variants(
        three_doors_profiles={
            "jinjing_siku_volume4": {"rule_id": "J4M-01"},
            "jingyou_fuying_volume4": {"rule_id": "JF4M-01"},
        },
        five_generals_profiles={
            "jinjing_siku_volume4": {"rule_id": "J4M-02"},
            "jingyou_fuying_volume4": {"rule_id": "JF4M-02"},
        },
        host_guest_relation_profiles={
            "jinjing_siku_volume4": {"rule_id": "J4M-03"},
            "jingyou_fuying_volume4": {"rule_id": "JF4M-03"},
        },
    )
    assert data["cross_source_merge"] is False
    assert data["three_doors"]["canonical_selected"] is None
    assert set(data["three_doors"]["profiles"]) == {
        "jinjing_siku_volume4", "jingyou_fuying_volume4"
    }
    assert data["three_doors"]["crosswalk"]["jinjing_rule_id"] == "J4M-01"
    assert data["three_doors"]["crosswalk"]["jingyou_rule_id"] == "JF4M-01"
    assert data["five_generals"]["crosswalk"]["jingyou_rule_id"] == "JF4M-02"
    assert data["host_guest_relation"]["crosswalk"]["jingyou_rule_id"] == "JF4M-03"
