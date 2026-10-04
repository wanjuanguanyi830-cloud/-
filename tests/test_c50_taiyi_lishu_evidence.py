import pytest

from kintaiyi.dayou_hexagram import compose_dayou_heavy_hexagram
from kintaiyi.taiyi_lishu_evidence import (
    ALLOWED_PATTERNS,
    CORONATION_CLOUD_NUMBERS,
    LEGACY_BOUNDARY,
    c50_catalog,
    coronation_cloud_evidence,
    taiyi_lishu_evidence_bundle,
)
from kintaiyi.volume9_ehui import han_gaozu_example
from kintaiyi.xiaoyou_hexagram import xiaoyou_heavy_hexagram


def _dayou():
    return compose_dayou_heavy_hexagram(
        inner_trigram="乾",
        outer_trigram="震",
        year_in_inner_trigram=13,
    )


def _complete(**overrides):
    kwargs = {
        "enthronement_ganzhi": "乙未",
        "ehui_result": han_gaozu_example(),
        "dayou_hexagram": _dayou(),
        "xiaoyou_hexagram": xiaoyou_heavy_hexagram(80),
        "taiyi_yunqi_hexagram_evidence": {
            "provided": True,
            "source_status": "explicit_upstream_evidence",
        },
        "pattern_evidence": [],
    }
    kwargs.update(overrides)
    return taiyi_lishu_evidence_bundle(**kwargs)


def test_c50_is_not_c42_or_c43_equivalent_formula():
    assert LEGACY_BOUNDARY["c42_equivalent_formula"] is False
    assert LEGACY_BOUNDARY["c43_equivalent_formula"] is False
    data = c50_catalog()
    assert data["final_lifespan_formula"] is None


def test_c50_incomplete_bundle_lists_each_missing_evidence_class():
    data = taiyi_lishu_evidence_bundle(
        enthronement_ganzhi="乙未",
    )
    assert data["evidence_bundle_complete"] is False
    assert data["status"] == "evidence_bundle_partial"
    joined = "；".join(data["pending"])
    assert "C43" in joined
    assert "C41" in joined
    assert "C47" in joined
    assert "运气爻卦象" in joined
    assert "囚迫击格掩挟" in joined


def test_c50_complete_bundle_still_does_not_invent_final_lifespan():
    data = _complete()
    assert data["evidence_bundle_complete"] is True
    assert data["status"] == "evidence_bundle_complete"
    assert data["final_lifespan_years"] is None
    assert data["final_lifespan_status"] == (
        "source_requires_composite_judgement_not_unique_formula"
    )
    assert data["c42_formula_reused_as_c50"] is False
    assert data["c43_formula_reused_as_c50"] is False


def test_c50_enthronement_ganzhi_uses_real_sexagenary_validation():
    data = _complete()
    assert data["enthronement_year"]["ganzhi"] == "乙未"

    with pytest.raises(ValueError, match="六十甲子"):
        _complete(enthronement_ganzhi="甲丑")


def test_c50_records_ganzhi_numbers_but_not_as_lifespan_formula():
    data = _complete(enthronement_ganzhi="甲子")
    assert data["enthronement_ganzhi_numbers"] == {
        "stem": 9,
        "branch": 9,
        "sum": 18,
        "source_dependency": "C42纳甲干支数表",
        "used_as_final_lifespan_formula": False,
    }


@pytest.mark.parametrize(
    "color,element,number",
    [
        ("黄", "土", 5),
        ("白", "金", 9),
        ("青", "木", 3),
        ("黑", "水", 6),
        ("赤", "火", 7),
    ],
)
def test_c50_coronation_cloud_numbers_are_source_table_only(
    color, element, number
):
    data = coronation_cloud_evidence(color)
    assert data["color"] == color
    assert data["element"] == element
    assert data["number"] == number
    assert data["interpretation_applied"] is False


def test_c50_cloud_observation_is_optional_and_does_not_change_completion():
    no_cloud = _complete()
    with_cloud = _complete(cloud_color="白")

    assert no_cloud["evidence_bundle_complete"] is True
    assert no_cloud["cloud"]["provided"] is False

    assert with_cloud["evidence_bundle_complete"] is True
    assert with_cloud["cloud"]["provided"] is True
    assert with_cloud["cloud"]["number"] == 9
    assert with_cloud["final_lifespan_years"] is None


def test_c50_cloud_table_is_fixed():
    assert CORONATION_CLOUD_NUMBERS == {
        "黄": {"element": "土", "number": 5},
        "白": {"element": "金", "number": 9},
        "青": {"element": "木", "number": 3},
        "黑": {"element": "水", "number": 6},
        "赤": {"element": "火", "number": 7},
    }
    with pytest.raises(ValueError):
        coronation_cloud_evidence("紫")


def test_c50_patterns_are_explicit_and_source_limited():
    assert ALLOWED_PATTERNS == frozenset({"囚", "迫", "击", "格", "掩", "挟"})
    data = _complete(pattern_evidence=["囚", "格", "挟"])
    assert data["pattern_checked"] is True
    assert data["pattern_evidence"] == ["囚", "格", "挟"]

    with pytest.raises(ValueError, match="未知C50格局"):
        _complete(pattern_evidence=["对"])


def test_c50_requires_explicit_empty_pattern_check():
    data = _complete(pattern_evidence=None)
    assert data["evidence_bundle_complete"] is False
    assert "无格局时传空list" in "；".join(data["pending"])


def test_c50_rejects_wrong_upstream_rule_identities():
    with pytest.raises(ValueError, match="C43-V9-EHUI"):
        _complete(ehui_result={"rule_id": "wrong"})
    with pytest.raises(ValueError, match="C41-DY-HEX"):
        _complete(dayou_hexagram={"rule_id": "wrong"})
    with pytest.raises(ValueError, match="C47-XY-HEX"):
        _complete(xiaoyou_hexagram={"rule_id": "wrong"})


def test_c50_preserves_upstream_evidence_without_recalculation():
    ehui = han_gaozu_example()
    dayou = _dayou()
    xiaoyou = xiaoyou_heavy_hexagram(80)
    yunqi = {"provided": True, "note": "external explicit evidence"}

    data = taiyi_lishu_evidence_bundle(
        enthronement_ganzhi="乙未",
        ehui_result=ehui,
        dayou_hexagram=dayou,
        xiaoyou_hexagram=xiaoyou,
        taiyi_yunqi_hexagram_evidence=yunqi,
        pattern_evidence=[],
    )

    assert data["ehui"] == ehui
    assert data["dayou"] == dayou
    assert data["xiaoyou"] == xiaoyou
    assert data["taiyi_yunqi_hexagram_evidence"] == yunqi
    assert data["four_spirit_formula_reconstructed"] is False
