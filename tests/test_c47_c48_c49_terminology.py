import json
from pathlib import Path

from kintaiyi.xiaoyou_hexagram import xiaoyou_heavy_hexagram
from kintaiyi.xiaoyou_line_omens import c48_catalog, xiaoyou_line_omens
from kintaiyi.dayou_xiaoyou_difference import c49_catalog, dayou_xiaoyou_difference


TERMS = Path("terminology/volume9-10.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c47_xiaoyou_hexagram_catalog_and_runtime_boundary():
    data = _load(TERMS)
    entry = next(e for e in data["entries"] if e["key"] == "xiaoyou_hexagram")
    result = xiaoyou_heavy_hexagram(1)

    assert entry["rule_ids"] == ["C47-XY-INNER", "C47-XY-OUTER", "C47-XY-HEX"]
    assert result["rule_id"] == "C47-XY-HEX"
    assert result["source_profile"] == "tongzong_volume9_xiaoyou"
    assert result["inner"]["years_per_trigram"] == 24
    assert result["inner"]["moving_line"] == 1
    assert result["outer"]["years_per_trigram"] == 3
    assert result["hexagram_name"] is None
    assert result["c38_track_used"] is False
    assert result["dayou_epoch_offset_used"] is False


def test_c48_requires_explicit_patterns_and_najia_but_can_be_fully_computable():
    data = _load(TERMS)
    entry = next(e for e in data["entries"] if e["key"] == "xiaoyou_line_omens")
    runtime = c48_catalog()

    assert entry["rule_id"] == runtime["rule_id"] == "C48-XY-OMEN"

    x47 = xiaoyou_heavy_hexagram(1)
    partial = xiaoyou_line_omens(
        x47,
        calc_harmonious=True,
        has_response=True,
    )
    assert partial["computable"] is False
    assert any("显式检查" in item for item in partial["pending"])
    assert any("纳甲" in item for item in partial["pending"])

    complete = xiaoyou_line_omens(
        x47,
        calc_harmonious=True,
        has_response=True,
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert complete["computable"] is True
    assert complete["legacy_sixtyfour_hexagram_lookup_used"] is False


def test_c49_compares_c41_and_c47_without_assigning_auspice():
    data = _load(TERMS)
    entry = next(e for e in data["entries"] if e["key"] == "dayou_xiaoyou_difference")
    runtime = c49_catalog()

    assert entry["rule_id"] == runtime["rule_id"] == "C49-DY-XY-DIFF"
    assert runtime["auspice_from_same_or_different"] is False

    dayou = {
        "rule_id": "C41-DY-HEX",
        "source_profile": "tongzong_volume9_dayou_hexagram",
        "structure": {"lower_trigram": "乾"},
    }
    xiaoyou = {
        "rule_id": "C47-XY-HEX",
        "source_profile": "tongzong_volume9_xiaoyou",
        "structure": {"lower_trigram": "乾"},
    }
    result = dayou_xiaoyou_difference(dayou, xiaoyou)
    assert result["same_inner_trigram"] is True
    assert result["auspice"] is None
    assert result["dayou"]["years_per_inner_trigram"] == 36
    assert result["xiaoyou"]["years_per_inner_trigram"] == 24


def test_rules_json_registers_c47_c48_c49():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert "C47-XY-HEX" in by_id["R-XIAOYOU-HEXAGRAM"]["rule_ids"]
    assert by_id["R-XIAOYOU-OMENS"]["rule_id"] == "C48-XY-OMEN"
    assert by_id["R-DAYOU-XIAOYOU-DIFF"]["rule_id"] == "C49-DY-XY-DIFF"
