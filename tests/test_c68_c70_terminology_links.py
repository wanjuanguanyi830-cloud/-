import json
from pathlib import Path

from kintaiyi.wenchang_nine_stars_tongzong import DIRECT_TEXT_EVIDENCE, STAR_TABLE, c70_catalog
from kintaiyi.wufu_auspicious_numbers import NUMBER_GROUPS


CYCLES = Path("terminology/cycles.json")
ZITING = Path("terminology/zitingjing.json")
WENCHANG = Path("terminology/wenchang-nine-stars.json")
RULES = Path("rules/taiyi_v1.json")
CROSSWALK = Path("terminology/crosswalk.json")


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


def test_c70_is_independent_stable_catalog_and_ziting_keeps_only_pointer():
    data = _load(WENCHANG)
    entry = next(e for e in data["entries"] if e["key"] == "wenchang_nine_stars")
    runtime = c70_catalog()

    assert entry["canonical_rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"
    assert entry["canonical_source_profile"] == runtime["source_profile"]
    assert entry["runtime"] == "kintaiyi.wenchang_nine_stars_tongzong.wenchang_nine_star_tongzong"
    assert entry["cycle"] == {
        "large_cycle": 2700,
        "small_cycle": 270,
        "years_per_star": 30,
        "start": "一宫文昌",
        "direction": "顺行九宫",
    }
    assert entry["ziting_manuscript_boundary"]["status"] == "not_attested_in_manuscript_toc"

    ziting = _load(ZITING)
    pointer = next(e for e in ziting["entries"] if e["key"] == "wenchang_nine_stars")
    assert pointer["term_type"] == "modern_edition_cross_source_recovery_pointer"
    assert pointer["primary_evidence_level"] == "ziting_manuscript_not_attested_modern_appendix_only"
    assert pointer["primary_result_allowed"] is False
    assert pointer["canonical_catalog"] == "terminology/wenchang-nine-stars.json"
    assert pointer["manuscript_toc_evidence"]["status"] == "title_not_attested"


def test_rules_json_registers_c68_and_c70_without_source_merge():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-WUFU-AUSPICIOUS"]["rule_id"] == "C68-WUFU-AUSPICIOUS-NUMBER"
    assert by_id["R-WENCHANG-NINE-STARS-TONGZONG"]["rule_id"] == (
        "C70-TONGZONG-WENCHANG-NINE-STARS"
    )
    assert "研易楼明钞本目录未见该题" in by_id["R-WENCHANG-NINE-STARS-TONGZONG"]["canonical"]


def test_c70_direct_evidence_matches_runtime_table_and_keeps_dynamic_boundary_closed():
    runtime = c70_catalog()
    evidence = runtime["direct_text_evidence"]

    assert evidence == DIRECT_TEXT_EVIDENCE
    assert evidence["witness_id"] == "NGJ892411999009267118912"
    assert evidence["facts"]["star_names"] == [row["star"] for row in STAR_TABLE]
    assert evidence["facts"]["years_per_star"] == 30
    assert evidence["facts"]["small_cycle"] == 270
    assert evidence["facts"]["large_cycle"] == 2700
    assert evidence["facts"]["start"] == "一宫文昌"
    assert evidence["facts"]["direction"] == "顺行九宫"
    assert runtime["dynamic_distribution_boundary"]["supported"] is False
    assert runtime["cross_source_canonical_selected"] == (
        "tongzong_volume6_ngj_wenchang_nine_stars"
    )


def test_nine_star_crosswalk_forbids_taiyi_wenchang_merge():
    data = _load(CROSSWALK)
    bridge = next(b for b in data["bridges"] if b["id"] == "CW-NINE-STARS-SOURCE-BOUNDARY")

    keys = {(m["catalog"], m["key"]) for m in bridge["members"]}
    assert keys == {
        ("terminology/zitingjing.json", "taiyi_nine_stars"),
        ("terminology/wenchang-nine-stars.json", "wenchang_nine_stars"),
    }
    assert bridge["relation"] == "distinct_nine_star_systems_with_explicit_source_separation"
    assert any("研易楼明钞本目录未见" in x for x in bridge["forbidden_merge"])
    assert any("来源假说" in x for x in bridge["forbidden_merge"])
