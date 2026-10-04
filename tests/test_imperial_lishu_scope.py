import pytest

from kintaiyi.imperial_lishu_scope import (
    LEGACY_REFERENCE_AUDIT,
    SCOPE,
    assemble_imperial_lishu_evidence,
    c50_catalog,
    imperial_lishu_scope,
)
from kintaiyi.taiyou_limit_tracks import bailiu_inner_track
from kintaiyi.xiaoyou_hexagram import xiaoyou_heavy_hexagram
from kintaiyi.xiaoyou_line_omens import xiaoyou_line_omens
from kintaiyi.volume9_ehui import han_gaozu_example


def _x47():
    return xiaoyou_heavy_hexagram(5)


def _x48():
    return xiaoyou_line_omens(
        _x47(),
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )


def test_c50_scope_subject_and_no_single_total_year_formula():
    data = imperial_lishu_scope()
    assert data["scope"]["subject"] == "帝王应天顺人始终之期"
    assert data["scope"]["independent_total_year_formula_attested"] is False
    assert data["specific_end_year"] is None
    assert data["single_formula_applied"] is False


def test_c50_base_method_records_taiyang_yinzhu_and_hegod_four_periods():
    base = SCOPE["base_ehui_method"]
    assert base["accession_year_branch_plus"] == "大义"
    assert base["primary_targets"] == ["太阳", "阴主"]
    assert base["hegod_extension"] is True
    assert base["four_period_structure"] == "太阳及其合神、阴主及其合神"
    assert base["implemented_runtime_dependency"] == "C43-V9-EHUI"


def test_c50_explicitly_excludes_c42_as_replacement_formula():
    exclusions = SCOPE["explicit_exclusions"]
    assert "C42" in exclusions
    assert "不等于C50帝王始终总纲" in exclusions["C42"]


def test_c50_correction_layers_point_to_existing_source_units():
    layers = {item["dependency"]: item for item in SCOPE["correction_layers"]}
    assert set(layers) == {"C38", "C47", "C48", "pattern_evidence"}
    assert all(item["role"] == "correction_evidence" for item in layers.values())


def test_c50_accession_cloud_is_explicitly_deferred():
    cloud = SCOPE["accession_cloud_layer"]
    assert cloud["status"] == "pending_separate_source_unit"
    assert "不并入C50总纲算法" in cloud["reason"]


def test_c50_empty_evidence_bundle_is_partial_and_never_computes_end_year():
    data = assemble_imperial_lishu_evidence()
    assert data["evidence_ready"] is False
    assert data["status"] == "partial_evidence"
    assert data["specific_end_year"] is None
    assert data["specific_end_year_computed"] is False
    assert data["single_formula_applied"] is False
    assert "缺基础厄会C43证据" in data["pending"]
    assert "缺太阳/阴主合神四神期的显式核对" in data["pending"]


def test_c50_full_explicit_evidence_becomes_ready_but_still_no_end_year():
    data = assemble_imperial_lishu_evidence(
        ehui=han_gaozu_example(),
        taiyou_inner=bailiu_inner_track(1),
        xiaoyou_hexagram=_x47(),
        xiaoyou_omens=_x48(),
        pattern_evidence=[],
        hegod_period_evidence=[
            {"target": "太阳合神", "period": "未"},
            {"target": "阴主合神", "period": "丑"},
        ],
    )
    assert data["evidence_ready"] is True
    assert data["status"] == "evidence_bundle_ready"
    assert data["pending"] == []
    assert data["specific_end_year"] is None
    assert data["specific_end_year_computed"] is False
    assert data["single_formula_applied"] is False


def test_c50_optional_correction_layers_can_be_absent_without_faking_formula():
    data = assemble_imperial_lishu_evidence(
        ehui=han_gaozu_example(),
        pattern_evidence=[],
        hegod_period_evidence=[],
    )
    assert data["evidence_ready"] is True
    assert data["correction_layers"]["taiyou_inner"] == {}
    assert data["correction_layers"]["xiaoyou_hexagram"] == {}
    assert data["correction_layers"]["xiaoyou_omens"] == {}
    assert data["specific_end_year"] is None


def test_c50_requires_explicit_pattern_check_even_if_no_patterns():
    data = assemble_imperial_lishu_evidence(
        ehui=han_gaozu_example(),
        hegod_period_evidence=[],
    )
    assert data["evidence_ready"] is False
    assert "无格局时传空list" in "；".join(data["pending"])


def test_c50_hegod_check_must_be_explicit_even_when_no_extra_periods():
    data = assemble_imperial_lishu_evidence(
        ehui=han_gaozu_example(),
        pattern_evidence=[],
    )
    assert data["evidence_ready"] is False
    assert "合神四神期" in "；".join(data["pending"])


def test_c50_rejects_wrong_rule_identities():
    with pytest.raises(ValueError, match="C43-V9-EHUI"):
        assemble_imperial_lishu_evidence(
            ehui={"rule_id": "wrong"},
            pattern_evidence=[],
            hegod_period_evidence=[],
        )

    with pytest.raises(ValueError, match="C38-BL-INNER"):
        assemble_imperial_lishu_evidence(
            taiyou_inner={"rule_id": "wrong"},
        )

    with pytest.raises(ValueError, match="C47-XY-HEX"):
        assemble_imperial_lishu_evidence(
            xiaoyou_hexagram={"rule_id": "wrong"},
        )

    with pytest.raises(ValueError, match="C48-XY-OMEN"):
        assemble_imperial_lishu_evidence(
            xiaoyou_omens={"rule_id": "wrong"},
        )


def test_c50_rejects_bad_evidence_container_shapes():
    with pytest.raises(TypeError, match="pattern_evidence"):
        assemble_imperial_lishu_evidence(pattern_evidence={"格": True})

    with pytest.raises(TypeError, match="hegod_period_evidence"):
        assemble_imperial_lishu_evidence(hegod_period_evidence=["未", "丑"])


def test_c50_legacy_functions_are_not_equivalent_to_scope_contract():
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    assert "guiyun.lishu_changduan" in LEGACY_REFERENCE_AUDIT["legacy_locations"]
    assert "guiyun.ehui_xingxian" in LEGACY_REFERENCE_AUDIT["legacy_locations"]
    assert any("不能代替C50" in item for item in LEGACY_REFERENCE_AUDIT["issues"])


def test_c50_catalog_has_no_runtime_total_year_formula():
    data = c50_catalog()
    assert data["rule_id"] == "C50-V10-LISHU-SCOPE"
    assert data["scope"]["independent_total_year_formula_attested"] is False
    assert data["legacy_reference_audit"]["canonical_equivalent"] is False
