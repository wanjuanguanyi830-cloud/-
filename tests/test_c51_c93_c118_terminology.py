import json
from pathlib import Path

from kintaiyi.coronation_cloud_omens import (
    FORM_EFFECTS,
    RELATION_EFFECTS,
    c51_catalog,
    coronation_cloud_omens,
)
from kintaiyi.jinjing_huangdao_tables import c118_catalog, term_day_position
from kintaiyi.zhifu_fire_states import KNOWN_STATES, c93_catalog, zhifu_known_fire_state


CYCLES = Path("terminology/cycles.json")
RITUAL = Path("terminology/ritual-timing.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c93_catalog_matches_only_directly_attested_fire_states():
    data = _load(CYCLES)
    entry = next(e for e in data["entries"] if e["key"] == "zhifu_fire_states")
    runtime = c93_catalog()

    assert entry["rule_id"] == "C93-ZHIFU-KNOWN-FIRE-STATE"
    assert entry["known_states"] == {
        str(palace): item["state"]
        for palace, item in KNOWN_STATES.items()
    }
    assert runtime["known_palaces"] == [2, 3, 4]
    assert entry["full_twelve_palace_state_table_ready"] is False


def test_c93_does_not_fill_unattested_palaces_from_twelve_stages():
    assert zhifu_known_fire_state(2)["state"] == "旺"
    assert zhifu_known_fire_state(3)["state"] == "长生"
    assert zhifu_known_fire_state(4)["state"] == "败"

    pending = zhifu_known_fire_state(5)
    assert pending["state"] is None
    assert pending["status"] == "source_pending"
    assert pending["position_boundary"]["auto_position_lookup_used"] is False


def test_c51_catalog_matches_direct_relation_and_form_layers():
    data = _load(RITUAL)
    entry = next(e for e in data["entries"] if e["key"] == "coronation_cloud_omens")
    runtime = c51_catalog()

    assert entry["rule_id"] == runtime["rule_id"] == "C51-CLOUD-OMEN"
    assert entry["relation_effects"] == RELATION_EFFECTS
    assert entry["form_effects"] == FORM_EFFECTS


def test_c51_allows_form_only_observation_without_forcing_element_relation():
    result = coronation_cloud_omens(day_ganzhi="甲子", cloud_form="阴云")

    assert result["rule_id"] == "C51-CLOUD-OMEN"
    assert result["relation_checked"] is False
    assert result["relation_status"] == "not_computable_without_single_color"
    assert result["form_effects"] == ["位祚不久"]
    assert result["overall_single_verdict"] is None


def test_c118_catalog_has_four_upstream_rule_ids():
    data = _load(RITUAL)
    entry = next(e for e in data["entries"] if e["key"] == "jinjing_huangdao_tables")
    runtime = c118_catalog()

    assert entry["rule_ids"] == runtime["rule_ids"] == [
        "C118-SOLAR-TERM-ANCHOR",
        "C118-MANSION-SPAN",
        "C118-MANSION-DIVISION",
        "C118-TERM-DAY-POSITION",
    ]
    assert entry["downstream"] == "C69B-CURRENT-TIME-LIUREN"


def test_c118_reproduces_jinjing_lidong_day_six_mansion_example():
    result = term_day_position("立冬", 6)

    assert result["computable"] is True
    assert result["mansion"] == "心"
    assert result["degree"] == {"numerator": 1, "denominator": 1}


def test_c118_is_ancient_table_upstream_not_modern_calendar_source_of_truth():
    data = _load(RITUAL)
    entry = next(e for e in data["entries"] if e["key"] == "jinjing_huangdao_tables")
    boundary = data["production_calendar_boundary"]

    assert any("不计算现代天文黄经" in note for note in entry["boundary_notes"])
    assert boundary["calendar_source_of_truth"] == "modern_astronomy_lunisolar"
    assert boundary["taiyi_year_boundary"] == "真实天文冬至交节瞬间"


def test_rules_json_registers_c51_c93_c118():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-ZHIFU-FIRE-STATE"]["rule_id"] == "C93-ZHIFU-KNOWN-FIRE-STATE"
    assert by_id["R-CORONATION-CLOUD"]["rule_id"] == "C51-CLOUD-OMEN"
    assert by_id["R-JINJING-HUANGDAO"]["rule_ids"][-1] == "C118-TERM-DAY-POSITION"
