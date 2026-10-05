import json
from pathlib import Path

import pytest

from kintaiyi.dayou_hexagram import FOUR_IMAGE_CE, dayou_epoch_variants
from kintaiyi.dayou_lishu import NAJIA_NUMBER, line_addition_policy, lishu_base_status
from kintaiyi.volume9_ehui import ehui_limit_from_evidence, parse_ganzhi
from kintaiyi.volume9_governance import REQUIRED_GODS, SOURCE_VARIANTS, governance_change_from_evidence
from kintaiyi.volume9_disaster_timing import BRANCH_MONTH, disaster_month_from_evidence
from kintaiyi.yinyang_nine_calamities import CALAMITY_SEGMENTS, calamity_timeline


CATALOG = Path("terminology/volume9-10.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c41_terminology_matches_four_image_ce_and_epoch_boundary():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "dayou_heavy_hexagram")

    assert entry["four_image_ce_per_line"] == FOUR_IMAGE_CE
    variants = dayou_epoch_variants()
    assert variants["canonical_selected"] is None
    assert variants["cross_source_merge"] is False
    assert variants["runtime_uses_epoch_variant"] is False


@pytest.mark.parametrize(
    ("line", "mode"),
    [
        (1, "single_current_line"),
        (2, "double_all_six_lines"),
        (3, "no_add_at_extreme"),
        (4, "single_current_line"),
        (5, "double_all_six_lines"),
        (6, "no_add_at_extreme"),
    ],
)
def test_c42_terminology_matches_najia_and_line_policy(line, mode):
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "dayou_lishu")

    assert entry["najia_number"] == NAJIA_NUMBER
    assert line_addition_policy(line)["mode"] == mode
    assert lishu_base_status()["automatic_remainder_formula"] is None


def test_c43_requires_full_sexagenary_and_explicit_source_evidence():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "ehui_limit")

    assert parse_ganzhi("乙未")["ganzhi"] == "乙未"
    with pytest.raises(ValueError):
        parse_ganzhi("未")

    partial = ehui_limit_from_evidence(enthronement_ganzhi="乙未")
    assert partial["computable"] is False
    assert partial["status"] == "not_computable"
    assert entry["required_inputs"] == [
        "enthronement_ganzhi",
        "taiyang_landing",
        "yinzhu_landing",
        "direction",
        "count_evidence",
    ]


def test_c44_preserves_six_god_core_and_unresolved_year_variants():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "governance_change")

    assert entry["required_gods"] == list(REQUIRED_GODS)
    assert entry["year_witness_variants"]["far"] == SOURCE_VARIANTS["tongzong"]["far_year_examples"]
    assert entry["year_witness_variants"]["near_tongzong"] == SOURCE_VARIANTS["tongzong"]["near_year_examples"]
    assert entry["year_witness_variants"]["near_taibai_bingbei"] == SOURCE_VARIANTS["taibai_bingbei"]["near_year_examples"]

    result = governance_change_from_evidence(
        foundation_ganzhi="甲子",
        god_landings={god: "子" for god in REQUIRED_GODS},
        calc_length="长",
        calc_harmonious=True,
        pattern_evidence={},
    )
    assert result["timing"]["distance_class"] == "远"
    assert result["timing"]["canonical_year_selected"] is None
    assert result["timing"]["source_variant_unresolved"] is True


def test_c45_month_mapping_and_dual_target_requirement_match_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "disaster_timing")

    assert entry["branch_month"] == BRANCH_MONTH

    partial = disaster_month_from_evidence(
        year_branch="子",
        year_hegod_anchor="子",
        wenchang_landing_after_year_addition="辰",
        palace_polarity="阳",
        wenchang_same_as_taiyi=False,
        pattern_evidence=[],
    )
    assert partial["computable"] is False
    assert any("天目" in item for item in partial["pending"])


def test_c46_timeline_matches_runtime_totals_and_normalized_fourth_segment():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "yinyang_nine_calamities")

    assert entry["segment_lengths"] == [item["duration_years"] for item in CALAMITY_SEGMENTS]
    assert entry["disaster_years"] == [item["disaster_years"] for item in CALAMITY_SEGMENTS]
    assert sum(entry["segment_lengths"]) == 4560
    assert sum(entry["disaster_years"]) == 57

    timeline = calamity_timeline()
    assert timeline[3]["duration_years"] == 720
    assert timeline[-1]["end_year"] == 4560


def test_c43_to_c46_keep_witness_volume_variant():
    data = _load(CATALOG)
    by_key = {entry["key"]: entry for entry in data["entries"]}

    for key in ("ehui_limit", "governance_change", "disaster_timing", "yinyang_nine_calamities"):
        witness = by_key[key]["source_witness"]
        assert witness == {
            "online_volume": 10,
            "project_legacy_volume": 9,
            "volume_status": "witness_volume_variant",
        }


def test_rules_json_points_to_current_volume9_runtime_paths():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-DAYOU-HEX"]["rule_id"] == "C41-DY-HEX"
    assert by_id["R-DAYOU-LISHU"]["rule_ids"] == ["C42-DY-LISHU", "C42-DY-ANJU"]
    assert by_id["R-EHUI-LIMIT"]["rule_id"] == "C43-V9-EHUI"
    assert by_id["R-GOVERNANCE-CHANGE"]["runtime"] == "kintaiyi.volume9_governance.governance_change_from_evidence"
    assert by_id["R-DISASTER-TIMING"]["rule_ids"] == [
        "C45-V9-MONTH", "C45-V9-DAY", "C45-V9-DISASTER"
    ]
    assert by_id["R-NINE-CALAMITIES"]["rule_id"] == "C46-YJ-9E"
