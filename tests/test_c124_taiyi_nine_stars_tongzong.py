import json
from pathlib import Path

from kintaiyi.taiyi_nine_stars_tongzong import (
    RULE_ID,
    c124_catalog,
    taiyi_nine_stars_tongzong,
)


ZITING = Path("terminology/zitingjing.json")
RULES = Path("rules/taiyi_v1.json")
CROSSWALK = Path("terminology/crosswalk.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c124_original_1121_example_resolves_tianqin_first_year():
    result = taiyi_nine_stars_tongzong(1121)

    assert result["rule_id"] == RULE_ID
    assert result["large_cycle"] == 900
    assert result["small_cycle"] == 90
    assert result["years_per_star"] == 10
    assert result["direct_star"] == "天禽"
    assert result["direct_star_number"] == 5
    assert result["year_in_star"] == 1


def test_c124_cycle_boundaries_are_inclusive():
    assert taiyi_nine_stars_tongzong(90)["direct_star"] == "天英"
    assert taiyi_nine_stars_tongzong(90)["year_in_star"] == 10
    assert taiyi_nine_stars_tongzong(91)["direct_star"] == "天蓬"
    assert taiyi_nine_stars_tongzong(91)["year_in_star"] == 1
    assert taiyi_nine_stars_tongzong(900)["direct_star"] == "天英"
    assert taiyi_nine_stars_tongzong(901)["direct_star"] == "天蓬"


def test_c124_bing_year_example_distributes_all_nine_stars_from_palace_eight():
    result = taiyi_nine_stars_tongzong(1, year_stem="丙")

    assert result["direct_star"] == "天蓬"
    assert result["direct_star_anchor_palace"] == 8
    assert [row["star"] for row in result["full_dynamic_distribution"]] == [
        "天蓬", "天芮", "天冲", "天辅", "天禽", "天心", "天柱", "天任", "天英"
    ]
    assert [row["current_palace"] for row in result["full_dynamic_distribution"]] == [
        8, 9, 1, 2, 3, 4, 5, 6, 7
    ]


def test_c124_jia_year_keeps_current_direct_star_in_its_base_palace():
    result = taiyi_nine_stars_tongzong(41, year_stem="甲")

    assert result["direct_star"] == "天禽"
    assert result["direct_star_anchor_palace"] == 5
    assert result["full_dynamic_distribution"][0]["current_palace"] == 5


def test_c124_rate_ten_is_explicitly_source_resolved():
    catalog = c124_catalog()
    resolution = catalog["source_evidence"]["rate_resolution"]

    assert resolution["selected_years_per_star"] == 10
    assert "1121" in resolution["reason"]
    assert "星率十" in resolution["reason"]


def test_c124_is_registered_below_ziting_static_primary_without_merge():
    ziting = _load(ZITING)
    entry = next(e for e in ziting["entries"] if e["key"] == "taiyi_nine_stars")
    profile = entry["source_specific_profiles"]["tongzong_volume6_dynamic"]

    assert entry["primary_evidence_level"] == "direct_text_verified"
    assert entry["primary_result_allowed"] is True
    assert profile["rule_id"] == RULE_ID
    assert profile["cycle"] == {
        "big_cycle": 900,
        "small_cycle": 90,
        "years_per_star": 10,
        "start_star": "天蓬",
        "direction": "顺行九星",
    }
    assert profile["dynamic_distribution_supported"] is True


def test_c124_rules_registry_and_nine_star_crosswalk_are_wired():
    rules = _load(RULES)
    by_id = {r["rule_id"]: r for r in rules["categories"]["public_rules"]}
    assert by_id[RULE_ID]["runtime"] == (
        "kintaiyi.taiyi_nine_stars_tongzong.taiyi_nine_stars_tongzong"
    )

    crosswalk = _load(CROSSWALK)
    bridge = next(b for b in crosswalk["bridges"] if b["id"] == "CW-NINE-STARS-SOURCE-BOUNDARY")
    taiyi = next(m for m in bridge["members"] if m["key"] == "taiyi_nine_stars")
    assert taiyi["source_specific_profile"]["rule_id"] == RULE_ID
    assert any("900/90/10" in x for x in bridge["forbidden_merge"])
    assert any("2700/270/30" in x for x in bridge["forbidden_merge"])
