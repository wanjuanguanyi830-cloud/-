import json
from pathlib import Path

from kintaiyi.source_profiles import build_pattern_source_variants


CATALOG = Path("terminology/patterns.json")
RULESET = Path("rules/jinjing/geju/ruleset.json")


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_pattern_terminology_covers_every_jinjing_ruleset_term():
    catalog = _load(CATALOG)
    ruleset = _load(RULESET)

    entries = [
        entry for entry in catalog["entries"]
        if entry.get("source_profile") == "jinjing_geju"
    ]
    for source_term in ruleset["rules"]:
        matches = [
            entry for entry in entries
            if source_term == entry["preferred_term"]
            or source_term in entry.get("aliases", [])
        ]
        assert len(matches) == 1, source_term


def test_pattern_profile_boundary_matches_runtime_container():
    catalog = _load(CATALOG)
    wrapped = build_pattern_source_variants(
        profiles={
            "jinjing_geju": {"ruleset": "jinjing-geju-1.0.0"},
            "tongzong_volume4": {"status": "structured_parallel_profile"},
        }
    )

    assert catalog["cross_source_policy"]["canonical_selected"] is None
    assert catalog["cross_source_policy"]["cross_source_merge"] is False
    assert wrapped["canonical_selected"] is None
    assert wrapped["cross_source_merge"] is False
    assert set(wrapped["profiles"]) == {"jinjing_geju", "tongzong_volume4"}


def test_jinjing_volume_three_and_four_terms_are_not_mislabelled():
    catalog = _load(CATALOG)
    by_term = {entry["preferred_term"]: entry for entry in catalog["entries"]}

    assert by_term["执提"]["source_volume"] == 4
    assert by_term["提格"]["source_volume"] == 4

    for term in (
        "掩", "击", "迫", "囚", "关", "格", "对",
        "提挟", "挟闭", "四郭固", "四郭杜",
    ):
        assert by_term[term]["source_volume"] == 3


def test_sigu_she_is_variant_only_not_canonical_output_term():
    catalog = _load(CATALOG)
    preferred = {entry["preferred_term"] for entry in catalog["entries"]}
    sigu_du = next(entry for entry in catalog["entries"] if entry["preferred_term"] == "四郭杜")

    assert "四郭社" not in preferred
    assert sigu_du["source_variants"] == ["四郭社"]
    assert any("不得成为主输出字段" in note for note in sigu_du["boundary_notes"])


def test_pattern_catalog_reuses_common_coordinate_catalog():
    catalog = _load(CATALOG)
    assert catalog["shared_catalog"] == "terminology/common-core.json"
