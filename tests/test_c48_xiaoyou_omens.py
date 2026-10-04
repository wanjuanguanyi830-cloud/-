import pytest

from kintaiyi.xiaoyou_hexagram import xiaoyou_heavy_hexagram
from kintaiyi.xiaoyou_omens import (
    BAD_PATTERNS,
    BRANCH_REGION,
    LEGACY_REFERENCE_AUDIT,
    STEM_REGION_VARIANTS,
    c48_source_catalog,
    xiaoyou_line_omens,
)


def test_c48_requires_c47_upstream_identity():
    with pytest.raises(ValueError, match="C47"):
        xiaoyou_line_omens({"rule_id": "wrong"})


def test_c48_second_fifth_lines_are_middle_path_peaceful():
    second = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(5),
        pattern_evidence=[],
        moving_line_najia="甲寅",
    )
    assert second["upstream"]["moving_line"] == 2
    assert second["line_omen"]["line_class"] == "中道"
    assert second["line_omen"]["summary"] == "安平之岁"
    assert second["line_omen"]["requires_calculation_response"] is False

    fifth = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(17),
        pattern_evidence=[],
        moving_line_najia="壬申",
    )
    assert fifth["upstream"]["moving_line"] == 5
    assert fifth["line_omen"]["summary"] == "安平之岁"


def test_c48_first_fourth_lines_require_both_harmony_and_response():
    good = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(1),
        calculation_harmonious=True,
        has_response=True,
        pattern_evidence=[],
        moving_line_najia="甲子",
    )
    assert good["line_omen"]["summary"] == "吉"
    assert good["line_omen"]["status"] == "direct"

    bad = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(13),
        calculation_harmonious=False,
        has_response=False,
        pattern_evidence=[],
        moving_line_najia="丙午",
    )
    assert bad["upstream"]["moving_line"] == 4
    assert bad["line_omen"]["summary"] == "君臣失助、世不宁"

    mixed = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(1),
        calculation_harmonious=True,
        has_response=False,
        pattern_evidence=[],
        moving_line_najia="甲子",
    )
    assert mixed["line_omen"]["status"] == "not_defined_by_source_passage"
    assert mixed["line_omen"]["summary"] is None


def test_c48_missing_first_fourth_conditions_stays_partial():
    data = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(1),
        pattern_evidence=[],
        moving_line_najia="甲子",
    )
    assert data["status"] == "partial_explicit_evidence"
    assert "初四爻" in "；".join(data["pending"])


def test_c48_inner_outer_extremes_and_pattern_severity_are_distinct():
    inner = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(9),
        pattern_evidence=["关", "迫"],
        moving_line_najia="庚寅",
    )
    assert inner["upstream"]["moving_line"] == 3
    assert inner["line_omen"]["line_class"] == "内极"
    assert inner["bad_pattern_severity"] == "内极尚轻"
    assert inner["bad_pattern_omens"] == ["水旱灾伤", "兵刃饥馑", "疾疫流亡"]

    outer = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(21),
        pattern_evidence=["格"],
        moving_line_najia="壬子",
    )
    assert outer["upstream"]["moving_line"] == 6
    assert outer["line_omen"]["line_class"] == "外极"
    assert outer["bad_pattern_severity"] == "外极为重"


def test_c48_three_talent_omens_follow_c47_outer_year():
    heaven = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(1),
        calculation_harmonious=True,
        has_response=True,
        pattern_evidence=[],
        moving_line_najia="甲子",
    )
    earth = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(2),
        calculation_harmonious=True,
        has_response=True,
        pattern_evidence=[],
        moving_line_najia="乙丑",
    )
    human = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(3),
        calculation_harmonious=True,
        has_response=True,
        pattern_evidence=[],
        moving_line_najia="丙寅",
    )

    assert heaven["upstream"]["three_talent"] == "理天"
    assert "日月失辉" in heaven["three_talent_omen"]["omens"]

    assert earth["upstream"]["three_talent"] == "理地"
    assert "风雨不调" in earth["three_talent_omen"]["omens"]

    assert human["upstream"]["three_talent"] == "理人"
    assert "人民疾疫" in human["three_talent_omen"]["omens"]


@pytest.mark.parametrize(
    "najia,group,expected",
    [
        ("甲寅", "甲乙", "风雷疾病"),
        ("丁巳", "丙丁", "大旱"),
        ("己未", "戊己", "飞蝗"),
        ("辛酉", "庚辛", "兵革攻战"),
        ("癸亥", "壬癸", "大水溢川"),
    ],
)
def test_c48_najia_stem_disaster_groups(najia, group, expected):
    data = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(5),
        pattern_evidence=[],
        moving_line_najia=najia,
    )
    assert data["najia"]["stem_disaster_group"] == group
    assert expected in data["najia"]["stem_disaster_omens"]


def test_c48_najia_does_not_use_sexagenary_parity_validation():
    data = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(5),
        pattern_evidence=[],
        moving_line_najia="甲寅",
    )
    assert data["najia"]["value"] == "甲寅"
    assert "不按六十甲子" in data["najia"]["policy"]


def test_c48_preserves_unresolved_stem_region_variants():
    ding = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(5),
        pattern_evidence=[],
        moving_line_najia="丁巳",
    )
    assert ding["najia"]["stem_region"] is None
    assert ding["najia"]["stem_region_variant"] == STEM_REGION_VARIANTS["丁"]
    assert ding["najia"]["stem_region_variant"]["canonical_selected"] is None

    xin = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(5),
        pattern_evidence=[],
        moving_line_najia="辛酉",
    )
    assert xin["najia"]["stem_region_variant"]["tongzong"] == ["西域", "梁", "益"]
    assert xin["najia"]["stem_region_variant"]["taibai_bingbei"] == ["西戎", "梁", "益"]


def test_c48_branch_regions_are_direct_table():
    data = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(5),
        pattern_evidence=[],
        moving_line_najia="壬戌",
    )
    assert data["najia"]["branch_region"] == "鲁"
    assert BRANCH_REGION["子"] == "齐"
    assert BRANCH_REGION["亥"] == "卫"


def test_c48_missing_najia_or_pattern_check_stays_partial():
    data = xiaoyou_line_omens(
        xiaoyou_heavy_hexagram(5),
    )
    assert data["complete"] is False
    assert data["najia"]["status"] == "not_computable"
    joined = "；".join(data["pending"])
    assert "显式检查" in joined
    assert "动爻纳甲" in joined


def test_c48_pattern_vocabulary_is_source_limited():
    assert BAD_PATTERNS == frozenset({"关", "囚", "掩", "迫", "击", "挟", "格", "对"})
    with pytest.raises(ValueError, match="未知"):
        xiaoyou_line_omens(
            xiaoyou_heavy_hexagram(5),
            pattern_evidence=["杜"],
            moving_line_najia="甲子",
        )


def test_c48_legacy_reference_is_not_equivalent():
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    joined = "；".join(LEGACY_REFERENCE_AUDIT["issues"])
    assert "najia_for_yao" in joined
    assert "算和有应" in joined
    assert "见证差异" in joined


def test_c48_catalog_keeps_layers_separate():
    data = c48_source_catalog()
    assert data["rule_id"] == "C48-XY-OMEN"
    assert data["source_profile"] == "tongzong_volume10_xiaoyou_omens"
    assert data["stem_region_variants"]["丁"]["canonical_selected"] is None
    assert data["branch_region"]["酉"] == "赵"
