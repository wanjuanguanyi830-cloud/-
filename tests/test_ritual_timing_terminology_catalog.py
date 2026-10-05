import json
from pathlib import Path

from kintaiyi.imperial_inspection import (
    CORNER_POSITIONS,
    DIRECTION_BY_TIANMU,
    imperial_inspection,
)
from kintaiyi.jinjing_current_time import current_time_core
from kintaiyi.jinjing_current_time_liuren import (
    c69b_catalog,
    palace_to_liuren_branch,
)


CATALOG = Path("terminology/ritual-timing.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c62_catalog_matches_corner_and_direction_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "imperial_inspection")

    assert set(entry["corner_positions"]) == set(CORNER_POSITIONS)
    assert {
        key: value["direction"]
        for key, value in DIRECTION_BY_TIANMU.items()
    } == entry["direction_by_tianmu"]

    result = imperial_inspection(
        taiyi_position="乾",
        tianmu_position="巽",
        month_patterns=[],
    )
    assert result["inspection_year"] is True
    assert result["direction"] == "西方"
    assert result["month_number"] is None


def test_c69_catalog_keeps_core_and_liuren_overlay_separate():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "current_time_method")

    assert entry["layers"]["core"]["runtime"] == "kintaiyi.jinjing_current_time.current_time_core"
    assert entry["layers"]["liuren_overlay"]["runtime"] == (
        "kintaiyi.jinjing_current_time_liuren.current_time_liuren_overlay"
    )
    assert "C69-CURRENT-TIME-CORE" in entry["layers"]["core"]["rule_ids"]
    assert "C69B-CURRENT-TIME-LIUREN" in entry["layers"]["liuren_overlay"]["rule_ids"]


def test_c69_core_requires_explicit_period_and_preserves_source_profile():
    result = current_time_core(day_stem="甲", period="朝")

    assert result["source_profile"] == "jinjing_volume1_current_time"
    assert result["rule_id"] == "C69-CURRENT-TIME-CORE"
    assert result["complete_current_time_formula"] is False


def test_c69b_middle_palace_projection_is_not_computable():
    result = palace_to_liuren_branch(5)

    assert result["rule_id"] == "C69B-PALACE-BRANCH-PROJECTION"
    assert result["computable"] is False


def test_c69b_catalog_contains_four_overlay_rule_ids():
    data = c69b_catalog()
    assert data["rule_ids"] == [
        "C69B-NOBLE-GROUND",
        "C69B-TWELVE-GENERAL-PLATE",
        "C69B-PALACE-BRANCH-PROJECTION",
        "C69B-CURRENT-TIME-LIUREN",
    ]


def test_ritual_timing_preserves_modern_production_calendar_boundary():
    data = _load(CATALOG)
    boundary = data["production_calendar_boundary"]

    assert boundary["calendar_source_of_truth"] == "modern_astronomy_lunisolar"
    assert boundary["taiyi_year_boundary"] == "真实天文冬至交节瞬间"


def test_rules_json_registers_c62_and_c69_layers():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-IMPERIAL-INSPECTION"]["rule_id"] == "C62-IMPERIAL-INSPECTION"
    assert "C69B-CURRENT-TIME-LIUREN" in by_id["R-CURRENT-TIME"]["rule_ids"]
