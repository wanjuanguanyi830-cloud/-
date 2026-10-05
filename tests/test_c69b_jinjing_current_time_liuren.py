import pytest

from kintaiyi.jinjing_current_time_liuren import (
    C69B_VERSION,
    c69b_catalog,
    current_time_liuren_overlay,
    general_under_branch,
    heaven_plate,
    noble_ground_branch,
    palace_to_liuren_branch,
    twelve_general_plate,
)


def test_c69b_month_general_adds_to_hour_branch():
    # 立冬六日心宿属卯；“加寅”即卯加地盘寅。
    plate = heaven_plate("卯", "寅")
    assert plate["寅"] == "卯"
    assert plate["子"] == "丑"
    assert plate["午"] == "未"


def test_c69b_geng_morning_noble_lands_at_zi_and_runs_forward():
    data = noble_ground_branch(
        day_stem="庚",
        period="朝",
        month_general_branch="卯",
        hour_branch="寅",
    )
    assert data["canonical"] == C69B_VERSION
    assert data["tianyi_ruler"] == "大吉"
    assert data["noble_heaven_branch"] == "丑"
    assert data["noble_ground_branch"] == "子"
    assert data["direction"] == "顺"


def test_c69b_twelve_generals_reproduce_jinjing_example_branches():
    plate = twelve_general_plate(
        day_stem="庚",
        period="朝",
        month_general_branch="卯",
        hour_branch="寅",
    )
    assert plate["general_by_ground"]["巳"] == "青龙"
    assert plate["general_by_ground"]["申"] == "太常"
    assert plate["general_by_ground"]["卯"] == "六合"
    assert plate["general_by_ground"]["午"] == "天空"


def test_c69b_full_jinjing_lidong_sixth_day_example():
    data = current_time_liuren_overlay(
        term="立冬",
        day_number=6,
        hour_branch="寅",
        day_stem="庚",
        period="朝",
        entity_palaces={
            "太乙": 9,
            "主大将": 9,
            "主参将": 7,
            "客大将": 4,
            "客参将": 2,
        },
    )

    assert data["computable"] is True
    assert data["day_position"]["mansion"] == "心"
    assert data["month_general_branch"] == "卯"
    assert data["general_plate"]["noble_ground_branch"] == "子"
    assert data["general_plate"]["direction"] == "顺"

    assert data["entities"]["太乙"]["general"] == "青龙"
    assert data["entities"]["主大将"]["general"] == "青龙"
    assert data["entities"]["主参将"]["general"] == "太常"
    assert data["entities"]["客大将"]["general"] == "六合"
    assert data["entities"]["客参将"]["general"] == "天空"

    assert data["entities"]["太乙"]["verdict"] == "吉"
    assert data["entities"]["主参将"]["verdict"] == "吉"
    assert data["entities"]["客大将"]["verdict"] == "吉"
    assert data["entities"]["客参将"]["verdict"] == "凶"


def test_c69b_source_transcription_tianding_is_not_silently_rewritten():
    projection = palace_to_liuren_branch(2)
    attested = projection["example_attestation"]
    assert attested["observed_general"] == "天空"
    assert attested["source_transcription"] == "天定"
    assert "公开转录" in attested["note"]


@pytest.mark.parametrize(
    ("palace", "branch"),
    [
        (1, "亥"),
        (2, "午"),
        (3, "寅"),
        (4, "卯"),
        (6, "酉"),
        (7, "申"),
        (8, "子"),
        (9, "巳"),
    ],
)
def test_c69b_palace_branch_projection_is_explicitly_lossy(palace, branch):
    data = palace_to_liuren_branch(palace)
    assert data["branch"] == branch
    assert data["projection_lossy"] is True


def test_c69b_center_five_is_not_projected_to_twelve_branches():
    data = palace_to_liuren_branch(5)
    assert data["computable"] is False
    assert data["branch"] is None
    assert data["status"] == "center_unprojectable"


def test_c69b_direct_branch_input_can_bypass_palace_projection():
    data = current_time_liuren_overlay(
        term="立冬",
        day_number=6,
        hour_branch="寅",
        day_stem="庚",
        period="朝",
        entity_branches={"自定义对象": "巳"},
    )
    assert data["entities"]["自定义对象"]["general"] == "青龙"
    assert data["entities"]["自定义对象"]["projection"] is None


def test_c69b_huangdao_ambiguity_propagates_as_not_computable():
    data = current_time_liuren_overlay(
        term="大寒",
        day_number=20,
        hour_branch="寅",
        day_stem="庚",
        period="朝",
    )
    assert data["computable"] is False
    assert data["status"] == "huangdao_upstream_not_computable"
    assert data["day_position"]["blocked_by"] == "虚"


def test_c69b_general_order_matches_c69_front_five_back_six():
    catalog = c69b_catalog()
    assert catalog["twelve_general_order"] == [
        "天乙贵神", "螣蛇", "朱雀", "六合", "勾陈", "青龙",
        "天空", "白虎", "太常", "玄武", "太阴", "天后",
    ]
    boundary = catalog["formula_boundary"]
    assert boundary["complete_for_explicit_inputs"] is True
    assert boundary["c69_complete_current_time_formula"] is False
    assert boundary["not_automatic"] == ["公历日期->节气第几日", "时辰->朝/暮判定"]
    assert "虚宿" in boundary["upstream_computability_limits"][0]
    assert boundary["coordinate_adapter_boundary"]["lossy"] is True
    assert boundary["coordinate_adapter_boundary"]["strict_alternative"] == "直接提供entity_branches"
    assert "不表示C69B" in boundary["c69_complete_false_means"]


def test_c69b_rejects_invalid_branch():
    with pytest.raises(ValueError):
        heaven_plate("卯", "不存在")
