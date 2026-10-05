import json
from pathlib import Path

import pytest

from kintaiyi.zitingjing_sources import RULES, build_zitingjing_rule_sources


CATALOG = Path("terminology/zitingjing.json")
WENCHANG = Path("terminology/wenchang-nine-stars.json")
MIGRATION = Path("terminology/zitingjing-migration-map.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_zitingjing_stable_catalog_excludes_wenchang_nine_stars_modern_appendix():
    data = _load(CATALOG)
    by_key = {entry["key"]: entry for entry in data["entries"]}

    assert set(by_key) == set(RULES) - {"wenchang_nine_stars"}
    assert len(by_key) == 5
    assert "wenchang_nine_stars" not in by_key

    for key, entry in by_key.items():
        assert entry["primary_evidence_level"] == RULES[key]["primary_evidence_level"]
        assert entry["preferred_term"] == RULES[key]["legacy_name"]


def test_primary_result_gate_matches_c18_runtime_for_ziting_stable_entries():
    data = _load(CATALOG)
    by_key = {entry["key"]: entry for entry in data["entries"]}

    direct = {"taiyi_nine_stars", "wenchang_changes", "shiji_changes"}
    blocked = {"three_banners", "nine_palace_nobles"}

    for key in direct:
        assert by_key[key]["primary_result_allowed"] is True
        wrapped = build_zitingjing_rule_sources(
            key,
            primary_result={"rule_key": key, "test": True},
        )
        assert wrapped["primary_ready"] is True
        assert wrapped["canonical_selected"] == "zitingjing"

    for key in blocked:
        assert by_key[key]["primary_result_allowed"] is False
        with pytest.raises(ValueError):
            build_zitingjing_rule_sources(
                key,
                primary_result={"rule_key": key, "test": True},
            )


def test_wenchang_nine_stars_keeps_legacy_source_slot_but_is_not_stable_ziting_term():
    migration = _load(MIGRATION)
    assert any(e["key"] == "wenchang_nine_stars" for e in migration["entries"])

    wrapped = build_zitingjing_rule_sources("wenchang_nine_stars")
    assert wrapped["primary_evidence_level"] == (
        "ziting_manuscript_not_attested_modern_appendix_only"
    )
    assert wrapped["status"] == "modern_appendix_cross_source_recovery_pointer"
    assert wrapped["primary_result_allowed"] is False
    assert wrapped["known_source_rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"


def test_independent_wenchang_catalog_is_tongzong_source_specific():
    data = _load(WENCHANG)
    entry = next(e for e in data["entries"] if e["key"] == "wenchang_nine_stars")

    assert data["catalog_id"] == "taiyi-wenchang-nine-stars-terminology-v1"
    assert entry["canonical_rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"
    assert entry["canonical_source_profile"] == (
        "tongzong_volume6_ngj_wenchang_nine_stars"
    )
    assert entry["ziting_manuscript_boundary"]["status"] == (
        "not_attested_in_manuscript_toc"
    )
    assert entry["ziting_manuscript_boundary"]["scan_pages"] == [5, 6]
    modern = entry["ziting_manuscript_boundary"]["modern_edition_appendix"]
    assert modern["status"] == "modern_edition_catalog_attested_provenance_unresolved"
    assert "来源假说" in modern["inference"]


def test_zitingjing_stable_catalog_preserves_migration_aliases_for_remaining_entries():
    catalog = _load(CATALOG)
    migration = _load(MIGRATION)

    stable = {entry["key"]: set(entry["aliases"]) for entry in catalog["entries"]}
    old = {entry["key"]: set(entry["aliases"]) for entry in migration["entries"]}

    for key in stable:
        assert old[key] <= stable[key]


def test_three_banners_and_nine_palace_nobles_are_cross_source_recovery_pointers():
    data = _load(CATALOG)
    by_key = {entry["key"]: entry for entry in data["entries"]}

    expected = {
        "three_banners": (
            "C126-TONGZONG-THREE-BANNERS",
            "tongzong_volume10_three_banners",
        ),
        "nine_palace_nobles": (
            "C127-TONGZONG-NINE-PALACE-NOBLES",
            "tongzong_volume10_nine_palace_nobles",
        ),
    }
    for key, (rule_id, profile) in expected.items():
        entry = by_key[key]
        assert entry["term_type"] == "legacy_cross_source_recovery_pointer"
        assert entry["primary_evidence_level"] == "ziting_not_attested_cross_source_only"
        assert entry["primary_result_allowed"] is False
        assert entry["canonical_selected"] is None
        assert entry["collation_sources"] == ["tongzong_volume10"]
        assert entry["known_executable_source_profile"] == profile
        source_profile = entry["source_specific_profiles"]["tongzong_volume10"]
        assert source_profile["rule_id"] == rule_id
        assert source_profile["source_profile"] == profile
        assert source_profile["status"] == "direct_source_specific_runtime"
        assert any("不代表紫庭已见同术" in note for note in entry["boundary_notes"])


def test_shiji_collation_keeps_ocr_corrections_separate_from_textual_variant():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "shiji_changes")

    assert entry["collation_status"].startswith("25_rows_collated")
    assert entry["ocr_corrections"] == [
        {"stem_group": "戊己", "witness_label": "水", "normalized_element": "木"},
        {"stem_group": "壬癸", "witness_label": "王", "normalized_element": "土"},
    ]
    assert "preserve_both_no_silent_merge" in entry["textual_variant_policy"]
