"""《景祐太乙福应经》卷四军事 source-specific runtimes.

JF4M-01..11 独立于《太乙金镜式经》J4M 实现。
本模块只解释 rules/jingyou_fuying_v4_military.json 已经锁定的《福应经》文字；
扫描待核字处保留 textual uncertainty，不借平行来源补缺。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import GODS, ELEMENTS


VERSION = "jingyou-fuying-v4-military-11-runtime-v1"
SOURCE_PROFILE = "jingyou_fuying_volume4"
RULESET = "jingyou-fuying-v4-military-11"

EIGHT_GATES = ("开", "休", "生", "伤", "杜", "景", "死", "惊")
LUCKY_GATES = {"开", "休", "生"}
DEPLOY_CALCS = {12, 22, 32}
DIRECTION_TABLE = {
    1: "西北", 2: "正南", 3: "东北", 4: "正东",
    6: "正西", 7: "西南", 8: "正北", 9: "东南",
}
INNER_HOST = {1, 8, 3, 4}
OUTER_GUEST = {9, 2, 7, 6}
FORMATION_ELEMENTS = {
    "曲阵": "水",
    "锐阵": "火",
    "直阵": "木",
    "方阵": "金",
    "圆阵": "土",
}

JF4M07_TERRAIN_TABLE = {
    "后高前低": {"formation": "锐阵", "effect": "利进战、溃敌"},
    "前高后低": {"formation": "直阵", "effect": "利近斗守御、疲敌"},
    "地形跨斜": {"formation": "圆阵", "effect": "不便战，宜坚固守"},
    "地形高而不平": {"formation": "方阵", "effect": "利四向、便斗战"},
    "左右势高岗": {"formation": "曲阵", "effect": "利吞敌"},
}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
GOD_ELEMENTS = dict(zip(GODS, ELEMENTS))
GOD_ALIASES = {"太蔟": "太簇"}
HIDDEN_CALCS = {11, 21, 31}

JF4M08_SOURCE_FACTS = {
    "urgent_requirements": ["得地形", "卒习服", "利器用"],
    "terrain_rules": [
        {"terrain_class": "步兵地", "favored": "步兵", "disfavored": "车骑", "source_ratio_text": "车骑二不当一"},
        {"terrain_class": "车骑地", "favored": "车骑", "disfavored": "步兵", "source_ratio_text": "步兵十不当一"},
        {"terrain_class": "弓弩地", "favored": "弓弩", "disfavored": "短兵", "source_ratio_text": "短兵百不当一"},
        {"terrain_class": "长戟地", "favored": "长戟", "disfavored": "剑楯", "source_ratio_text": "剑楯三不当一"},
        {"terrain_class": "矛鋋地", "favored": "矛鋋", "disfavored": "长戟", "source_ratio_text": "长戟二不当一"},
        {"terrain_class": "曲道剑楯地", "favored": "剑楯", "disfavored": "弓弩", "source_ratio_text": "弓弩三不当一"},
    ],
    "discipline_rules": {
        "soldiers_untrained": "不习服百不当十",
        "general_does_not_inspect_troops": "将不省兵五不当一",
    },
}


def _base(rule_id: str, name: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "canonical": VERSION,
        "ruleset": RULESET,
        "source_profile": SOURCE_PROFILE,
        "source_rule_id": rule_id,
        "name": name,
        "cross_source_merge": False,
    }


def _bool_or_none(name: str, value: Any) -> bool | None:
    if value is not None and not isinstance(value, bool):
        raise TypeError(f"{name}须为bool或None")
    return value


def _pattern_list(name: str, value: list[str] | tuple[str, ...] | None) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name}须为list/tuple或None")
    result = []
    for item in value:
        if not isinstance(item, str):
            raise TypeError(f"{name}各项须为str")
        result.append(item)
    return result


def direct_gate_from_period_count(period_count: int) -> dict[str, Any]:
    """JF4M-01 直使门：240一周，30一移。"""
    result = _base("JF4M-01", "释三门具不具")
    if isinstance(period_count, bool) or not isinstance(period_count, int) or period_count <= 0:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "period_count": period_count,
            "policy": "须给正整数累计数；岁/月/日/时如何换成累计数由各自上游负责。",
        }
    within = (period_count - 1) % 240 + 1
    index = (within - 1) // 30
    return {
        **result,
        "status": "ok",
        "computable": True,
        "period_count": period_count,
        "within_240_cycle": within,
        "block_of_30": index + 1,
        "direct_gate": EIGHT_GATES[index],
        "gate_order": list(EIGHT_GATES),
        "policy": "只实现《福应经》本条240周、30一换；不调用《金镜》直门函数。",
    }


def three_doors(
    *,
    taiyi_gate: str | None = None,
    tianmu_gate: str | None = None,
    period_count: int | None = None,
) -> dict[str, Any]:
    """JF4M-01 三门具不具。"""
    result = _base("JF4M-01", "释三门具不具")
    for label, gate in (("taiyi_gate", taiyi_gate), ("tianmu_gate", tianmu_gate)):
        if gate is not None and gate not in EIGHT_GATES:
            return {
                **result,
                "status": "not_computable",
                "computable": False,
                label: gate,
                "valid_gates": list(EIGHT_GATES),
            }

    direct = direct_gate_from_period_count(period_count) if period_count is not None else None
    gates = {g for g in (taiyi_gate, tianmu_gate) if g is not None}
    if "休" in gates:
        ready = False
        status = "three_doors_not_ready"
        source_case = "太乙或天目临休门：三门不具"
        not_ready_count = 3
    elif taiyi_gate is not None and tianmu_gate is not None and gates == {"开", "生"}:
        ready = False
        status = "two_doors_not_ready"
        source_case = "太乙、天目分临开生：二门不具"
        not_ready_count = 2
    elif taiyi_gate is None or tianmu_gate is None:
        ready = None
        status = "not_computable"
        source_case = "缺太乙或天目所临门"
        not_ready_count = None
    else:
        ready = None
        status = "not_defined_by_source_passage"
        source_case = "本条未展开该门组合"
        not_ready_count = None

    return {
        **result,
        "status": status,
        "computable": ready is not None,
        "taiyi_gate": taiyi_gate,
        "tianmu_gate": tianmu_gate,
        "three_doors": ["开", "休", "生"],
        "three_doors_ready": ready,
        "not_ready_count": not_ready_count,
        "source_case": source_case,
        "direct_gate_result": direct,
        "policy": "只判《福应经》明确组合；直使门周期与门具事实分栏。",
    }


def five_generals(
    *,
    shiji_yanji: bool | None = None,
    wenchang_qiupo: bool | None = None,
    third_condition_clear: bool | None = None,
    three_doors_ready: bool | None = None,
) -> dict[str, Any]:
    """JF4M-02 五将发不发。

    third_condition_clear 对应电子转录“大小将不相开”这一待核字条件：
    True 只表示调用方确认“第三条件满足”，不在本函数解释“相开”的技术含义。
    """
    result = _base("JF4M-02", "释五将发不发")
    shiji_yanji = _bool_or_none("shiji_yanji", shiji_yanji)
    wenchang_qiupo = _bool_or_none("wenchang_qiupo", wenchang_qiupo)
    third_condition_clear = _bool_or_none("third_condition_clear", third_condition_clear)
    three_doors_ready = _bool_or_none("three_doors_ready", three_doors_ready)

    blockers = []
    if shiji_yanji is True:
        blockers.append("始击有掩击")
    if wenchang_qiupo is True:
        blockers.append("文昌有囚迫")
    if third_condition_clear is False:
        blockers.append("第三条件未满足（原转录‘大小将不相开’待核字）")

    facts_known = all(
        isinstance(v, bool)
        for v in (shiji_yanji, wenchang_qiupo, third_condition_clear)
    )
    if blockers:
        released = False
    elif facts_known:
        released = True
    else:
        released = None

    if three_doors_ready is False or released is False:
        combined = False
    elif three_doors_ready is True and released is True:
        combined = True
    else:
        combined = None

    return {
        **result,
        "status": "ok" if released is not None else "not_computable",
        "computable": released is not None,
        "shiji_yanji": shiji_yanji,
        "wenchang_qiupo": wenchang_qiupo,
        "third_condition_clear": third_condition_clear,
        "third_condition_source_reading": "大小将不相开",
        "textual_uncertainty": "该字样待扫描核字；不得自动等同《金镜》‘主客大小将无相关’。",
        "blockers": blockers if released is not None else None,
        "five_generals_released": released,
        "three_doors_ready": three_doors_ready,
        "combined_ready": combined,
        "deployment_allowed_by_doors": three_doors_ready,
        "engagement_allowed_by_generals": released,
        "policy": "五将条件与三门条件分栏；疑字条件只接显式事实，不跨来源解释。",
    }


def _god_element(name: str | None) -> tuple[str | None, str | None]:
    if name is None:
        return None, None
    canonical = GOD_ALIASES.get(name, name)
    return canonical, GOD_ELEMENTS.get(canonical)


def host_guest_relation(
    *,
    host_eye_element: str | None = None,
    guest_eye_element: str | None = None,
    host_eye_god: str | None = None,
    guest_eye_god: str | None = None,
    calculation_scope: str = "日计",
) -> dict[str, Any]:
    """JF4M-03 主客相关。"""
    result = _base("JF4M-03", "释主客相关")
    if calculation_scope != "日计":
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "calculation_scope": calculation_scope,
            "required_scope": "日计",
        }

    host_god, host_from_god = _god_element(host_eye_god)
    guest_god, guest_from_god = _god_element(guest_eye_god)

    if host_eye_element is None:
        host_eye_element = host_from_god
    elif host_from_god is not None and host_eye_element != host_from_god:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "conflict": "host_eye_element_vs_god",
        }

    if guest_eye_element is None:
        guest_eye_element = guest_from_god
    elif guest_from_god is not None and guest_eye_element != guest_from_god:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "conflict": "guest_eye_element_vs_god",
        }

    valid = set(CONTROLS)
    if host_eye_element not in valid or guest_eye_element not in valid:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "host_eye_element": host_eye_element,
            "guest_eye_element": guest_eye_element,
            "known_gods": sorted(GOD_ELEMENTS),
        }

    if CONTROLS[guest_eye_element] == host_eye_element:
        relation, winner, loser = "客关得主", "客", "主"
    elif CONTROLS[host_eye_element] == guest_eye_element:
        relation, winner, loser = "主人关得客", "主", "客"
    else:
        relation = winner = loser = None

    return {
        **result,
        "status": "ok",
        "computable": True,
        "calculation_scope": "日计",
        "host_eye_element": host_eye_element,
        "guest_eye_element": guest_eye_element,
        "host_eye_god": host_eye_god,
        "guest_eye_god": guest_eye_god,
        "host_eye_god_canonical": host_god,
        "guest_eye_god_canonical": guest_god,
        "relation": relation,
        "winner": winner,
        "loser": loser,
        "canonical_outcome": f"{winner}胜" if winner else "本条无相制关关系",
        "policy": "只按《福应经》日计二目所临神五行相制判关胜负；无相制时不扩断。",
    }


def host_guest_action(
    context: str,
    *,
    three_doors_ready: bool | None = None,
    five_generals_released: bool | None = None,
    yin_yang_harmonious: bool | None = None,
    host_calc: int | None = None,
    guest_calc: int | None = None,
) -> dict[str, Any]:
    """JF4M-04 主客先后动静。"""
    result = _base("JF4M-04", "释主客")
    contexts = {
        "陈兵原野": {"first_mover": "客", "responder": "主"},
        "field_battle": {"first_mover": "客", "responder": "主"},
        "安居之势": {"first_mover": "主", "responder": "客"},
        "settled_context": {"first_mover": "主", "responder": "客"},
    }
    if context not in contexts:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "context": context,
            "valid_contexts": ["陈兵原野", "安居之势"],
        }

    three_doors_ready = _bool_or_none("three_doors_ready", three_doors_ready)
    five_generals_released = _bool_or_none("five_generals_released", five_generals_released)
    yin_yang_harmonious = _bool_or_none("yin_yang_harmonious", yin_yang_harmonious)
    readiness = {
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
        "yin_yang_harmonious": yin_yang_harmonious,
    }
    role = contexts[context]
    all_known = all(isinstance(v, bool) for v in readiness.values())
    all_good = all_known and all(readiness.values())
    all_bad = all_known and not any(readiness.values())

    if all_good:
        status = "favorable"
        winner = role["first_mover"]
        loser = role["responder"]
        advice = "先起者胜，后起者负"
    elif all_bad:
        status = "hold_and_defend"
        winner = loser = None
        advice = "三项不利，宜固守"
    elif not all_known:
        status = "not_computable"
        winner = loser = None
        advice = "缺三门、五将或阴阳和事实"
    else:
        status = "mixed_not_defined"
        winner = loser = None
        advice = "混合组合本条未明确，不扩写"

    return {
        **result,
        "status": status,
        "computable": all_good or all_bad,
        "context": "陈兵原野" if context in {"陈兵原野", "field_battle"} else "安居之势",
        "roles": copy.deepcopy(role),
        **readiness,
        "winner": winner,
        "loser": loser,
        "action_advice": advice,
        "cross_side_calc_reference": {
            "欲知主人": {"target_calc": "主算", "value": host_calc},
            "欲知客": {"target_calc": "客算", "value": guest_calc},
        },
        "policy": "只判《福应经》本条的先后角色与三项和不和；不覆盖JF4M-03五行胜负。",
    }


def dispatch_troops(
    calc_value: int,
    *,
    three_doors_ready: bool | None = None,
    five_generals_released: bool | None = None,
    exit_gate: str | None = None,
) -> dict[str, Any]:
    """JF4M-05 出师略地。"""
    result = _base("JF4M-05", "释出师略地")
    three_doors_ready = _bool_or_none("three_doors_ready", three_doors_ready)
    five_generals_released = _bool_or_none("five_generals_released", five_generals_released)

    calc_ready = calc_value in DEPLOY_CALCS
    gate_valid = None if exit_gate is None else exit_gate in LUCKY_GATES

    if not calc_ready:
        status, ready = "hold", False
    elif three_doors_ready is False or five_generals_released is False:
        status, ready = "hold", False
    elif not isinstance(three_doors_ready, bool) or not isinstance(five_generals_released, bool):
        status, ready = "not_computable", None
    elif gate_valid is False:
        status, ready = "hold", False
    elif gate_valid is None:
        status, ready = "ready_pending_gate", None
    else:
        status, ready = "ready", True

    return {
        **result,
        "status": status,
        "computable": status != "not_computable",
        "calc_value": calc_value,
        "eligible_calcs": sorted(DEPLOY_CALCS),
        "calc_ready": calc_ready,
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
        "exit_gate": exit_gate,
        "lucky_gates": ["开", "休", "生"],
        "exit_gate_valid": gate_valid,
        "deployment_ready": ready,
        "policy": "算12/22/32、门具、将发、出开休生四项分栏；不借《金镜》或《统宗》补条件。",
    }


def deploy_direction(rule_number: int) -> dict[str, Any]:
    """JF4M-06 陈兵向背/出兵方向。"""
    result = _base("JF4M-06", "释陈兵向背")
    if rule_number not in DIRECTION_TABLE:
        return {
            **result,
            "status": "not_defined_by_source_passage",
            "computable": False,
            "input": rule_number,
            "defined_rule_numbers": list(DIRECTION_TABLE),
            "policy": "只认1/2/3/4/6/7/8/9；不取个位，不与《金镜》阵旗表互补。",
        }
    return {
        **result,
        "status": "ok",
        "computable": True,
        "input": rule_number,
        "direction": DIRECTION_TABLE[rule_number],
        "direction_table": dict(DIRECTION_TABLE),
        "policy": "直接读取《福应经》卷四自身方向表。",
    }


def _formation_contest(host_formation: str | None, guest_formation: str | None) -> dict[str, Any]:
    if host_formation is None or guest_formation is None:
        return {"winner": None, "relation": "not_computable"}
    if host_formation not in FORMATION_ELEMENTS or guest_formation not in FORMATION_ELEMENTS:
        return {"winner": None, "relation": "unknown_formation"}
    he = FORMATION_ELEMENTS[host_formation]
    ge = FORMATION_ELEMENTS[guest_formation]
    if CONTROLS[he] == ge:
        return {"winner": "主", "relation": f"{he}制{ge}"}
    if CONTROLS[ge] == he:
        return {"winner": "客", "relation": f"{ge}制{he}"}
    return {"winner": None, "relation": "无相克，本条不扩断"}


def formation_by_terrain(
    *,
    host_formation: str | None = None,
    guest_formation: str | None = None,
    terrain_shape: str | None = None,
) -> dict[str, Any]:
    """JF4M-07 置阵随地。"""
    result = _base("JF4M-07", "释置阵随地")
    contest = _formation_contest(host_formation, guest_formation)
    terrain_rule = copy.deepcopy(JF4M07_TERRAIN_TABLE.get(terrain_shape))

    if terrain_shape is None:
        terrain_status = "not_requested"
    elif terrain_rule is None:
        terrain_status = "not_defined_by_source_passage"
    else:
        terrain_status = "ok"

    return {
        **result,
        "status": (
            "ok"
            if terrain_rule is not None or contest["relation"] not in {"not_computable", "unknown_formation"}
            else "partial"
        ),
        "computable": terrain_rule is not None or contest["relation"] not in {"not_computable", "unknown_formation"},
        "formation_elements": dict(FORMATION_ELEMENTS),
        "host_formation": host_formation,
        "guest_formation": guest_formation,
        "formation_contest": contest,
        "terrain_shape": terrain_shape,
        "terrain_rule": terrain_rule,
        "terrain_table": copy.deepcopy(JF4M07_TERRAIN_TABLE),
        "terrain_status": terrain_status,
        "direction_relation": {"顺其乡": "益吉", "反其乡": "不取为自动胜负"},
        "policy": "五阵五行相制与地形选阵分栏；当前地形表来自《福应经》卷四转录，不借J4M表。",
    }


def adapt_to_terrain(
    terrain_class: str | None = None,
    *,
    soldiers_trained: bool | None = None,
    equipment_serviceable: bool | None = None,
    general_inspects_troops: bool | None = None,
) -> dict[str, Any]:
    """JF4M-08 随地形制变。"""
    result = _base("JF4M-08", "释随地形制变")
    soldiers_trained = _bool_or_none("soldiers_trained", soldiers_trained)
    equipment_serviceable = _bool_or_none("equipment_serviceable", equipment_serviceable)
    general_inspects_troops = _bool_or_none("general_inspects_troops", general_inspects_troops)

    terrain = next(
        (item for item in JF4M08_SOURCE_FACTS["terrain_rules"] if item["terrain_class"] == terrain_class),
        None,
    )
    warnings = []
    if soldiers_trained is False:
        warnings.append(JF4M08_SOURCE_FACTS["discipline_rules"]["soldiers_untrained"])
    if equipment_serviceable is False:
        warnings.append("器用不利：本条列为急务之一")
    if general_inspects_troops is False:
        warnings.append(JF4M08_SOURCE_FACTS["discipline_rules"]["general_does_not_inspect_troops"])

    return {
        **result,
        "status": "ok" if terrain is not None else "partial",
        "computable": terrain is not None,
        "terrain_class": terrain_class,
        "terrain_rule": copy.deepcopy(terrain),
        "source_facts": copy.deepcopy(JF4M08_SOURCE_FACTS),
        "soldiers_trained": soldiers_trained,
        "equipment_serviceable": equipment_serviceable,
        "general_inspects_troops": general_inspects_troops,
        "warnings": warnings,
        "policy": "保留《福应经》自身二不当一、百不当十、五不当一等读法；不得用《金镜》比例覆盖。",
    }


def taiyi_outer_inner(
    taiyi_palace: int,
    *,
    three_doors_ready: bool | None = None,
    five_generals_released: bool | None = None,
) -> dict[str, Any]:
    """JF4M-09 太乙在天外地内宫。"""
    result = _base("JF4M-09", "释太乙在天外地内宫")
    three_doors_ready = _bool_or_none("three_doors_ready", three_doors_ready)
    five_generals_released = _bool_or_none("five_generals_released", five_generals_released)

    if taiyi_palace in INNER_HOST:
        realm, assists = "地内", "主"
    elif taiyi_palace in OUTER_GUEST:
        realm, assists = "天外", "客"
    else:
        return {
            **result,
            "status": "not_defined_by_source_passage",
            "computable": False,
            "taiyi_palace": taiyi_palace,
            "canonical_groups": {
                "地内助主": sorted(INNER_HOST),
                "天外助客": sorted(OUTER_GUEST),
            },
        }

    if three_doors_ready is False or five_generals_released is False:
        decisive = False
    elif three_doors_ready is True and five_generals_released is True:
        decisive = True
    else:
        decisive = None

    return {
        **result,
        "status": "ok",
        "computable": True,
        "taiyi_palace": taiyi_palace,
        "realm": realm,
        "assists": assists,
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
        "decisive_ready": decisive,
        "canonical_groups": {
            "地内助主": sorted(INNER_HOST),
            "天外助客": sorted(OUTER_GUEST),
        },
        "policy": "1宫明确属于《福应经》地内助主；不得改成《金镜》1宫未定义。",
    }


JF4M10_PHENOMENA = {"风", "云", "飞鸟", "众鸟"}


def weather_bird_support(events: list[dict[str, Any]]) -> dict[str, Any]:
    """JF4M-10 风云飞鸟助战：解释当前《福应经》卷四转录已锁定的观测句。"""
    result = _base("JF4M-10", "释太乙风云飞鸟置战")
    if not isinstance(events, list):
        raise TypeError("events须为list")

    judgments = []
    for event in events:
        if not isinstance(event, dict):
            raise TypeError("events各项须为dict")
        phenomenon = event.get("phenomenon")
        if phenomenon not in JF4M10_PHENOMENA:
            judgments.append({
                "event": copy.deepcopy(event),
                "matched": False,
                "note": "必须显式标明风/云/飞鸟/众鸟。",
            })
            continue

        action = event.get("action")
        source_anchor = event.get("source_anchor")
        target = event.get("target")
        wing_target = event.get("wing_target")
        returning_wind = event.get("returning_wind")
        birds_circling = event.get("birds_circling")
        flag_broken = event.get("flag_broken")
        crowd_noisy = event.get("crowd_noisy")

        judgment = {
            "event": copy.deepcopy(event),
            "matched": True,
            "winner": None,
            "loser": None,
            "omen": None,
            "source_case": None,
        }

        if target in {"太乙", "太乙宫"} and action in {"冲", "格", "迫", "击", "冲格迫击"}:
            judgment.update(omen="大败", source_case="风云飞鸟冲格迫击太乙宫")
        elif action in {"迫", "击", "迫击"} and target in {"客大将", "客将", "客大将宫"}:
            judgment.update(loser="客", source_case="迫击客大将宫")
        elif action in {"迫", "击", "迫击"} and target in {"主大将", "主将", "主大将宫"}:
            judgment.update(loser="主", source_case="迫击主大将宫")
        elif source_anchor in {"主人刑", "主刑"} and action in {"来", "上来"}:
            judgment.update(loser="主", source_case="从主人刑上来")
        elif source_anchor == "客刑" and action in {"来", "上来"}:
            judgment.update(loser="客", source_case="从客刑上来")
        elif source_anchor in {"主目"} and action in {"击", "去击"} and target in {"客大将", "客大将宫"}:
            judgment.update(loser="客", source_case="从主目上去击客大将宫")
        elif source_anchor in {"客", "客目"} and action in {"击", "去击"} and target in {"主大将", "主大将宫"}:
            judgment.update(loser="主", source_case="从客目上去击主大将宫")
        elif source_anchor in {"太岁", "太阴", "月建"} and action == "击" and target in {"主人阵", "主阵"}:
            judgment.update(loser="主", source_case=f"从{source_anchor}上来击主人阵")
        elif source_anchor in {"太岁", "太阴", "月建"} and action == "击" and target == "客阵":
            judgment.update(loser="客", source_case=f"从{source_anchor}上来击客阵")
        elif wing_target in {"主人阵前", "主阵前"}:
            judgment.update(winner="主", source_case="来翼主人阵前")
        elif wing_target == "客阵前":
            judgment.update(winner="客", source_case="来翼客阵前")
        elif returning_wind is True and (birds_circling is True or flag_broken is True):
            judgment.update(omen="大败之兆", source_case="回旋风起且飞鸟旋阵或旗竿折")
        elif crowd_noisy is True and action in {"冲阵", "冲", "衝阵", "衝"} and target in {"主人阵", "主阵"}:
            judgment.update(loser="主", omen="凶", source_case="众鸟翼噪并风云冲主人阵")
        elif crowd_noisy is True and action in {"冲阵", "冲", "衝阵", "衝"} and target == "客阵":
            judgment.update(loser="客", omen="凶", source_case="众鸟翼噪并风云冲客阵")
        elif crowd_noisy is True and action in {"冲阵", "冲", "衝阵", "衝"}:
            judgment.update(omen="凶", source_case="众鸟翼噪并风云冲阵而来")
        else:
            judgment.update(
                matched=False,
                source_case="当前转录未覆盖该观测组合",
                note="不以J4M-11或盘内飞鸟位置补断。",
            )
        judgments.append(judgment)

    matched = [x for x in judgments if x["matched"]]
    return {
        **result,
        "status": "ok" if matched else "not_defined_by_source_passage",
        "computable": bool(matched),
        "events": copy.deepcopy(events),
        "judgments": judgments,
        "observation_schema": {
            "phenomenon": sorted(JF4M10_PHENOMENA),
            "fields": [
                "phenomenon", "action", "source_anchor", "target", "wing_target",
                "returning_wind", "birds_circling", "flag_broken", "crowd_noisy",
            ],
        },
        "policy": "只解释《福应经》卷四当前转录明确观测句；不调用J4M-11，不从盘内飞鸟位置伪造外部观测。",
    }


def odd_ambush(
    *,
    army_size: int | None = None,
    tianmu_location: Any = None,
    calc_value: int | None = None,
    yanpo: bool | None = None,
    enemy_near: bool | None = None,
) -> dict[str, Any]:
    """JF4M-11 奇伏。"""
    result = _base("JF4M-11", "释奇伏")
    yanpo = _bool_or_none("yanpo", yanpo)
    enemy_near = _bool_or_none("enemy_near", enemy_near)

    if army_size is None:
        count = None
        count_status = "not_requested"
    elif isinstance(army_size, bool) or not isinstance(army_size, int) or army_size <= 0:
        count = None
        count_status = "invalid_army_size"
    elif army_size % 10 == 0:
        count = army_size * 3 // 10
        count_status = "exact_from_three_tenths"
    else:
        count = None
        count_status = "ratio_known_rounding_unspecified"

    hidden = calc_value in HIDDEN_CALCS if calc_value is not None else None
    recommendations = []
    if hidden is True:
        recommendations.append("伏藏隐迹")
    if yanpo is True:
        recommendations.append("掩迫时发")
    if enemy_near is True:
        recommendations.append("伏于要害")

    return {
        **result,
        "status": "ok",
        "computable": True,
        "army_size": army_size,
        "odd_force_ratio": {"numerator": 3, "denominator": 10},
        "odd_force_count": count,
        "odd_force_count_status": count_status,
        "tianmu_location": copy.deepcopy(tianmu_location),
        "great_kill_location": copy.deepcopy(tianmu_location),
        "great_kill_note": "奇兵必从大杀之地；本条大杀为天目所临之下。",
        "position_note": "转录另记其地居高、去敌三五里。",
        "calc_value": calc_value,
        "concealment_calcs": sorted(HIDDEN_CALCS),
        "concealment_time": hidden,
        "yanpo": yanpo,
        "enemy_near": enemy_near,
        "recommendations": recommendations,
        "divergence_from_jinjing": "《福应经》作奇兵必从大杀之地；不得改写为《金镜》伏兵必败大煞之地。",
        "policy": "奇兵比例、大杀位、11/21/31伏藏、掩迫、贼近要害分栏；不借J4M-10的12/22/32伏兵时。",
    }


def jf4m_runtime_catalog() -> dict[str, Any]:
    return {
        "canonical": VERSION,
        "source_profile": SOURCE_PROFILE,
        "ruleset": RULESET,
        "implemented": [f"JF4M-{n:02d}" for n in range(1, 12)],
        "cross_source_merge": False,
        "source_limited": True,
        "pending_textual_uncertainty": {
            "JF4M-02": "大小将不相开的技术义仍待扫描/异本核字",
        },
        "policy": "11条均有独立福应经runtime；不调用J4M平行实现，疑字/未锁定句保持pending。",
    }
