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

    assert data["schema_version"] == "1.2"
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

    assert data["last_update"] == "C110"
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
