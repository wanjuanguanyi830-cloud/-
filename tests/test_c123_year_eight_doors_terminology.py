import json
from pathlib import Path

from kintaiyi.jinjing_eight_door_overlay import open_door_overlay
from kintaiyi.jinjing_year_door_relations import year_door_meeting
from kintaiyi.jinjing_year_eight_doors import YEAR_DOOR_ORDER, c123_catalog, year_duty_door


RITUAL = Path("terminology/ritual-timing.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c123_year_door_catalog_matches_runtime_cycle():
    data = _load(RITUAL)
    entry = next(e for e in data["entries"] if e["key"] == "year_eight_doors")
    runtime = c123_catalog()

    assert entry["rule_id"] == runtime["rule_id"] == "C123-YEAR-DUTY-DOOR"
    assert entry["door_order"] == list(YEAR_DOOR_ORDER)
    assert entry["outer_cycle"] == runtime["outer_cycle"] == 720
    assert entry["inner_cycle"] == runtime["inner_cycle"] == 240
    assert entry["years_per_door"] == runtime["years_per_door"] == 30


def test_c123_uses_30_year_blocks_not_c119_time_blocks():
    assert year_duty_door(1)["duty_door"] == "开"
    assert year_duty_door(30)["duty_door"] == "开"
    assert year_duty_door(31)["duty_door"] == "休"
    assert year_duty_door(61)["duty_door"] == "生"


def test_year_open_door_overlay_matches_fixed_eight_direction_order():
    overlay = open_door_overlay(1)

    assert overlay["anchor_door"] == "开"
    assert overlay["palace_to_door"] == {
        1: "开", 8: "休", 3: "生", 4: "伤",
        9: "杜", 2: "景", 7: "死", 6: "惊",
    }


def test_three_good_door_meeting_is_local_relation_not_final_military_verdict():
    result = year_door_meeting(
        taiyi_palace=1,
        host_big_palace=8,
        guest_big_palace=4,
    )

    assert result["host"]["gate_under_taiyi_overlay"] == "休"
    assert result["host"]["verdict"] == "大利"
    assert result["guest"]["gate_under_taiyi_overlay"] == "伤"
    assert result["guest"]["verdict"] is None
    assert "局部" in result["policy"]


def test_rules_json_registers_c123():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-YEAR-EIGHT-DOORS"]["rule_id"] == "C123-YEAR-DUTY-DOOR"
