import pytest

from kintaiyi.eight_divinations import sancai, wuyin_from_calc


@pytest.mark.parametrize(
    ("calc", "components", "structural_missing", "classic_tags"),
    [
        (1, {"ten": False, "five": False, "one": True}, ["天", "地"], ["无天", "无地"]),
        (4, {"ten": False, "five": False, "one": True}, ["天", "地"], ["无天", "无地"]),
        (5, {"ten": False, "five": True, "one": False}, ["天", "人"], ["杜塞"]),
        (9, {"ten": False, "five": True, "one": True}, ["天"], ["无天"]),
        (10, {"ten": True, "five": False, "one": False}, ["地", "人"], ["无人"]),
        (11, {"ten": True, "five": False, "one": True}, ["地"], ["无地"]),
        (15, {"ten": True, "five": True, "one": False}, ["人"], ["杜塞"]),
        (16, {"ten": True, "five": True, "one": True}, [], ["三才俱足"]),
        (20, {"ten": True, "five": False, "one": False}, ["地", "人"], ["无人"]),
        (25, {"ten": True, "five": True, "one": False}, ["人"], ["杜塞"]),
        (35, {"ten": True, "five": True, "one": False}, ["人"], ["杜塞"]),
        (39, {"ten": True, "five": True, "one": True}, [], ["三才俱足"]),
        (40, {"ten": True, "five": False, "one": False}, ["地", "人"], ["无人"]),
    ],
)
def test_sancai_separates_structure_from_classic_tags(
    calc, components, structural_missing, classic_tags
):
    result = sancai(calc)

    assert result["components"] == components
    assert result["structural_missing"] == structural_missing
    assert result["missing"] == structural_missing
    assert result["classic_tags"] == classic_tags
    assert result["sancai_full_classic"] == ("三才俱足" in classic_tags)
    assert result["blocked_classic"] == ("杜塞" in classic_tags)


@pytest.mark.parametrize("calc", [5, 15, 25, 35])
def test_blocked_numbers_are_not_relabelled_from_structural_missing(calc):
    result = sancai(calc)

    assert result["classic_tags"] == ["杜塞"]
    assert "无人" not in result["classic_tags"]
    assert result["components"]["five"] is True
    assert result["components"]["one"] is False
    assert result["components"]["ten"] is (calc != 5)


@pytest.mark.parametrize(
    ("calc", "tail", "tone", "element", "kind"),
    [
        (1, 1, "宫", "土", "正音"),
        (2, 2, "宫", "土", "比音"),
        (5, 5, "羽", "水", "正音"),
        (6, 6, "羽", "水", "比音"),
        (9, 9, "角", "木", "正音"),
        (10, 10, "角", "木", "比音"),
        (20, 10, "角", "木", "比音"),
        (39, 9, "角", "木", "正音"),
        (40, 10, "角", "木", "比音"),
    ],
)
def test_wuyin_assigns_zheng_bi_and_treats_zero_as_ten(
    calc, tail, tone, element, kind
):
    result = wuyin_from_calc(calc)

    assert result["tail"] == tail
    assert result["tone"] == tone
    assert result["element"] == element
    assert result["tone_kind"] == kind
    assert result["pending"] == []
