import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "rules" / "jinjing_v4_witness_matrix.json"


def _matrix():
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def test_c108_witness_matrix_keeps_siku_as_canonical_profile():
    data = _matrix()
    assert data["audit_id"] == "C109-JINJING-V4-WITNESS-AGREEMENT-PATTERNS"
    assert data["canonical_profile"] == "jinjing_siku_volume4"
    assert data["witnesses"]["ncl"]["canonical_override"] is False
    assert data["witnesses"]["jingyou"]["canonical_override"] is False
    assert len(data["entries"]) == 12


def test_c108_j4m06_pending_details_cannot_be_backfilled_from_jingyou():
    data = _matrix()
    row = {item["rule_id"]: item for item in data["entries"]}["J4M-06"]

    assert row["siku"]["values"] == [1, 2, 4, 5, 6, 9]
    assert row["ncl"]["values"] == [1, 2, 3, 4, 6, 7, 8, 9]
    assert row["jingyou"]["values"] == [1, 2, 3, 4, 6, 7, 8, 9]
    assert row["ncl"]["historical_pending_c108"] == [
        "战利方向逐项",
        "背地逐项",
        "阵形逐项",
        "旗色逐项",
    ]
    assert row["ncl"]["pending"] == []
    assert row["ncl"]["status"] == "full_table_direct_visual_verified_C110"
    assert "不互补" in row["hard_boundary"]
    assert "不覆盖" in row["hard_boundary"]


def test_c108_substantive_variants_are_typed_not_flattened_to_aliases():
    data = _matrix()
    rows = {item["rule_id"]: item for item in data["entries"]}

    assert "numeric" in rows["J4M-05"]["difference_class"]
    assert "table_structure" in rows["J4M-06"]["difference_class"]
    assert "palace_group" in rows["J4M-09"]["difference_class"]
    assert "event_verdict" in rows["J4M-11"]["difference_class"]
    assert "verdict" in rows["J4M-12"]["difference_class"]

    assert rows["J4M-09"]["siku"]["inner"] == [8, 3, 4]
    assert rows["J4M-09"]["ncl"]["inner"] == [1, 8, 3, 4]
    assert rows["J4M-12"]["siku"]["west_white"]["base_verdict"] is None
    assert rows["J4M-12"]["ncl"]["west_white"]["base_verdict"] == "大胜"


def test_c109_ncl_jingyou_agreement_cluster_is_observation_not_stemma():
    data = _matrix()
    cluster = data["agreement_patterns"]["NCL06604_JINGYOU_CLUSTER"]

    assert float(data["schema_version"]) >= 1.1
    assert cluster["status"] == "observed_agreement_pattern_not_stemma"

    matches = {item["rule_id"]: item for item in cluster["matches"]}
    assert matches["J4M-06"]["ncl"].startswith("1/2/3/4/6/7/8/9")
    assert matches["J4M-09"]["ncl"] == [1, 8, 3, 4]
    assert matches["J4M-09"]["jingyou"] == [1, 8, 3, 4]
    assert matches["J4M-11"]["ncl"] == ["主人刑→主人败", "客刑→客败"]
    assert matches["J4M-11"]["jingyou"] == ["主人刑→主人败", "客刑→客败"]

    assert any("不据三条一致读法断定" in item for item in cluster["non_claims"])
    assert any("不据一致读法建立抄本谱系" in item for item in cluster["non_claims"])
    assert any("不把NCL与《福应经》合并成一个source profile" in item for item in cluster["non_claims"])


def test_c110_ncl_j4m06_full_table_is_directly_verified_from_supplied_scans():
    data = _matrix()
    row = {item["rule_id"]: item for item in data["entries"]}["J4M-06"]
    table = row["ncl"]["full_table"]

    assert "C110" in data["updates"]
    assert table["1"] == {
        "出军": "西北",
        "战利": "东南",
        "背地": "深涧隐匿之地",
        "阵": "曲阵",
        "旗": "黑旗",
    }
    assert table["2"]["战利"] is None
    assert table["2"]["背地"] == "土山曼行邪道之地"
    assert table["3"]["阵"] == "直阵"
    assert table["3"]["背地"] == "山邑火光耀耀之地"
    assert table["4"]["出军"] == "正东"
    assert table["6"]["背地"] == "水泽沟堑丘墟之地"
    assert table["7"]["背地"] == "川泽丘阜积石之地"
    assert table["8"]["阵"] == "曲阵"
    assert table["8"]["旗"] == "黑旗"
    assert table["9"]["阵"] == "锐阵"
    assert table["9"]["旗"] == "赤旗"

    assert any("直戰" in item and "陣" in item for item in row["ncl"]["scribal_features"])
    assert any("正南" in item and "東" in item for item in row["ncl"]["scribal_features"])
    assert "觀方制變" in row["ncl"]["closing_text"]


