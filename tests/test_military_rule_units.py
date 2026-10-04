from kintaiyi.military_derived_profiles import (
    VOLUME15_TOPICS,
    VOLUME17_TOPICS,
    build_volume15_military_profile,
    build_volume17_military_profile,
)
from kintaiyi.military_rule_units import (
    RULE_UNITS,
    low_dependency_candidates,
    military_rule_unit_catalog,
    payload_key_to_rule_id,
    rule_unit,
    units_for_profile,
)


def test_c22_has_25_source_rules_and_one_cross_volume_helper():
    catalog = military_rule_unit_catalog()
    assert catalog["source_rule_count"] == 25
    assert len(catalog["volume15_source_rules"]) == 14
    assert len(catalog["volume17_source_rules"]) == 11
    assert len(catalog["derived_helpers"]) == 1
    assert catalog["derived_helpers"][0]["rule_id"] == "V17-D1"


def test_volume15_composite_topics_all_have_unique_rule_ids():
    mapping = payload_key_to_rule_id()
    assert tuple(item["payload_key"] for item in units_for_profile("tongzong_volume15")) == VOLUME15_TOPICS
    assert len({mapping[key] for key in VOLUME15_TOPICS}) == len(VOLUME15_TOPICS)
    assert mapping["奇兵伏兵"] == "V15-01"
    assert mapping["軍勢勝負"] == "V15-14"


def test_volume17_composite_topics_distinguish_source_rules_from_cross_helper():
    mapping = payload_key_to_rule_id()
    assert set(VOLUME17_TOPICS) == {
        item["payload_key"]
        for item in units_for_profile("tongzong_volume17")
    } | {
        item["payload_key"]
        for item in units_for_profile("cross_volume_helper")
    }
    assert mapping["求索所得"] == "V17-09"
    assert mapping["孤虛對照"] == "V17-D1"
    assert mapping["時計諸事"] == "V17-10"
    assert mapping["占望行人"] == "V17-11"


def test_guxu_comparison_is_not_a_volume17_source_rule():
    data = rule_unit("V17-D1")
    assert data["source_status"] == "derived_cross_volume_helper"
    assert data["volume_profile"] == "cross_volume_helper"
    assert "卷五" in data["source_title"]
    assert "卷十七" in data["source_title"]
    assert "不是独立卷十七原法" in data["notes"]


def test_low_dependency_candidates_are_explicit_and_exclude_cross_volume_helper():
    ids = [item["rule_id"] for item in low_dependency_candidates()]
    assert ids == [
        "V15-02",
        "V15-03",
        "V15-04",
        "V15-05",
        "V15-06",
        "V15-09",
        "V15-12",
        "V15-13",
    ]
    assert "V17-D1" not in ids


def test_j4m_and_c8_overlap_is_metadata_not_equivalence():
    assert rule_unit("V15-01")["overlaps"] == ["J4M-10"]
    assert "独立source profile" in rule_unit("V15-01")["notes"]
    assert rule_unit("V15-07")["overlaps"] == ["J4M-07", "J4M-08"]
    assert rule_unit("V15-08")["overlaps"] == ["C8-L2", "C8-L3"]
    assert rule_unit("V15-14")["overlaps"] == ["J4M-11", "J4M-12"]
    assert rule_unit("V17-02")["overlaps"] == ["C8-L3"]


def test_external_observation_rules_declare_external_inputs():
    assert rule_unit("V15-09")["external_inputs"] == ["wind_direction_branch"]
    assert rule_unit("V15-12")["external_inputs"] == ["wind_palace"]
    assert rule_unit("V15-13")["external_inputs"] == ["cloud_from_palace"]


def test_c21_profiles_now_expose_rule_id_crosswalk():
    v15 = build_volume15_military_profile()
    v17 = build_volume17_military_profile()
    assert v15["rule_units"]["五陣置旗"] == "V15-02"
    assert v15["rule_units"]["軍勢勝負"] == "V15-14"
    assert v17["rule_units"]["求索所得"] == "V17-09"
    assert v17["rule_units"]["孤虛對照"] == "V17-D1"


def test_unknown_rule_id_is_rejected():
    import pytest
    with pytest.raises(ValueError):
        rule_unit("V17-99")


def test_reference_function_dependencies_are_preserved_as_metadata():
    assert rule_unit("V15-02")["inputs"] == ["home_cal", "away_cal"]
    assert rule_unit("V15-05")["inputs"] == []
    assert rule_unit("V17-04")["inputs"] == ["taiyi", "shiji", "away_general"]
    assert rule_unit("V17-11")["inputs"] == [
        "taiyi", "home_cal", "away_cal", "skyeyes", "shiji", "patterns"
    ]


def test_catalog_policy_forbids_composite_dict_as_source_rule():
    catalog = military_rule_unit_catalog()
    assert "综合卷次只作容器" in catalog["policy"]
    assert "跨卷helper另列" in catalog["policy"]
    assert set(RULE_UNITS) == {
        *(f"V15-{i:02d}" for i in range(1, 15)),
        *(f"V17-{i:02d}" for i in range(1, 12)),
        "V17-D1",
    }
