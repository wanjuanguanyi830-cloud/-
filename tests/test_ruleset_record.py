import json
from pathlib import Path

from rules.jinjing.geju import GEJU_RULESET, GEJU_RULESET_VERSION, PALACE_RING, SIXTEEN_RING


RULESET_FILE = Path(__file__).parents[1] / "rules" / "jinjing" / "geju" / "ruleset.json"


def test_machine_readable_rule_record_matches_engine_constants():
    ruleset = json.loads(RULESET_FILE.read_text(encoding="utf-8"))
    assert ruleset["ruleset_id"] == GEJU_RULESET
    assert ruleset["ruleset_version"] == GEJU_RULESET_VERSION
    assert tuple(ruleset["coordinates"]["sixteen_ring"]) == SIXTEEN_RING
    assert tuple(ruleset["coordinates"]["palace_ring"]) == PALACE_RING
    assert ruleset["canonical_field_names"]["四郭杜"] == ["四郭杜"]
    assert ruleset["eight_door"]["zero_remainder_means"] == 240

