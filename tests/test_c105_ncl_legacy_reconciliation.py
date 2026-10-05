import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "terminology" / "ncl06604-legacy-reconciliation-map.json"


def test_c105_ncl_reconciliation_map_never_synthesizes_legacy_ids():
    data = json.loads(MAP.read_text(encoding="utf-8"))

    assert data["audit_id"] == "C105-NCL06604-LEGACY-TERMINOLOGY-RECONCILIATION"
    assert data["witness"]["id"] == "NCL-06604"
    assert data["witness"]["historical_processing_status"] == (
        "prior_scan_and_preliminary_terminology_work_confirmed_by_user"
    )
    assert data["witness"]["old_store_status"] == "not_retrieved"

    assert data["safety"]["synthetic_legacy_ids_allowed"] is False
    assert data["safety"]["duplicate_import_as_new_source_allowed"] is False
    assert all(item["legacy_record_id"] is None for item in data["entries"])


def test_c105_reconciliation_keys_cover_reverified_ncl_terms():
    data = json.loads(MAP.read_text(encoding="utf-8"))
    by_key = {item["key"]: item for item in data["entries"]}

    assert by_key["j4m03_taicu"]["canonical_term"] == "太簇"
    assert by_key["j4m03_taicu"]["accepted_variant"] == "太蔟"
    assert by_key["j4m05_chushi_values"]["ncl_pages"] == [58]
    assert by_key["j4m06_chenbing_xiangbei"]["ncl_pages"] == [59, 60]
    assert "1/2/3/4/6/7/8/9" in by_key["j4m06_chenbing_xiangbei"]["current_verified_evidence"]
    assert by_key["j4m08_maoshan"]["canonical_term"] == "矛鋋"
    assert "一八三四" in by_key["j4m09_inner_palaces"]["current_verified_evidence"]
    assert "推奇兵伏兵法" in by_key["j4m10_qibing_fubing_title"]["current_verified_evidence"]
    assert "主人刑/客刑" in by_key["j4m11_fengyun_feiniao"]["current_verified_evidence"]
    assert "大胜" in by_key["j4m12_yunqi"]["current_verified_evidence"]
