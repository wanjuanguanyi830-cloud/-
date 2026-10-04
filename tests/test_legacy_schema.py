from kintaiyi.legacy_schema import (
    LEGACY_SCHEMA_POLICY_VERSION,
    classify_legacy_field,
    legacy_field_manifest,
    replacement_path_for_legacy,
)


def test_migrated_fact_has_single_v2_target():
    data = classify_legacy_field("太乙落宮")
    assert data["policy_version"] == LEGACY_SCHEMA_POLICY_VERSION
    assert data["status"] == "migrated_fact"
    assert data["target"] == "board.taiyi.palace"
    assert data["replacement"] is None


def test_quarantined_field_declares_structured_replacement():
    data = classify_legacy_field("軍事戰略")
    assert data["status"] == "quarantined"
    assert data["target"] == "compat.quarantined_legacy_keys"
    assert data["replacement"] == "analysis.military"
    assert replacement_path_for_legacy("軍事戰略") == "analysis.military"


def test_old_seven_method_and_game_theory_replacements_are_explicit():
    assert replacement_path_for_legacy("推猛虎相拒") == "analysis.seven_methods"
    assert replacement_path_for_legacy("運籌博弈分析") == "modern.game_theory"


def test_unknown_legacy_field_is_unported_not_guessed():
    data = classify_legacy_field("卷十二")
    assert data["status"] == "unported"
    assert data["target"] is None
    assert data["replacement"] is None


def test_embedded_v2_is_special_not_legacy_fact():
    data = classify_legacy_field("v2")
    assert data["status"] == "embedded_v2"
    assert data["target"] == "v2"


def test_manifest_classifies_each_field_once():
    manifest = legacy_field_manifest({
        "太乙落宮": 1,
        "軍事戰略": {"legacy": True},
        "卷十二": {"legacy": True},
        "v2": {"schema_version": "2.0"},
    })
    assert manifest["derived_migration_metadata"] is True
    assert manifest["field_count"] == 4
    assert manifest["counts"] == {
        "migrated_fact": 1,
        "quarantined": 1,
        "unported": 1,
        "embedded_v2": 1,
    }


def test_simplified_and_traditional_aliases_share_policy():
    trad = classify_legacy_field("太乙落宮")
    simp = classify_legacy_field("太乙落宫")
    assert trad["status"] == simp["status"] == "migrated_fact"
    assert trad["target"] == simp["target"] == "board.taiyi.palace"

    trad = classify_legacy_field("軍事戰略")
    simp = classify_legacy_field("军事战略")
    assert trad["replacement"] == simp["replacement"] == "analysis.military"
