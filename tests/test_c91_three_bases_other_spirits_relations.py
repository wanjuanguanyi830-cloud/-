import pytest

from kintaiyi.three_bases_other_spirits_relations import (
    POSITION_BOUNDARY,
    RULES,
    c91_catalog,
    three_base_other_relation,
)


def test_c91_has_exactly_nine_pairs():
    assert len(RULES) == 9
    assert set(RULES) == {
        (base, counterpart)
        for base in ("君基", "臣基", "民基")
        for counterpart in ("四神", "大游", "小游")
    }


@pytest.mark.parametrize(
    "base,counterpart,effect",
    [
        ("臣基", "四神", "水涝"),
        ("臣基", "大游", "饥馑"),
        ("臣基", "小游", "上下不协"),
        ("民基", "四神", "民多流荡"),
        ("民基", "大游", "人民流移"),
        ("民基", "小游", "稼穑丰收"),
    ],
)
def test_c91_chen_min_direct_omens(base, counterpart, effect):
    data = three_base_other_relation(base, counterpart, same_palace=True)
    assert data["status"] == "explicit_same_palace_direct_omen"
    assert effect in data["selected_effects"]


def test_c91_junji_four_spirits_keeps_governance_branches():
    data = three_base_other_relation("君基", "四神", same_palace=True)
    assert data["structure"] == "conditional_governance"
    assert data["selected_effects"] == []
    good = data["conditional_branches"]["favorable_source_conduct"]
    bad = data["conditional_branches"]["adverse_source_conduct"]
    assert "敬奉宗庙" in good["conduct"]
    assert "邦国道泰" in good["effects"]
    assert "废祀祭" in bad["conduct"]
    assert "淫雨为灾" in bad["effects"]


def test_c91_junji_dayou_keeps_base_omens_and_response_condition():
    data = three_base_other_relation("君基", "大游", same_palace=True)
    assert data["structure"] == "conditional_response"
    assert data["base_omens"] == ["兵革", "水旱", "疾疫之祸"]
    assert data["selected_effects"] == []
    assert data["text_boundary"]
    assert "修明德" in data["conditional_branches"]["favorable_source_conduct"]["conduct"]
    assert "国耗民竭" in data["conditional_branches"]["adverse_source_conduct"]["effects"]


def test_c91_junji_xiaoyou_keeps_direct_conflict_and_prescribed_response():
    data = three_base_other_relation("君基", "小游", same_palace=True)
    assert data["structure"] == "direct_omen_with_response"
    assert "争之象" in data["selected_effects"]
    assert "祸乱不可胜言" in data["selected_effects"]
    assert "修武备" in data["prescribed_response"]
    assert "君主亲征" in data["prescribed_response"]


def test_c91_conditional_branch_selects_only_requested_outcome():
    good = three_base_other_relation(
        "君基",
        "四神",
        same_palace=True,
        conduct_branch="favorable_source_conduct",
    )
    bad = three_base_other_relation(
        "君基",
        "四神",
        same_palace=True,
        conduct_branch="adverse_source_conduct",
    )
    assert good["selected_effects"] == ["阴阳调", "邦国道泰"]
    assert "水暴百川" in bad["selected_effects"]


def test_c91_no_auto_same_palace_and_false_is_empty():
    missing = three_base_other_relation("民基", "大游", same_palace=None)
    assert missing["selected_effects"] == []
    assert missing["status"] == "same_palace_unchecked"
    assert "不从位置runtime自动判断" in "；".join(missing["pending"])

    false = three_base_other_relation("民基", "大游", same_palace=False)
    assert false["selected_effects"] == []
    assert false["status"] == "not_same_palace"


def test_c91_conduct_branch_restricted_to_conditional_rules():
    with pytest.raises(ValueError, match="没有C91可选"):
        three_base_other_relation(
            "臣基",
            "四神",
            same_palace=True,
            conduct_branch="favorable_source_conduct",
        )
    with pytest.raises(ValueError, match="不能选择"):
        three_base_other_relation(
            "君基",
            "大游",
            same_palace=False,
            conduct_branch="adverse_source_conduct",
        )


def test_c91_aliases_normalize_without_creating_new_rules():
    assert three_base_other_relation(
        "臣基", "四神水宿", same_palace=True
    )["counterpart"] == "四神"
    assert three_base_other_relation(
        "民基", "太遊", same_palace=True
    )["counterpart"] == "大游"
    assert three_base_other_relation(
        "民基", "小遊", same_palace=True
    )["counterpart"] == "小游"


def test_c91_rejects_bad_names_and_types():
    with pytest.raises(ValueError, match="君基/臣基/民基"):
        three_base_other_relation("五福", "四神", same_palace=True)
    with pytest.raises(ValueError, match="四神/大游/小游"):
        three_base_other_relation("君基", "天乙", same_palace=True)
    with pytest.raises(TypeError, match="same_palace"):
        three_base_other_relation("君基", "四神", same_palace="同宫")


def test_c91_never_auto_reads_positions():
    data = three_base_other_relation("臣基", "大游", same_palace=True)
    assert data["position_boundary"] == POSITION_BOUNDARY
    assert data["position_boundary"]["auto_position_lookup_used"] is False
    assert data["position_boundary"]["auto_same_palace_inference_used"] is False


def test_c91_catalog_locks_pair_count_and_scope():
    data = c91_catalog()
    assert data["pair_count"] == 9
    assert data["counterparts"] == ["四神", "大游", "小游"]
    assert data["position_boundary"]["three_bases_position_runtime"] == "C66"
