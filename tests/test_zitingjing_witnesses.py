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
    witness = zitingjing_manuscript_witnesses()["witnesses"]["taibai_bingbei_harvard_qing_copy"]
    assert witness["ziting_text_evidence"]["level"] == "direct_online_transcription"
    assert "太乙紫庭经表" in witness["ziting_text_evidence"]["attested_titles"]
    assert "太乙紫庭序" in witness["ziting_text_evidence"]["attested_titles"]
    assert witness["wenchang_nine_star_appendix"]["status"] == "not_located_in_current_online_search"


def test_shanghai_yanyilou_witness_records_prior_user_provided_file_without_claiming_current_reinspection():
    witness = zitingjing_manuscript_witnesses()["witnesses"]["shanghai_yanyilou_ming_copy"]
    assert witness["user_previously_provided_manuscript_file"] is True
    assert witness["current_session_file_index_status"] == "not_retrievable_in_current_file_index"
    assert witness["direct_text_reinspection_status"] == "pending_reinspection_from_previously_provided_file"
    assert witness["catalog_attestation"]["appendix_title"] == "附太乙文昌九星值宫术"
    assert witness["catalog_attestation"]["evidence_level"] == "catalog_attested_text_pending"
    assert witness["resource_report"]["status"] == "previously_user_provided_file_not_currently_retrievable"


def test_peking_university_copy_stays_unverified_until_catalog_found():
    witness = zitingjing_manuscript_witnesses()["witnesses"]["peking_university_reported_copy"]
    assert witness["holding_evidence"] == "secondary_article_report_only"
    assert witness["direct_catalog_record_found"] is False
    assert witness["online_resource_found"] is False


def test_historical_bibliography_does_not_prove_current_copy_identity():
    witness = zitingjing_manuscript_witnesses()["witnesses"]["qianqingtang_bibliographic_entry"]
    assert witness["evidence_level"] == "title_attested_only"
    assert witness["identity_resolution"] == "not_proven_identical_to_current_ziting_mijue_copy"


def test_wenchang_appendix_locator_stays_primary_text_pending():
    status = wenchang_nine_star_appendix_locator_status()
    assert status["status"] == "catalog_attested_primary_text_pending"
    assert status["shanghai_yanyilou"]["catalog_attested"] is True
    assert status["shanghai_yanyilou"]["user_previously_provided_file"] is True
    assert status["shanghai_yanyilou"]["direct_text_reinspection_status"] == "pending"
    assert status["harvard_qing_compilation"]["ziting_text_present"] is True
    assert status["harvard_qing_compilation"]["appendix_direct_text_located"] is False
    assert status["peking_university"]["holding_verified_by_library_catalog"] is False
    assert status["primary_result_allowed"] is False
