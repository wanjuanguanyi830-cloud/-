import json
from pathlib import Path


ROOT = Path(__file__).parents[1]
STATUS_FILE = ROOT / "terminology" / "zitingjing-recovery-status.json"
MAP_FILE = ROOT / "terminology" / "zitingjing-migration-map.json"


def _status():
    return json.loads(STATUS_FILE.read_text(encoding="utf-8"))


def _migration():
    return json.loads(MAP_FILE.read_text(encoding="utf-8"))


def test_c81_recovery_audit_blocks_synthetic_parser_and_store():
    data = _status()
    assert data["audit_id"] == "C81-ZITINGJING-TERMINOLOGY-RECOVERY-AVAILABILITY"
    assert data["recovery_status"] == "blocked_missing_original_store"
    assert data["original_schema_available"] is False
    assert data["original_file_available"] is False
    assert data["parser_allowed"] is False
    assert data["synthetic_reconstruction_allowed"] is False


def test_c81_repository_history_checks_are_explicit():
    data = _status()
    checks = data["repository_checks"]
    assert checks["current_tree_contains_target"] is False
    assert checks["git_history_matches"] == 0
    assert checks["git_history_paths_checked"] == [
        "terminology.json",
        "terminology/terminology.json",
        "data/terminology.json",
    ]
    assert checks["all_visible_branch_trees_checked"] is True
    assert checks["legacy_store_found_in_visible_git"] is False
    assert checks["visible_branches_checked"] == [
        "main",
        "codex/c1-c7-canonical",
        "codex/taiyi-base-motion-2026-10-04",
        "codex/taiyi-rules-v2-20261005",
        "integrate-taiyi-war-v1-20261004",
    ]


def test_c81_library_no_match_is_not_misreported_as_nonexistence():
    data = _status()
    ext = data["external_recovery_checks"]
    assert ext["chatgpt_library_title_or_content_match"] is False
    assert ext["status"] == "no_retrievable_prior_file_found_in_current_recovery_pass"
    assert "not evidence" in ext["note"]

    local = ext["user_reported_local_copy"]
    assert local["location"] == "local E drive"
    assert local["status"] == "exists_user_confirmed_not_mounted_in_current_runtime"

    residue = ext["legacy_scan_extraction_residue"]
    assert residue["asset"] == "terminology/zitingjing-legacy-scan-recovery.json"
    assert residue["direct_manuscript_pages_reattached"] is False
    assert residue["old_store_fields_recovered"] is False


def test_c81_core_entries_match_c40_recovery_order():
    data = _status()
    migration = _migration()
    ordered = [
        item["key"]
        for item in sorted(data["core_entries"], key=lambda item: item["priority"])
    ]
    assert ordered == migration["recovery_order"]
    assert len(ordered) == 6
    by_key = {item["key"]: item for item in data["core_entries"]}
    assert by_key["wenchang_nine_stars"]["legacy_scan_extraction_residue_available"] is True
    assert all(
        not item["legacy_scan_extraction_residue_available"]
        for key, item in by_key.items()
        if key != "wenchang_nine_stars"
    )
    assert by_key["wenchang_nine_stars"]["current_rule_source_gap"] is True
    assert by_key["three_banners"]["current_rule_source_gap"] is False
    assert by_key["nine_palace_nobles"]["current_rule_source_gap"] is False
    assert by_key["three_banners"]["known_executable_rule_id"] == (
        "C126-TONGZONG-THREE-BANNERS"
    )
    assert by_key["nine_palace_nobles"]["known_executable_rule_id"] == (
        "C127-TONGZONG-NINE-PALACE-NOBLES"
    )


def test_c81_manuscript_fields_are_not_faked():
    data = _status()
    migration = _migration()
    for item in data["core_entries"]:
        assert item["recovered_from_original_store"] is False
        assert item["manuscript_form_recoverable_now"] is False
        assert item["source_page_recoverable_now"] is False

    for item in migration["entries"]:
        assert item["manuscript_form"] is None
        assert item["source_page"] is None


def test_c81_external_sources_cannot_backfill_yanyilou_fields():
    data = _status()
    banned = set(data["non_substitutable_sources"])
    assert "太乙统宗宝鉴" in banned
    assert "三才世纬" in banned
    assert "C70文昌九星统宗profile" in banned
    assert any("Do not use external collation" in line for line in data["policy"])


def test_c81_unblock_contract_distinguishes_store_recovery_from_page_recovery():
    data = _status()
    evidence = " ".join(data["acceptable_unblock_evidence"])
    assert "exact historical terminology.json" in evidence
    assert "manuscript_form/source_page only" in evidence
    assert any("one-time adapter" in line for line in data["policy"])
    assert any("C81 is an availability audit" in line for line in data["policy"])
    assert any("parser_allowed remains false" in line for line in data["policy"])
