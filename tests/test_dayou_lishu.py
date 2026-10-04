import pytest

from kintaiyi.dayou_hexagram import compose_dayou_heavy_hexagram
from kintaiyi.dayou_lishu import (
    NAJIA_NUMBER,
    NAJIA_WITNESS_NOTE,
    SOURCE_EXAMPLE_CONFLICT,
    anju_governance_assessment,
    anju_line_assessment,
    compose_lishu,
    line_addition_policy,
    lishu_base_status,
    najia_addition,
    najia_number,
    najia_pair_value,
)


def _heavy(inner="乾", outer="震", year=6):
    return compose_dayou_heavy_hexagram(
        inner_trigram=inner,
        outer_trigram=outer,
        year_in_inner_trigram=year,
    )


def test_c42_najia_number_table_uses_si_hai_four_not_ji_hai():
    assert najia_number("甲") == 9
    assert najia_number("己") == 9
    assert najia_number("子") == 9
    assert najia_number("午") == 9
    assert najia_number("乙") == 8
    assert najia_number("庚") == 8
    assert najia_number("丑") == 8
    assert najia_number("未") == 8
    assert najia_number("丙") == 7
    assert najia_number("辛") == 7
    assert najia_number("寅") == 7
    assert najia_number("申") == 7
    assert najia_number("丁") == 6
    assert najia_number("壬") == 6
    assert najia_number("卯") == 6
    assert najia_number("酉") == 6
    assert najia_number("戊") == 5
    assert najia_number("癸") == 5
    assert najia_number("辰") == 5
    assert najia_number("戌") == 5
    assert najia_number("巳") == 4
    assert najia_number("亥") == 4
    assert NAJIA_WITNESS_NOTE["tongzong_ocr"] == "末组在线OCR见“己亥四”"
    assert NAJIA_WITNESS_NOTE["normalized"] == "巳亥"
    assert NAJIA_WITNESS_NOTE["status"] == "ocr_corrected_by_collation"


def test_c42_najia_pair_example_jiazi_is_eighteen():
    data = najia_pair_value("甲", "子")
    assert data == {
        "stem": "甲",
        "branch": "子",
        "stem_value": 9,
        "branch_value": 9,
        "pair_value": 18,
    }


@pytest.mark.parametrize(
    "line,mode,multiplier",
    [
        (1, "single_current_line", 1),
        (2, "double_all_six_lines", 2),
        (3, "no_add_at_extreme", 0),
        (4, "single_current_line", 1),
        (5, "double_all_six_lines", 2),
        (6, "no_add_at_extreme", 0),
    ],
)
def test_c42_line_addition_policy(line, mode, multiplier):
    data = line_addition_policy(line)
    assert data["mode"] == mode
    assert data["multiplier"] == multiplier
    assert data["inner_extreme"] is (line == 3)
    assert data["outer_extreme"] is (line == 6)


def test_c42_initial_or_fourth_line_adds_current_line_only():
    first = najia_addition(1, current_pair=("甲", "子"))
    fourth = najia_addition(4, current_pair=("丁", "卯"))

    assert first["computable"] is True
    assert first["addition"] == 18
    assert len(first["components"]) == 1

    assert fourth["computable"] is True
    assert fourth["addition"] == 12
    assert len(fourth["components"]) == 1


def test_c42_second_or_fifth_line_requires_all_six_pairs_and_doubles_sum():
    pairs = [
        ("甲", "子"),
        ("乙", "丑"),
        ("丙", "寅"),
        ("丁", "卯"),
        ("戊", "辰"),
        ("癸", "亥"),
    ]
    base = sum(najia_pair_value(*pair)["pair_value"] for pair in pairs)

    second = najia_addition(2, six_line_pairs=pairs)
    fifth = najia_addition(5, six_line_pairs=pairs)

    assert second["base_six_line_sum"] == base
    assert second["addition"] == base * 2
    assert fifth["addition"] == base * 2
    assert len(second["components"]) == 6


def test_c42_second_line_without_six_pairs_is_not_computable():
    data = najia_addition(2)
    assert data["computable"] is False
    assert data["addition"] is None
    assert "六爻全部纳甲" in data["pending"][0]


