import json
from pathlib import Path

import pytest

from kintaiyi.source_profiles import (
    MILITARY_P0_CROSSWALK,
    build_military_p0_source_variants,
)


CATALOG = Path("terminology/military-p0.json")


def _load():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def test_military_p0_catalog_matches_source_profile_crosswalk():
    data = _load()
    by_key = {entry["key"]: entry for entry in data["entries"]}

    for key in ("three_doors", "five_generals", "host_guest_relation"):
        entry = by_key[key]
        crosswalk = MILITARY_P0_CROSSWALK[key]

        assert entry["source_rule_refs"]["jinjing_siku_volume4"] == crosswalk["jinjing_rule_id"]
        assert entry["source_rule_refs"]["jingyou_fuying_volume4"] == crosswalk["jingyou_rule_id"]
        assert entry["c8_equivalent_formula"] is False
        assert crosswalk["c8_equivalent_formula"] is False


def test_three_doors_and_five_generals_allow_c8_role_only():
    data = _load()
    by_key = {entry["key"]: entry for entry in data["entries"]}

    assert "c8_upstream" in by_key["three_doors"]["source_profiles"]
    assert "c8_upstream" in by_key["five_generals"]["source_profiles"]

    wrapped = build_military_p0_source_variants(
        three_doors_profiles={
            "c8_upstream": {"layer_id": "C8-L2", "ready": True},
        },
        five_generals_profiles={
            "c8_upstream": {"layer_id": "C8-L2", "released": False},
        },
    )
    assert wrapped["three_doors"]["profiles"]["c8_upstream"]["layer_id"] == "C8-L2"
    assert wrapped["five_generals"]["profiles"]["c8_upstream"]["layer_id"] == "C8-L2"


def test_host_guest_relation_never_accepts_c8_as_source_replacement():
    data = _load()
    entry = next(e for e in data["entries"] if e["key"] == "host_guest_relation")

    assert "c8_upstream" not in entry["source_profiles"]
    with pytest.raises(ValueError):
        build_military_p0_source_variants(
            host_guest_relation_profiles={
                "c8_upstream": {"layer_id": "C8-L3"},
            }
        )


def test_effective_five_generals_is_integration_not_source_rule():
    data = _load()
    entry = next(e for e in data["entries"] if e["key"] == "effective_five_generals_readiness")

    assert entry["rule_id"] == "CORE-WUJIANG-READY"
    assert entry["canonical_source_rule"] is False
    assert any("不是《金镜》J4M-02原文" in note for note in entry["boundary_notes"])


def test_military_p0_profiles_remain_unmerged():
    data = _load()
    policy = data["cross_source_policy"]

    assert policy["canonical_selected"] is None
    assert policy["cross_source_merge"] is False
    assert policy["c8_formula_equivalent"] is False


def test_jingyou_five_generals_collation_is_resolved_in_p0_catalog():
    data = _load()
    profile = data["source_profiles"]["jingyou_fuying_volume4"]
    entry = next(e for e in data["entries"] if e["key"] == "five_generals")

    assert profile["pending_textual_uncertainty"] == []
    resolved = profile["resolved_collation"]["JF4M-02"]
    assert resolved["source_form"] == "大小将不相开"
    assert resolved["normalized_reading"] == "主客大小将无相关"
    assert resolved["normalized_semantics"] == "四将无同宫之关"
    assert any("四将无同宫之关" in note for note in entry["boundary_notes"])
