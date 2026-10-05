import pytest

from kintaiyi.jinjing_direct_envoy import (
    C121_VERSION,
    c121_catalog,
    direct_envoy_anchor,
    direct_envoy_movement_catalog,
)


@pytest.mark.parametrize(
    ("period", "palace", "tianmu"),
    [
        (1, 1, "武德"),
        (2, 6, "地主"),
        (3, 1, "大炅"),
        (4, 6, "武德"),
        (5, 1, "地主"),
        (6, 6, "大炅"),
    ],
)
def test_c121_yang_six_period_anchor_table(period, palace, tianmu):
    data = direct_envoy_anchor("阳遁", period)
    assert data["canonical"] == C121_VERSION
    assert data["solstice_basis"] == "冬至"
    assert data["taiyi_palace"] == palace
    assert data["tianmu"] == tianmu
    assert data["jishen"] == "寅"
    assert data["anchor_time"] == "夜半甲子"


@pytest.mark.parametrize(
    ("period", "palace", "tianmu"),
    [
        (1, 9, "吕申"),
        (2, 4, "大威"),
        (3, 9, "阴德"),
        (4, 4, "吕申"),
        (5, 9, "大威"),
        (6, 4, "阴德"),
    ],
)
def test_c121_yin_six_period_anchor_table(period, palace, tianmu):
    data = direct_envoy_anchor("阴遁", period)
    assert data["solstice_basis"] == "夏至"
    assert data["taiyi_palace"] == palace
    assert data["tianmu"] == tianmu
    assert data["jishen"] == "申"


def test_c121_never_uses_center_five_in_direct_taiyi_paths():
    catalog = c121_catalog()
    yang = catalog["movement_rules"]["阳遁"]["taiyi"]
    yin = catalog["movement_rules"]["阴遁"]["taiyi"]
    assert yang["center_five_used"] is False
    assert yin["center_five_used"] is False
    assert 5 not in yang["path"]
    assert 5 not in yin["path"]


def test_c121_preserves_movement_statements_without_claiming_full_runtime():
    yang = direct_envoy_movement_catalog("阳")
    assert "太乙直使三时一移" in yang["rules"]["taiyi"]["source_statements"]
    assert "乾坤二宫二时一移" in yang["rules"]["tianmu"]["source_statements"]
    assert yang["continuous_runtime_implemented"] is False


def test_c121_wang_ximing_revision_boundary_is_explicit():
    data = direct_envoy_anchor("阳遁", 1)
    boundary = data["wang_ximing_boundary"]
    assert boundary["continuous_runtime_implemented"] is False
    assert "气应早晚" in boundary["direct_summary"]


def test_c121_rejects_invalid_period_and_dun():
    with pytest.raises(ValueError):
        direct_envoy_anchor("阳遁", 0)
    with pytest.raises(ValueError):
        direct_envoy_anchor("未知", 1)
    with pytest.raises(TypeError):
        direct_envoy_anchor("阳遁", True)
