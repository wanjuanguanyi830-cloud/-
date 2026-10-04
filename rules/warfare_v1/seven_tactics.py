"""Seven Taiyi war methods, v1; each returns auditable intermediate results."""

from __future__ import annotations

from collections.abc import Mapping

from ..common.taiyi_space import (
    PALACE_CENTER_POSITION,
    dashen_from_lushen,
    element_at,
    element_for_palace,
    fire_stage,
    qi_state,
    palace_for_position,
    palace_position,
)

RULESET_ID = "taiyi-war-seven-v1"
RULESET_VERSION = "1.0.0"

BREAKABLE_STATES = frozenset(("休", "囚", "死"))
STRONG_STATES = frozenset(("旺", "相"))
WEAK_STATES = frozenset(("休", "囚", "死"))


def _state_for_fire(position: str) -> str:
    return qi_state("火", element_at(position))


def _general_detail(palace: int) -> dict:
    element = element_for_palace(palace)
    if palace not in PALACE_CENTER_POSITION:
        return {
            "宮": palace, "五行": element, "可計算": False,
            "缺少": "五宮暫無十六宮代表點校定",
        }
    point = dashen_from_lushen(palace)
    state = _state_for_fire(point)
    stage = fire_stage(point)
    if stage == "帝旺":
        strength = "不可觸犯"
    elif stage in ("臨官", "冠帶"):
        strength = "專斷"
    elif state in STRONG_STATES:
        strength = "強"
    elif state in WEAK_STATES or stage == "墓":
        strength = "弱"
    else:
        strength = "未定"
    return {
        "宮": palace, "代表點": palace_position(palace),
        "大神落點": point, "五行": element_at(point), "五態": state,
        "火氣階段": stage, "強弱": strength, "可計算": True,
    }


def linjin_ask_way(start_branch: str) -> dict:
    """T7-01: apply 吕申加位 four consecutive times from the uprising-year branch."""
    if start_branch not in "子丑寅卯辰巳午未申酉戌亥":
        raise ValueError("起兵年支必須是十二支之一")
    chain = [start_branch]
    for _ in range(4):
        chain.append(dashen_from_lushen(chain[-1]))
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "術": "臨津問道", "起兵年支": start_branch,
        "破年支": chain[1], "破月支": chain[2],
        "破日支": chain[3], "破時支": chain[4],
        "推步": chain,
        "曆法落實": None,
    }


def lion_reversal(start_branch: str) -> dict:
    """T7-02: test the fire deity's five-state result; do not infer a date."""
    if start_branch not in "子丑寅卯辰巳午未申酉戌亥":
        raise ValueError("起兵年支必須是十二支之一")
    point = dashen_from_lushen(start_branch)
    state = _state_for_fire(point)
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "術": "獅子反擲", "起兵年支": start_branch,
        "大神落點": point, "宮": palace_for_position(point),
        "大神五行": "火", "落點五行": element_at(point),
        "五態": state, "可破": state in BREAKABLE_STATES,
        "應期": None,
    }


def white_cloud_roll(home_general: int, away_general: int) -> dict:
    """T7-03: calculate host and guest generals independently."""
    home = _general_detail(home_general)
    away = _general_detail(away_general)
    advantage = None
    if home["可計算"] and away["可計算"]:
        if home["強弱"] == "強" and away["強弱"] == "弱":
            advantage = "主"
        elif away["強弱"] == "強" and home["強弱"] == "弱":
            advantage = "客"
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "術": "白雲卷空", "主": home, "客": away, "勝勢": advantage,
    }


def fierce_tiger(encampment_taiyi_palace: int) -> dict:
    """T7-04: assess the enemy camp from the Taiyi palace on encampment day."""
    point = dashen_from_lushen(encampment_taiyi_palace)
    state = _state_for_fire(point)
    stage = fire_stage(point)
    if state in STRONG_STATES:
        verdict = "敵營不可攻"
    elif stage in ("衰", "死", "墓"):
        verdict = "敵營不久破"
    else:
        verdict = None
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "術": "猛虎相拒", "下營日太乙宮": encampment_taiyi_palace,
        "大神落點": point, "宮": palace_for_position(point),
        "落點五行": element_at(point), "五態": state,
        "火氣階段": stage, "斷": verdict,
    }


def _general_environment_detail(palace: int, environment: str) -> dict:
    element = element_for_palace(palace)
    return {
        "宮": palace, "將五行": element,
        "五態": qi_state(element, environment),
    }


