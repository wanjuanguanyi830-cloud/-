import pytest

from kintaiyi.coronation_cloud_omens import (
    BRANCH_ELEMENT,
    LEGACY_REFERENCE_AUDIT,
    RELATION_EFFECTS,
    STEM_ELEMENT,
    c51_catalog,
    coronation_cloud_omens,
)


def test_c51_stem_and_branch_elements_are_separate():
    assert STEM_ELEMENT["甲"] == "木"
    assert STEM_ELEMENT["己"] == "土"
    assert STEM_ELEMENT["壬"] == "水"

    assert BRANCH_ELEMENT["寅"] == "木"
    assert BRANCH_ELEMENT["午"] == "火"
    assert BRANCH_ELEMENT["申"] == "金"
    assert BRANCH_ELEMENT["子"] == "水"
    assert BRANCH_ELEMENT["辰"] == "土"


def test_c51_cloud_generates_day_uses_stem_element():
    data = coronation_cloud_omens(
        day_ganzhi="丙寅",
        cloud_color="青",
    )
    assert data["day_element"] == "火"
    assert data["chen_element"] == "木"
    assert data["relation_flags"]["云生日"] is True
    assert data["relations"] == ["云生日"]
    assert data["relation_effects"] == ["国祚昌", "多子"]


def test_c51_cloud_generates_chen_uses_branch_element_not_stem():
    data = coronation_cloud_omens(
        day_ganzhi="乙巳",
        cloud_color="青",
    )
    assert data["day_element"] == "木"
    assert data["chen_element"] == "火"
    assert data["relation_flags"]["云生辰"] is True
    assert data["relation_flags"]["比和"] is True
    assert data["relations"] == ["云生辰", "比和"]
    assert "内宫享福" in data["relation_effects"]
    assert "多女" in data["relation_effects"]
    assert "吉" in data["relation_effects"]


def test_c51_cloud_controls_day_means_no_heir_effect():
    data = coronation_cloud_omens(
        day_ganzhi="戊子",
        cloud_color="青",
    )
    assert data["day_element"] == "土"
    assert data["relation_flags"]["云克日"] is True
    assert data["relations"] == ["云克日"]
    assert data["relation_effects"] == ["绝嗣"]


def test_c51_day_generates_cloud_is_kept_as_separate_good_relation():
    data = coronation_cloud_omens(
        day_ganzhi="壬子",
        cloud_color="青",
    )
    assert data["day_element"] == "水"
    assert data["relation_flags"]["日生云"] is True
    assert data["relations"] == ["日生云"]
    assert data["relation_effects"] == ["吉"]


def test_c51_same_element_is_bihe():
    data = coronation_cloud_omens(
        day_ganzhi="甲子",
        cloud_color="青",
    )
    assert data["relation_flags"]["比和"] is True
    assert data["relations"] == ["比和"]
    assert data["relation_effects"] == ["吉"]


def test_c51_multiple_relations_are_not_collapsed_to_single_verdict():
    data = coronation_cloud_omens(
        day_ganzhi="乙巳",
        cloud_color="青",
    )
    assert len(data["relations"]) == 2
    assert data["overall_single_verdict"] is None


def test_c51_dark_cloud_and_five_color_cloud_are_form_evidence():
    dark = coronation_cloud_omens(
        day_ganzhi="甲子",
        cloud_color="白",
        cloud_form="阴云",
    )
    assert dark["form_effects"] == ["位祚不久"]

    five = coronation_cloud_omens(
        day_ganzhi="甲子",
        cloud_color="白",
        cloud_form="五色彩云",
    )
    assert five["form_effects"] == ["国代绵远寿昌", "子孙兴旺"]


def test_c51_dark_cloud_can_be_observed_without_single_color():
    data = coronation_cloud_omens(
        day_ganzhi="甲子",
        cloud_form="阴云",
    )
    assert data["cloud"]["provided"] is False
    assert data["relation_checked"] is False
    assert data["relation_status"] == "not_computable_without_single_color"
    assert data["relations"] == []
    assert data["form_effects"] == ["位祚不久"]


def test_c51_five_color_cloud_can_be_observed_without_single_color():
    data = coronation_cloud_omens(
        day_ganzhi="甲子",
        cloud_form="五色彩云",
    )
    assert data["cloud"]["provided"] is False
    assert data["relation_checked"] is False
    assert data["relations"] == []
    assert data["form_effects"] == ["国代绵远寿昌", "子孙兴旺"]


def test_c51_cloud_numbers_keep_sheng_cheng_pair_unselected():
    data = coronation_cloud_omens(
        day_ganzhi="甲子",
        cloud_color="青",
    )
    assert data["cloud"]["sheng_number"] == 3
    assert data["cloud"]["cheng_number"] == 8
    assert data["cloud"]["selected_number"] is None
    assert data["cloud_number_selection"] is None
    assert data["cloud_number_selection_status"] == "sheng_cheng_pair_unselected"


def test_c51_ganzhi_numbers_reuse_corrected_c42_table():
    data = coronation_cloud_omens(
        day_ganzhi="己亥",
        cloud_color="黑",
    )
    assert data["ganzhi_numbers"] == {
        "stem": 9,
        "branch": 4,
        "sum": 13,
        "source_dependency": "C42纳甲干支数表",
    }


def test_c51_does_not_invent_year_month_day_hour_scale():
    data = coronation_cloud_omens(
        day_ganzhi="己亥",
        cloud_color="黑",
    )
    assert data["time_scale"] is None
    assert data["specific_period"] is None
    assert "no_unique_selection_rule" in data["time_scale_status"]


def test_c51_relation_effect_table_is_directly_structured():
    assert RELATION_EFFECTS == {
        "云生日": ["国祚昌", "多子"],
        "云生辰": ["内宫享福", "多女"],
        "云克日": ["绝嗣"],
        "日生云": ["吉"],
        "比和": ["吉"],
    }


def test_c51_legacy_reference_is_not_equivalent():
    assert LEGACY_REFERENCE_AUDIT["canonical_equivalent"] is False
    assert any("日支" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
    assert any("己列为4" in item for item in LEGACY_REFERENCE_AUDIT["issues"])
    assert any("if/elif" in item for item in LEGACY_REFERENCE_AUDIT["issues"])


def test_c51_requires_at_least_one_cloud_observation():
    with pytest.raises(ValueError, match="至少一种"):
        coronation_cloud_omens(day_ganzhi="甲子")


def test_c51_rejects_invalid_cloud_form_color_or_ganzhi():
    with pytest.raises(ValueError, match="cloud_form"):
        coronation_cloud_omens(
            day_ganzhi="甲子",
            cloud_color="青",
            cloud_form="乌云",
        )
    with pytest.raises(ValueError, match="cloud_color"):
        coronation_cloud_omens(
            day_ganzhi="甲子",
            cloud_color="紫",
        )
    with pytest.raises(ValueError, match="六十甲子"):
        coronation_cloud_omens(
            day_ganzhi="甲丑",
            cloud_color="青",
        )


def test_c51_catalog_keeps_source_tables_and_audit():
    data = c51_catalog()
    assert data["rule_id"] == "C51-CLOUD-OMEN"
    assert data["stem_elements"]["丙"] == "火"
    assert data["branch_elements"]["巳"] == "火"
    assert data["cloud_numbers"]["青"]["sheng_number"] == 3
    assert data["cloud_numbers"]["青"]["cheng_number"] == 8
    assert data["legacy_reference_audit"]["canonical_equivalent"] is False
