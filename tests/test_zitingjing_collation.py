from kintaiyi.zitingjing_collation import (
    sancai_shiwei_wenchang_collation_payload,
    tongzong_volume6_wenchang_collation_payload,
    wenchang_nine_stars_collation_witnesses,
)
from kintaiyi.zitingjing_sources import build_zitingjing_rule_sources


def test_wenchang_collation_keeps_primary_pending():
    data = wenchang_nine_stars_collation_witnesses()
    assert data["rule_key"] == "wenchang_nine_stars"
    assert data["primary_evidence_level"] == "catalog_attested_text_pending"
    assert data["primary_result"] is None
    assert data["canonical_selected"] is None


def test_wenchang_collation_records_star_name_variants():
    data = wenchang_nine_stars_collation_witnesses()
    witnesses = {item["source_id"]: item for item in data["witnesses"]}

    assert witnesses["sancai_shiwei_volume81"]["star_names_reading"][2:4] == ["明雄", "阴玄"]
    assert witnesses["tongzong_volume6_cadal02094393"]["star_names_reading"][2:4] == ["明雄", "阴德"]
    assert witnesses["tongzong_volume6_ngj"]["star_names_reading"][2:4] == ["明维", "阴德"]
    assert data["variant_conflicts"]["star_names"]["status"] == "conflicting_readings"


def test_wenchang_cycle_rate_is_explicitly_unresolved():
    data = wenchang_nine_stars_collation_witnesses()
    conflict = data["variant_conflicts"]["cycle_rate"]
    assert conflict["status"] == "unresolved"
    assert conflict["values_seen"] == [10, 30]

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


def test_sancai_shiwei_can_be_stored_as_external_collation_for_wenchang_only():
    data = build_zitingjing_rule_sources(
        "wenchang_nine_stars",
        collation_results={
            "tongzong_volume6": tongzong_volume6_wenchang_collation_payload(),
            "sancai_shiwei_volume81": sancai_shiwei_wenchang_collation_payload(),
        },
    )
    assert data["primary_ready"] is False
    assert data["status"] == "primary_text_pending"
    assert data["canonical_selected"] is None
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


def test_c70_tongzong_runtime_does_not_promote_zitingjing_primary():
    data = wenchang_nine_stars_collation_witnesses()
    assert data["primary_result"] is None
    assert data["canonical_selected"] is None
    assert data["source_specific_runtimes"] == [
        {
            "source_id": "tongzong_volume6_ngj",
            "rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
            "cross_source_canonical": False,
        }
    ]
    ngj = next(
        item for item in data["witnesses"]
        if item["source_id"] == "tongzong_volume6_ngj"
    )
    assert ngj["source_specific_runtime"]["available"] is True
    assert ngj["source_specific_runtime"]["zitingjing_primary_result"] is False
