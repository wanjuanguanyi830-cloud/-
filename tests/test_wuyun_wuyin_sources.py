import pytest

from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot
from kintaiyi.wuyun_wuyin_sources import (
    annual_movement,
    build_wuyun_wuyin_source_variants,
    six_qi_assignment,
    volume10_wuyun_profile,
    volume3_wuyin_from_calc,
    volume3_wuyun_profile,
    wuyin_origin_table,
)


@pytest.mark.parametrize(
    "stem,element",
    [
        ("甲", "土"), ("己", "土"),
        ("乙", "金"), ("庚", "金"),
        ("丙", "水"), ("辛", "水"),
        ("丁", "木"), ("壬", "木"),
        ("戊", "火"), ("癸", "火"),
    ],
)
def test_c37_annual_movement_by_stem(stem, element):
    data = annual_movement(stem)
    assert data["movement_element"] == element
    assert data["movement"] == f"{element}运"
    assert data["shared_core"] is True


@pytest.mark.parametrize(
    "branch,qi,transformation,opposite",
    [
        ("子", "少阴", "热", "午"),
        ("丑", "太阴", "湿", "未"),
        ("寅", "少阳", "相火", "申"),
        ("卯", "阳明", "燥", "酉"),
        ("辰", "太阳", "寒", "戌"),
        ("巳", "厥阴", "风", "亥"),
    ],
)
def test_c37_six_qi_branch_pairing(branch, qi, transformation, opposite):
    data = six_qi_assignment(branch)
    assert data["sitian"] == {"qi": qi, "transformation": transformation}
    assert data["zaiquan_branch"] == opposite
    assert data["zaiquan"]["qi"] == qi


def test_c37_volume3_wuyun_does_not_compute_volume10_suihui():
    data = volume3_wuyun_profile("甲", host_eye="文昌", guest_eye="始击")
    assert data["source_profile"] == "tongzong_volume3_wuyun"
    assert data["rule_id"] == "C37-V3-WYUN"
    assert data["five_movement"]["movement"] == "土运"
    assert data["host_qi"]["role"] == "主气"
    assert data["guest_qi"]["role"] == "客气"
    assert data["suihui_computed"] is False
    assert data["tianfu_computed"] is False


def test_c37_volume10_wuyun_uses_c39_collation_without_copying_old_formula():
    data = volume10_wuyun_profile("乙", "酉", host_eye="文昌", guest_eye="始击")
    assert data["source_profile"] == "tongzong_volume10_wuyun"
    assert data["rule_id"] == "C37-V10-WYUN"
    assert data["five_movement"]["movement"] == "金运"
    assert data["six_qi"]["sitian"] == {"qi": "阳明", "transformation": "燥"}
    assert data["suihui_relations"] == []
    assert data["suihui_status"] == "core_tables_collated_meeting_variant_pending"
    assert data["collation"]["core_tables_status"] == "collated"
    assert data["meeting_enum_status"] == "source_variant_unresolved"
    assert data["year_stem_only_finalizes_taiguo_buji"] is False
    assert data["cross_volume_merge"] is False


@pytest.mark.parametrize(
    "calc,tone,element,subject",
    [
        (1, "宫", "土", "人君"),
        (3, "徵", "火", "宗庙"),
        (5, "羽", "水", "后妃"),
        (7, "商", "金", "子孙"),
        (9, "角", "木", "疾病"),
        (10, "角", "木", "疾病"),
        (15, "羽", "水", "后妃"),
    ],
)
def test_c37_wuyin_reuses_only_d8_03_core(calc, tone, element, subject):
    data = volume3_wuyin_from_calc(calc)
    assert data["source_profile"] == "tongzong_volume3_wuyin"
    assert data["tone"] == tone
    assert data["element"] == element
    assert data["subject"] == subject
    assert data["d8_crosswalk"]["rule_id"] == "D8-03"
    assert data["d8_crosswalk"]["formula_reused"] is True
    assert data["number_subject_rule_d8_08_used"] is False


def test_c37_wuyin_origin_table_is_volume3_only():
    data = wuyin_origin_table()
    assert data["source_profile"] == "tongzong_volume3_wuyin"
    rows = {tuple(item["numbers"]): item for item in data["pairs"]}
    assert rows[(1, 2)]["tone"] == "宫"
    assert rows[(5, 6)]["tone"] == "羽"
    assert rows[(9, 10)]["subject"] == "疾病"
    assert "卷三" in data["policy"]


def _legacy_snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "五運六氣": {"legacy": "卷三卷十混合输出"},
        "五音之數": {"legacy": "卷三综合输出"},
    }


def test_c37_legacy_fields_are_quarantined_to_split_profiles():
    wy = classify_legacy_field("五運六氣")
    yin = classify_legacy_field("五音之數")

    assert wy["status"] == "quarantined"
    assert wy["replacement"] == (
        "source_variants.wuyun_wuyin.wuyun_liuqi.legacy_replacement"
    )
    assert yin["status"] == "quarantined"
    assert yin["replacement"] == (
        "source_variants.wuyun_wuyin.wuyin_number.profiles.tongzong_volume3"
    )


def test_c37_no_profiles_leave_both_legacy_replacement_gaps():
    snapshot = attach_v2_to_snapshot(_legacy_snapshot())
    report = audit_legacy_snapshot(snapshot)
    assert report["replacement_gaps"] == [
        "source_variants.wuyun_wuyin.wuyun_liuqi.legacy_replacement",
        "source_variants.wuyun_wuyin.wuyin_number.profiles.tongzong_volume3",
    ]


def test_c37_only_volume3_wuyun_does_not_clear_mixed_wuyun_legacy_gap():
    variants = build_wuyun_wuyin_source_variants(
        volume3_wuyun=volume3_wuyun_profile("甲"),
        volume3_wuyin=volume3_wuyin_from_calc(1),
    )
    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants={"wuyun_wuyin": variants},
    )
    report = audit_legacy_snapshot(snapshot)

    assert report["replacement_gaps"] == [
        "source_variants.wuyun_wuyin.wuyun_liuqi.legacy_replacement",
    ]
    assert variants["wuyun_liuqi"]["legacy_replacement"] == {}
    assert variants["wuyin_number"]["profiles"]["tongzong_volume3"]


def test_c37_both_wuyun_profiles_plus_volume3_wuyin_clear_legacy_gaps():
    variants = build_wuyun_wuyin_source_variants(
        volume3_wuyun=volume3_wuyun_profile("甲"),
        volume10_wuyun=volume10_wuyun_profile("甲", "子"),
        volume3_wuyin=volume3_wuyin_from_calc(1),
    )
    snapshot = attach_v2_to_snapshot(
        _legacy_snapshot(),
        source_variants={"wuyun_wuyin": variants},
    )
    report = audit_legacy_snapshot(snapshot)

    assert report["replacement_gaps"] == []
    assert report["ready_for_v2_core_consumption"] is True
    assert variants["wuyun_liuqi"]["legacy_replacement"]["source_split_complete"] is True
    assert variants["wuyun_liuqi"]["cross_source_merge"] is False


def test_c37_profile_builder_rejects_wrong_source_identity():
    with pytest.raises(ValueError):
        build_wuyun_wuyin_source_variants(
            volume3_wuyun={
                "source_profile": "tongzong_volume10_wuyun",
                "rule_id": "C37-V3-WYUN",
            }
        )