def test_c42_second_line_rejects_wrong_pair_count():
    with pytest.raises(ValueError, match="六爻"):
        najia_addition(2, six_line_pairs=[("甲", "子")] * 5)


@pytest.mark.parametrize("line", [3, 6])
def test_c42_extreme_lines_add_zero_without_najia_input(line):
    data = najia_addition(line)
    assert data["computable"] is True
    assert data["addition"] == 0
    assert data["components"] == []


def test_c42_lishu_base_keeps_conflicting_historical_example_unresolved():
    data = lishu_base_status()
    assert data["automatic_remainder_formula"] is None
    assert data["status"] == "source_example_conflict_requires_explicit_base"
    assert SOURCE_EXAMPLE_CONFLICT["wanli_jiwei"]["status"] == "source_example_arithmetic_conflict"
    assert SOURCE_EXAMPLE_CONFLICT["hongwu"]["status"] == "arithmetically_consistent"
    assert SOURCE_EXAMPLE_CONFLICT["hongwu"]["reported_after_ce"] == 175


def test_c42_compose_lishu_reads_corrected_c41_heavy_ce():
    heavy = _heavy()
    assert heavy["ce"]["total"] == 192

    data = compose_lishu(
        heavy,
        line=1,
        current_pair=("甲", "子"),
    )
    assert data["heavy_hexagram_ce"] == 192
    assert data["final_lishu"] is None
    assert data["status"] == "not_computable_base_remainder_unresolved"
    assert data["automatic_outer_cycle_remainder_used"] is False


def test_c42_compose_lishu_computes_only_from_explicit_base():
    heavy = _heavy()
    data = compose_lishu(
        heavy,
        line=1,
        current_pair=("甲", "子"),
        base_remainder_after_ce=48,
    )
    assert data["najia_addition"]["addition"] == 18
    assert data["base_remainder_after_ce"] == 48
    assert data["final_lishu"] == 66
    assert data["status"] == "computed_from_explicit_base"


def test_c42_extreme_line_final_lishu_equals_explicit_base():
    data = compose_lishu(
        _heavy(year=18),
        line=3,
        base_remainder_after_ce=175,
    )
    assert data["najia_addition"]["addition"] == 0
    assert data["final_lishu"] == 175


def test_c42_rejects_non_c41_heavy_hexagram():
    with pytest.raises(ValueError, match="C41-DY-HEX"):
        compose_lishu({"rule_id": "fake"}, line=1, current_pair=("甲", "子"))


@pytest.mark.parametrize(
    "line,length,phase,extreme,severity",
    [
        (1, "长", None, None, None),
        (2, "长", "正旺", None, None),
        (3, "短", None, "内极", "较轻"),
        (4, "长", None, None, None),
        (5, "长", "时已过", None, None),
        (6, "短", None, "外极", "较重"),
    ],
)
def test_c42_anju_base_line_classification(line, length, phase, extreme, severity):
    data = anju_line_assessment(line)
    assert data["base_length"] == length
    assert data["phase"] == phase
    assert data["extreme"] == extreme
    assert data["extreme_severity"] == severity
    assert data["corrections_applied"] is False


def test_c42_anju_governance_evidence_stays_separate_from_base_result():
    data = anju_governance_assessment(
        3,
        yin_yang_in_position=True,
        yang_line_has_response=False,
        ruler_minister_relation="合",
        extra_patterns=[{"pattern": "掩", "effect": "另论"}],
    )
    assert data["base_result"] == "历数短"
    assert data["governance_evidence"] == [
        {"condition": "阴阳得位", "effect": "政治安"},
        {"condition": "阳爻无应", "effect": "君失臣辅"},
        {"condition": "君臣合", "effect": "政亨"},
    ]
    assert data["extra_patterns"] == [{"pattern": "掩", "effect": "另论"}]
    assert data["corrections_applied"] is False


def test_c42_anju_rejects_unknown_ruler_minister_relation():
    with pytest.raises(ValueError, match="合/格"):
        anju_governance_assessment(1, ruler_minister_relation="和")


def test_c42_invalid_najia_token_rejected():
    with pytest.raises(ValueError):
        najia_number("宫")
    with pytest.raises(TypeError):
        najia_addition(1, current_pair=("甲",))
