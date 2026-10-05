import pytest

from kintaiyi.wander_conjunctions import (
    C112_VERSION,
    c112_catalog,
    wander_conjunction_relation,
)


def test_c112_catalog_locks_only_four_recovered_pairs():
    catalog = c112_catalog()
    assert catalog["canonical"] == C112_VERSION
    assert catalog["pair_count"] == 4
    assert set(catalog["pair_rules"]) == {
        ("五福", "大游"),
        ("五福", "小游"),
        ("四神", "小游"),
        ("大游", "小游"),
    }
    assert catalog["position_boundary"]["auto_position_lookup_used"] is False
    assert catalog["position_boundary"]["auto_same_palace_inference_used"] is False
    assert catalog["position_boundary"]["auto_opposite_division_lookup_used"] is False


def test_wufu_dayou_keeps_two_source_layers_separate():
    data = wander_conjunction_relation("五福", "大游", same_palace=True)
    assert data["status"] == "explicit_same_palace_layered_direct"
    assert [layer["source_section"] for layer in data["effect_layers"]] == [
        "明五福太乙所主术",
        "明大游太乙所主术",
    ]
    assert data["effect_layers"][0]["effects"] == ["五福之福减半", "兵盗", "水旱不免"]
    assert data["effect_layers"][1]["effects"] == ["兵革之灾降于对冲之分"]
    assert data["selected_effects"] == []
    assert "自动求具体对冲分野" in data["localization_boundary"]


@pytest.mark.parametrize(
    ("virtue", "expected"),
    [
        (True, ["有德者昌"]),
        (False, ["失德者殃"]),
    ],
)
def test_wufu_xiaoyou_requires_explicit_virtue_branch(virtue, expected):
    data = wander_conjunction_relation(
        "五福",
        "小遊",
        same_palace=True,
        virtue=virtue,
    )
    assert data["pair"] == ["五福", "小游"]
    assert data["status"] == "explicit_same_palace_virtue_branch"
    assert data["selected_effects"] == expected

    pending = wander_conjunction_relation("五福", "小游", same_palace=True)
    assert pending["status"] == "explicit_same_palace_pending_virtue"
    assert pending["selected_effects"] == []
    assert pending["pending"]


def test_four_spirit_xiaoyou_direct_omen():
    data = wander_conjunction_relation("四神水宿", "小游", same_palace=True)
    assert data["pair"] == ["四神", "小游"]
    assert data["selected_effects"] == ["人民不安", "多生水涝疾疫"]
    assert data["status"] == "explicit_same_palace_direct_omen"


def test_dayou_xiaoyou_uses_collated_xiongbao_reading():
    data = wander_conjunction_relation("太游", "小游", same_palace=True)
    assert data["pair"] == ["大游", "小游"]
    assert data["selected_effects"] == ["兵丧", "水旱", "凶暴大作"]
    assert "CADAL" in data["text_boundary"]


def test_same_palace_must_be_explicit():
    pending = wander_conjunction_relation("四神", "小游", same_palace=None)
    assert pending["status"] == "same_palace_unchecked"
    assert pending["effect_layers"] == []
    assert pending["selected_effects"] == []

    absent = wander_conjunction_relation("大游", "小游", same_palace=False)
    assert absent["status"] == "not_same_palace"
    assert absent["selected_effects"] == []


def test_c112_does_not_duplicate_pairs_owned_by_other_layers():
    with pytest.raises(ValueError):
        wander_conjunction_relation("五福", "四神", same_palace=True)
    with pytest.raises(ValueError):
        wander_conjunction_relation("天乙", "小游", same_palace=True)


def test_virtue_cannot_leak_to_non_wufu_xiaoyou_pairs():
    with pytest.raises(ValueError):
        wander_conjunction_relation("大游", "小游", same_palace=True, virtue=True)
    with pytest.raises(ValueError):
        wander_conjunction_relation("五福", "小游", same_palace=None, virtue=True)
