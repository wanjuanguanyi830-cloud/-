import json
from pathlib import Path

from kintaiyi.wenchang_nine_stars_tongzong import c70_catalog
from kintaiyi.wufu_auspicious_numbers import NUMBER_GROUPS


CYCLES = Path("terminology/cycles.json")
ZITING = Path("terminology/zitingjing.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c68_wufu_number_groups_match_runtime():
    data = _load(CYCLES)
    entry = next(e for e in data["entries"] if e["key"] == "five_blessings_auspicious_number")

    assert {
        name: tuple(numbers)
        for name, numbers in entry["number_groups"].items()
    } == NUMBER_GROUPS
    assert entry["rule_id"] == "C68-WUFU-AUSPICIOUS-NUMBER"
    assert "不从积年自动调用C67" in entry["input_contract"]


def test_c70_tongzong_profile_is_nested_below_ziting_primary_boundary():
    data = _load(ZITING)
    entry = next(e for e in data["entries"] if e["key"] == "wenchang_nine_stars")
    profile = entry["source_specific_profiles"]["tongzong_volume6_ngj"]
    runtime = c70_catalog()

    assert entry["primary_evidence_level"] == "catalog_attested_text_pending"
    assert entry["primary_result_allowed"] is False
    assert profile["rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"
    assert profile["source_profile"] == runtime["source_profile"]
    assert profile["cycle"] == {
        "big_cycle": 2700,
        "small_cycle": 270,
        "years_per_star": 30,
        "start_palace": 1,
        "direction": "forward",
    }
    assert profile["full_dynamic_distribution_supported"] is False


def test_rules_json_registers_c68_and_c70_without_source_merge():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-WUFU-AUSPICIOUS"]["rule_id"] == "C68-WUFU-AUSPICIOUS-NUMBER"
    assert by_id["R-WENCHANG-NINE-STARS-TONGZONG"]["rule_id"] == (
        "C70-TONGZONG-WENCHANG-NINE-STARS"
    )
    assert "不得反填" in by_id["R-WENCHANG-NINE-STARS-TONGZONG"]["canonical"]
