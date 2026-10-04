"""C9 现代博弈特征投影。

本模块不是古法真源。它只把已经结构化的七术结果投影为现代博弈可消费特征，
并明确标记 derived_modern_feature=True。

禁止：
- 把整个七术结果 str(...) 后搜索“成/吉/正/利”等字；
- 用洛书九宫解释本项目太乙九宫；
- 把 not_computable/pending 强行量化成吉凶；
- 反向修改七术 canonical 结果。
"""

from __future__ import annotations

from typing import Any

from .taiyi_rules import NINE_PALACE_TRIGRAM, PALACE_WX, integer

GAME_THEORY_FEATURE_VERSION = "taiyi-game-theory-c9-v1"

# C9读共享太乙九宫映射，不自行维护另一份卦名表。
TAIYI_PALACE_TRIGRAM = NINE_PALACE_TRIGRAM

_QI_SCORE = {"旺": 2.0, "相": 1.0, "休": 0.0, "囚": -1.0, "死": -2.0}


def _base_projection(rule_id: str | None, method_result: dict[str, Any]) -> dict[str, Any]:
    status = method_result.get("status", "ok")
    missing = list(method_result.get("missing", method_result.get("missing_inputs", [])) or [])
    computable = status not in ("not_computable", "pending") and not missing
    return {
        "schema_version": "1.0",
        "canonical": GAME_THEORY_FEATURE_VERSION,
        "derived_modern_feature": True,
        "source_category": "seven_methods",
        "source_rule_id": rule_id,
        "source_status": status,
        "computable": computable,
        "missing_inputs": missing,
        "signal": None,
        "score": None,
        "strategy_adjustments": {},
        "notes": [],
    }


