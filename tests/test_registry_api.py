import json
from importlib import resources

from kintaiyi.api import (
    calculate,
    calculate_rule,
    explain_result,
    get_rule,
    get_term,
    list_catalogs,
    list_operations,
    registry_snapshot,
    resolve_runtime,
    rule_runtime_candidates,
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


def test_calculate_rule_resolves_d8_by_rule_id():
    result = calculate_rule("D8-01", 15)
    assert result["rule_id"] == "D8-01"
    assert result["components"] == {"ten": True, "five": True, "one": False}
    assert result["classic_tags"] == ["杜塞"]


def test_calculate_rule_auto_selects_unique_source_profile_key():
    result = calculate_rule("C67-WUFU-TONGZONG", 1)
    assert result["rule_id"] == "C67-WUFU-TONGZONG"
    assert result["profile_key"] == "tongzong"
    assert result["source_profile"] == "tongzong_volume6_7_wufu"


def test_calculate_rule_resolves_tongzong_and_ziting_nine_star_cycles_separately():
    tongzong = calculate_rule("C124-TONGZONG-TAIYI-NINE-STARS", 1121)
    ziting = calculate_rule("C125-ZITING-TAIYI-NINE-STARS-CYCLE", 1937281)

    assert tongzong["direct_star"] == "天禽"
    assert tongzong["source_profile"] == "tongzong_volume6_taiyi_nine_stars"
    assert ziting["direct_star"] == "天辅"
    assert ziting["rule_id"] == "C125-ZITING-TAIYI-NINE-STARS-CYCLE"


def test_rule_runtime_candidates_deduplicate_same_runtime_across_layers():
    candidates = rule_runtime_candidates("C124-TONGZONG-TAIYI-NINE-STARS")
    assert len(candidates) == 1
    assert candidates[0]["runtime"] == (
        "kintaiyi.taiyi_nine_stars_tongzong.taiyi_nine_stars_tongzong"
    )
    assert len(candidates[0]["origins"]) >= 2


def test_operation_registry_now_covers_all_seven_and_eight_method_aliases():
    operations = {item["name"]: item for item in list_operations()}
    expected = {
        *(f"seven.{name}" for name in (
            "lijin", "lion", "cloud", "tiger", "leigong", "dragon", "return_army"
        )),
        *(f"eight.{name}" for name in (
            "sancai", "length", "wuyin", "gudan", "inner_outer",
            "quantity", "yinyang_ehui", "preparedness"
        )),
    }
    assert expected <= set(operations)


def test_all_tongzong_military_source_rules_resolve_through_public_rule_api():
    source_rule_ids = [
        *(f"V15-{n:02d}" for n in range(1, 15)),
        *(f"V17-{n:02d}" for n in range(1, 12)),
    ]
    for rule_id in source_rule_ids:
        candidates = __import__("kintaiyi.api", fromlist=["rule_runtime_candidates"]).rule_runtime_candidates(rule_id)
        assert len(candidates) == 1
        assert callable(resolve_runtime(candidates[0]["runtime"]))


def test_public_rule_facade_normalizes_source_rule_id_without_removing_original():
    result = calculate_rule(
        "V15-01",
        skyeyes="巽",
        shiji="乾",
        home_cal=11,
        away_cal=22,
        pattern_evidence=[],
    )

    assert result["source_rule_id"] == "V15-01"
    assert result["rule_id"] == "V15-01"
    assert result["registry_normalized_rule_id"] is True
    explanation = explain_result(result)
    assert explanation["rule_id"] == "V15-01"
    assert explanation["rule_registry"]["count"] >= 1


def test_source_record_only_jingyou_rule_is_not_promoted_to_calculation_runtime():
    import pytest

    with pytest.raises(KeyError):
        calculate_rule("JF4M-04")
