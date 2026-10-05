import json
from pathlib import Path

RULESET_FILE = Path(__file__).parents[1] / "rules" / "jingyou_fuying_v4_military.json"


def _rules():
    data = json.loads(RULESET_FILE.read_text(encoding="utf-8"))
    return data, data["rules"]


def test_jingyou_volume4_is_independent_eleven_rule_profile():
    data, rules = _rules()
    assert data["ruleset_id"] == "jingyou-fuying-v4-military-11"
    assert data["source"]["profile"] == "jingyou_fuying_volume4"
    assert data["cross_source_merge"] is False
    assert data["canonical_selected"] is None
    assert [r["id"] for r in rules] == [f"JF4M-{i:02d}" for i in range(1, 12)]


def test_jingyou_parallel_crosswalk_does_not_reuse_j4m_ids():
    _, rules = _rules()
    pairs = [(r["id"], r["parallel_jinjing_rule"]) for r in rules]
    assert ("JF4M-01", "J4M-01") in pairs
    assert ("JF4M-09", "J4M-09") in pairs
    assert ("JF4M-10", "J4M-11") in pairs
    assert ("JF4M-11", "J4M-10") in pairs
    assert len({r["id"] for r in rules}) == 11


def test_jingyou_chenbing_and_inner_outer_keep_their_own_tables():
    _, rules = _rules()
    by_id = {r["id"]: r for r in rules}
    assert set(by_id["JF4M-06"]["canonical"]["direction_table"]) == {
        "1", "2", "3", "4", "6", "7", "8", "9"
    }
    assert by_id["JF4M-09"]["canonical"]["inner_palaces_help_host"] == [1, 8, 3, 4]
    assert by_id["JF4M-09"]["canonical"]["outer_palaces_help_guest"] == [9, 2, 7, 6]


def test_jingyou_qifu_and_weather_bird_material_differences_are_explicit():
    _, rules = _rules()
    by_id = {r["id"]: r for r in rules}
    qifu = by_id["JF4M-11"]
    assert "奇兵必从大杀之地" in qifu["canonical_summary"]
    assert "不得互改" in qifu["divergence_from_jinjing"]

    weather = by_id["JF4M-10"]
    joined = " ".join(weather["notable_readings"])
    assert "迫击客大将宫客败" in joined
    assert "从主人刑上来主人败" in joined


def test_jingyou_record_only_profile_never_claims_runtime():
    _, rules = _rules()
    assert all(r["implementation_status"] == "source_record_only" for r in rules)
    assert all("runtime" not in r for r in rules)
