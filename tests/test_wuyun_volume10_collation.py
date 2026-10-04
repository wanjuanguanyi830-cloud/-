import pytest

from kintaiyi.wuyun_volume10_collation import (
    MEETING_ENUM_WITNESSES,
    MOVEMENT_PERIOD_WITNESSES,
    MOVEMENT_TONES,
    SIX_QI_ELEMENTS,
    meeting_enum_collation,
    movement_period_witness,
    movement_tone,
    six_qi_element,
    volume10_wuyun_collation,
)
from kintaiyi.wuyun_wuyin_sources import volume10_wuyun_profile


def test_c39_five_movements_map_to_five_tones():
    assert MOVEMENT_TONES == {
        "土": {"tone": "宫", "heaven_qi": "黄天"},
        "金": {"tone": "商", "heaven_qi": "素天"},
        "水": {"tone": "羽", "heaven_qi": "玄天"},
        "木": {"tone": "角", "heaven_qi": "苍天"},
        "火": {"tone": "徵", "heaven_qi": "丹天"},
    }


@pytest.mark.parametrize(
    "element,tone",
    [("土", "宫"), ("金", "商"), ("水", "羽"), ("木", "角"), ("火", "徵")],
)
def test_c39_movement_tone_helper(element, tone):
    data = movement_tone(element)
    assert data["element"] == element
    assert data["tone"] == tone
    assert data["source_profile"] == "tongzong_volume10_wuyun_collation"


def test_c39_six_qi_elements_preserve_ocr_witnesses():
    assert SIX_QI_ELEMENTS["厥阴"]["element"] == "木"
    assert SIX_QI_ELEMENTS["少阴"]["element"] == "火"
    assert SIX_QI_ELEMENTS["太阴"]["element"] == "土"
    assert SIX_QI_ELEMENTS["少阳"]["element"] == "火"
    assert SIX_QI_ELEMENTS["阳明"]["element"] == "金"
    assert SIX_QI_ELEMENTS["太阳"]["element"] == "水"

    assert SIX_QI_ELEMENTS["少阴"]["tongzong_witness"] == "少阴君火势化"
    assert SIX_QI_ELEMENTS["少阳"]["tongzong_witness"] == "少阳相火水化"
    assert SIX_QI_ELEMENTS["少阳"]["collation"] == "暑化"
    assert SIX_QI_ELEMENTS["少阳"]["status"] == "ocr_or_textual_variant_preserved"


def test_c39_six_qi_helper_rejects_unknown_name():
    with pytest.raises(ValueError):
        six_qi_element("少阳火")


def test_c39_period_tables_keep_tongzong_and_collation_labels_separate():
    assert MOVEMENT_PERIOD_WITNESSES["太过"]["土"] == {
        "tongzong": "崇阜之纪",
        "collation": "敦阜之纪",
        "status": "textual_variant_preserved",
    }
    assert MOVEMENT_PERIOD_WITNESSES["不及"]["土"]["tongzong"] == "卑坚之纪"
    assert MOVEMENT_PERIOD_WITNESSES["不及"]["土"]["collation"] == "卑监之纪"
    assert MOVEMENT_PERIOD_WITNESSES["平气"]["火"]["tongzong"] == "外明之纪"
    assert MOVEMENT_PERIOD_WITNESSES["平气"]["火"]["collation"] == "升明之纪"
    assert MOVEMENT_PERIOD_WITNESSES["平气"]["金"]["tongzong"] == "主君之纪"
    assert MOVEMENT_PERIOD_WITNESSES["平气"]["金"]["collation"] == "审平之纪"


def test_c39_period_witness_never_selects_variant_silently():
    data = movement_period_witness("平气", "金")
    assert data["tongzong"] == "主君之纪"
    assert data["collation"] == "审平之纪"
    assert data["canonical_selected"] is None


def test_c39_meeting_enum_preserves_three_vs_four_item_witnesses():
    assert MEETING_ENUM_WITNESSES["tongzong"]["items"] == ["天会", "岁会", "逆会"]
    assert MEETING_ENUM_WITNESSES["tongzong"]["convergence"] == "三合辐辏则为太乙天符"
    assert MEETING_ENUM_WITNESSES["taibai_bingbei"]["items"] == [
        "天会", "岁会", "逆会", "辐辏"
    ]

    data = meeting_enum_collation()
    assert data["status"] == "source_variant_unresolved"
    assert data["canonical_selected"] is None
    assert data["cross_source_merge"] is False


def test_c39_collation_does_not_finalize_taiguo_buji_from_stem_alone():
    data = volume10_wuyun_collation()
    assert data["core_tables_status"] == "collated"
    assert data["meeting_enum_status"] == "source_variant_unresolved"
    assert data["year_stem_only_finalizes_taiguo_buji"] is False
    assert data["taiyi_tianfu_formula_status"] == (
        "requires_structured_nine_palace_and_meeting_inputs"
    )


def test_c39_volume10_profile_reports_refined_status():
    data = volume10_wuyun_profile("甲", "子")
    assert data["suihui_status"] == "core_tables_collated_meeting_variant_pending"
    assert data["meeting_enum_status"] == "source_variant_unresolved"
    assert data["year_stem_only_finalizes_taiguo_buji"] is False
    assert data["collation"]["core_tables_status"] == "collated"
    assert data["suihui_relations"] == []


def test_c39_invalid_state_or_element_rejected():
    with pytest.raises(ValueError):
        movement_period_witness("旺", "木")
    with pytest.raises(ValueError):
        movement_period_witness("太过", "风")
