from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.zitingjing_primary import (
    PRIMARY_SOURCE_TITLE,
    TAIYI_NINE_STARS_PRIMARY,
    build_c19_verified_primary_results,
    c19_primary_catalog,
    shiji_changes_primary_core,
    shiji_year_element_collation,
    taiyi_nine_stars_primary,
    wenchang_changes_primary,
)
from kintaiyi.zitingjing_sources import build_zitingjing_source_variants


def test_c19_uses_full_taiyi_zitingjing_title():
    assert PRIMARY_SOURCE_TITLE == "太乙紫庭经"


def test_taiyi_nine_stars_primary_has_nine_palaces_and_four_good_five_bad():
    data = taiyi_nine_stars_primary()
    table = data["table"]
    assert len(table) == 9
    assert [item["palace"] for item in table] == list(range(1, 10))
    assert sum(item["fortune"] == "吉" for item in table) == 4
    assert sum(item["fortune"] == "凶" for item in table) == 5
    assert data["source_locator"]["section"] == "释九宫所值九星"
    assert data["primary_source_title"] == "太乙紫庭经"


def test_taiyi_nine_stars_primary_keeps_current_witness_reading_for_palace_three():
    item = next(item for item in TAIYI_NINE_STARS_PRIMARY if item["palace"] == 3)
    assert item == {
        "palace": 3,
        "star": "天冲",
        "region": "青州",
        "fortune": "凶",
    }
    data = taiyi_nine_stars_primary()
    variant = data["known_variants"][0]
    assert variant["field"] == "palace_3_tianchong_fortune"
    assert variant["primary_witness"] == "凶"
    assert variant["collation_witness"] == "吉"
    assert variant["resolution"] == "preserve_both_no_silent_merge"


def test_wenchang_primary_relations_are_source_limited():
    data = wenchang_changes_primary()
    assert data["identity"] == {
        "name": "文昌",
        "role": "天目",
        "element": "土",
        "symbolic_role": "辅相",
    }
    assert data["relations_to_taiyi"]["same_palace"]["pattern"] == "囚"
    assert data["relations_to_taiyi"]["one_palace_ahead"]["pattern"] == "外迫"
    assert data["relations_to_taiyi"]["one_palace_behind"]["pattern"] == "内迫"
    assert data["relations_to_taiyi"]["opposite"]["pattern"] == "对"
    assert data["two_eyes_related"]["home_favored_palaces"] == [1, 8, 3, 7]
    assert data["two_eyes_related"]["away_favored_palaces"] == [4, 9, 6, 2]


def test_shiji_primary_core_includes_collated_year_element_table():
    data = shiji_changes_primary_core()
    assert data["identity"]["astral_correspondence"] == "荧惑之精"
    assert data["identity"]["element"] == "火"
    assert data["military_role"]["role"] == "客目"
    assert data["military_role"]["favors"] == "客"
    assert data["relations"]["covers_taiyi"]["pattern"] == "掩"
    assert data["relations"]["covers_wenchang"]["pattern"] == "关"
    assert data["relations"]["covers_wenchang"]["home_favored_palaces"] == [1, 8, 3, 7]
    assert data["relations"]["covers_wenchang"]["away_favored_palaces"] == [4, 9, 2, 6]
    assert data["relations"]["adjacent_to_taiyi"]["pattern"] == "击"
    assert data["detailed_year_stem_element_table_status"] == "collated_with_preserved_variants"
    assert data["year_element_collation"]["normalization_complete"] is True


def test_shiji_year_element_collation_has_25_normalized_rows():
    data = shiji_year_element_collation()
    assert data["normalized_row_count"] == 25
    assert data["normalization_complete"] is True
    for group in ("甲乙", "丙丁", "戊己", "庚辛", "壬癸"):
        rows = data["stem_groups"][group]["rows"]
        assert {row["element"] for row in rows} == {"木", "火", "土", "金", "水"}


