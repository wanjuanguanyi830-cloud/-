import json
from importlib import resources

from kintaiyi.api import (
    calculate,
    explain_result,
    get_rule,
    get_term,
    list_catalogs,
    list_operations,
    registry_snapshot,
    resolve_runtime,
)


def test_registry_points_to_existing_layer_indexes_without_copying_them():
    registry = registry_snapshot()
    assert registry["layers"]["terminology"]["index"] == "terminology/catalog-index.json"
    assert registry["layers"]["rules"]["index"] == "rules/taiyi_v1.json"
    assert registry["layers"]["runtime"]["public_facade"] == "kintaiyi.api"
    assert registry["compatibility"]["legacy_imports_preserved"] is True


def test_catalog_index_is_exposed_through_public_api():
    catalogs = list_catalogs()
    assert catalogs
    assert len({item["catalog_id"] for item in catalogs}) == len(catalogs)
    assert any(item["path"] == "terminology/d8-eight-divinations.json" for item in catalogs)
    assert any(item["path"] == "terminology/zitingjing.json" for item in catalogs)


def test_get_term_and_get_rule_follow_existing_owners():
    term = get_term("三才")
    assert term["count"] >= 1
    assert any(match["catalog_path"] == "terminology/d8-eight-divinations.json" for match in term["matches"])

    rule = get_rule("D8-01")
    assert rule["count"] >= 1
    assert any(match["category"] == "eight_divinations" for match in rule["matches"])


def test_public_sancai_operation_preserves_confirmed_blocked_boundaries():
    five = calculate("eight.sancai", 5)
    assert five["components"] == {"ten": False, "five": True, "one": False}
    assert "杜塞" in five["classic_tags"]

    fifteen = calculate("eight.sancai", 15)
    assert fifteen["components"] == {"ten": True, "five": True, "one": False}
    assert "杜塞" in fifteen["classic_tags"]
    assert "无人" not in fifteen["classic_tags"]


def test_public_nine_star_operation_keeps_source_profile_boundary():
    result = calculate("stars.taiyi.tongzong_dynamic", 1121)
    assert result["rule_id"] == "C124-TONGZONG-TAIYI-NINE-STARS"
    assert result["source_profile"] == "tongzong_volume6_taiyi_nine_stars"
    assert result["direct_star"] == "天禽"
    assert result["year_in_star"] == 1


def test_all_stable_operation_runtime_references_resolve():
    for operation in list_operations():
        if operation["status"] == "stable":
            assert callable(resolve_runtime(operation["runtime"]))


def test_explain_result_attaches_rule_registry_without_recomputing():
    result = calculate("eight.sancai", 15)
    explanation = explain_result(result)
    assert explanation["rule_id"] == "D8-01"
    assert explanation["rule_registry"]["count"] >= 1
    assert "does not recompute" in explanation["policy"]


def test_packaged_registry_and_schemas_are_json_resources():
    json.loads(resources.files("registry").joinpath("catalog.json").read_text(encoding="utf-8"))
    json.loads(resources.files("registry").joinpath("operations.json").read_text(encoding="utf-8"))
    json.loads(resources.files("schemas").joinpath("registry.schema.json").read_text(encoding="utf-8"))
    json.loads(resources.files("schemas").joinpath("operation.schema.json").read_text(encoding="utf-8"))
    json.loads(resources.files("schemas").joinpath("result.schema.json").read_text(encoding="utf-8"))
