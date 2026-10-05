from pathlib import Path


DOC = Path("docs/taiyi_v1.md")


def _text():
    return DOC.read_text(encoding="utf-8")


def test_sancai_documentation_matches_confirmed_blocked_boundaries():
    text = _text()
    assert "5仅有地；15/25/35仅有天与地" in text
    assert "15结构全有" not in text
    assert "sancai(15)                         # 结构全有" not in text


def test_wuyin_documentation_no_longer_calls_zheng_bi_pending():
    text = _text()
    assert "1/3/5/7/9为正音" in text
    assert "2/4/6/8/10为比音" in text
    assert "正音/比音未确认" not in text
    assert "五音正比音" not in text.split("仍待校", 1)[-1]


def test_gudan_documentation_forbids_unlisted_decomposition():
    text = _text()
    assert "未列混合数不得再由十位/尾数拆分强塞分类或基本影响" in text
    assert "异性组合分别保留已有基本影响" not in text


def test_cycle_documentation_does_not_restore_retired_mixed_profiles():
    text = _text()
    assert "旧项目的 `+250` 只保留在 legacy quarantine" in text
    assert '默认 `profile="project"` 偏移+250' not in text
    assert "大游默认 `jinjing_tongzong`" not in text
    assert "C67-WUFU-TONGZONG" in text
    assert "C107-DAYOU-TONGZONG" in text