def thunder_god_water(taiyi_palace: int, generals: Mapping[str, int]) -> dict:
    """T7-05: compare each supplied general with the deity's lower-palace element."""
    point = dashen_from_lushen(taiyi_palace)
    environment = element_at(point)
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "術": "雷公入水", "太乙宮": taiyi_palace,
        "大神落點": point, "環境五行": environment,
        "四將": {
            name: _general_environment_detail(palace, environment)
            for name, palace in generals.items()
        },
    }


def _controls(attacker_palace: int, target_palace: int | None) -> bool | None:
    if target_palace is None:
        return None
    attacker = element_for_palace(attacker_palace)
    target = element_for_palace(target_palace)
    return attacker != target and {
        "木": "土", "土": "水", "水": "火", "火": "金", "金": "木",
    }[attacker] == target


def white_dragon_cloud(
    taiyi_palace: int,
    home_big: int,
    away_big: int,
    home_vassal: int | None = None,
    away_vassal: int | None = None,
) -> dict:
    """T7-06: return separate camp氣 and the confirmed 克 checks.

    刑 is kept separate: no刑表 is encoded in v1 until the cited source table is
    transcribed and checked. The source's severe death wording applies when
    the enemy big general controls the home big or supplied home vassal.
    """
    point = dashen_from_lushen(taiyi_palace)
    environment = element_at(point)
    controls_big = _controls(away_big, home_big)
    controls_vassal = _controls(away_big, home_vassal)
    death_condition = controls_big is True or controls_vassal is True
    home_state = qi_state(element_for_palace(home_big), environment)
    away_state = qi_state(element_for_palace(away_big), environment)
    home_camp = "宜出军、下营、屯军" if home_state in STRONG_STATES else "不宜出军" if home_state in WEAK_STATES else None
    away_camp = "宜出军、下营、屯军" if away_state in STRONG_STATES else "不宜出军" if away_state in WEAK_STATES else None
    home_vassal_detail = None if home_vassal is None else _general_environment_detail(home_vassal, environment)
    away_vassal_detail = None if away_vassal is None else _general_environment_detail(away_vassal, environment)
    home_vassal_camp = None if home_vassal_detail is None else (
        "宜出军、下营、屯军" if home_vassal_detail["五態"] in STRONG_STATES
        else "不宜出军" if home_vassal_detail["五態"] in WEAK_STATES else None
    )
    away_vassal_camp = None if away_vassal_detail is None else (
        "宜出军、下营、屯军" if away_vassal_detail["五態"] in STRONG_STATES
        else "不宜出军" if away_vassal_detail["五態"] in WEAK_STATES else None
    )
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "術": "白龍得雲", "太乙宮": taiyi_palace,
        "大神落點": point, "環境五行": environment,
        "主大將": _general_environment_detail(home_big, environment),
        "客大將": _general_environment_detail(away_big, environment),
        "主參將": home_vassal_detail, "客參將": away_vassal_detail,
        "主軍下營": home_camp, "客軍下營": away_camp,
        "主參將下營": home_vassal_camp, "客參將下營": away_vassal_camp,
        "刑克": {
            "敵大克主大": controls_big,
            "敵大克主參": controls_vassal,
            "已知克條件觸發": death_condition,
            "刑條件": None,
        },
        "出戰判定": "出戰必死" if death_condition else None,
    }


def return_army(
    enemy_arrival_taiyi: int | None,
    home_general: int | None = None,
    away_general: int | None = None,
) -> dict:
    """T7-07: use the enemy's initial-arrival Taiyi, never its current general."""
    if enemy_arrival_taiyi is None:
        return {
            "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
            "術": "回軍無言", "可計算": False,
            "缺少輸入": "敵軍初來時間的太乙宮",
        }
    point = dashen_from_lushen(enemy_arrival_taiyi)
    environment = element_at(point)
    home = _general_environment_detail(home_general, environment) if home_general is not None else None
    away = _general_environment_detail(away_general, environment) if away_general is not None else None
    if away is None:
        enemy_reading = None
        enemy_ambush = None
    else:
        enemy_reading = away["五態"]
        enemy_ambush = "有伏兵，宜防" if enemy_reading in STRONG_STATES else "敵自破，可攻"
    home_ambush = None if home is None else ("我方宜設伏" if home["五態"] in STRONG_STATES else None)
    return {
        "規則集": RULESET_ID, "規則版本": RULESET_VERSION,
        "術": "回軍無言", "可計算": True,
        "敵初來太乙宮": enemy_arrival_taiyi,
        "大神落點": point, "環境五行": environment,
        "本軍": home, "敵軍": away,
        "敵軍伏兵判斷": enemy_ambush, "我方設伏判斷": home_ambush,
    }

