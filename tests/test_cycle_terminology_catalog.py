import json
from pathlib import Path

from kintaiyi.dayou_position_source_profiles import (
    PALACE_PATH as DAYOU_PATH,
    TAOJIN_PATH,
    PROFILES as DAYOU_PROFILES,
)
from kintaiyi.dayou_tianmu_source_profiles import (
    PROFILES as DAYOU_TIANMU_PROFILES,
    TIANMU_PATH,
)
from kintaiyi.four_spirit_tongzong import SOURCE_WITNESS as FOUR_SPIRIT_WITNESS
from kintaiyi.limit_cycles import BAILIU_SPEC, YANGJIU_SPEC
from kintaiyi.state_spirit_cycles import SPIRITS, TWELVE_PALACES
from kintaiyi.taiyou_limit_tracks import (
    TAIYOU_PALACE_PATH,
    TAIYOU_TRIGRAM_PATH,
)
from kintaiyi.three_bases_cycles import BANG_SURPLUS, THREE_BASES
from kintaiyi.wufu_source_profiles import (
    PROFILES as WUFU_PROFILES,
    WUFU_PALACES,
)
from kintaiyi.xiaoyou_position import (
    PALACE_PATH as XIAOYOU_PATH,
    PROFILES as XIAOYOU_PROFILES,
)


CATALOG = Path("terminology/cycles.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_three_bases_catalog_matches_c66_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "three_bases")

    assert entry["common_surplus"]["value"] == BANG_SURPLUS
    for name, spec in THREE_BASES.items():
        assert entry["members"][name] == {
            "rule_id": spec["rule_id"],
            "identity": spec["identity"],
            "big_cycle": spec["big_cycle"],
            "small_cycle": spec["small_cycle"],
            "years_per_state": spec["years_per_state"],
            "start_branch": spec["start_branch"],
        }


def test_wufu_catalog_matches_source_specific_profiles():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "five_blessings")

    assert entry["stable_core"]["effective_cycle"] == 225
    assert entry["stable_core"]["years_per_palace"] == 45
    assert [
        (item["position"], item["palace_name"])
        for item in entry["stable_core"]["route"]
    ] == [
        (item["position"], item["name"])
        for item in WUFU_PALACES
    ]

    for profile in ("tongzong", "jinjing"):
        catalog_profile = entry["source_profiles"][profile]
        runtime_profile = WUFU_PROFILES[profile]
        assert catalog_profile["rule_id"] == runtime_profile["rule_id"]
        assert catalog_profile["source_profile"] == runtime_profile["source_profile"]
        assert catalog_profile["surplus"] == runtime_profile["surplus"]
        assert catalog_profile["big_cycle"] == runtime_profile["big_cycle"]
        assert catalog_profile["small_cycle"] == runtime_profile["small_cycle"]


def test_dayou_position_catalog_matches_c107_profiles():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "big_wander_position")

    assert entry["stable_core"]["path"] == list(DAYOU_PATH)
    assert entry["stable_core"]["excluded_palace"] == 5
    assert entry["stable_core"]["small_cycle"] == 288
    assert entry["stable_core"]["years_per_palace"] == 36

    assert entry["stable_core"]["path_scope"] == "jinjing_and_tongzong"

    for profile in ("jinjing", "tongzong", "taojin"):
        catalog_profile = entry["source_profiles"][profile]
        runtime_profile = DAYOU_PROFILES[profile]
        assert catalog_profile["rule_id"] == runtime_profile["rule_id"]
        assert catalog_profile["source_profile"] == runtime_profile["source_profile"]
        assert catalog_profile["epoch"] == runtime_profile["epoch"]
        assert catalog_profile["surplus"] == runtime_profile["surplus"]
        assert catalog_profile["outer_cycle"] == runtime_profile["outer_cycle"]

    assert entry["source_profiles"]["taojin"]["path"] == list(TAOJIN_PATH)
    assert entry["source_profiles"]["taojin"]["direction"] == "reverse"


def test_dayou_tianmu_catalog_matches_c106_profiles():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "big_wander_skyeye")

    assert entry["stable_core"]["path"] == list(TIANMU_PATH)
    assert entry["stable_core"]["path_length"] == 18

    for profile in ("jinjing", "tongzong"):
        catalog_profile = entry["source_profiles"][profile]
        runtime_profile = DAYOU_TIANMU_PROFILES[profile]
        assert catalog_profile["rule_id"] == runtime_profile["rule_id"]
        assert catalog_profile["source_profile"] == runtime_profile["source_profile"]
        assert catalog_profile["surplus"] == runtime_profile["surplus"]
        assert catalog_profile["outer_cycle"] == runtime_profile["outer_cycle"]
        assert catalog_profile["small_cycle"] == runtime_profile["small_cycle"]


