from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.military_derived_profiles import (
    VOLUME15_TOPICS,
    VOLUME17_TOPICS,
    build_military_derived_source_variants,
    build_volume15_military_profile,
    build_volume17_military_profile,
)
from kintaiyi.pan_adapter import attach_v2_to_snapshot


def test_volume15_topics_match_reference_composite_shape():
    assert VOLUME15_TOPICS == (
        "奇兵伏兵",
        "五陣置旗",
        "出兵稱神",
        "陳兵出鄉",
        "選將之術",
        "教兵之術",
        "隨地制變",
        "分合用兵",
        "五音風",
        "五音觀風察將",
        "安營置陣",
        "風從八卦",
        "雲氣逆順",
        "軍勢勝負",
    )


def test_volume17_topics_match_reference_composite_shape():
    assert VOLUME17_TOPICS == (
        "出兵用時",
        "敵國動靜",
        "間諜虛實",
        "敵使虛實",
        "敵兵來方",
        "見聞虛實",
        "討捕叛亡",
        "執囚對吏",
        "求索所得",
        "孤虛對照",
        "時計諸事",
        "占望行人",
    )


def test_volume15_profile_is_derived_and_never_cross_merged():
    data = build_volume15_military_profile({"奇兵伏兵": {"legacy": True}})
    assert data["derived_military_profile"] is True
    assert data["cross_volume_merge"] is False
    assert data["cross_c8_merge"] is False
    assert data["cross_j4m_merge"] is False
    assert data["complete"] is False
    assert data["payload"]["奇兵伏兵"] == {"legacy": True}


def test_volume17_profile_is_derived_and_never_cross_merged():
    data = build_volume17_military_profile({"敵國動靜": {"legacy": True}})
    assert data["derived_military_profile"] is True
    assert data["cross_volume_merge"] is False
    assert data["cross_c8_merge"] is False
    assert data["cross_j4m_merge"] is False
    assert data["complete"] is False


def test_unknown_topics_do_not_get_silently_promoted():
    data = build_volume15_military_profile({
        "奇兵伏兵": {},
        "卷五主客动静": {"wrong": True},
    })
    assert data["unknown_topics"] == ["卷五主客动静"]
    assert data["complete"] is False


def test_boundaries_explicitly_reject_c8_j4m_equivalence():
    v15 = build_volume15_military_profile()
    assert "J4M-10" in v15["boundaries"]["J4M"]["奇兵伏兵"]
    assert "不得" in v15["boundaries"]["J4M"]["軍勢勝負"]
    assert "不得反写" in v15["boundaries"]["C8"]["分合用兵"]

    v17 = build_volume17_military_profile()
    assert "不是 C8" in v17["boundaries"]["C8"]["敵國動靜"]
    assert "跨卷对照" in v17["boundaries"]["C8"]["求索所得"]


def test_legacy_volume15_and_17_are_quarantined_to_independent_profiles():
    v15 = classify_legacy_field("軍事應用")
    v17 = classify_legacy_field("軍事占斷")
    assert v15["status"] == "quarantined"
    assert v15["replacement"] == (
        "source_variants.military_derived.tongzong_volume15.payload"
    )
    assert v17["status"] == "quarantined"
    assert v17["replacement"] == (
        "source_variants.military_derived.tongzong_volume17.payload"
    )


def _legacy_snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "軍事應用": {"奇兵伏兵": {"old": True}},
        "軍事占斷": {"敵國動靜": {"old": True}},
    }


def test_empty_derived_profiles_do_not_clear_replacement_gaps():
    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants=build_military_derived_source_variants(),
    )
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.military_derived.tongzong_volume15.payload",
        "source_variants.military_derived.tongzong_volume17.payload",
    ]
    assert report["ready_for_v2_core_consumption"] is False


def test_explicit_independent_profiles_clear_only_their_own_gaps():
    variants = build_military_derived_source_variants(
        volume15={"奇兵伏兵": {"source": "卷十五"}},
        volume17={"敵國動靜": {"source": "卷十七"}},
    )
    snapshot = attach_v2_to_snapshot(_legacy_snapshot(), source_variants=variants)
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True
    assert report["quarantined_key_count"] == 2


def test_profiles_do_not_promote_old_military_to_analysis_military():
    variants = build_military_derived_source_variants(
        volume15={"奇兵伏兵": {"source": "卷十五"}},
        volume17={"敵國動靜": {"source": "卷十七"}},
    )
    snapshot = attach_v2_to_snapshot(_legacy_snapshot(), source_variants=variants)
    assert snapshot["v2"]["analysis"]["military"] == {}
    assert snapshot["v2"]["source_variants"]["military_derived"]["cross_volume_merge"] is False
