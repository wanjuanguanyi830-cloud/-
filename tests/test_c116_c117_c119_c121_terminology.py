import json
from pathlib import Path

from kintaiyi.jinjing_xuanming import ROLE_TO_XUANMING, c116_catalog, xuanming_for_role
from kintaiyi.jinjing_taigong_timing import c117_catalog
from kintaiyi.jinjing_time_eight_doors import (
    YANG_TIME_DOORS,
    YIN_TIME_DOORS,
    c119_catalog,
    time_duty_door,
)
from kintaiyi.jinjing_direct_envoy import (
    YANG_ANCHORS,
    YIN_ANCHORS,
    c121_catalog,
    direct_envoy_anchor,
)


RITUAL = Path("terminology/ritual-timing.json")
MILITARY = Path("terminology/military-p0.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c116_xuanming_catalog_matches_direct_role_table():
    data = _load(RITUAL)
    entry = next(e for e in data["entries"] if e["key"] == "xuanming_role")
    runtime = c116_catalog()

    assert entry["rule_id"] == runtime["rule_id"] == "C116-XUANMING-ROLE"
    assert {
        role: item["target"]
        for role, item in ROLE_TO_XUANMING.items()
    } == entry["role_targets"]

    assert xuanming_for_role("天子")["xuanming_target"] == "天乙"
    assert xuanming_for_role("二干石")["role"] == "二千石"
    assert xuanming_for_role("庶人")["target_type"] == "annual_position"


def test_c117_taigong_catalog_requires_explicit_evidence_and_cross_source_readiness_is_labelled():
    data = _load(MILITARY)
    entry = next(e for e in data["entries"] if e["key"] == "taigong_timing")
    runtime = c117_catalog()

    assert entry["rule_id"] == runtime["rule_id"] == "C117-TAIGONG-TIMING"
    assert runtime["auto_rule_lookups"] is False
    assert set(entry["auspicious_doors"]) == {"开", "休", "生"}
    assert entry["cross_source_readiness"]["source_text_rewritten"] is False
    assert entry["xuanming_dependency"] == "C116-XUANMING-ROLE"


def test_c119_time_duty_doors_use_30_time_units_not_year_cycle():
    data = _load(RITUAL)
    entry = next(e for e in data["entries"] if e["key"] == "time_eight_doors")
    runtime = c119_catalog()

    assert entry["yang_time_doors"] == list(YANG_TIME_DOORS)
    assert entry["yin_time_doors"] == list(YIN_TIME_DOORS)
    assert entry["time_block"] == runtime["time_block"] == 30
    assert entry["time_door_cycle"] == runtime["time_door_cycle"] == 120

    assert time_duty_door("阳遁", 0)["duty_door"] == "开"
    assert time_duty_door("阳遁", 30)["duty_door"] == "生"
    assert time_duty_door("阴遁", 0)["duty_door"] == "杜"
    assert time_duty_door("阴遁", 30)["duty_door"] == "死"


def test_c121_direct_envoy_catalog_matches_six_anchor_tables_and_stays_noncontinuous():
    data = _load(RITUAL)
    entry = next(e for e in data["entries"] if e["key"] == "direct_envoy_anchors")
    runtime = c121_catalog()

    assert entry["rule_ids"] == runtime["rule_ids"]
    assert len(YANG_ANCHORS) == len(YIN_ANCHORS) == 6
    assert entry["continuous_runtime_implemented"] is False
    assert runtime["wang_ximing_boundary"]["continuous_runtime_implemented"] is False

    yang = direct_envoy_anchor("阳遁", 1)
    yin = direct_envoy_anchor("阴遁", 1)
    assert (yang["taiyi_palace"], yang["tianmu"], yang["jishen"]) == (1, "武德", "寅")
    assert (yin["taiyi_palace"], yin["tianmu"], yin["jishen"]) == (9, "吕申", "申")
    assert yang["movement_rules"]["taiyi"]["center_five_used"] is False
    assert yin["movement_rules"]["taiyi"]["center_five_used"] is False


def test_rules_json_registers_c116_c117_c119_c121():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-XUANMING"]["rule_id"] == "C116-XUANMING-ROLE"
    assert by_id["R-TAIGONG-TIMING"]["rule_id"] == "C117-TAIGONG-TIMING"
    assert "C119-WINTER-TIME-DUTY-DOOR" in by_id["R-TIME-EIGHT-DOORS"]["rule_ids"]
    assert by_id["R-DIRECT-ENVOY"]["rule_ids"] == [
        "C121-DIRECT-ENVOY-ANCHOR",
        "C121-DIRECT-ENVOY-MOVEMENT",
    ]
