import json
from pathlib import Path

from kintaiyi.zitingjing_sources import build_zitingjing_rule_sources


RECOVERY = Path("terminology/zitingjing-legacy-scan-recovery.json")
MIGRATION = Path("terminology/zitingjing-migration-map.json")
WENCHANG = Path("terminology/wenchang-nine-stars.json")
INDEX = Path("terminology/catalog-index.json")
MANIFEST = Path("terminology/legacy-recovery-manifest.json")
STATUS = Path("terminology/zitingjing-recovery-status.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_prior_workflow_code_residue_is_not_promoted_to_yanyilou_manuscript():
    recovery = _load(RECOVERY)
    entry = next(e for e in recovery["entries"] if e["key"] == "wenchang_nine_stars")

    assert recovery["status"] == (
        "prior_manuscript_scan_confirmed_code_residue_source_ambiguous"
    )
    assert entry["recovered_star_sequence"] == [
        "文曲", "玄鳳", "明維", "昭搖", "立華", "華明", "玄武", "玄冥", "雄明"
    ]
    assert entry["current_audit"]["canonical_equivalent"] is False
    assert "《太乙统宗宝鉴》卷六" in entry["current_audit"]["provenance_correction"]


def test_wenchang_stable_catalog_is_tongzong_and_ziting_slot_is_pointer_only():
    data = _load(WENCHANG)
    entry = next(e for e in data["entries"] if e["key"] == "wenchang_nine_stars")

    assert entry["canonical_rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"
    assert entry["ziting_manuscript_boundary"]["status"] == "not_attested_in_manuscript_toc"

    wrapped = build_zitingjing_rule_sources("wenchang_nine_stars")
    assert wrapped["status"] == "modern_appendix_cross_source_recovery_pointer"
    assert wrapped["primary_ready"] is False
    assert wrapped["canonical_selected"] is None
    assert wrapped["known_source_rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"


def test_migration_map_and_index_keep_history_without_readding_ziting_stable_term():
    migration = _load(MIGRATION)
    entry = next(e for e in migration["entries"] if e["key"] == "wenchang_nine_stars")
    assert entry["legacy_scan_recovery_asset"] == (
        "terminology/zitingjing-legacy-scan-recovery.json"
    )
    assert "文曲" in entry["legacy_recovered_forms"]

    index = _load(INDEX)
    stable_paths = {x["path"] for x in index["stable_catalogs"]}
    assert "terminology/wenchang-nine-stars.json" in stable_paths
    assert any(
        x["path"] == "terminology/zitingjing-legacy-scan-recovery.json"
        for x in index["migration_assets"]
    )


def test_legacy_manifest_moves_wenchang_stable_ref_without_faking_old_fields():
    manifest = _load(MANIFEST)
    entry = next(
        x for x in manifest["stable_entries"]
        if x["stable_ref"] == {
            "catalog": "terminology/wenchang-nine-stars.json",
            "key": "wenchang_nine_stars",
        }
    )
    assert entry["legacy_match_status"].startswith("stable_source_resolved")
    assert entry["legacy_fields"]["old_term_record_id"] is None
    assert entry["legacy_fields"]["source_page"] is None
    assert entry["legacy_fields"]["old_aliases"] is None
    assert "文曲" in entry["recovered_prior_workflow_forms"]


def test_recovery_status_marks_manuscript_reattached_and_rule_source_gap_closed():
    status = _load(STATUS)
    manuscript = status["external_recovery_checks"]["current_conversation_manuscript"]
    assert manuscript["status"] == "reattached_and_toc_inspected"
    assert manuscript["toc_pages"] == [5, 6]
    assert manuscript["wenchang_nine_stars_title_attested"] is False

    entry = next(e for e in status["core_entries"] if e["key"] == "wenchang_nine_stars")
    assert entry["current_rule_source_gap"] is False
    assert entry["known_executable_rule_id"] == "C70-TONGZONG-WENCHANG-NINE-STARS"
    assert entry["known_executable_source_profile"] == (
        "tongzong_volume6_ngj_wenchang_nine_stars"
    )


def test_prior_tongzong_taiyi_nine_star_residue_is_separate_from_yanyilou_scan():
    recovery = _load(RECOVERY)
    entry = next(e for e in recovery["entries"] if e["key"] == "taiyi_nine_stars")

    assert entry["explicit_source_comment"] == "《太乙统宗宝鉴》卷六·太乙九星"
    assert entry["recovered_cycle_annotation"] == {
        "large_cycle": 900,
        "small_cycle": 90,
        "rate": 10,
        "start_text": "命起天蓬順行九星",
    }
    assert entry["current_audit"]["current_replacement"] == "C124-TONGZONG-TAIYI-NINE-STARS"