def test_xiaoyou_catalog_matches_c103_profiles():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "small_wander_position")

    assert entry["stable_core"]["path"] == list(XIAOYOU_PATH)
    assert entry["stable_core"]["small_cycle"] == 24
    assert entry["stable_core"]["years_per_palace"] == 3
    assert entry["stable_core"]["excluded_palace"] == 5

    for profile in ("jinjing", "tongzong"):
        catalog_profile = entry["source_profiles"][profile]
        runtime_profile = XIAOYOU_PROFILES[profile]
        assert catalog_profile["rule_id"] == runtime_profile["rule_id"]
        assert catalog_profile["source_profile"] == runtime_profile["source_profile"]
        assert catalog_profile["outer_cycle"] == runtime_profile["outer_cycle"]


def test_four_taiyi_catalog_matches_c64_and_c92_position_layers():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "four_taiyi")

    assert entry["canonical_names"] == ["天乙", "地乙", "直符", "四神"]
    assert entry["common_position_core"]["palace_order"] == list(TWELVE_PALACES)

    for name in ("天乙", "地乙", "直符"):
        assert entry["members"][name]["element"] == SPIRITS[name]["element"]
        assert entry["members"][name]["rule_id"] == SPIRITS[name]["rule_id"]
        assert entry["members"][name]["start_palace"] == SPIRITS[name]["start_palace"]

    four_spirit_formula = FOUR_SPIRIT_WITNESS["primary"]["position_formula"]
    assert entry["members"]["四神"]["element"] == "水"
    assert entry["members"]["四神"]["start_palace"] == four_spirit_formula["start_palace"]
    assert entry["name_policy"]["直符"] == "canonical"
    assert "not_enabled_by_default" in entry["name_policy"]["值符"]


def test_yangjiu_bailiu_catalog_matches_c36_specs():
    data = _load(CATALOG)
    by_key = {entry["key"]: entry for entry in data["entries"]}

    assert by_key["yangjiu"]["big_limit"] == YANGJIU_SPEC["big_limit"]
    assert by_key["yangjiu"]["small_limit"] == YANGJIU_SPEC["small_limit"]
    assert by_key["yangjiu"]["small_limit_count"] == YANGJIU_SPEC["small_limit_count"]
    assert by_key["yangjiu"]["surplus_offset"] == YANGJIU_SPEC["surplus_offset"]

    assert by_key["bailiu"]["big_limit"] == BAILIU_SPEC["big_limit"]
    assert by_key["bailiu"]["small_limit"] == BAILIU_SPEC["small_limit"]
    assert by_key["bailiu"]["small_limit_count"] == BAILIU_SPEC["small_limit_count"]
    assert by_key["bailiu"]["surplus_offset"] == BAILIU_SPEC["surplus_offset"]


def test_taiyou_limit_tracks_match_c38_paths_and_roles():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "taiyou_limit_tracks")

    assert [
        (item["palace"], item["trigram"])
        for item in entry["path"]
    ] == list(zip(TAIYOU_PALACE_PATH, TAIYOU_TRIGRAM_PATH))

    assert entry["tracks"]["阳九外卦"] == {
        "rule_id": "C38-YJ-OUTER",
        "limit_rule_id": "C36-YJ",
        "years_per_palace": 10,
        "years_per_round": 80,
        "rounds_per_big_limit": 57,
    }
    assert entry["tracks"]["百六内卦"] == {
        "rule_id": "C38-BL-INNER",
        "limit_rule_id": "C36-BL",
        "years_per_palace": 36,
        "years_per_round": 288,
        "rounds_per_big_limit": 15,
    }


def test_cycle_catalog_preserves_modern_production_calendar_boundary():
    data = _load(CATALOG)
    boundary = data["production_calendar_boundary"]

    assert boundary["calendar_source_of_truth"] == "modern_astronomy_lunisolar"
    assert boundary["taiyi_year_boundary"] == "真实天文冬至交节瞬间"
    for forbidden in ("元旦", "春节", "立春", "春分"):
        assert forbidden in boundary["policy"]


def test_rules_json_no_longer_promotes_legacy_mixed_cycle_profiles():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-WF"]["source_profiles"]["tongzong"]["rule_id"] == "C67-WUFU-TONGZONG"
    assert by_id["R-WF"]["source_profiles"]["jinjing"]["rule_id"] == "C67-WUFU-JINJING"
    assert by_id["R-DY"]["source_profiles"]["jinjing"]["rule_id"] == "C107-DAYOU-JINJING"
    assert by_id["R-DY"]["source_profiles"]["tongzong"]["rule_id"] == "C107-DAYOU-TONGZONG"
    assert by_id["R-DY"]["source_profiles"]["taojin"]["rule_id"] == "C107-DAYOU-TAOJIN"
    assert by_id["R-XIAOYOU"]["source_profiles"]["jinjing"]["rule_id"] == "C103-XIAOYOU-JINJING"
    assert by_id["R-THREE-BASES"]["rule_ids"] == ["C66-JUNJI", "C66-CHENJI", "C66-MINJI"]
    assert by_id["R-LIMITS"]["rule_ids"] == [
        "C36-YJ", "C36-BL", "C38-YJ-OUTER", "C38-BL-INNER"
    ]
