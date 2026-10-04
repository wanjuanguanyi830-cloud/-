import pytest

from kintaiyi.coronation_cloud_omens import LEGACY_REFERENCE_AUDIT as C51_LEGACY
from kintaiyi.ten_essences_positions import LEGACY_AUDIT as C53_LEGACY
from kintaiyi.ten_essences_sixteen_gods import LEGACY_AUDIT as C55_LEGACY
from kintaiyi.ten_essences_tianshi import LEGACY_AUDIT as C56_LEGACY
from kintaiyi.volume9_disaster_timing import LEGACY_REFERENCE_AUDIT as C45_LEGACY
from kintaiyi.volume9_ehui import LEGACY_REFERENCE_AUDIT as C43_LEGACY
from kintaiyi.volume9_governance import LEGACY_REFERENCE_AUDIT as C44_LEGACY
from kintaiyi.yinyang_nine_calamities import LEGACY_REFERENCE_AUDIT as C46_LEGACY
from kintaiyi.legacy_formula_quarantine import (
    QUARANTINE,
    is_quarantined,
    quarantine_record,
    quarantine_registry,
)


def test_c57_high_risk_known_wrong_or_nonequivalent_legacy_is_centralized():
    required = {
        "config.flybird",
        "config.fivewind",
        "config.eightwind",
        "config.threewind",
        "config.taijun",
        "config.wuxing",
        "config.tian_wang",
        "config.kingfu",
        "config.tian_shi",
        "yunqi._TEN_JING_FN",
        "yunqi.shijing_shu",
        "guiyun.yinyang_jiu_e",
        "guiyun.ehui_xingxian",
        "guiyun.guozheng_bianyi",
        "guiyun.suizhong_zaifa",
        "guiyun.yunqi_zhanbo",
        "guiyun.outer_hexagram_offset_50",
        "legacy.flybird_wl",
    }
    assert required <= set(QUARANTINE)


def test_c57_every_record_is_explicitly_blocked_from_promotion():
    data = quarantine_registry()
    assert data["all_promotion_blocked"] is True
    assert data["record_count"] == len(QUARANTINE)
    for row in data["records"]:
        assert row["promotion_allowed"] is False
        assert row["canonical_equivalent"] is False
        assert row["reason"]
        assert row["source_module"]


@pytest.mark.parametrize(
    "identifier,replacement",
    [
        ("config.flybird", "C53-FLYBIRD"),
        ("config.fivewind", "C53-FIVEWIND"),
        ("config.eightwind", "C53-EIGHTWIND"),
        ("config.threewind", "C53-THREEWIND"),
        ("config.tian_wang", "C55-TIANHUANG"),
        ("config.kingfu", "C55-DIFU"),
        ("config.tian_shi", "C56-TIANSHI"),
        ("yunqi.shijing_shu", "C54-TAIYI-NUMBER"),
        ("guiyun.yinyang_jiu_e", "C46-YJ-9E"),
        ("guiyun.ehui_xingxian", "C43-V9-EHUI"),
        ("guiyun.guozheng_bianyi", "C44-V9-GOV"),
        ("guiyun.suizhong_zaifa", "C45-V9-DISASTER"),
        ("guiyun.yunqi_zhanbo", "C51-CLOUD-OMEN"),
        ("legacy.flybird_wl", "J4M-11"),
    ],
)
def test_c57_replacements_are_explicit(identifier, replacement):
    row = quarantine_record(identifier)
    assert replacement in row["replacement_rule_ids"]


def test_c57_matches_existing_module_level_false_equivalence_audits():
    assert C53_LEGACY["config.flybird"]["canonical_equivalent"] is False
    assert C53_LEGACY["config.fivewind"]["canonical_equivalent"] is False
    assert C55_LEGACY["config.tian_wang"]["canonical_equivalent"] is False
    assert C55_LEGACY["config.kingfu"]["canonical_equivalent"] is False
    assert C56_LEGACY["canonical_equivalent"] is False

    for audit in (C43_LEGACY, C44_LEGACY, C45_LEGACY, C46_LEGACY, C51_LEGACY):
        assert audit["canonical_equivalent"] is False


def test_c57_does_not_misclassify_valid_modern_profile_as_formula_error():
    assert not is_quarantined("modern_liunian_nayin_2026")
    assert not is_quarantined("MODERN-LIUNIAN-NAYIN")


def test_c57_unknown_identifier_is_not_silently_classified():
    assert is_quarantined("unknown.legacy.formula") is False
    with pytest.raises(KeyError, match="未登记"):
        quarantine_record("unknown.legacy.formula")


def test_c57_preserves_specific_known_error_reasons():
    assert "%8" in QUARANTINE["config.flybird"]["reason"]
    assert "%29" in QUARANTINE["config.fivewind"]["reason"]
    assert "第二段以后" in QUARANTINE["guiyun.yinyang_jiu_e"]["reason"]
    assert "日支" in QUARANTINE["guiyun.yunqi_zhanbo"]["reason"]
    assert "外部" in QUARANTINE["legacy.flybird_wl"]["reason"]
