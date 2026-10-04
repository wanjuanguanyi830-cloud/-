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


def test_runtime_status_matches_second_batch_implementation():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-03"]["implementation_status"] == "implemented_source_specific"
    assert any(path.endswith(".zhuke_xiangguan") for path in by_id["J4M-03"]["runtime"])
    assert any(path.endswith(".j4m03_eye_element_from_god") for path in by_id["J4M-03"]["runtime"])
    assert by_id["J4M-03"]["target_crosswalk"]["layer"] is None

    assert by_id["J4M-05"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-05"]["runtime"].endswith(".chushi_fa")
    assert "兵额表" in by_id["J4M-05"]["implementation_note"]

    assert by_id["J4M-10"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-10"]["runtime"].endswith(".qifu_fa")
    assert by_id["J4M-10"]["target_crosswalk"]["layer"] is None


def test_runtime_status_matches_third_batch_implementation():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-01"]["implementation_status"] == "implemented_source_specific"
    assert any(path.endswith(".sanmen_jubu") for path in by_id["J4M-01"]["runtime"])
    assert any(path.endswith(".zhimen_from_cycle_count") for path in by_id["J4M-01"]["runtime"])

    assert by_id["J4M-02"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-02"]["runtime"].endswith(".wujiang_fabu")

    assert by_id["J4M-08"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-08"]["runtime"].endswith(".suidi_zhibian")
    assert by_id["J4M-08"]["domain"] != by_id["J4M-07"]["domain"]


def test_runtime_status_matches_observation_batch_implementation():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}

    assert by_id["J4M-11"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-11"]["runtime"].endswith(".fengyun_feiniao_zhuzhan")
    assert "not_computable" in by_id["J4M-11"]["implementation_note"]

    assert by_id["J4M-12"]["implementation_status"] == "implemented_source_specific"
    assert by_id["J4M-12"]["runtime"].endswith(".yunqi_dingshengfu")
    assert "不以五行常识补表" in by_id["J4M-12"]["implementation_note"]


def test_j4m04_is_now_source_complete_but_c8_crosswalk_remains_roles_only():
    _, rules = _rules()
    by_id = {item["id"]: item for item in rules}
    rule = by_id["J4M-04"]

    assert rule["implementation_status"] == "implemented_source_specific"
    assert rule["runtime"].endswith(".zhuke_fa")
    assert rule["target_crosswalk"]["layer"] == "C8-L3"
    assert rule["target_crosswalk"]["status"] == "source_runtime_complete_c8_roles_only"
    assert "先胜后负" in rule["implementation_note"]


def test_j4m03_ancient_collation_resolves_two_eye_nayin_without_modern_merge():
    _, rules = _rules()
    rule = {item["id"]: item for item in rules}["J4M-03"]

    assert rule["implementation_status"] == "implemented_source_specific"
    assert rule["collation_status"] == "resolved_by_two_eye_nayin_collation"
    assert rule["canonical"]["scope"] == "日计"
    assert "文昌" in rule["canonical"]["host_eye"]
    assert "始击" in rule["canonical"]["guest_eye"]
    assert "日计二目纳音" in rule["collation_evidence"]["jingyou_taiyi_fuyingjing"]
    assert "二目纳音" in rule["collation_evidence"]["taiyi_taojinge"]

    quarantined = " ".join(rule["legacy_reference_quarantined"])
    assert "wc_n_sj" in quarantined
    assert "主将是否与太乙同宫" in quarantined
    assert "现代《太乙数纳音体系（修正版）》" in quarantined
    assert "不得静默回写" in quarantined
