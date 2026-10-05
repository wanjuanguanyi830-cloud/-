import json
from pathlib import Path


RULES = Path("rules/taiyi_v1.json")
MILITARY_P0 = Path("terminology/military-p0.json")


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_top_level_pending_contains_only_current_unresolved_work():
    pending = _load(RULES)["pending"]
    joined = "\n".join(pending)

    assert len(pending) == 4
    assert "T7-02" in joined
    assert "T7-06" in joined
    assert "淘金歌大游" not in joined
    assert "terminology.json" in joined
    assert "研易楼藏《太乙紫庭祕訣》明钞本" in joined
    assert "JF4M-02" not in joined
    assert "JF4M-07" not in joined
    assert "JF4M-10" not in joined

    # These are confirmed boundaries/history, not unresolved research items.
    assert "结构全有不自动赋予" not in joined
    assert "目标仓库没有原版旧config.py" not in joined


def test_jingyou_p0_profile_is_runtime_available_and_collation_resolved():
    data = _load(MILITARY_P0)
    profile = data["source_profiles"]["jingyou_fuying_volume4"]

    assert profile["status"] == "implemented_source_specific"
    assert profile["runtime_catalog"] == (
        "kintaiyi.jingyou_fuying_v4_military.jf4m_runtime_catalog"
    )
    assert profile["pending_textual_uncertainty"] == []
    assert profile["resolved_collation"]["JF4M-02"]["normalized_semantics"] == (
        "四将无同宫之关"
    )
