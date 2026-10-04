from kintaiyi.game_theory import (
    build_game_theory_feature_bundle,
    project_seven_method_for_game_theory,
    project_seven_methods_for_game_theory,
    taiyi_palace_feature,
)
from kintaiyi.seven_methods import lion, tiger


def test_projection_ignores_lucky_words_in_unrelated_text():
    result = {
        "rule_id": "T7-04",
        "category": "seven_methods",
        "status": "ok",
        "verdict": "不可攻",
        "notes": ["这里故意放入：成、吉、正、利，均不得改变判定"],
    }
    data = project_seven_method_for_game_theory(result)
    assert data["signal"] == "attack_window_closed"
    assert data["score"] == -1.0
    assert data["strategy_adjustments"] == {"attack_enemy": -1.0}


def test_projection_reads_explicit_t7_04_verdict_only():
    positive = {
        "rule_id": "T7-04",
        "status": "ok",
        "verdict": "敌营不久破/可攻",
        "notes": ["凶败不利等说明文字不应反向覆盖"],
    }
    data = project_seven_method_for_game_theory(positive)
    assert data["signal"] == "attack_window_open"
    assert data["score"] == 1.0


def test_projection_accepts_canonical_t7_04_and_perspective():
    canonical = {
        "rule_id": "T7-04", "status": "ok", "verdict": "可攻",
        "notes": ["不根据吉凶文字扩展"],
    }
    home = project_seven_method_for_game_theory(canonical)
    away = project_seven_method_for_game_theory(canonical, perspective="away")
    assert home["signal"] == away["signal"] == "attack_window_open"
    assert home["score"] == 1.0 and away["score"] == -1.0
    assert away["derived_modern_feature"] is True
    assert away["perspective"] == "away"


def test_timing_method_does_not_become_generic_good_or_bad():
    result = {
        "rule_id": "T7-01",
        "status": "ok",
        "break_year_branch": "卯",
        "break_month_branch": "午",
        "break_day_branch": "酉",
        "break_hour_branch": "子",
        "source_example_note": "有利成吉正",
    }
    data = project_seven_method_for_game_theory(result)
    assert data["signal"] == "timing_only"
    assert data["score"] is None
    assert data["strategy_adjustments"] == {}


def test_not_computable_stays_unscored():
    result = {
        "rule_id": "T7-07",
        "status": "not_computable",
        "missing": ["enemy_arrival_taiyi"],
        "enemy_verdict": "无伏、自破、可攻",
    }
    data = project_seven_method_for_game_theory(result)
    assert data["computable"] is False
    assert data["score"] is None
    assert data["signal"] is None


def test_projection_accepts_canonical_t7_07_verdict_and_assistant_field():
    result = {
        "rule_id": "T7-07", "status": "ok",
        "enemy_verdict": "无伏兵、自破、可攻", "home_verdict": "本军宜伏",
    }
    data = project_seven_method_for_game_theory(result)
    assert data["signal"] == "ambush_risk_low"
    assert data["strategy_adjustments"] == {"advance": 1.0, "own_ambush": 1.0}


def test_real_seven_method_outputs_can_be_projected():
    lion_data = project_seven_method_for_game_theory(lion("甲子"))
    tiger_data = project_seven_method_for_game_theory(tiger(3))
    assert lion_data["source_rule_id"] == "T7-02"
    assert lion_data["derived_modern_feature"] is True
    assert tiger_data["source_rule_id"] == "T7-04"


def test_batch_projection_has_explicit_modern_marker():
    data = project_seven_methods_for_game_theory({
        "lion": lion("甲子"),
        "tiger": tiger(3),
    })
    assert data["derived_modern_feature"] is True
    assert len(data["features"]) == 2
    assert data["policy"] == "结构化字段投影；禁止字符串吉凶搜索。"


def test_taiyi_palace_mapping_is_not_luoshu_mapping():
    assert taiyi_palace_feature(1)["trigram"] == "乾"
    assert taiyi_palace_feature(2)["trigram"] == "离"
    assert taiyi_palace_feature(3)["trigram"] == "艮"
    assert taiyi_palace_feature(4)["trigram"] == "震"
    assert taiyi_palace_feature(6)["trigram"] == "兑"
    assert taiyi_palace_feature(7)["trigram"] == "坤"
    assert taiyi_palace_feature(8)["trigram"] == "坎"
    assert taiyi_palace_feature(9)["trigram"] == "巽"


def test_center_has_no_invented_positional_effect():
    data = taiyi_palace_feature(5)
    assert data["trigram"] == "中"
    assert data["element"] == "土"
    assert data["positional_effect_allowed"] is False


def test_bundle_never_enables_cross_system_palace_mapping():
    data = build_game_theory_feature_bundle(
        seven_methods=[tiger(3)],
        taiyi_palace=1,
        military={"source_profile": "volume5_strict"},
    )
    assert data["cross_system_palace_mapping"] is False
    assert data["taiyi_palace"]["mapping_system"] == "taiyi_nine_palace"
    assert data["military"]["source_profile"] == "volume5_strict"
