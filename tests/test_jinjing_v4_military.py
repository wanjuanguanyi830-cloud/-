from kintaiyi.jinjing_v4_military import (
    chenbing_xiangbei,
    j4m_low_dependency_catalog,
    taiyi_tianwai_dinei,
    zhizhen_suidi,
)


def test_j4m06_chenbing_xiangbei_uses_only_source_defined_rule_numbers():
    one = chenbing_xiangbei(1)
    assert one["rule_id"] == "J4M-06"
    assert one["出军"] == "西北"
    assert one["战利"] == "东南"
    assert one["阵"] == "方阵"
    assert one["旗"] == "白旗"

    two = chenbing_xiangbei(2)
    assert two["邪道"] == "西南"
    assert two["阵"] == "直阵"
    assert two["旗"] == "青旗"

    six = chenbing_xiangbei(6)
    assert six["出军"] == "正西"
    assert six["战利"] == "正东"
    assert six["阵"] == "方阵"

    undefined = chenbing_xiangbei(3)
    assert undefined["computable"] is False
    assert undefined["status"] == "not_defined_by_source_passage"
    assert undefined["defined_rule_numbers"] == [1, 2, 4, 5, 6, 9]


def test_j4m07_terrain_formations_keep_formation_and_five_element_together():
    cases = {
        "后高前下": ("锐阵", "火"),
        "前高后下": ("直阵", "木"),
        "地洿邪": ("圆阵", "土"),
        "地高而平": ("方阵", "金"),
        "左右势高": ("曲阵", "水"),
    }
    for terrain, expected in cases.items():
        data = zhizhen_suidi(terrain)
        assert data["rule_id"] == "J4M-07"
        assert (data["宜阵"], data["五行"]) == expected
        assert data["direction_relation"] == {"顺其向": "吉", "反其向": "凶"}

    unknown = zhizhen_suidi("未知地形")
    assert unknown["computable"] is False
    assert unknown["status"] == "not_computable"


def test_j4m09_jinjing_profile_does_not_import_tongzong_palace_one():
    inner = taiyi_tianwai_dinei(8, three_doors_ready=True, five_generals_released=True)
    assert inner["rule_id"] == "J4M-09"
    assert inner["source_profile"] == "jinjing_siku_volume4"
    assert inner["realm"] == "地内"
    assert inner["assists"] == "主"
    assert inner["decisive_ready"] is True

    outer = taiyi_tianwai_dinei(9, three_doors_ready=True, five_generals_released=True)
    assert outer["realm"] == "天外"
    assert outer["assists"] == "客"

    palace_one = taiyi_tianwai_dinei(1)
    assert palace_one["computable"] is False
    assert palace_one["realm"] is None
    assert palace_one["assists"] is None
    assert palace_one["canonical_groups"]["地内助主"] == [8, 3, 4]


def test_j4m09_does_not_declare_decisive_readiness_without_doors_and_generals():
    missing = taiyi_tianwai_dinei(3)
    assert missing["decisive_ready"] is None

    blocked = taiyi_tianwai_dinei(3, three_doors_ready=True, five_generals_released=False)
    assert blocked["decisive_ready"] is False


def test_low_dependency_catalog_is_explicitly_partial():
    catalog = j4m_low_dependency_catalog()
    assert catalog["implemented"] == ["J4M-06", "J4M-07", "J4M-09"]
    assert "J4M-03" in catalog["pending"]
    assert "J4M-08" in catalog["pending"]
    assert "J4M-11" in catalog["pending"]
    assert "J4M-12" in catalog["pending"]
