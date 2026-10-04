import pytest

from kintaiyi.ten_essences_number import taiyi_number
from kintaiyi.ten_essences_number_weather import (
    ALLOWED_RELATIONS,
    DIRECT_NUMBER_RULES,
    FLYBIRD_PALACE_RULE,
    LEGACY_AUDIT,
    NUMBER_50_VARIANT,
    c59_catalog,
    taiyi_number_weather_omens,
)


def _n(value: int):
    return taiyi_number(value)


def test_c59_requires_c54_identity():
    with pytest.raises(ValueError, match="C54-TAIYI-NUMBER"):
        taiyi_number_weather_omens({"rule_id": "wrong"}, relations=[])


def test_c59_number_30_direct_weather():
    data = taiyi_number_weather_omens(_n(30), relations=[])
    assert data["taiyi_number"] == 30
    assert data["matched_omens"] == [{
        "kind": "number",
        "number": 30,
        "effects": ["日晕", "大风"],
        "source_status": "direct_parallel",
    }]


def test_c59_number_40_direct_weather():
    data = taiyi_number_weather_omens(_n(40), relations=[])
    assert data["matched_omens"][0]["effects"] == ["阴雨", "黄雾"]


def test_c59_number_50_standalone_is_unresolved_not_hardcoded():
    data = taiyi_number_weather_omens(_n(50), relations=[])
    assert data["matched_omens"][0]["kind"] == "number_variant"
    assert data["matched_omens"][0]["effects"] is None
    assert data["unresolved_variant_count"] == 1
    assert data["number_50_variant"]["canonical_standalone_50_effects"] is None


def test_c59_number_50_plus_tianmu_wangxiang_returns_safe_intersection():
    data = taiyi_number_weather_omens(
        _n(50),
        relations=["合天目"],
        tianmu_qi_state="旺相",
    )
    safe = [
        row for row in data["matched_omens"]
        if row["kind"] == "safe_variant_intersection"
    ]
    assert safe == [{
        "kind": "safe_variant_intersection",
        "number": 50,
        "relation": "合天目",
        "qi_state": "旺相",
        "effects": ["日晕"],
        "source_status": "cross_witness_safe_intersection",
    }]


def test_c59_tianmu_relation_requires_explicit_qi_state():
    data = taiyi_number_weather_omens(
        _n(20),
        relations=["合天目"],
    )
    assert data["status"] == "partial_explicit_evidence"
    assert data["matched_omens"] == []
    assert "tianmu_qi_state" in "；".join(data["pending"])


def test_c59_tianmu_wangxiang_direct_relation():
    data = taiyi_number_weather_omens(
        _n(20),
        relations=["合天目"],
        tianmu_qi_state="旺相",
    )
    assert data["matched_omens"][0]["effects"] == ["日晕"]
    assert data["matched_omens"][0]["source_status"] == (
        "collation_direct_primary_clause_ambiguous"
    )


def test_c59_basic_taiyi_relations():
    same = taiyi_number_weather_omens(
        _n(20),
        relations=["合太乙"],
    )
    assert same["matched_omens"][0]["effects"] == ["日晕", "大风"]

    clash = taiyi_number_weather_omens(
        _n(20),
        relations=["冲太乙"],
    )
    assert clash["matched_omens"][0]["effects"] == ["日晕", "风起"]


def test_c59_taiyi_pincer_tianmu():
    data = taiyi_number_weather_omens(
        _n(20),
        relations=["太乙挟天目"],
    )
    assert data["matched_omens"][0]["effects"] == ["阴雨", "日晕", "大风"]


def test_c59_flybird_relation_requires_explicit_palace():
    missing = taiyi_number_weather_omens(
        _n(20),
        relations=["合飞鸟"],
    )
    assert missing["status"] == "partial_explicit_evidence"
    assert "flybird_palace" in "；".join(missing["pending"])

    hit = taiyi_number_weather_omens(
        _n(20),
        relations=["合飞鸟"],
        flybird_palace=8,
    )
    assert hit["matched_omens"][0]["effects"] == ["日晕"]


def test_c59_flybird_only_6_8_9_palaces_match():
    for palace in FLYBIRD_PALACE_RULE["required_palaces"]:
        data = taiyi_number_weather_omens(
            _n(20),
            relations=["合飞鸟"],
            flybird_palace=palace,
        )
        assert data["matched_omens"]

    miss = taiyi_number_weather_omens(
        _n(20),
        relations=["合飞鸟"],
        flybird_palace=5,
    )
    assert miss["matched_omens"] == []


@pytest.mark.parametrize(
    "relation,effects",
    [
        ("与天地并", ["日晕"]),
        ("与主计合", ["日晕"]),
        ("与天地相当", ["大风"]),
        ("与太乙飞鸟合", ["疾风"]),
    ],
)
def test_c59_other_explicit_relations(relation, effects):
    data = taiyi_number_weather_omens(
        _n(20),
        relations=[relation],
    )
    assert data["matched_omens"][0]["effects"] == effects


def test_c59_no_relations_must_be_explicit_empty_list():
    data = taiyi_number_weather_omens(_n(20))
    assert data["relations_checked"] is False
    assert data["status"] == "partial_explicit_evidence"
    assert "无关系时传空list" in "；".join(data["pending"])


def test_c59_no_relation_auto_inference():
    data = taiyi_number_weather_omens(_n(30), relations=[])
    assert data["auto_relation_inference_used"] is False
    assert data["relations"] == []
    assert len(data["matched_omens"]) == 1


def test_c59_rejects_unknown_relation_and_bad_palace():
    with pytest.raises(ValueError, match="未知C59关系"):
        taiyi_number_weather_omens(
            _n(20),
            relations=["合帝符"],
        )
    with pytest.raises(ValueError, match="1..9"):
        taiyi_number_weather_omens(
            _n(20),
            relations=["合飞鸟"],
            flybird_palace=10,
        )


def test_c59_allowed_relations_are_source_limited():
    assert ALLOWED_RELATIONS == frozenset({
        "合太乙",
        "冲太乙",
        "合天目",
        "太乙挟天目",
        "合飞鸟",
        "与天地并",
        "与主计合",
        "与天地相当",
        "与太乙飞鸟合",
    })


def test_c59_legacy_wrapper_is_not_canonical_equivalent():
    assert LEGACY_AUDIT["numeric_core_equivalent"] is True
    assert LEGACY_AUDIT["wrapper_canonical_equivalent"] is False
    assert any("50" in item for item in LEGACY_AUDIT["issues"])
    assert any("10/5" in item for item in LEGACY_AUDIT["issues"])


def test_c59_catalog_preserves_50_variant():
    data = c59_catalog()
    assert data["direct_number_rules"] == DIRECT_NUMBER_RULES
    assert data["number_50_variant"] == NUMBER_50_VARIANT
    assert data["number_50_variant"]["canonical_standalone_50_effects"] is None
    assert data["auto_relation_inference_used"] is False
