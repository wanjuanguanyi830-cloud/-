import pytest

from kintaiyi.wufu_four_taiyi_relations import (
    COORDINATE_BOUNDARY,
    COUNTERPARTS,
    RECENT_WORK_INTERPRETATION,
    c94_catalog,
    wufu_four_taiyi_relation,
)


PROFILE = "oct4_recovered_four_taiyi_elemental"


@pytest.mark.parametrize(
    "counterpart,element,effects",
    [
        ("天乙", "金", ["兵盗"]),
        ("地乙", "土", ["疫疠", "民灾"]),
        ("直符", "火", ["旱蝗"]),
        ("四神", "水", ["淋雨", "川溃"]),
    ],
)
def test_c94_recovers_oct4_four_element_mapping(counterpart, element, effects):
    data = wufu_four_taiyi_relation(
        counterpart,
        same_wufu_domain=True,
        interpretation_profile=PROFILE,
    )
    assert data["counterpart_element"] == element
    assert data["effects"] == ["五福之福减损", *effects]
    assert data["status"] == "explicit_same_wufu_domain_relation"


def test_c94_requires_explicit_interpretation_profile():
    with pytest.raises(TypeError):
        wufu_four_taiyi_relation("天乙", same_wufu_domain=True)

    with pytest.raises(ValueError, match="oct4_recovered"):
        wufu_four_taiyi_relation(
            "天乙",
            same_wufu_domain=True,
            interpretation_profile="literal_same_palace",
        )


def test_c94_missing_relation_evidence_stays_pending():
    data = wufu_four_taiyi_relation(
        "地乙",
        same_wufu_domain=None,
        interpretation_profile=PROFILE,
    )
    assert data["effects"] == []
    assert data["status"] == "same_wufu_domain_unchecked"
    assert "不从位置或五域坐标自动判断" in "；".join(data["pending"])


def test_c94_explicit_not_same_domain_has_no_effect():
    data = wufu_four_taiyi_relation(
        "四神",
        same_wufu_domain=False,
        interpretation_profile=PROFILE,
    )
    assert data["effects"] == []
    assert data["status"] == "not_same_wufu_domain"


def test_c94_never_auto_reads_coordinate_or_position_layers():
    data = wufu_four_taiyi_relation(
        "直符",
        same_wufu_domain=True,
        interpretation_profile=PROFILE,
    )
    assert data["coordinate_boundary"] == COORDINATE_BOUNDARY
    assert data["coordinate_boundary"]["auto_coordinate_lookup_used"] is False
    assert data["coordinate_boundary"]["auto_relation_inference_used"] is False
    assert data["coordinate_boundary"]["coordinate_reference"] == (
        "terminology/wufu_domains.json"
    )


def test_c94_legacy_zhifu_alias_requires_opt_in():
    with pytest.raises(ValueError, match="值符不是C94 canonical"):
        wufu_four_taiyi_relation(
            "值符",
            same_wufu_domain=True,
            interpretation_profile=PROFILE,
        )

    data = wufu_four_taiyi_relation(
        "值符",
        same_wufu_domain=True,
        interpretation_profile=PROFILE,
        allow_legacy_zhifu_alias=True,
    )
    assert data["counterpart"] == "直符"
    assert data["effects"][-1] == "旱蝗"


def test_c94_recovery_is_strictly_inside_oct4_oct5_window():
    data = RECENT_WORK_INTERPRETATION
    assert data["created_from"]["file_commit_date"].startswith("2026-10-04")
    assert data["coordinate_basis"]["file_commit_date"].startswith("2026-10-04")
    assert data["time_window_policy"] == (
        "only_2026-10-04_and_2026-10-05_prior_work"
    )


def test_c94_catalog_has_no_implicit_interpretation_default():
    data = c94_catalog()
    assert data["interpretation_profile_required"] is True
    assert data["default_interpretation_profile"] is None
    assert set(data["counterparts"]) == set(COUNTERPARTS)
