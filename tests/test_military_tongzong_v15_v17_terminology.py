import importlib
import json
from pathlib import Path

from kintaiyi.cross_volume_helpers import c32_catalog
from kintaiyi.military_rule_units import military_rule_unit_catalog
from kintaiyi.tongzong_v15_low_dependency import c23_catalog
from kintaiyi.tongzong_v15_observations import c24_catalog
from kintaiyi.tongzong_v15_wind_sound import c25_catalog
from kintaiyi.tongzong_v15_remaining import remaining_v15_catalog
from kintaiyi.tongzong_v17_low_dependency import c26_catalog
from kintaiyi.tongzong_v17_structured import c27_catalog
from kintaiyi.tongzong_v17_high_dependency import c28_catalog


CATALOG = Path("terminology/military-tongzong-v15-v17.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _resolve(ref):
    module_name, attr = ref.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), attr)


def test_tongzong_military_catalog_matches_rule_unit_counts():
    data = _load(CATALOG)
    runtime = military_rule_unit_catalog()

    source_entries = [e for e in data["entries"] if e["canonical_source_rule"]]
    helpers = [e for e in data["entries"] if not e["canonical_source_rule"]]

    assert len(source_entries) == runtime["source_rule_count"] == 25
    assert len(helpers) == len(runtime["derived_helpers"]) == 1
    assert helpers[0]["rule_id"] == "V17-D1"


def test_c23_to_c28_implemented_source_rules_match_terminology_runtime_ids():
    data = _load(CATALOG)
    by_id = {e["rule_id"]: e for e in data["entries"]}

    declared = set()
    for catalog in (
        c23_catalog(),
        c24_catalog(),
        c25_catalog(),
        remaining_v15_catalog(),
        c26_catalog(),
        c27_catalog(),
        c28_catalog(),
    ):
        declared.update(catalog["implemented"])

    expected = {
        *{f"V15-{n:02d}" for n in range(1, 15)},
        *{f"V17-{n:02d}" for n in range(1, 12)},
    }
    source_runtime_ids = {
        rid for rid, entry in by_id.items()
        if entry["runtime"] is not None and entry["canonical_source_rule"]
    }

    assert declared == expected
    assert source_runtime_ids == expected

    for rid in expected:
        assert by_id[rid]["implementation_status"] == "implemented_source_specific"
        assert callable(_resolve(by_id[rid]["runtime"]))
        assert callable(_resolve(by_id[rid]["catalog_runtime"]))


def test_no_canonical_tongzong_military_source_rule_remains_runtime_pending():
    data = _load(CATALOG)

    pending = {
        entry["rule_id"]
        for entry in data["entries"]
        if entry["canonical_source_rule"] and entry["runtime"] is None
    }

    assert pending == set()
    assert all(
        entry["implementation_status"] == "implemented_source_specific"
        for entry in data["entries"]
        if entry["canonical_source_rule"]
    )

def test_v17_d1_is_implemented_cross_volume_helper_not_source_rule():
    data = _load(CATALOG)
    helper = next(e for e in data["entries"] if e["rule_id"] == "V17-D1")
    c32 = c32_catalog()

    assert helper["source_profile"] == "cross_volume_helper"
    assert helper["canonical_source_rule"] is False
    assert helper["dependency_class"] == "derived_cross_volume"
    assert helper["implementation_status"] == "implemented_derived_helper"
    assert helper["runtime"] == "kintaiyi.cross_volume_helpers.build_guxu_cross_volume_helper"
    assert c32["helpers"] == ["V17-D1"]
    assert c32["canonical_source_rule_count"] == 0
    assert callable(_resolve(helper["runtime"]))
    assert callable(_resolve(helper["catalog_runtime"]))
    assert set(helper["overlaps"]) == {"volume5_inner_outer_attack", "V17-09"}


def test_high_risk_overlaps_remain_source_separated():
    data = _load(CATALOG)
    by_id = {e["rule_id"]: e for e in data["entries"]}

    assert "J4M-10" in by_id["V15-01"]["overlaps"]
    assert "J4M-06" in by_id["V15-04"]["overlaps"]
    assert set(by_id["V15-07"]["overlaps"]) == {"J4M-07", "J4M-08"}
    assert set(by_id["V15-14"]["overlaps"]) == {"J4M-11", "J4M-12"}
    assert "J4M-05" in by_id["V17-01"]["overlaps"]
    assert "C8-L3" in by_id["V17-02"]["overlaps"]


def test_rules_json_registers_complete_tongzong_runtime_coverage():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    source = by_id["R-TONGZONG-MILITARY-V15-V17"]
    assert len(source["rule_ids"]) == 25
    assert set(source["implemented_rule_ids"]) == {
        *{f"V15-{n:02d}" for n in range(1, 15)},
        *{f"V17-{n:02d}" for n in range(1, 12)},
    }

    derived = by_id["R-TONGZONG-MILITARY-DERIVED"]
    assert derived["rule_id"] == "V17-D1"
    assert derived["canonical_source_rule"] is False
    assert derived["runtime"] == "kintaiyi.cross_volume_helpers.build_guxu_cross_volume_helper"
