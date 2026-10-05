import json
from pathlib import Path

import pytest

from kintaiyi.zitingjing_sources import RULES, build_zitingjing_rule_sources


CATALOG = Path("terminology/zitingjing.json")
MIGRATION = Path("terminology/zitingjing-migration-map.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_zitingjing_catalog_covers_exactly_the_six_source_container_rules():
    data = _load(CATALOG)
    by_key = {entry["key"]: entry for entry in data["entries"]}

    assert set(by_key) == set(RULES)
    assert len(by_key) == 6

    for key, meta in RULES.items():
        assert by_key[key]["primary_evidence_level"] == meta["primary_evidence_level"]
        assert by_key[key]["preferred_term"] == meta["legacy_name"]


def test_primary_result_gate_matches_c18_runtime():
    data = _load(CATALOG)
    by_key = {entry["key"]: entry for entry in data["entries"]}

    direct = {"taiyi_nine_stars", "wenchang_changes", "shiji_changes"}
    blocked = {"wenchang_nine_stars", "three_banners", "nine_palace_nobles"}

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


def test_zitingjing_stable_catalog_preserves_migration_aliases():
    catalog = _load(CATALOG)
    migration = _load(MIGRATION)

    stable = {entry["key"]: set(entry["aliases"]) for entry in catalog["entries"]}
    old = {entry["key"]: set(entry["aliases"]) for entry in migration["entries"]}

    for key in stable:
        assert old[key] <= stable[key]


def test_wenchang_nine_stars_is_modern_appendix_cross_source_pointer():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "wenchang_nine_stars")

    assert entry["primary_evidence_level"] == "ziting_manuscript_not_attested_modern_appendix_only"
    assert entry["primary_result_allowed"] is False
    assert entry["runtime"] is None
    assert entry["canonical_selected"] is None
    assert entry["term_type"] == "modern_edition_cross_source_recovery_pointer"
    assert entry["canonical_catalog"] == "terminology/wenchang-nine-stars.json"
    assert entry["manuscript_toc_evidence"]["status"] == "title_not_attested"
    assert entry["modern_edition_appendix"]["status"] == "modern_edition_catalog_attested_provenance_unresolved"


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


def test_wenchang_modern_appendix_does_not_restore_ziting_primary():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "wenchang_nine_stars")

    assert entry["manuscript_toc_evidence"]["pages"] == [5, 6]
    assert entry["manuscript_toc_evidence"]["status"] == "title_not_attested"
    assert entry["modern_edition_appendix"]["title"] == "附太乙文昌九星值宮術"
    assert "只作来源假说" in entry["modern_edition_appendix"]["inference"]
    assert entry["primary_result_allowed"] is False
    assert entry["runtime"] is None
