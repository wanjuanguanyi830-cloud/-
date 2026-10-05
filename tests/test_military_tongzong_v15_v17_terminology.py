import importlib
import json
from pathlib import Path

from kintaiyi.military_rule_units import military_rule_unit_catalog
from kintaiyi.tongzong_v15_low_dependency import c23_catalog


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


def test_only_c23_implemented_volume15_rules_have_runtime_refs():
    data = _load(CATALOG)
    c23 = c23_catalog()
    by_id = {e["rule_id"]: e for e in data["entries"]}

    implemented = set(c23["implemented"])
    source_runtime_ids = {
        rid for rid, e in by_id.items()
        if e["runtime"] is not None and e["canonical_source_rule"]
    }

    assert implemented == {"V15-02", "V15-03", "V15-04", "V15-05", "V15-06"}
    assert source_runtime_ids == implemented

    for rid in implemented:
        assert callable(_resolve(by_id[rid]["runtime"]))

    assert by_id["V17-D1"]["implementation_status"] == "implemented_derived_helper"
    assert callable(_resolve(by_id["V17-D1"]["runtime"]))


def test_reference_function_is_not_treated_as_runtime_for_pending_units():
    data = _load(CATALOG)

    for entry in data["entries"]:
        if entry["rule_id"] in {"V15-02", "V15-03", "V15-04", "V15-05", "V15-06", "V17-D1"}:
            continue
        assert entry["runtime"] is None
        assert entry["reference_function"]
        assert entry["implementation_status"] == "source_rule_catalog_only"


def test_high_risk_overlaps_remain_source_separated():
    data = _load(CATALOG)
    by_id = {e["rule_id"]: e for e in data["entries"]}

    assert "J4M-10" in by_id["V15-01"]["overlaps"]
    assert "J4M-06" in by_id["V15-04"]["overlaps"]
    assert set(by_id["V15-07"]["overlaps"]) == {"J4M-07", "J4M-08"}
    assert set(by_id["V15-14"]["overlaps"]) == {"J4M-11", "J4M-12"}
    assert "J4M-05" in by_id["V17-01"]["overlaps"]
    assert "C8-L3" in by_id["V17-02"]["overlaps"]


def test_v17_d1_is_explicit_cross_volume_helper():
    data = _load(CATALOG)
    helper = next(e for e in data["entries"] if e["rule_id"] == "V17-D1")

    assert helper["source_profile"] == "cross_volume_helper"
    assert helper["canonical_source_rule"] is False
    assert helper["dependency_class"] == "derived_cross_volume"
    assert helper["implementation_status"] == "implemented_derived_helper"
    assert helper["runtime"] == "kintaiyi.cross_volume_helpers.build_guxu_cross_volume_helper"
    assert set(helper["overlaps"]) == {"volume5_inner_outer_attack", "V17-09"}


def test_rules_json_registers_tongzong_military_units():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    source = by_id["R-TONGZONG-MILITARY-V15-V17"]
    assert len(source["rule_ids"]) == 25
    assert source["implemented_rule_ids"] == [
        "V15-02", "V15-03", "V15-04", "V15-05", "V15-06"
    ]
    assert by_id["R-TONGZONG-MILITARY-DERIVED"]["rule_id"] == "V17-D1"
    assert by_id["R-TONGZONG-MILITARY-DERIVED"]["canonical_source_rule"] is False
