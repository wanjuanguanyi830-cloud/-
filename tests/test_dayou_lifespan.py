import pytest

from kintaiyi.dayou_lifespan import (
    GAN_NUMBER,
    ZHI_NUMBER,
    lifespan_term_from_remainder,
    moving_line_najia_adjustment,
    najia_pair_number,
    najia_symbol_number,
    settled_reign_assessment,
)


def test_c42_najia_number_table_keeps_ji_at_nine_and_si_hai_at_four():
    assert GAN_NUMBER == {
        "甲": 9, "己": 9,
        "乙": 8, "庚": 8,
        "丙": 7, "辛": 7,
        "丁": 6, "壬": 6,
        "戊": 5, "癸": 5,
    }
    assert ZHI_NUMBER["巳"] == 4
    assert ZHI_NUMBER["亥"] == 4
    assert najia_symbol_number("己")["number"] == 9
    assert najia_symbol_number("亥")["number"] == 4


def test_c42_najia_pair_adds_stem_and_branch_numbers():
    data = najia_pair_number("甲", "子")
    assert data["stem_number"] == 9
    assert data["branch_number"] == 9
    assert data["pair_number"] == 18

    data = najia_pair_number("己", "亥")
    assert data["stem_number"] == 9
    assert data["branch_number"] == 4
    assert data["pair_number"] == 13


def test_c42_initial_and_fourth_lines_add_current_line_only():
    first = moving_line_najia_adjustment(1, current_najia=("甲", "子"))
    assert first["addition"] == 18
    assert first["addition_rule"] == "只加本爻纳甲干支"

    fourth = moving_line_najia_adjustment(4, current_najia=("癸", "亥"))
    assert fourth["addition"] == 9


def test_c42_second_and_fifth_lines_double_all_six_line_najia_numbers():
    six = [
        ("甲", "子"),
        ("乙", "丑"),
        ("丙", "寅"),
        ("丁", "卯"),
        ("戊", "辰"),
        ("己", "亥"),
    ]
    raw = (
        18 + 16 + 14 + 12 + 10 + 13
    )
    second = moving_line_najia_adjustment(2, six_line_najia=six)
    fifth = moving_line_najia_adjustment(5, six_line_najia=six)

    assert second["raw_six_line_total"] == raw
    assert second["addition"] == raw * 2
    assert second["multiplier"] == 2
    assert fifth["addition"] == raw * 2


def test_c42_third_and_sixth_lines_do_not_add_najia():
    third = moving_line_najia_adjustment(3)
    sixth = moving_line_najia_adjustment(6)

    assert third["addition"] == 0
    assert third["addition_rule"] == "不倍不加"
    assert sixth["addition"] == 0


def test_c42_missing_najia_inputs_stay_not_computable():
    first = moving_line_najia_adjustment(1)
    second = moving_line_najia_adjustment(2)

    assert first["status"] == "not_computable"
    assert first["addition"] is None
    assert second["status"] == "not_computable"
    assert second["addition"] is None


def test_c42_lifespan_post_remainder_step_does_not_apply_epoch_formula():
    data = lifespan_term_from_remainder(
        11,
        1,
        current_najia=("甲", "子"),
    )
    assert data["lifespan_term"] == 29
    assert data["formula_scope"] == "post_four_image_ce_remainder_plus_moving_line_najia"
    assert data["epoch_formula_applied"] is False


def test_c42_exact_division_is_not_filled_by_guess():
    data = lifespan_term_from_remainder(0, 3)
    assert data["computable"] is False
    assert data["status"] == "exact_division_source_not_expanded"
    assert data["lifespan_term"] is None


@pytest.mark.parametrize(
    "line,length_class,phase",
    [
        (1, "长", "长位"),
        (2, "长", "正旺"),
        (3, "短", "内极"),
        (4, "长", "长位"),
        (5, "长", "时已过"),
        (6, "短", "外极"),
    ],
)
def test_c42_settled_reign_line_classes(line, length_class, phase):
    data = settled_reign_assessment(line)
    assert data["length_class"] == length_class
    assert data["phase"] == phase


def test_c42_settled_reign_scope_and_extreme_severity():
    inner = settled_reign_assessment(3, scope="内卦")
    assert inner["scope_length"] == "历数应长"
    assert inner["extreme_severity"] == "内极灾轻"

    outer = settled_reign_assessment(6, scope="外卦")
    assert outer["scope_length"] == "历数应短"
    assert outer["extreme_severity"] == "外极灾重"


def test_c42_settled_reign_position_response_and_relation_are_separate():
    data = settled_reign_assessment(
        2,
        scope="内卦",
        yin_yang_in_position=True,
        line_is_yang=True,
        has_response=True,
        ruler_minister_relation="合",
    )
    assert data["position_judgment"] == "政治安"
    assert data["response_judgment"] == "君得臣之助"
    assert data["relation_judgment"] == "政道亨"

    bad = settled_reign_assessment(
        5,
        yin_yang_in_position=False,
        line_is_yang=True,
        has_response=False,
        ruler_minister_relation="格",
    )
    assert bad["position_judgment"] == "政治乱"
    assert bad["response_judgment"] == "君失臣之辅"
    assert bad["relation_judgment"] == "政道乖"


def test_c42_does_not_expand_yin_line_response_rule():
    data = settled_reign_assessment(
        4,
        line_is_yang=False,
        has_response=True,
    )
    assert data["response_judgment"] == "source_not_expanded_for_yin_line_response"


def test_c42_rejects_bad_inputs():
    with pytest.raises(ValueError):
        najia_pair_number("己", "天")
    with pytest.raises(ValueError):
        moving_line_najia_adjustment(7)
    with pytest.raises(ValueError):
        moving_line_najia_adjustment(2, six_line_najia=[("甲", "子")])
    with pytest.raises(ValueError):
        settled_reign_assessment(1, scope="宫")
