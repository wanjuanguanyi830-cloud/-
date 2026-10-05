from kintaiyi.zitingjing_collation import (
    sancai_shiwei_wenchang_collation_payload,
    tongzong_volume6_wenchang_collation_payload,
    wenchang_nine_stars_collation_witnesses,
)
from kintaiyi.zitingjing_sources import build_zitingjing_rule_sources


def test_wenchang_collation_selects_c70_ngj_without_ziting_primary():
    data = wenchang_nine_stars_collation_witnesses()

    assert data["rule_key"] == "wenchang_nine_stars"
    assert data["stable_rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"
    assert data["stable_source_profile"] == (
        "tongzong_volume6_ngj_wenchang_nine_stars"
    )
    assert data["canonical_selected"] == "tongzong_volume6_ngj"
    assert data["ziting_manuscript"]["status"] == "toc_title_not_attested"
    assert data["ziting_manuscript"]["toc_pages"] == [5, 6]
    assert data["ziting_manuscript"]["primary_result"] is None
    assert data["modern_edition_appendix"]["status"] == (
        "catalog_attested_provenance_unresolved"
    )


def test_wenchang_collation_records_star_name_variants():
    data = wenchang_nine_stars_collation_witnesses()
    witnesses = {item["source_id"]: item for item in data["witnesses"]}

    assert witnesses["sancai_shiwei_volume81"]["star_names_reading"][2:4] == [
        "明雄", "阴玄"
    ]
    assert witnesses["tongzong_volume6_cadal02094393"]["star_names_reading"][2:4] == [
        "明雄", "阴德"
    ]
    assert witnesses["tongzong_volume6_ngj"]["star_names_reading"][2:4] == [
        "明维", "阴德"
    ]
    assert data["variant_conflicts"]["star_names"]["status"] == "conflicting_readings"


def test_wenchang_cycle_conflict_is_preserved_while_ngj_profile_resolves_c70():
    data = wenchang_nine_stars_collation_witnesses()
    conflict = data["variant_conflicts"]["cycle_rate"]

    assert conflict["status"] == "cross_witness_conflict_selected_profile_resolved"
    assert conflict["values_seen"] == [10, 30]
    assert conflict["selected_profile_value"] == 30

    cadal = next(
        item for item in data["witnesses"]
        if item["source_id"] == "tongzong_volume6_cadal02094393"
    )
    assert cadal["cycle_evidence"]["prose_rate_years_per_palace"] == 10
    assert cadal["cycle_evidence"]["algorithm_rate_years_per_palace"] == 30
    assert cadal["cycle_evidence"]["internal_conflict"] is True

    ngj = next(
        item for item in data["witnesses"]
        if item["source_id"] == "tongzong_volume6_ngj"
    )
    assert ngj["cycle_evidence"] == {
        "prose_rate_years_per_palace": 30,
        "algorithm_rate_years_per_palace": 30,
        "small_cycle_years": 270,
        "large_cycle_years": 2700,
        "internal_conflict": False,
    }


def test_legacy_ziting_source_container_keeps_wenchang_as_cross_source_pointer():
    data = build_zitingjing_rule_sources(
        "wenchang_nine_stars",
        collation_results={
            "tongzong_volume6": tongzong_volume6_wenchang_collation_payload(),
            "sancai_shiwei_volume81": sancai_shiwei_wenchang_collation_payload(),
        },
    )

    assert data["primary_ready"] is False
    assert data["primary_result_allowed"] is False
    assert data["status"] == "modern_appendix_cross_source_recovery_pointer"
    assert data["canonical_selected"] is None
    assert data["known_source_rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"
    assert set(data["collation_results"]) == {
        "tongzong_volume6",
        "sancai_shiwei_volume81",
    }


def test_sancai_shiwei_is_not_a_generic_ziting_collation_source():
    try:
        build_zitingjing_rule_sources(
            "taiyi_nine_stars",
            collation_results={
                "sancai_shiwei_volume81": {"wrong_scope": True},
            },
        )
    except ValueError as exc:
        assert "未知参校来源" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_c70_ngj_is_selected_stable_profile_without_becoming_ziting_primary():
    data = wenchang_nine_stars_collation_witnesses()

    assert data["source_specific_runtimes"] == [
        {
            "source_id": "tongzong_volume6_ngj",
            "rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
            "source_profile": "tongzong_volume6_ngj_wenchang_nine_stars",
            "selected_stable_profile": True,
        }
    ]

    ngj = next(
        item for item in data["witnesses"]
        if item["source_id"] == "tongzong_volume6_ngj"
    )
    assert ngj["source_specific_runtime"]["available"] is True
    assert ngj["source_specific_runtime"]["selected_stable_profile"] is True
    assert ngj["source_specific_runtime"]["zitingjing_primary_result"] is False


def test_tongzong_collation_payload_records_selected_profile_and_keeps_conflict():
    payload = tongzong_volume6_wenchang_collation_payload()

    assert payload["canonical_selected"] == "tongzong_volume6_ngj"
    assert payload["selected_source_profile"] == (
        "tongzong_volume6_ngj_wenchang_nine_stars"
    )
    assert payload["cycle_rate_resolved_for_selected_profile"] is True
    assert payload["cross_witness_cycle_conflict"] is True
