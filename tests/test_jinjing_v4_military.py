from kintaiyi.jinjing_v4_military import (
    chenbing_xiangbei,
    chushi_fa,
    j4m_low_dependency_catalog,
    qifu_fa,
    taiyi_tianwai_dinei,
    zhizhen_suidi,
    zhuke_xiangguan,
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


def test_j4m03_host_guest_control_follows_explicit_five_element_examples():
    guest_wins = zhuke_xiangguan("木", "金")
    assert guest_wins["rule_id"] == "J4M-03"
    assert guest_wins["relation"] == "客关得主人"
    assert guest_wins["winner"] == "客"
    assert guest_wins["fully_computable"] is False
    assert guest_wins["day_nayin"]["status"] == "missing"

    host_wins = zhuke_xiangguan("土", "水", day_nayin_element="金")
    assert host_wins["relation"] == "主人关得客"
    assert host_wins["winner"] == "主"
    assert host_wins["day_nayin"]["status"] == "provided_role_pending"

    no_control = zhuke_xiangguan("木", "水")
    assert no_control["relation"] is None
    assert no_control["winner"] is None
    assert no_control["status"] == "no_control_relation_defined"


def test_j4m03_does_not_invent_day_nayin_effect():
    data = zhuke_xiangguan("木", "金", day_nayin_element="火")
    assert data["winner"] == "客"
    assert data["day_nayin"]["value"] == "火"
    assert data["day_nayin"]["status"] == "provided_role_pending"
    assert data["fully_computable"] is False


def test_j4m05_campaign_requires_calc_doors_generals_and_lucky_gate():
    ready = chushi_fa(
        12,
        three_doors_ready=True,
        five_generals_released=True,
        exit_gate="开",
    )
    assert ready["rule_id"] == "J4M-05"
    assert ready["deployment_ready"] is True
    assert ready["status"] == "ready"

    pending_gate = chushi_fa(
        22,
        three_doors_ready=True,
        five_generals_released=True,
    )
    assert pending_gate["source_prerequisites_ready"] is True
    assert pending_gate["deployment_ready"] is None
    assert pending_gate["status"] == "ready_pending_gate"

    bad_calc = chushi_fa(
        13,
        three_doors_ready=True,
        five_generals_released=True,
        exit_gate="生",
    )
    assert bad_calc["deployment_ready"] is False
    assert bad_calc["calc_ready"] is False

    bad_gate = chushi_fa(
        32,
        three_doors_ready=True,
        five_generals_released=True,
        exit_gate="杜",
    )
    assert bad_gate["deployment_ready"] is False
    assert bad_gate["exit_gate_valid"] is False


def test_j4m10_qifu_keeps_each_source_condition_separate():
    hundred = qifu_fa(
        army_size=100,
        calc_value=12,
        tianmu_location="高丛",
        yanpo=True,
        terrain="山林",
    )
    assert hundred["rule_id"] == "J4M-10"
    assert hundred["odd_force_count"] == 30
    assert hundred["ambush_time"] is True
    assert hundred["concealment_time"] is False
    assert hundred["great_kill_location"] == "高丛"
    assert hundred["yanpo_status"] == "favorable_required_timing_present"

    hidden = qifu_fa(calc_value=21, enemy_urgent=True)
    assert hidden["ambush_time"] is False
    assert hidden["concealment_time"] is True
    assert "藏于山林沟涧" in hidden["recommendations"]
    assert "伏于要害" in hidden["recommendations"]

    odd_size = qifu_fa(army_size=101)
    assert odd_size["odd_force_count"] is None
    assert odd_size["odd_force_count_status"] == "ratio_known_rounding_unspecified"


def test_low_dependency_catalog_is_explicitly_partial():
    catalog = j4m_low_dependency_catalog()
    assert catalog["implemented"] == ["J4M-05", "J4M-06", "J4M-07", "J4M-09", "J4M-10"]
    assert catalog["partial"] == ["J4M-03", "J4M-04"]
    assert "J4M-01" in catalog["pending"]
    assert "J4M-08" in catalog["pending"]
    assert "J4M-11" in catalog["pending"]
    assert "J4M-12" in catalog["pending"]