def test_shiji_collation_corrects_only_ocr_labels_with_witness_trail():
    data = shiji_year_element_collation()
    corrections = {
        (item["stem_group"], item["witness_label"], item["normalized_element"])
        for item in data["ocr_corrections"]
    }
    assert ("戊己", "水", "木") in corrections
    assert ("壬癸", "王", "土") in corrections
    assert len(data["ocr_corrections"]) == 2


def test_shiji_gengxin_earth_summer_variant_is_preserved():
    data = shiji_year_element_collation()
    variant = next(
        item for item in data["textual_variants"]
        if item["stem_group"] == "庚辛" and item["element"] == "土"
    )
    assert variant["variants"]["taiyi_zitingjing_online"] == "夏大旱"
    assert variant["variants"]["taiyi_mishu_and_tongzong_collation"] == "夏大水"
    assert variant["resolution"] == "preserve_both_no_silent_merge"


def test_c19_catalog_marks_only_three_direct_primary_items_as_implemented():
    data = c19_primary_catalog()
    assert set(data["implemented"]) == {
        "taiyi_nine_stars",
        "wenchang_changes",
        "shiji_changes",
    }
    assert data["pending"] == [
        "wenchang_nine_stars",
        "three_banners",
        "nine_palace_nobles",
    ]
    assert data["locators"]["wenchang_nine_stars"]["status"] == "catalog_attested_primary_text_pending"
    assert "两处现代整理本目录" in data["locators"]["wenchang_nine_stars"]["catalog_witness"]["evidence"]
    assert data["locators"]["three_banners"]["status"] == "project_primary_attribution_unverified"
    assert data["locators"]["three_banners"]["catalog_check"]["ziting_mijue_catalog_result"] == "not_found"
    assert data["locators"]["three_banners"]["collation_locator"]["source"] == "太乙统宗宝鉴卷十"
    assert data["locators"]["nine_palace_nobles"]["status"] == "project_primary_attribution_unverified"
    assert data["locators"]["nine_palace_nobles"]["catalog_check"]["ziting_mijue_catalog_result"] == "not_found"
    assert data["locators"]["nine_palace_nobles"]["collation_locator"]["source"] == "太乙统宗宝鉴卷十"


def test_verified_primary_results_do_not_substitute_for_missing_legacy_collation_profiles():
    variants = build_zitingjing_source_variants(
        results=build_c19_verified_primary_results()
    )
    snapshot = attach_v2_to_snapshot({
        "太乙落宮": 1,
        "太乙": "乾",
        "太乙九星": {"legacy": True},
        "文昌九星": {"legacy": True},
        "文昌變化": {"legacy": True},
        "始擊變化": {"legacy": True},
        "三旗行宮": {"legacy": True},
        "九宮貴神": {"legacy": True},
    }, source_variants=variants)

    report = audit_legacy_snapshot(snapshot)

    # 旧flat六项源自统宗实现；即使三项已有紫庭primary，
    # 也不能拿primary_result替代同源统宗collation profile。
    assert report["replacement_gaps"] == [
        "source_variants.zitingjing.rules.taiyi_nine_stars.collation_results.tongzong_volume6",
        "source_variants.zitingjing.rules.wenchang_nine_stars.collation_results.tongzong_volume6",
        "source_variants.zitingjing.rules.wenchang_changes.collation_results.tongzong_volume6",
        "source_variants.zitingjing.rules.shiji_changes.collation_results.tongzong_volume6",
        "source_variants.zitingjing.rules.three_banners.collation_results.tongzong_volume10",
        "source_variants.zitingjing.rules.nine_palace_nobles.collation_results.tongzong_volume10",
    ]
    assert report["ready_for_v2_core_consumption"] is False


def test_c19_primary_results_do_not_fill_pending_rules_with_collation_guesses():
    results = build_c19_verified_primary_results()
    assert "wenchang_nine_stars" not in results
    assert "three_banners" not in results
    assert "nine_palace_nobles" not in results