def _qi_state_score(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    return _QI_SCORE.get(value)


def _project_t7_01(result: dict[str, Any], out: dict[str, Any]) -> None:
    # 临津问道给出破年/月/日/时的时间链，不是通用吉凶。
    if not out["computable"]:
        return
    out["signal"] = "timing_only"
    out["notes"].append("T7-01仅投影应期；不自动生成胜负支付值。")


def _project_t7_02(result: dict[str, Any], out: dict[str, Any]) -> None:
    if not out["computable"]:
        return
    verdict = result.get("verdict")
    if verdict == "合破":
        out["signal"] = "enemy_break_possible"
        out["score"] = 1.0
        out["strategy_adjustments"] = {"attack_enemy": 1.0}
    elif verdict == "不破":
        out["signal"] = "enemy_break_resisted"
        out["score"] = -1.0
        out["strategy_adjustments"] = {"attack_enemy": -1.0}
    else:
        out["signal"] = "unknown"
        out["notes"].append("T7-02未知 verdict，不从说明文字猜测。")


def _project_t7_03(result: dict[str, Any], out: dict[str, Any]) -> None:
    if not out["computable"]:
        return
    home_state = ((result.get("home") or {}).get("dashen") or {}).get("state")
    away_state = ((result.get("away") or {}).get("dashen") or {}).get("state")
    home_score = _qi_state_score(home_state)
    away_score = _qi_state_score(away_state)
    if home_score is None or away_score is None:
        out["signal"] = "unknown"
        out["notes"].append("T7-03缺明确五态，不从 verdict 文本反推。")
        return
    delta = home_score - away_score
    out["score"] = delta
    out["signal"] = "home_stronger" if delta > 0 else "away_stronger" if delta < 0 else "balanced"
    out["strategy_adjustments"] = {"relative_force_posture": delta}


def _project_t7_04(result: dict[str, Any], out: dict[str, Any]) -> None:
    if not out["computable"]:
        return
    verdict = result.get("verdict")
    if verdict in ("可攻", "敌营不久破/可攻"):
        out["signal"] = "attack_window_open"
        out["score"] = 1.0
        out["strategy_adjustments"] = {"attack_enemy": 1.0}
    elif verdict == "不可攻":
        out["signal"] = "attack_window_closed"
        out["score"] = -1.0
        out["strategy_adjustments"] = {"attack_enemy": -1.0}
    elif verdict in ("原典未明言", "无明确断语"):
        out["signal"] = "indeterminate"
        out["score"] = 0.0
    else:
        out["signal"] = "unknown"
        out["notes"].append("T7-04未知 verdict，不做字符串关键词推断。")


def _project_t7_05(result: dict[str, Any], out: dict[str, Any]) -> None:
    if not out["computable"]:
        return
    generals = result.get("generals")
    if not isinstance(generals, dict):
        out["signal"] = "unknown"
        return
    home = [_qi_state_score((generals.get(k) or {}).get("state"))
            for k in ("home_general", "home_assistant", "home_vassal")]
    away = [_qi_state_score((generals.get(k) or {}).get("state"))
            for k in ("away_general", "away_assistant", "away_vassal")]
    home = [x for x in home if x is not None]
    away = [x for x in away if x is not None]
    if not home or not away:
        out["signal"] = "partial_force_state"
        out["notes"].append("T7-05将帅状态不完整，不强行合成为胜负。")
        return
    delta = sum(home) / len(home) - sum(away) / len(away)
    out["score"] = delta
    out["signal"] = "home_force_advantage" if delta > 0 else "away_force_advantage" if delta < 0 else "balanced"
    out["strategy_adjustments"] = {"relative_force_posture": delta}


def _project_t7_06(result: dict[str, Any], out: dict[str, Any]) -> None:
    if not out["computable"]:
        return
    generals = result.get("generals")
    if not isinstance(generals, dict):
        out["signal"] = "unknown"
        return
    home_has_qi = (generals.get("home_general") or {}).get("has_qi")
    away_has_qi = (generals.get("away_general") or {}).get("has_qi")
    if isinstance(home_has_qi, bool) and isinstance(away_has_qi, bool):
        delta = float(home_has_qi) - float(away_has_qi)
        out["score"] = delta
        out["signal"] = "home_deployment_advantage" if delta > 0 else "away_deployment_advantage" if delta < 0 else "balanced"
        out["strategy_adjustments"] = {"deployment": delta}
    else:
        out["signal"] = "partial_deployment_state"

    conflicts = result.get("conflicts")
    if isinstance(conflicts, dict):
        home_conflict = bool((conflicts.get("home") or {}).get("severe"))
        away_conflict = bool((conflicts.get("away") or {}).get("severe"))
        if home_conflict or away_conflict:
            out["notes"].append(
                "T7-06严重刑克仅读取结构化 severe；未提供刑表时不从文字猜测。"
            )
            out["strategy_adjustments"]["home_severe_conflict"] = -1.0 if home_conflict else 0.0
            out["strategy_adjustments"]["away_severe_conflict"] = 1.0 if away_conflict else 0.0


def _project_t7_07(result: dict[str, Any], out: dict[str, Any]) -> None:
    if not out["computable"]:
        return
    enemy_verdict = result.get("enemy_verdict")
    if enemy_verdict in ("无伏兵、自破、可攻", "无伏、自破、可攻"):
        out["signal"] = "ambush_risk_low"
        out["score"] = 1.0
        out["strategy_adjustments"] = {"advance": 1.0}
    elif enemy_verdict == "有伏兵须防":
        out["signal"] = "ambush_risk_high"
        out["score"] = -1.0
        out["strategy_adjustments"] = {"advance": -1.0}
    else:
        out["signal"] = "unknown"
        out["notes"].append("T7-07缺明确 enemy_verdict，不从 aliases/notes 猜测。")

    if result.get("home_verdict") in ("本军宜伏", "宜自设伏"):
        out["strategy_adjustments"]["own_ambush"] = 1.0


_PROJECTORS = {
    "T7-01": _project_t7_01,
    "T7-02": _project_t7_02,
    "T7-03": _project_t7_03,
    "T7-04": _project_t7_04,
    "T7-05": _project_t7_05,
    "T7-06": _project_t7_06,
    "T7-07": _project_t7_07,
}


def project_seven_method_for_game_theory(method_result: dict[str, Any],
                                         perspective: str = "home") -> dict[str, Any]:
    """把一个结构化七术结果投影为现代博弈特征。

    只读明确字段；任何额外 prose、notes、aliases 中出现的“吉/利/成/正”
    都不会影响结果。
    """
    if not isinstance(method_result, dict):
        raise TypeError("method_result须为dict")
    if perspective not in ("home", "away"):
        raise ValueError("perspective须为home或away")
    rule_id = method_result.get("rule_id")
    out = _base_projection(rule_id, method_result)
    out["perspective"] = perspective
    projector = _PROJECTORS.get(rule_id)
    if projector is None:
        out["computable"] = False
        out["signal"] = "unsupported_rule"
        out["notes"].append("仅支持T7-01..07结构化结果。")
        return out
    projector(method_result, out)
    if perspective == "away":
        if isinstance(out["score"], (int, float)) and not isinstance(out["score"], bool):
            out["score"] = -out["score"]
        out["strategy_adjustments"] = {
            key: -value if isinstance(value, (int, float)) and not isinstance(value, bool) else value
            for key, value in out["strategy_adjustments"].items()
        }
        out["notes"].append("数值特征按客方视角取反；signal仍描述原七术字段表达的事件。")
    return out


def project_seven_methods_for_game_theory(methods: Any, perspective: str = "home") -> dict[str, Any]:
    """批量投影七术；接受 dict.values 或 iterable。"""
    values = methods.values() if isinstance(methods, dict) else methods
    projected = [project_seven_method_for_game_theory(item, perspective=perspective) for item in values]
    return {
        "canonical": GAME_THEORY_FEATURE_VERSION,
        "derived_modern_feature": True,
        "features": projected,
        "computable_count": sum(1 for item in projected if item["computable"]),
        "scored_count": sum(1 for item in projected if item["score"] is not None),
        "policy": "结构化字段投影；禁止字符串吉凶搜索。",
    }


def taiyi_palace_feature(palace: int) -> dict[str, Any]:
    """返回博弈层可用的太乙九宫位置事实，明确拒绝洛书宫义偷换。"""
    palace = integer(palace, 1, 9)
    return {
        "canonical": GAME_THEORY_FEATURE_VERSION,
        "derived_modern_feature": True,
        "mapping_system": "taiyi_nine_palace",
        "palace": palace,
        "trigram": TAIYI_PALACE_TRIGRAM[palace],
        "element": PALACE_WX[palace],
        "is_center": palace == 5,
        "positional_effect_allowed": palace != 5,
        "policy": "使用太乙九宫：1乾2离3艮4震5中6兑7坤8坎9巽；不得套洛书宫义。",
    }


def build_game_theory_feature_bundle(*, seven_methods: Any = (), taiyi_palace: int | None = None,
                                     military: dict[str, Any] | None = None,
                                     perspective: str = "home") -> dict[str, Any]:
    """组合现代博弈输入特征；不反写古法结果，不在此求 Nash。"""
    seven = project_seven_methods_for_game_theory(seven_methods, perspective=perspective)
    return {
        "canonical": GAME_THEORY_FEATURE_VERSION,
        "derived_modern_feature": True,
        "source_of_truth": "structured_taiyi_results",
        "seven_methods": seven,
        "perspective": perspective,
        "taiyi_palace": taiyi_palace_feature(taiyi_palace) if taiyi_palace is not None else None,
        "military": military,
        "cross_system_palace_mapping": False,
        "notes": [
            "C9第一阶段只建立可审计特征投影；支付矩阵/Nash属于后续现代模型，不得伪称古法结论。"
        ],
    }
