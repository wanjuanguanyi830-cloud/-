import json
from pathlib import Path

from kintaiyi.taiyi_lishu_evidence import c50_catalog, taiyi_lishu_evidence_bundle


TERMS = Path("terminology/volume9-10.json")
RULES = Path("rules/taiyi_v1.json")


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_c50_catalog_is_evidence_bundle_not_lifespan_formula():
    data = _load(TERMS)
    entry = next(e for e in data["entries"] if e["key"] == "taiyi_lishu_evidence")
    runtime = c50_catalog()

    assert entry["rule_id"] == runtime["rule_id"] == "C50-LISHU-EVIDENCE"
    assert entry["final_lifespan_formula"] is None
    assert runtime["final_lifespan_formula"] is None
    assert "太阳/阴主厄会" in entry["required_evidence_classes"]
    assert "太游轨运卦爻" in entry["required_evidence_classes"]
    assert "小游轨运卦爻" in entry["required_evidence_classes"]


def test_c50_partial_bundle_preserves_missing_evidence_instead_of_inventing_final_year():
    result = taiyi_lishu_evidence_bundle(
        enthronement_ganzhi="甲子",
        pattern_evidence=[],
    )

    assert result["rule_id"] == "C50-LISHU-EVIDENCE"
    assert result["source_profile"] == "tongzong_volume10_lishu_evidence"
    assert result["enthronement_ganzhi_numbers"]["used_as_final_lifespan_formula"] is False
    assert result["final_lifespan"] is None
    assert result["status"] == "partial"
    assert any("厄会" in item for item in result["pending"])
    assert any("太游" in item for item in result["pending"])
    assert any("小游" in item for item in result["pending"])


def test_rules_json_registers_c50():
    data = _load(RULES)
    by_id = {rule["id"]: rule for rule in data["categories"]["public_rules"]}

    assert by_id["R-TAIYI-LISHU-EVIDENCE"]["rule_id"] == "C50-LISHU-EVIDENCE"
