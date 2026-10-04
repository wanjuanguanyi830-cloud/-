from kintaiyi.zitingjing_primary_catalog import (
    PRIMARY_SOURCE_TITLE,
    primary_catalog,
    primary_catalog_entry,
)
from kintaiyi.zitingjing_source_facts import (
    c19_source_fact_bundle,
    zitingjing_nine_star_source_facts,
    zitingjing_wenchang_change_source_facts,
)


def test_primary_catalog_uses_full_source_title():
    data = primary_catalog()
    assert data["primary_source"] == "zitingjing"
    assert data["primary_source_title"] == "太乙紫庭经"


def test_direct_primary_chapters_are_only_marked_when_located():
    nine = primary_catalog_entry("taiyi_nine_stars")
    wc = primary_catalog_entry("wenchang_changes")
    assert nine["primary_location_status"] == "direct_primary_chapter_located"
    assert nine["primary_chapter_title"] == "释九宫所值九星"
    assert wc["primary_location_status"] == "direct_primary_chapter_located"
    assert wc["primary_chapter_title"] == "释天目变化"


def test_pending_rules_do_not_pretend_primary_text_is_located():
    for key in ("wenchang_nine_stars", "three_banners", "nine_palace_nobles"):
        item = primary_catalog_entry(key)
        assert item["implementation_status"] == "pending_direct_primary_text"
        assert item["primary_location_status"] in {
            "bibliographic_anchor_only",
            "pending_direct_primary_location",
        }


def test_shiji_is_toc_confirmed_but_not_yet_direct_page_fetched():
    item = primary_catalog_entry("shiji_changes")
    assert item["primary_location_status"] == "toc_confirmed_primary_chapter"
    assert item["primary_chapter_title"] == "始击变化"
    assert item["implementation_status"] == "pending_direct_page_fetch"


def test_nine_star_static_facts_match_primary_chapter_structure():
    data = zitingjing_nine_star_source_facts()
    assert data["source"] == "太乙紫庭经"
    assert data["chapter"] == "释九宫所值九星"
    assert data["computational_formula_promoted"] is False
    facts = data["facts"]
    assert len(facts) == 9
    assert [item["star"] for item in facts] == [
        "天蓬", "天芮", "天冲", "天辅", "天禽", "天心", "天柱", "天任", "天英"
    ]
    assert [item["palace"] for item in facts] == list(range(1, 10))
    assert [item["auspice"] for item in facts] == [
        "凶", "凶", "凶", "吉", "吉", "吉", "凶", "吉", "凶"
    ]


def test_nine_star_source_facts_do_not_promote_old_900_90_formula():
    data = zitingjing_nine_star_source_facts()
    assert data["cycle_note"]["value_star_cycle_years"] == 10
    assert data["computational_formula_promoted"] is False
    assert "900" not in str(data)
    assert "90" not in str(data)


def test_wenchang_source_facts_preserve_tianmu_identity_and_relations():
    data = zitingjing_wenchang_change_source_facts()
    facts = data["facts"]
    assert facts["identity"] == {
        "heaven_name": "天目",
        "earth_name": "文昌",
        "element": "土",
        "role": "辅相",
    }
    rel = {item["relation"]: item for item in facts["relations"]}
    assert rel["囚"]["condition"] == "文昌与太乙同宫"
    assert rel["外迫"]["condition"] == "文昌在太乙前一宫"
    assert rel["内迫"]["condition"] == "文昌在太乙后一宫"
    assert rel["对"]["condition"] == "文昌与太乙相冲"
    assert rel["二目相关"]["condition"] == "文昌与始击同宫"


def test_wenchang_primary_variant_keeps_palace_one_against_tongzong_excerpt():
    data = zitingjing_wenchang_change_source_facts()
    variant = data["source_variants"]["wenchang_two_eyes_groups"]
    assert variant["primary_taiyi_zitingjing"]["home_favored"] == [1, 8, 3, 7]
    assert variant["tongzong_volume6_collation_excerpt"]["home_favored"] == [8, 3, 7]
    assert variant["status"] == "variant_requires_collation"
    assert "不得" in variant["policy"]


def test_bundle_only_exposes_primary_text_we_have_structured():
    data = c19_source_fact_bundle()
    assert data["primary_source_title"] == PRIMARY_SOURCE_TITLE
    assert data["implemented_as_source_facts_only"] == [
        "taiyi_nine_stars",
        "wenchang_changes",
    ]
    assert "three_banners" in data["not_yet_implemented_from_primary_text"]
    assert "nine_palace_nobles" in data["not_yet_implemented_from_primary_text"]