def test_c111_ncl_j4m07_body_preserves_terrain_wording_without_overwriting_siku():
    data = _matrix()
    row = {item["rule_id"]: item for item in data["entries"]}["J4M-07"]

    assert "C111" in data["updates"]
    assert row["ncl"]["formation_elements"] == {
        "曲阵": "水",
        "锐阵": "火",
        "直阵": "木",
        "方阵": "金",
        "圆阵": "土",
    }
    assert row["ncl"]["terrain_table"]["后高前下"] == "锐阵"
    assert row["ncl"]["terrain_table"]["前高后下"] == "直阵"
    assert row["ncl"]["terrain_table"]["地跨邪"] == "圆阵"
    assert row["ncl"]["terrain_table"]["地高而平"] == "方阵"
    assert row["ncl"]["terrain_table"]["左右势高"] == "曲阵"
    assert row["ncl"]["direction_rule"] == "地顺其向则吉；地反其向则凶"
    assert "觀方置變" in row["ncl"]["closing_text"]
    assert "地跨邪" in row["hard_boundary"]
    assert "四库canonical" in row["hard_boundary"]


def test_c112_ncl_j4m08_opening_stage_remains_in_update_history():
    data = _matrix()
    row = {item["rule_id"]: item for item in data["entries"]}["J4M-08"]

    assert "C112" in data["updates"]
    assert row["ncl"]["opening_triplet"] == ["士卒服习", "随其地形", "善用兵器"]
    assert row["ncl"]["visible_continuation"] == "五丈之沟居堑之水山林"
    assert "C115" in data["updates"]
    assert row["ncl"]["pending"] == []


def test_c115_ncl_j4m08_full_body_and_mixed_witness_pattern():
    data = _matrix()
    row = {item["rule_id"]: item for item in data["entries"]}["J4M-08"]

    assert "C115" in data["updates"]
    assert row["ncl"]["status"] == "full_contiguous_body_direct_visual_verified_C115"
    assert row["ncl"]["pending"] == []

    rows = row["ncl"]["terrain_weapon_rows"]
    assert rows[0] == {
        "terrain": "五丈之沟居堑之水山林积石川泽丘阜草木所临",
        "favored": "步兵",
        "ratio": "车骑三不当一",
    }
    assert rows[3]["favored"] == "矛鋋"
    assert rows[3]["ratio"] == "弓弩三不当一"
    assert row["ncl"]["training"]["ratio"] == "百不当一"
    assert row["ncl"]["equipment_general"]["ratio"] == "五不当一"

    mixed = data["agreement_patterns"]["NCL06604_J4M08_MIXED_PATTERN"]
    assert mixed["status"] == "mixed_agreement_pattern_not_stemma"
    by_feature = {item["feature"]: item for item in mixed["examples"]}
    assert by_feature["步兵地比例"]["ncl"] == by_feature["步兵地比例"]["siku"]
    assert by_feature["将不习兵比例"]["ncl"] == by_feature["将不习兵比例"]["jingyou"]
    assert by_feature["将不习兵比例"]["ncl"] != by_feature["将不习兵比例"]["siku"]
    assert any("不据局部比例一致" in item for item in mixed["non_claims"])


def test_c120_j4m09_boundary_is_verified_without_recomputing_c86_palace_groups():
    data = _matrix()
    row = {item["rule_id"]: item for item in data["entries"]}["J4M-09"]

    assert "C120" in data["updates"]
    assert "C120" in data["updates"]
    assert row["ncl"]["previous_rule_closing"] == "此之要也"
    assert row["ncl"]["body_title"] == "推太乙在天外地内法"
    assert row["ncl"]["opening_text"] == "古法曰太乙在一八三四宫者为地内宫助主人"
    assert row["ncl"]["boundary_status"] == "J4M-08_to_J4M-09_direct_visual_verified_C120"
    assert row["ncl"]["palace_group_status"] == "direct_visual_verified_C86"
    assert row["ncl"]["inner"] == [1, 8, 3, 4]
    assert row["ncl"]["outer"] == [9, 2, 7, 6]
    assert "不以NCL的1宫补四库canonical" in row["hard_boundary"]


def test_c123_ncl_coverage_summary_is_complete_and_noncanonical():
    data = _matrix()
    summary = data["ncl_coverage_summary"]

    assert data["last_update"] == "C123"
    assert "C123" in data["updates"]
    assert summary["counts"] == {
        "locator_only": 4,
        "selected_readings": 5,
        "full_rule": 3,
        "total": 12,
    }
    assert summary["full_rule_ids"] == ["J4M-06", "J4M-07", "J4M-08"]
    assert summary["selected_reading_ids"] == ["J4M-05", "J4M-09", "J4M-10", "J4M-11", "J4M-12"]
    assert summary["locator_only_ids"] == ["J4M-01", "J4M-02", "J4M-03", "J4M-04"]
    assert "不改变任何canonical或runtime" in summary["policy"]

    rows = {item["rule_id"]: item for item in data["entries"]}
    assert rows["J4M-01"]["ncl"]["coverage"]["status_group"] == "locator_only"
    assert rows["J4M-06"]["ncl"]["coverage"]["status_group"] == "full_rule"
    assert rows["J4M-08"]["ncl"]["coverage"]["evidence_level"] == "full_contiguous_body_direct_visual_verified"
    assert rows["J4M-10"]["ncl"]["coverage"]["status_group"] == "selected_readings"
