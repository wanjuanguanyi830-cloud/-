import pytest

from kintaiyi.xiaoyou_hexagram import xiaoyou_heavy_hexagram
from kintaiyi.xiaoyou_line_omens import (
    BRANCH_REGIONS,
    LEGACY_REFERENCE_AUDIT,
    SOURCE_WITNESS,
    STEM_OMENS,
    STEM_REGIONS,
    THREE_TALENT_OMENS,
    c48_catalog,
    xiaoyou_line_omens,
)


def _x47(year: int):
    return xiaoyou_heavy_hexagram(year)


def test_c48_records_volume_boundary_variant():
    assert SOURCE_WITNESS["online_witness_volume"] == 10
    assert SOURCE_WITNESS["volume_status"] == "witness_volume_boundary_variant"
    assert "卷九末" in SOURCE_WITNESS["alternate_catalog_boundary"]


@pytest.mark.parametrize(
    "year,line,expected",
    [
        (1, 1, "初四"),
        (5, 2, "中道"),
        (9, 3, "内极"),
        (13, 4, "初四"),
        (17, 5, "中道"),
        (21, 6, "外极"),
    ],
)
def test_c48_line_classes_follow_c47_inner_moving_line(year, line, expected):
    data = xiaoyou_line_omens(
        _x47(year),
        calc_harmonious=True,
        has_response=True,
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert data["c47"]["inner_moving_line"] == line
    assert data["line_assessment"]["class"] == expected


def test_c48_second_and_fifth_lines_are_stable_middle_way():
    second = xiaoyou_line_omens(
        _x47(5),
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    fifth = xiaoyou_line_omens(
        _x47(17),
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert second["line_assessment"]["verdict"] == "安平"
    assert fifth["line_assessment"]["verdict"] == "安平"
    assert second["line_assessment"]["computable"] is True
    assert fifth["line_assessment"]["computable"] is True


def test_c48_initial_or_fourth_requires_harmony_and_response():
    missing = xiaoyou_line_omens(
        _x47(1),
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert missing["line_assessment"]["computable"] is False
    assert missing["status"] == "partial"
    assert len(missing["line_assessment"]["pending"]) == 2

    good = xiaoyou_line_omens(
        _x47(1),
        calc_harmonious=True,
        has_response=True,
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert good["line_assessment"]["verdict"] == "吉"

    bad = xiaoyou_line_omens(
        _x47(13),
        calc_harmonious=False,
        has_response=False,
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert bad["line_assessment"]["verdict"] == "君臣失助、世不宁"

    mixed = xiaoyou_line_omens(
        _x47(13),
        calc_harmonious=True,
        has_response=False,
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert mixed["line_assessment"]["verdict"] == "mixed_evidence"


def test_c48_inner_and_outer_extremes_keep_severity_difference():
    inner = xiaoyou_line_omens(
        _x47(9),
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    outer = xiaoyou_line_omens(
        _x47(21),
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert inner["line_assessment"]["verdict"] == "凶变，内极尚轻"
    assert inner["line_assessment"]["severity"] == "较轻"
    assert outer["line_assessment"]["verdict"] == "凶变，外极为重"
    assert outer["line_assessment"]["severity"] == "较重"


@pytest.mark.parametrize(
    "year,talent",
    [(1, "理天"), (2, "理地"), (3, "理人")],
)
def test_c48_three_talent_comes_from_c47_outer_track(year, talent):
    data = xiaoyou_line_omens(
        _x47(year),
        calc_harmonious=True,
        has_response=True,
        pattern_evidence=[],
        moving_line_najia=("甲", "子"),
    )
    assert data["three_talent"]["state"] == talent
    assert data["three_talent"]["omens"] == THREE_TALENT_OMENS[talent]


def test_c48_pattern_evidence_only_adds_aggravating_omens():
    data = xiaoyou_line_omens(
        _x47(5),
        pattern_evidence=["关", "掩", "格"],
        moving_line_najia=("甲", "子"),
    )
    assert data["line_assessment"]["verdict"] == "安平"
    assert data["pattern_omens"] == ["水旱灾伤", "兵刃饥馑", "疾疫流亡"]
    assert data["patterns_aggravate_only"] is True


def test_c48_requires_explicit_pattern_check_even_when_none_present():
    data = xiaoyou_line_omens(
        _x47(5),
        moving_line_najia=("甲", "子"),
    )
    assert data["computable"] is False
    assert "无格局时传空list" in "；".join(data["pending"])


def test_c48_requires_explicit_najia_and_never_forces_hexagram_name():
    data = xiaoyou_line_omens(
        _x47(5),
        pattern_evidence=[],
    )
    assert data["computable"] is False
    assert data["najia"]["provided"] is False
    assert data["legacy_sixtyfour_hexagram_lookup_used"] is False
    assert "显式提供动爻纳甲" in "；".join(data["pending"])


def test_c48_stem_omens_preserve_uncertain_ocr_instead_of_silent_normalization():
    jia = STEM_OMENS["甲"]
    assert jia["effects"] == ["疾病"]
    assert jia["witness_text"] == "风宣疾病"
    assert jia["uncertain_text"] == ["风宣"]
    assert jia["status"] == "partial_text_uncertain"

    geng = STEM_OMENS["庚"]
    assert geng["effects"] == ["兵革攻战", "贼盗相伤", "国界不安"]
    assert "夭慧变现" in geng["uncertain_text"]
    assert geng["status"] == "partial_text_uncertain"


@pytest.mark.parametrize(
    "stem,region",
    [
        ("甲", "齐"),
        ("乙", "夷"),
        ("丙", "楚"),
        ("丁", "蛮"),
        ("戊", "中"),
        ("己", "豫"),
        ("庚", "秦"),
        ("辛", "西域"),
        ("壬", "燕冀"),
        ("癸", "北狄"),
    ],
)
def test_c48_direct_stem_regions_do_not_use_legacy_extensions(stem, region):
    assert STEM_REGIONS[stem] == region
    data = xiaoyou_line_omens(
        _x47(5),
        pattern_evidence=[],
        moving_line_najia=(stem, "子"),
    )
    assert data["najia"]["stem_region"] == region
    assert data["legacy_fenye_extensions_used"] is False


def test_c48_branch_regions_match_direct_source_table():
    assert BRANCH_REGIONS == {
        "子": "齐", "丑": "吴", "寅": "燕", "卯": "宋",
        "辰": "郑", "巳": "楚", "午": "周", "未": "秦",
        "申": "晋", "酉": "赵", "戌": "鲁", "亥": "卫",
    }
    data = xiaoyou_line_omens(
        _x47(5),
        pattern_evidence=[],
        moving_line_najia=("壬", "亥"),
    )
    assert data["najia"]["stem_region"] == "燕冀"
    assert data["najia"]["branch_region"] == "卫"


def test_c48_najia_effects_are_grouped_by_stem_pair():
    bing = xiaoyou_line_omens(
        _x47(5),
        pattern_evidence=[],
        moving_line_najia=("丙", "巳"),
    )
    assert bing["najia"]["stem_omens"]["effects"] == [
        "大旱", "亢怪", "口舌妖言", "后宫有谋"
    ]

    ren = xiaoyou_line_omens(
        _x47(5),
        pattern_evidence=[],
        moving_line_najia=("壬", "亥"),
    )
    assert ren["najia"]["stem_omens"]["effects"] == [
        "淋雨阴沉", "大水溢川", "后妃不安"
    ]


def test_c48_rejects_wrong_c47_identity():
    with pytest.raises(ValueError, match="C47-XY-HEX"):
        xiaoyou_line_omens(
            {"rule_id": "wrong", "source_profile": "tongzong_volume9_xiaoyou"},
            pattern_evidence=[],
            moving_line_najia=("甲", "子"),
        )


def test_c48_rejects_unknown_pattern_or_bad_najia():
    with pytest.raises(ValueError, match="未知小游格局"):
        xiaoyou_line_omens(
            _x47(5),
            pattern_evidence=["杜"],
            moving_line_najia=("甲", "子"),
        )
    with pytest.raises(ValueError, match="十天干"):
        xiaoyou_line_omens(
            _x47(5),
            pattern_evidence=[],
            moving_line_najia=("宫", "子"),
        )
    with pytest.raises(ValueError, match="十二地支"):
        xiaoyou_line_omens(
            _x47(5),
            pattern_evidence=[],
            moving_line_najia=("甲", "艮"),
        )


def test_c48_catalog_marks_legacy_summary_as_non_equivalent():
    data = c48_catalog()
    assert data["rule_id"] == "C48-XY-OMEN"
    assert data["legacy_reference_audit"]["canonical_equivalent"] is False
    assert any("六十四卦" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
    assert any("扩展" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
