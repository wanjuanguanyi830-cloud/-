import pytest

from kintaiyi.jinjing_xuanming import (
    C116_VERSION,
    c116_catalog,
    xuanming_for_role,
    xuanming_matches,
)


@pytest.mark.parametrize(
    ("role", "target", "target_type"),
    [
        ("天子", "天乙", "twelve_general"),
        ("皇后", "天后", "twelve_general"),
        ("公侯", "太常", "twelve_general"),
        ("将军", "勾陈", "twelve_general"),
        ("九牧", "螣蛇", "twelve_general"),
        ("常侍", "天空", "twelve_general"),
        ("二千石", "青龙", "twelve_general"),
        ("大夫", "朱雀", "twelve_general"),
        ("吏士", "朱雀", "twelve_general"),
        ("庶人", "行年", "annual_position"),
    ],
)
def test_c116_direct_xuanming_table(role, target, target_type):
    data = xuanming_for_role(role)
    assert data["canonical"] == C116_VERSION
    assert data["xuanming_target"] == target
    assert data["target_type"] == target_type
    assert data["verdict"] is None


def test_c116_ocr_alias_does_not_change_canonical_role():
    data = xuanming_for_role("二干石")
    assert data["role"] == "二千石"
    assert data["input_role"] == "二干石"
    assert data["xuanming_target"] == "青龙"


def test_c116_match_requires_explicit_current_target():
    pending = xuanming_matches("天子", None)
    assert pending["matches"] is None
    assert pending["status"] == "target_unchecked"

    matched = xuanming_matches("天子", "天乙")
    assert matched["matches"] is True

    not_matched = xuanming_matches("天子", "天后")
    assert not_matched["matches"] is False


def test_c116_catalog_has_ten_runtime_roles():
    catalog = c116_catalog()
    assert len(catalog["role_to_xuanming"]) == 10
    assert catalog["role_to_xuanming"]["大夫"]["target"] == "朱雀"
    assert catalog["role_to_xuanming"]["吏士"]["target"] == "朱雀"


def test_c116_rejects_unknown_role():
    with pytest.raises(ValueError):
        xuanming_for_role("未知")
