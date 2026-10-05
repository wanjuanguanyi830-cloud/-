import json
from pathlib import Path

from kintaiyi.state_spirit_conjunctions import PAIR_RULES as C65_PAIRS
from kintaiyi.three_bases_wufu_conjunctions import PAIR_RULES as C74_PAIRS
from kintaiyi.three_bases_three_spirits_relations import RULES as C90_RULES
from kintaiyi.three_bases_other_spirits_relations import RULES as C91_RULES
from kintaiyi.wufu_four_taiyi_relations import COUNTERPARTS as C94_COUNTERPARTS
from kintaiyi.wander_conjunctions import PAIR_RULES as C113_PAIRS


CATALOG = Path("terminology/relations.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _pair_set(rows):
    return {tuple(row) for row in rows}


def test_c65_relation_pairs_match_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "three_spirit_same_palace")

    assert _pair_set(entry["pairs"]) == set(C65_PAIRS)
    assert entry["auto_position_lookup_used"] is False
    assert entry["name_policy"]["直符"] == "canonical"


def test_c74_relation_pairs_match_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "three_bases_wufu_same_palace")

    assert _pair_set(entry["pairs"]) == set(C74_PAIRS)
    assert entry["auto_position_lookup_used"] is False
    assert "initial_conjunction" in entry["extra_input"]


def test_c90_relation_domain_matches_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "three_bases_three_spirits")

    assert entry["pair_count"] == len(C90_RULES) == 9
    assert {
        (base, spirit)
        for base in entry["bases"]
        for spirit in entry["spirits"]
    } == set(C90_RULES)
    assert entry["auto_position_lookup_used"] is False


def test_c91_relation_domain_matches_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "three_bases_other_spirits")

    assert entry["pair_count"] == len(C91_RULES) == 9
    assert {
        (base, counterpart)
        for base in entry["bases"]
        for counterpart in entry["counterparts"]
    } == set(C91_RULES)
    assert entry["auto_position_lookup_used"] is False


def test_c94_four_taiyi_counterparts_match_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "wufu_four_taiyi_domain")

    assert entry["counterparts"] == C94_COUNTERPARTS
    assert entry["interpretation_profile_required"] == "oct4_recovered_four_taiyi_elemental"
    assert entry["auto_coordinate_lookup_used"] is False


def test_c113_recovered_pairs_match_runtime_and_do_not_duplicate_other_domains():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "wander_conjunctions")

    assert _pair_set(entry["pairs"]) == set(C113_PAIRS)
    assert entry["auto_position_lookup_used"] is False

    c65 = _pair_set(next(e for e in data["entries"] if e["key"] == "three_spirit_same_palace")["pairs"])
    c74 = _pair_set(next(e for e in data["entries"] if e["key"] == "three_bases_wufu_same_palace")["pairs"])
    assert not set(C113_PAIRS) & c65
    assert not set(C113_PAIRS) & c74


def test_relation_catalog_global_policy_forbids_auto_same_palace_inference():
    data = _load(CATALOG)

    assert any("不自动读取位置层" in line for line in data["global_policy"])
    assert any("位置相同不等于自动应用古籍断语" in line for line in data["global_policy"])


def test_rules_json_registers_relation_layers():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-REL-C65"]["rule_id"] == "C65-THREE-SPIRIT-SAME-PALACE"
    assert by_id["R-REL-C74"]["rule_id"] == "C74-THREE-BASES-WUFU-SAME-PALACE"
    assert by_id["R-REL-C90"]["rule_id"] == "C90-THREE-BASES-THREE-SPIRITS"
    assert by_id["R-REL-C91"]["rule_id"] == "C91-THREE-BASES-OTHER-SPIRITS"
    assert by_id["R-REL-C94"]["rule_id"] == "C94-WUFU-FOUR-TAIYI-DOMAIN-RELATION"
    assert by_id["R-REL-C113"]["rule_id"] == "C113-RECOVERED-WANDER-CONJUNCTIONS"
