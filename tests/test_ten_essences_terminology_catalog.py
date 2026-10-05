import json
from pathlib import Path

from kintaiyi.ten_essences_source_registry import TEN_ESSENCES, LEGACY_NAME_AUDIT
from kintaiyi.ten_essences_positions import (
    FLYBIRD_PATHS,
    FIVEWIND_PATHS,
    TAIZUN_PATHS,
    EIGHTWIND_PATHS,
    THREEWIND_PATHS,
    WUXING_PATHS,
)
from kintaiyi.ten_essences_number import c54_catalog, taiyi_number
from kintaiyi.ten_essences_sixteen_gods import c55_catalog
from kintaiyi.ten_essences_tianshi import c56_catalog
from kintaiyi.ten_essences_number_omens import taiyi_number_omens


CATALOG = Path("terminology/ten-essences.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _by_key():
    data = _load(CATALOG)
    return {entry["key"]: entry for entry in data["entries"]}


def test_ten_essence_registry_order_and_small_cycles_match_c52():
    by_key = _by_key()
    group = by_key["ten_essences"]

    expected_order = [row["name"] for row in TEN_ESSENCES]
    expected_cycles = {row["name"]: row["small_cycle"] for row in TEN_ESSENCES}

    assert group["canonical_order"] == expected_order
    assert group["small_cycles"] == expected_cycles
    assert group["legacy_name_policy"]["地符"]["canonical"] == "帝符"
    assert LEGACY_NAME_AUDIT["太岁"]["status"] == "not_a_ten_essence"


def test_c53_position_paths_match_runtime_constants():
    by_key = _by_key()

    assert by_key["flybird"]["yang_path"] == list(FLYBIRD_PATHS["阳"])
    assert by_key["flybird"]["yin_path"] == list(FLYBIRD_PATHS["阴"])
    assert by_key["fivewind"]["yang_path"] == list(FIVEWIND_PATHS["阳"])
    assert by_key["fivewind"]["yin_path"] == list(FIVEWIND_PATHS["阴"])
    assert by_key["taizun"]["yang_path"] == list(TAIZUN_PATHS["阳"])
    assert by_key["taizun"]["yin_path"] == list(TAIZUN_PATHS["阴"])
    assert by_key["eightwind"]["yang_path"] == list(EIGHTWIND_PATHS["阳"])
    assert by_key["eightwind"]["yin_path"] == list(EIGHTWIND_PATHS["阴"])
    assert by_key["threewind"]["yang_path"] == list(THREEWIND_PATHS["阳"])
    assert by_key["threewind"]["yin_path"] == list(THREEWIND_PATHS["阴"])
    assert by_key["wuxing_essence"]["yang_path"] == list(WUXING_PATHS["阳"])
    assert by_key["wuxing_essence"]["yin_path"] == list(WUXING_PATHS["阴"])


def test_c54_number_is_numeric_layer_without_weather_omens():
    by_key = _by_key()
    entry = by_key["taiyi_number"]
    runtime = c54_catalog()

    assert entry["rule_id"] == runtime["rule_id"] == "C54-TAIYI-NUMBER"
    assert entry["output_range"] == [1, 72]

    result = taiyi_number(72)
    assert result["rule_id"] == "C54-TAIYI-NUMBER"
    assert result["taiyi_number"] == 72
    assert result["weather_omens_applied"] is False


def test_c55_and_c56_runtime_ids_match_catalog():
    by_key = _by_key()
    c55 = c55_catalog()
    c56 = c56_catalog()

    assert by_key["tianhuang"]["rule_id"] in c55["rule_ids"]
    assert by_key["difu"]["rule_id"] in c55["rule_ids"]
    assert by_key["tianshi"]["rule_id"] == "C56-TIANSHI"
    assert c56["rule_id"] == "C56-TIANSHI"


def test_ten_essence_flybird_is_not_military_external_observation():
    entry = _by_key()["flybird"]
    assert any("J4M-11" in note for note in entry["boundary_notes"])


def test_cloud_layers_are_explicit_and_separate():
    by_key = _by_key()

    c57 = by_key["cloud_conjunctions"]
    c58 = by_key["cloud_observations"]
    c59 = by_key["number_weather_omens"]

    assert c57["rule_id"] == "C57-TEN-ESSENCE-CLOUD-CONJUNCTION"
    assert c58["rule_ids"] == ["C58-CLOUD-TIMING", "C58-WEATHER-OBSERVATION"]
    assert c59["rule_id"] == "C59-TAIYI-NUMBER-OMEN"
    assert any("不从C53/C55/C56落宫自动判断" in note for note in c57["boundary_notes"])
    assert any("真实外部观察" in note for note in c58["boundary_notes"])
    assert any("不调用C54自动取数" in note for note in c59["boundary_notes"])


def test_c59_keeps_number_50_unresolved_and_does_not_reuse_legacy_10_5():
    result = taiyi_number_omens(50, relations=[])

    assert result["rule_id"] == "C59-TAIYI-NUMBER-OMEN"
    assert result["unresolved_variant_count"] == 1
    assert result["unresolved_variants"][0]["taiyi_number"] == 50

    plain10 = taiyi_number_omens(10, relations=[])
    assert not any(
        item.get("kind") == "special_number"
        for item in plain10["matched_omens"]
    )


def test_rules_json_registers_ten_essence_layering():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}
    rule = by_id["R-TEN-ESSENCES"]

    assert "C52-TEN-ESSENCES-REGISTRY" in rule["rule_ids"]
    assert "C53-FLYBIRD" in rule["rule_ids"]
    assert "C54-TAIYI-NUMBER" in rule["rule_ids"]
    assert "C59-TAIYI-NUMBER-OMEN" in rule["rule_ids"]
    assert any("J4M-11" in item for item in rule["forbidden_merges"])
