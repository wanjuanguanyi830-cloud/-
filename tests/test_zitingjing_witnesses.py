from kintaiyi.zitingjing_witnesses import (
    wenchang_nine_star_appendix_locator_status,
    zitingjing_manuscript_witnesses,
)


def test_ziting_manuscript_witnesses_do_not_select_one_canonical_copy():
    data = zitingjing_manuscript_witnesses()
    assert data["canonical_manuscript_selected"] is None
    assert data["cross_witness_identity_assumed"] is False
    assert set(data["witnesses"]) == {
        "taibai_bingbei_harvard_qing_copy",
        "shanghai_yanyilou_ming_copy",
        "peking_university_reported_copy",
        "qianqingtang_bibliographic_entry",
    }


def test_harvard_witness_attests_ziting_text_but_not_appendix_location():
    witness = zitingjing_manuscript_witnesses()["witnesses"][
        "taibai_bingbei_harvard_qing_copy"
    ]
    assert witness["ziting_text_evidence"]["level"] == "direct_online_transcription"
    assert "太乙紫庭经表" in witness["ziting_text_evidence"]["attested_titles"]
    assert "太乙紫庭序" in witness["ziting_text_evidence"]["attested_titles"]
    assert witness["wenchang_nine_star_appendix"]["status"] == (
        "not_located_in_current_online_search"
    )


def test_shanghai_yanyilou_witness_records_reattached_scan_and_toc_result():
    witness = zitingjing_manuscript_witnesses()["witnesses"][
        "shanghai_yanyilou_ming_copy"
    ]

    assert witness["witness_type"] == "user_provided_manuscript_scan"
    assert witness["user_previously_provided_manuscript_file"] is True
    assert witness["current_session_file_index_status"] == (
        "reattached_current_conversation"
    )
    assert witness["direct_text_reinspection_status"] == "toc_inspected"
    assert witness["current_uploaded_pdf_pages"] == 150

    toc = witness["manuscript_toc_evidence"]
    assert toc["pdf_pages"] == [5, 6]
    assert toc["volumes_one_to_twelve_attested"] is True
    assert toc["wenchang_nine_stars_title_attested"] is False

    modern = witness["modern_edition"]
    assert modern["appendix_title"] == "附太乙文昌九星值宫术"
    assert modern["appendix_provenance"] == "unresolved"
    assert "来源假说" in modern["note"]


def test_peking_university_copy_stays_unverified_until_catalog_found():
    witness = zitingjing_manuscript_witnesses()["witnesses"][
        "peking_university_reported_copy"
    ]
    assert witness["holding_evidence"] == "secondary_article_report_only"
    assert witness["direct_catalog_record_found"] is False
    assert witness["online_resource_found"] is False


def test_historical_bibliography_does_not_prove_current_copy_identity():
    witness = zitingjing_manuscript_witnesses()["witnesses"][
        "qianqingtang_bibliographic_entry"
    ]
    assert witness["evidence_level"] == "title_attested_only"
    assert witness["identity_resolution"] == (
        "not_proven_identical_to_current_ziting_mijue_copy"
    )


def test_wenchang_appendix_locator_closes_rule_gap_but_keeps_editorial_provenance_open():
    status = wenchang_nine_star_appendix_locator_status()

    assert status["status"] == (
        "manuscript_toc_not_attested_modern_appendix_provenance_unresolved"
    )
    assert status["shanghai_yanyilou"]["manuscript_scan_reattached"] is True
    assert status["shanghai_yanyilou"]["toc_pages"] == [5, 6]
    assert status["shanghai_yanyilou"]["toc_title_attested"] is False
    assert status["shanghai_yanyilou"]["direct_text_reinspection_status"] == (
        "toc_inspected"
    )

    assert status["modern_edition"]["appendix_title_attested"] is True
    assert status["modern_edition"]["provenance"] == "unresolved"
    assert status["modern_edition"]["tongzong_addition_hypothesis"] == (
        "plausible_not_proven"
    )

    assert status["ziting_primary_result_allowed"] is False
    assert status["current_rule_source_gap"] is False
    assert status["known_executable_rule_id"] == (
        "C70-TONGZONG-WENCHANG-NINE-STARS"
    )
    assert status["known_executable_source_profile"] == (
        "tongzong_volume6_ngj_wenchang_nine_stars"
    )
