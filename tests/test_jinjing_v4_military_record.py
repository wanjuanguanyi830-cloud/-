import json
from pathlib import Path


RULESET_FILE = Path(__file__).parents[1] / "rules" / "jinjing_v4_military.json"


def _rules():
    data = json.loads(RULESET_FILE.read_text(encoding="utf-8"))
    return data, data["rules"]


def test_jinjing_v4_military_has_exact_twelve_body_heading_order():
    data, rules = _rules()
    assert data["ruleset_id"] == "jinjing-siku-v4-military-12"
    assert data["source"]["volume"] == 4
    assert len(rules) == 12
    assert [item["id"] for item in rules] == [f"J4M-{i:02d}" for i in range(1, 13)]
    assert [item["body_title"] for item in rules] == [
        "推三门具不具",
        "推五将发不发",
        "推主客相关法",
        "推主客",
        "推出师法",
        "推陈兵向背",
        "推制阵随地法",
        "推随地制变",
        "推太乙在天外地内法",
        "推奇伏法",
        "推太乙风云飞鸟助战法",
        "推阵有风云气定胜负",
    ]


def test_near_named_rules_remain_distinct():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-03"]["domain"] != by_id["J4M-04"]["domain"]
    assert by_id["J4M-03"]["target_crosswalk"]["layer"] is None
    assert by_id["J4M-04"]["target_crosswalk"]["layer"] == "C8-L3"

    assert by_id["J4M-07"]["body_title"] == "推制阵随地法"
    assert by_id["J4M-08"]["body_title"] == "推随地制变"
    assert by_id["J4M-07"]["domain"] != by_id["J4M-08"]["domain"]

    assert by_id["J4M-05"]["target_crosswalk"]["status"] == "missing_do_not_substitute_chushi_luedi"
    assert by_id["J4M-06"]["target_crosswalk"]["status"] == "missing_do_not_substitute_chenbing_chuxiang"


def test_toc_title_variants_are_aliases_not_extra_rules():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert "推主客相关" in by_id["J4M-03"]["toc_aliases"]
    assert "推障向背法" in by_id["J4M-06"]["toc_aliases"]
    assert "推置阵随地法" in by_id["J4M-07"]["toc_aliases"]
    assert "推随地置变" in by_id["J4M-08"]["toc_aliases"]
    assert "推奇兵伏兵法" in by_id["J4M-10"]["toc_aliases"]
    assert "推对阵有云气定胜负" in by_id["J4M-12"]["toc_aliases"]


def test_jinjing_and_tongzong_taiyi_inner_outer_profiles_are_not_silently_merged():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-09"]

    assert rule["canonical"]["inner_palaces_help_host"] == [8, 3, 4]
    assert rule["canonical"]["outer_palaces_help_guest"] == [9, 2, 7, 6]
    assert rule["canonical"]["palace_1"] == "not_listed_in_jinjing_siku_v4_text"

    tongzong = rule["source_variants"]["tongzong_volume5"]
    assert tongzong["inner_palaces_help_host"] == [1, 8, 3, 4]
    assert tongzong["status"] == "separate_source_variant"
