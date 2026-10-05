import json
from pathlib import Path

from kintaiyi.wuyun_volume10_collation import (
    MEETING_ENUM_WITNESSES,
    MOVEMENT_TONES,
    SIX_QI_ELEMENTS,
)
from kintaiyi.wuyun_wuyin_sources import (
    FIVE_MOVEMENT_BY_STEM,
    SOURCE_PROFILES,
    WUYIN_PAIR_TABLE,
    build_wuyun_wuyin_source_variants,
    volume3_wuyin_from_calc,
    volume3_wuyun_profile,
    volume10_wuyun_profile,
)


CATALOG = Path("terminology/wuyun-wuyin.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_wuyun_profiles_are_split_by_volume_and_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "wuyun_liuqi")
    profiles = entry["source_profiles"]

    assert set(profiles) == {"tongzong_volume3", "tongzong_volume10"}
    assert profiles["tongzong_volume3"]["rule_id"] == "C37-V3-WYUN"
    assert profiles["tongzong_volume10"]["rule_id"] == "C37-V10-WYUN"
    assert profiles["tongzong_volume3"]["source_profile"] == "tongzong_volume3_wuyun"
    assert profiles["tongzong_volume10"]["source_profile"] == "tongzong_volume10_wuyun"
    assert SOURCE_PROFILES["tongzong_volume3_wuyun"]["volume"] == 3
    assert SOURCE_PROFILES["tongzong_volume10_wuyun"]["volume"] == 10
    assert data["cross_source_policy"]["cross_volume_merge"] is False


def test_five_movement_by_stem_matches_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "wuyun_liuqi")

    assert entry["shared_five_movement_by_stem"] == FIVE_MOVEMENT_BY_STEM


def test_volume10_collation_tables_match_runtime():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "volume10_wuyun_collation")

    assert entry["movement_tones"] == MOVEMENT_TONES
    assert {
        name: {"element": item["element"], "qi": item["qi"]}
        for name, item in SIX_QI_ELEMENTS.items()
    } == entry["six_qi_elements"]
    assert entry["meeting_enum_witnesses"]["tongzong"] == MEETING_ENUM_WITNESSES["tongzong"]["items"]
    assert entry["meeting_enum_witnesses"]["taibai_bingbei"] == MEETING_ENUM_WITNESSES["taibai_bingbei"]["items"]
    assert entry["meeting_enum_status"] == "source_variant_unresolved"


def test_wuyin_number_pairs_match_runtime_and_d8_crosswalk():
    data = _load(CATALOG)
    entry = next(e for e in data["entries"] if e["key"] == "wuyin_number")

    expected = {
        "/".join(str(n) for n in pair): item
        for pair, item in WUYIN_PAIR_TABLE.items()
    }
    assert entry["pairs"] == expected
    assert entry["rule_id"] == "C37-V3-WYIN"
    assert entry["source_profile"] == "tongzong_volume3_wuyin"
    assert entry["d8_crosswalk"]["rule_id"] == "D8-03"
    assert entry["d8_crosswalk"]["formula_reused"] is True


def test_wuyin_number_reuses_d8_03_not_d8_08():
    result = volume3_wuyin_from_calc(15)

    assert result["tone"] == "羽"
    assert result["element"] == "水"
    assert result["subject"] == "后妃"
    assert result["d8_crosswalk"]["rule_id"] == "D8-03"
    assert result["number_subject_rule_d8_08_used"] is False


def test_wuyun_source_variant_container_requires_both_profiles_for_legacy_replacement():
    v3 = volume3_wuyun_profile("甲")
    v10 = volume10_wuyun_profile("甲", "子")

    partial = build_wuyun_wuyin_source_variants(volume3_wuyun=v3)
    assert partial["wuyun_liuqi"]["legacy_replacement"] == {}

    complete = build_wuyun_wuyin_source_variants(
        volume3_wuyun=v3,
        volume10_wuyun=v10,
    )
    assert complete["wuyun_liuqi"]["legacy_replacement"]["source_split_complete"] is True
    assert complete["wuyun_liuqi"]["cross_source_merge"] is False


def test_wuyun_catalog_preserves_modern_production_calendar_boundary():
    data = _load(CATALOG)
    boundary = data["production_calendar_boundary"]

    assert boundary["calendar_source_of_truth"] == "modern_astronomy_lunisolar"
    assert boundary["taiyi_year_boundary"] == "真实天文冬至交节瞬间"


def test_rules_json_points_to_c37_and_c39_layers():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-WUYUN-LIUQI"]["source_profiles"]["tongzong_volume3"]["rule_id"] == "C37-V3-WYUN"
    assert by_id["R-WUYUN-LIUQI"]["source_profiles"]["tongzong_volume10"]["rule_id"] == "C37-V10-WYUN"
    assert by_id["R-WUYUN-LIUQI"]["source_profiles"]["tongzong_volume10"]["collation_rule"] == "C39"
    assert by_id["R-WUYIN-NUMBER"]["rule_id"] == "C37-V3-WYIN"
    assert by_id["R-WUYIN-NUMBER"]["d8_crosswalk"] == "D8-03"
    assert by_id["R-WUYIN-NUMBER"]["d8_08_used"] is False
