from kintaiyi.legacy_schema import classify_legacy_field
from kintaiyi.migration_audit import audit_legacy_snapshot
from kintaiyi.pan_adapter import attach_v2_to_snapshot, extract_legacy_snapshot_facts
from kintaiyi.pan_v2 import build_pan_v2, validate_pan_v2


def _snapshot():
    return {
        "太乙落宮": 1,
        "太乙": "乾",
        "天乙": "申",
        "地乙": "巳",
        "四神": "亥",
        "直符": "寅",
        "合神": "丑",
        "計神": "子",
        "十六宮分佈": {
            "巳": ["天乙"],
            "午": [],
            "乾": ["太乙"],
            "中": [],
        },
    }


def test_c16_fields_are_migrated_in_c14_policy():
    expected = {
        "天乙": "board.generals.tianyi",
        "地乙": "board.generals.diyi",
        "四神": "board.generals.four_spirits",
        "直符": "board.generals.zhifu",
        "合神": "board.generals.hegod",
        "計神": "board.generals.jigod",
        "十六宮分佈": "board.sixteen_palaces",
    }
    for key, target in expected.items():
        item = classify_legacy_field(key)
        assert item["status"] == "migrated_fact"
        assert item["target"] == target


def test_basic_spirits_are_migrated_as_sector_facts_not_general_palaces():
    facts = extract_legacy_snapshot_facts(_snapshot())
    generals = facts["board"]["generals"]
    assert generals["tianyi"] == {"sector": "申"}
    assert generals["diyi"] == {"sector": "巳"}
    assert generals["four_spirits"] == {"sector": "亥"}
    assert generals["zhifu"] == {"sector": "寅"}
    assert generals["hegod"] == {"sector": "丑"}
    assert generals["jigod"] == {"sector": "子"}
    for item in generals.values():
        assert "palace" not in item


def test_sixteen_palace_distribution_is_preserved_as_board_fact():
    v2 = attach_v2_to_snapshot(_snapshot())["v2"]
    assert v2["board"]["sixteen_palaces"] == {
        "巳": ["天乙"],
        "午": [],
        "乾": ["太乙"],
        "中": [],
    }


def test_builder_always_has_sixteen_palace_board_section():
    data = build_pan_v2()
    assert "sixteen_palaces" in data["board"]
    assert data["board"]["sixteen_palaces"] == {}
    checked = validate_pan_v2(data)
    assert checked["valid"] is True


def test_c13_no_longer_reports_c16_board_fields_as_unported():
    snapshot = attach_v2_to_snapshot(_snapshot())
    report = audit_legacy_snapshot(snapshot)
    for key in ("天乙", "地乙", "四神", "直符", "合神", "計神", "十六宮分佈"):
        assert key in report["migrated_fact_keys"]
        assert key not in report["unported_legacy_keys"]
    assert report["unported_legacy_keys"] == []


def test_c16_does_not_promote_old_descriptions_or_run_rules():
    snapshot = _snapshot()
    snapshot["天乙"] = "中"
    snapshot["十六宮分佈"] = {"中": ["天乙", "地乙"]}
    v2 = attach_v2_to_snapshot(snapshot)["v2"]
    assert v2["board"]["generals"]["tianyi"]["sector"] == "中"
    assert v2["board"]["sixteen_palaces"]["中"] == ["天乙", "地乙"]
    assert v2["analysis"]["patterns"] == {}
    assert v2["analysis"]["military"] == {}
