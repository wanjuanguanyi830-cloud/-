import pytest

from kintaiyi.three_bases_three_spirits_relations import (
    POSITION_BOUNDARY,
    RULES,
    c82_catalog,
    three_base_spirit_relation,
)


def test_c90_has_exactly_nine_direct_pairs():
    assert len(RULES) == 9
    assert set(RULES) == {
        (base, spirit)
        for base in ("君基", "臣基", "民基")
        for spirit in ("天乙", "地乙", "直符")
    }


@pytest.mark.parametrize(
    "base,spirit,effect",
    [
        ("臣基", "天乙", "盗贼"),
        ("臣基", "地乙", "百姓失务"),
        ("臣基", "直符", "火灾"),
        ("民基", "天乙", "人民不安"),
        ("民基", "地乙", "禾谷不收"),
        ("民基", "直符", "飞蝗为害"),
    ],
)
def test_c90_chen_min_direct_omens(base, spirit, effect):
    data = three_base_spirit_relation(
        base,
        spirit,
        same_palace=True,
    )
    assert data["structure"] == "direct_omen"
    assert data["status"] == "explicit_same_palace_direct_omen"
    assert effect in data["selected_effects"]
    assert data["conditional_branches"] is None


@pytest.mark.parametrize("spirit", ["天乙", "地乙", "直符"])
def test_c90_junji_requires_explicit_conduct_branch(spirit):
    data = three_base_spirit_relation(
        "君基",
        spirit,
        same_palace=True,
    )
    assert data["structure"] == "conditional_governance"
    assert data["selected_effects"] == []
    assert set(data["conditional_branches"]) == {
        "favorable_source_conduct",
        "adverse_source_conduct",
    }
    assert "conduct_branch" in "；".join(data["pending"])


def test_c90_junji_tianyi_keeps_favorable_and_adverse_branches():
    good = three_base_spirit_relation(
        "君基",
        "天乙",
        same_palace=True,
        conduct_branch="favorable_source_conduct",
    )
    bad = three_base_spirit_relation(
        "君基",
        "天乙",
        same_palace=True,
        conduct_branch="adverse_source_conduct",
    )
    assert good["selected_effects"] == ["君国致祯祥"]
    assert "兵火之咎" in bad["selected_effects"]
    assert "征不道" in good["conditional_branches"]["favorable_source_conduct"]["conduct"]
    assert "好攻战" in bad["conditional_branches"]["adverse_source_conduct"]["conduct"]


def test_c90_junji_diyi_keeps_agriculture_vs_luxury_conditions():
    data = three_base_spirit_relation(
        "君基",
        "地乙",
        same_palace=True,
    )
    good = data["conditional_branches"]["favorable_source_conduct"]
    bad = data["conditional_branches"]["adverse_source_conduct"]
    assert "务农桑" in good["conduct"]
    assert "地生祥瑞" in good["effects"]
    assert "广营宫室" in bad["conduct"]
    assert "地生异类妖物" in bad["effects"]


def test_c90_junji_zhifu_uses_only_stable_condition_core():
    data = three_base_spirit_relation(
        "君基",
        "直符",
        same_palace=True,
    )
    assert data["source_status"] == "direct_conditional_stable_core"
    assert data["text_boundary"]
    assert "率由旧章" in data["conditional_branches"]["favorable_source_conduct"]["conduct"]
    assert "谗邪胜正" in data["conditional_branches"]["adverse_source_conduct"]["conduct"]


def test_c90_missing_or_false_same_palace_never_applies_effects():
    missing = three_base_spirit_relation("民基", "天乙", same_palace=None)
    assert missing["selected_effects"] == []
    assert missing["status"] == "same_palace_unchecked"
    assert "不从C66/C64自动判断" in "；".join(missing["pending"])

    false = three_base_spirit_relation("民基", "天乙", same_palace=False)
    assert false["selected_effects"] == []
    assert false["status"] == "not_same_palace"


def test_c90_conduct_branch_is_restricted_to_junji_and_same_palace():
    with pytest.raises(ValueError, match="仅用于君基"):
        three_base_spirit_relation(
            "臣基",
            "天乙",
            same_palace=True,
            conduct_branch="favorable_source_conduct",
        )
    with pytest.raises(ValueError, match="不能选择"):
        three_base_spirit_relation(
            "君基",
            "天乙",
            same_palace=False,
            conduct_branch="favorable_source_conduct",
        )
    with pytest.raises(ValueError, match="conduct_branch"):
        three_base_spirit_relation(
            "君基",
            "天乙",
            same_palace=True,
            conduct_branch="good",
        )


def test_c90_legacy_zhifu_alias_requires_explicit_opt_in():
    with pytest.raises(ValueError, match="值符不是C90 canonical"):
        three_base_spirit_relation("民基", "值符", same_palace=True)

    data = three_base_spirit_relation(
        "民基",
        "值符",
        same_palace=True,
        allow_legacy_zhifu_alias=True,
    )
    assert data["spirit"] == "直符"
    assert "飞蝗为害" in data["selected_effects"]


def test_c90_rejects_bad_names_and_same_palace_type():
    with pytest.raises(ValueError, match="君基/臣基/民基"):
        three_base_spirit_relation("五福", "天乙", same_palace=True)
    with pytest.raises(ValueError, match="天乙/地乙/直符"):
        three_base_spirit_relation("君基", "四神", same_palace=True)
    with pytest.raises(TypeError, match="same_palace"):
        three_base_spirit_relation("君基", "天乙", same_palace="同宫")


def test_c90_never_auto_reads_position_runtimes():
    data = three_base_spirit_relation("臣基", "地乙", same_palace=True)
    assert data["position_boundary"] == POSITION_BOUNDARY
    assert data["position_boundary"]["auto_position_lookup_used"] is False
    assert data["position_boundary"]["auto_same_palace_inference_used"] is False


def test_c90_catalog_locks_pair_count_and_boundaries():
    data = c82_catalog()
    assert data["pair_count"] == 9
    assert data["bases"] == ["君基", "臣基", "民基"]
    assert data["spirits"] == ["天乙", "地乙", "直符"]
    assert data["position_boundary"]["three_bases_position_runtime"] == "C66"
    assert data["position_boundary"]["three_spirits_position_runtime"] == "C64"
