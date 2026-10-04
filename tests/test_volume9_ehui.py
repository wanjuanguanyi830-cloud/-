import pytest

from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.unported_catalog import catalog_unported_field
from kintaiyi.volume9_ehui import (
    DIRECTION_WITNESS,
    GOD_IDENTITIES,
    LEGACY_REFERENCE_AUDIT,
    build_volume9_ehui_source_variant,
    ehui_limit_from_evidence,
    han_gaozu_example,
    parse_ganzhi,
)


def test_c43_requires_full_enthronement_ganzhi_not_branch_only():
    assert parse_ganzhi("乙未") == {
        "stem": "乙",
        "branch": "未",
        "ganzhi": "乙未",
    }
    with pytest.raises(ValueError):
        parse_ganzhi("未")
    with pytest.raises(ValueError):
        parse_ganzhi("乙")
    with pytest.raises(ValueError):
        parse_ganzhi("乙天")


def test_c43_preserves_source_god_identities_and_direction_structure():
    assert GOD_IDENTITIES == {
        "大义": "天心",
        "太阳": "天罡",
        "阴主": "天魁",
    }
    assert DIRECTION_WITNESS["boundaries"] == ["大武", "和德"]
    assert DIRECTION_WITNESS["reverse_half"] == [
        "天道", "大威", "大神", "大炅", "太阳", "高丛", "吕申"
    ]
    assert DIRECTION_WITNESS["forward_half"] == [
        "武德", "太簇", "阴主", "阴德", "大义", "地主", "阳德"
    ]
    assert DIRECTION_WITNESS["status"] == "direct_text_structure_only"


def test_c43_legacy_reference_is_explicitly_not_equivalent():
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    assert any("year_zhi" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
    assert any("16位" in item for item in LEGACY_REFERENCE_AUDIT["issues"])


def test_c43_incomplete_inputs_are_not_computable():
    data = ehui_limit_from_evidence(enthronement_ganzhi="乙未")
    assert data["computable"] is False
    assert data["status"] == "not_computable"
    assert data["base_limit_years"] is None
    assert len(data["pending"]) == 4
    assert data["legacy_simple_step_formula_used"] is False


def test_c43_does_not_turn_landings_into_simple_step_distance():
    data = ehui_limit_from_evidence(
        enthronement_ganzhi="乙未",
        taiyang_landing="申",
        yinzhu_landing="寅",
        direction="逆",
    )
    assert data["computable"] is False
    assert data["base_limit_years"] is None
    assert data["pending"] == ["须提供原文神数累计证据，不以16位步数代替"]
    assert data["legacy_simple_step_formula_used"] is False


def test_c43_han_gaozu_example_reproduces_explicit_source_count():
    data = han_gaozu_example()
    assert data["enthronement"]["ganzhi"] == "乙未"
    assert data["taiyang"]["landing"] == "申"
    assert data["yinzhu"]["landing"] == "寅"
    assert data["direction"] == "逆"
    assert data["count_evidence"] == [
        {"label": "起数", "value": 1},
        {"label": "大威", "value": 2},
        {"label": "大炅", "value": 9},
        {"label": "高丛", "value": 4},
    ]
    assert data["base_limit_years"] == 16
    assert data["computable"] is True
    assert data["status"] == "computed_from_explicit_source_evidence"


def test_c43_han_example_keeps_year12_taiyi_ge_as_separate_correction():
    data = han_gaozu_example()
    assert data["base_limit_years"] == 16
    assert data["corrections_applied"] is False
    assert data["correction_evidence"] == [
        {
            "year": 12,
            "condition": "太乙入六十七局，丙午与太岁格",
            "effect": "主崩亡",
        }
    ]


def test_c43_count_evidence_is_explicit_not_hidden_formula():
    data = ehui_limit_from_evidence(
        enthronement_ganzhi="甲子",
        taiyang_landing="辰",
        yinzhu_landing="戌",
        direction="顺",
        count_evidence=[
            {"label": "起数", "value": 1},
            {"label": "某神", "value": 8},
        ],
    )
    assert data["base_limit_years"] == 9
    assert data["count_evidence"] == [
        {"label": "起数", "value": 1},
        {"label": "某神", "value": 8},
    ]


def test_c43_rejects_bad_point_direction_or_count_shape():
    with pytest.raises(ValueError):
        ehui_limit_from_evidence(
            enthronement_ganzhi="甲子",
            taiyang_landing="中",
        )
    with pytest.raises(ValueError):
        ehui_limit_from_evidence(
            enthronement_ganzhi="甲子",
            direction="左",
        )
    with pytest.raises(TypeError):
        ehui_limit_from_evidence(
            enthronement_ganzhi="甲子",
            count_evidence=["大威2"],
        )


def test_c43_catalog_marks_old_formula_as_non_wholesale_migration():
    item = catalog_unported_field("厄會行限")
    assert item["layer"] == "canonical"
    assert item["source_scope"] == "tongzong_volume9_direct_strict_contract"
    assert item["action"] == "use_c43_explicit_evidence_contract"
    assert item["migrate_whole"] is False
    assert "16位步数" in item["notes"]


def test_c43_legacy_field_is_quarantined_to_volume9_source_slot():
    item = classify_legacy_field("厄會行限")
    assert item["status"] == "quarantined"
    assert item["replacement"] == (
        "source_variants.volume9.ehui_limit.legacy_replacement"
    )


def _legacy_snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "厄會行限": {"旧": "按year_zhi简单16位步数"},
    }


def test_c43_old_flat_value_never_auto_promotes():
    snapshot = attach_v2_to_snapshot(_legacy_snapshot())
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.volume9.ehui_limit.legacy_replacement"
    ]
    assert snapshot["v2"]["analysis"]["patterns"] == {}
    assert "厄會行限" in snapshot["v2"]["compat"]["quarantined_legacy_keys"]


def test_c43_incomplete_structured_contract_does_not_clear_gap():
    incomplete = ehui_limit_from_evidence(enthronement_ganzhi="乙未")
    variants = {
        "volume9": {
            "ehui_limit": build_volume9_ehui_source_variant(incomplete)
        }
    }
    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants=variants,
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.volume9.ehui_limit.legacy_replacement"
    ]


def test_c43_complete_source_evidence_clears_legacy_gap():
    complete = han_gaozu_example()
    wrapped = build_volume9_ehui_source_variant(complete)
    assert wrapped["legacy_replacement"] == {
        "source_replacement_complete": True,
        "rule_id": "C43-V9-EHUI",
    }

    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants={"volume9": {"ehui_limit": wrapped}},
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True


def test_c43_source_variant_wrapper_rejects_wrong_rule_identity():
    with pytest.raises(ValueError, match="C43"):
        build_volume9_ehui_source_variant({
            "rule_id": "wrong",
            "source_profile": "tongzong_volume9_ehui_limit",
            "computable": True,
        })
