"""C8 卷五军事实战综合层。

原则：本模块只组合已经独立的基础术，不复制八占公式，不把卷九/卷十七等
规则偷偷并入卷五主判断。三门、五将和将帅旺衰在来源公式尚未完成独立校勘
前，作为上游事实输入。
"""

from . import eight_divinations as d8

C8_VERSION = "taiyi-c8-v1"


def _not_computable(name, *missing):
    return {
        "name": name,
        "status": "not_computable",
        "computable": False,
        "missing_inputs": [item for item in missing if item],
    }


def _normalize_three_doors(value):
    if isinstance(value, bool):
        return {"raw": value, "ready": value, "status": "ok"}
    if isinstance(value, dict):
        ready = value.get("ready")
        if isinstance(ready, bool):
            return {"raw": value, "ready": ready, "status": "ok"}
        return {"raw": value, "ready": None, "status": "pending"}
    if isinstance(value, str):
        text = value.strip()
        if "三門不具" in text or "三门不具" in text:
            return {"raw": value, "ready": False, "status": "ok"}
        if "三門具" in text or "三门具" in text:
            return {"raw": value, "ready": True, "status": "ok"}
        return {"raw": value, "ready": None, "status": "pending"}
    if value is None:
        return {"raw": None, "ready": None, "status": "not_computable"}
    return {"raw": value, "ready": None, "status": "pending"}


def _normalize_five_generals(value):
    if isinstance(value, bool):
        return {"raw": value, "released": value, "status": "ok"}
    if isinstance(value, dict):
        released = value.get("released")
        if isinstance(released, bool):
            return {"raw": value, "released": released, "status": "ok"}
        return {"raw": value, "released": None, "status": "pending"}
    if isinstance(value, str):
        text = value.strip()
        if "五將不發" in text or "五将不发" in text or "杜塞無門" in text or "杜塞无门" in text:
            return {"raw": value, "released": False, "status": "ok"}
        if "五將發" in text or "五将发" in text:
            return {"raw": value, "released": True, "status": "ok"}
        return {"raw": value, "released": None, "status": "pending"}
    if value is None:
        return {"raw": None, "released": None, "status": "not_computable"}
    return {"raw": value, "released": None, "status": "pending"}


def eight_divinations_layer(*, home_cal=None, away_cal=None, taiyi=None, skyeyes=None):
    """把 D8-01..08 作为卷五军事综合层的基础事实，不重算、不覆盖。"""
    home = {}
    away = {}

    if home_cal is None:
        home = _not_computable("主算八占", "home_cal")
    else:
        home = {
            "sancai": d8.sancai(home_cal),
            "length": d8.calc_length(home_cal),
            "wuyin": d8.wuyin_from_calc(home_cal),
            "gudan": d8.gudan_state(home_cal),
            "preparedness": d8.calc_preparedness(home_cal),
        }

    if away_cal is None:
        away = _not_computable("客算八占", "away_cal")
    else:
        away = {
            "sancai": d8.sancai(away_cal),
            "length": d8.calc_length(away_cal),
            "wuyin": d8.wuyin_from_calc(away_cal),
            "gudan": d8.gudan_state(away_cal),
            "preparedness": d8.calc_preparedness(away_cal),
        }

    comparison = (
        d8.suenwl(home_cal, away_cal)
        if home_cal is not None and away_cal is not None
        else _not_computable("多少占胜负", *(
            name for name, value in (("home_cal", home_cal), ("away_cal", away_cal))
            if value is None
        ))
    )
    attack = (
        d8.attack_realm(skyeyes)
        if skyeyes is not None
        else _not_computable("内外占攻击", "skyeyes")
    )
    danger = (
        d8.tui_danger(taiyi, home_cal, away_cal)
        if taiyi is not None and home_cal is not None
        else _not_computable("阴阳厄会", *(
            name for name, value in (("taiyi", taiyi), ("home_cal", home_cal))
            if value is None
        ))
    )

    return {
        "layer_id": "C8-L1",
        "name": "八占基础结果",
        "source_scope": "canonical_eight_divinations",
        "source_rule": "D8-01..08",
        "status": "ok",
        "home": home,
        "away": away,
        "comparison": comparison,
        "attack_realm": attack,
        "danger": danger,
        "policy": "仅调用 D8-01..08；五音与数有所主分栏，互不替代。",
    }


def three_doors_five_generals_layer(three_doors=None, five_generals=None):
    """三门五将只接收上游结论；C8 不在这里重算八门或五将公式。"""
    doors = _normalize_three_doors(three_doors)
    generals = _normalize_five_generals(five_generals)

    if doors["ready"] is False or generals["released"] is False:
        joint_ready = False
    elif doors["ready"] is True and generals["released"] is True:
        joint_ready = True
    else:
        joint_ready = None

    return {
        "layer_id": "C8-L2",
        "name": "三门五将",
        "source_scope": "volume5_military",
        "source_rule": "三门五将（上游事实；底层公式待独立校勘）",
        "three_doors": doors,
        "five_generals": generals,
        "joint_ready": joint_ready,
        "computable": joint_ready is not None,
        "policy": "只归一化上游事实，不从太乙宫、八门、天目或将宫自行反推。",
        "pending": [] if joint_ready is not None else ["三门或五将的上游结果未给定/未识别"],
    }


def zhuke_dongjing_layer(three_doors_five_generals):
    """卷五主客动静：只处理先后角色与行动姿态，不夹带八占胜负公式。"""
    ready = three_doors_five_generals.get("joint_ready")
    roles = {
        "field_battle": {
            "first_mover": "客",
            "responder": "主",
            "note": "野战旗鼓相望：先动者为客，后应者为主",
        },
        "settled_context": {
            "first_mover": "主",
            "responder": "客",
            "note": "安居之代：先举者为主，后应者为客",
        },
    }

    if ready is True:
        status = "ready"
        posture = "可进入主客动静判断"
        pending = []
    elif ready is False:
        status = "hold"
        posture = "三门或五将不备，综合层只标固守倾向，不据此宣判胜负"
        pending = []
    else:
        status = "not_computable"
        posture = "三门五将未定，暂不合成行动判断"
        pending = ["缺三门五将可判事实"]

    return {
        "layer_id": "C8-L3",
        "name": "主客动静",
        "source_scope": "volume5_military",
        "source_rule": "明主客以分先后动静之术",
        "status": status,
        "roles": roles,
        "posture": posture,
        "winner": None,
        "policy": "动静角色不改写 D8-06 多少胜负，也不以算长短另造胜负。",
        "pending": pending,
    }


def _commander_assessment(side, state=None, palace=None):
    base = {"side": side, "palace": palace, "strength_state": state}
    if state is None:
        return {
            **base,
            "status": "not_computable",
            "capable": None,
            "verdict": "未提供经校勘的将帅旺衰状态",
        }
    if state in ("旺", "相"):
        return {
            **base,
            "status": "favorable",
            "capable": True,
            "verdict": "有气，可任",
        }
    if state in ("囚", "死"):
        return {
            **base,
            "status": "unfavorable",
            "capable": False,
            "verdict": "无气，不利将帅",
        }
    if state == "休":
        return {
            **base,
            "status": "pending",
            "capable": None,
            "verdict": "休态原文归类待校，不强判贤否",
        }
    return {
        **base,
        "status": "pending",
        "capable": None,
        "verdict": "未知旺衰标签，待来源校勘",
    }


def jiangshuai_xianfou_layer(*, home_state=None, away_state=None,
                             home_palace=None, away_palace=None):
    """将帅贤否只消费明确的旺衰状态，不借七术 Mode B 或十二长生代替。"""
    home = _commander_assessment("主", home_state, home_palace)
    away = _commander_assessment("客", away_state, away_palace)
    return {
        "layer_id": "C8-L4",
        "name": "将帅贤否",
        "source_scope": "volume5_military",
        "source_rule": "明内外将帅贤否之术",
        "home": home,
        "away": away,
        "policy": "旺/相作有气，囚/死作无气；休与其他标签保留 pending。禁止套用七术五态或十二长生作替代来源。",
        "computable": home["status"] != "not_computable" or away["status"] != "not_computable",
    }


def legacy_projection(c8_result):
    """旧中文展示键的只读投影；不作为 canonical 真源。"""
    layers = c8_result["layers"]
    d8_layer = layers["eight_divinations"]
    return {
        "内外占攻击": d8_layer["attack_realm"],
        "算长短缓急": {
            "主算": d8_layer["home"].get("length") if isinstance(d8_layer["home"], dict) else None,
            "客算": d8_layer["away"].get("length") if isinstance(d8_layer["away"], dict) else None,
        },
        "五音": {
            "主算": d8_layer["home"].get("wuyin") if isinstance(d8_layer["home"], dict) else None,
            "客算": d8_layer["away"].get("wuyin") if isinstance(d8_layer["away"], dict) else None,
        },
        "数孤单成败": {
            "主算": d8_layer["home"].get("gudan") if isinstance(d8_layer["home"], dict) else None,
            "客算": d8_layer["away"].get("gudan") if isinstance(d8_layer["away"], dict) else None,
        },
        "数有所主": {
            "主算": d8_layer["home"].get("preparedness") if isinstance(d8_layer["home"], dict) else None,
            "客算": d8_layer["away"].get("preparedness") if isinstance(d8_layer["away"], dict) else None,
        },
        "多少占胜负": d8_layer["comparison"],
        "三门五将": layers["three_doors_five_generals"],
        "主客动静": layers["host_guest_movement"],
        "将帅贤否": layers["commanders"],
    }


def junshi_zhanlue(*, home_cal=None, away_cal=None, taiyi=None, skyeyes=None,
                   three_doors=None, five_generals=None,
                   home_general_state=None, away_general_state=None,
                   home_general_palace=None, away_general_palace=None):
    """C8 总入口：四层组合，默认排除跨卷混合法。"""
    layer1 = eight_divinations_layer(
        home_cal=home_cal, away_cal=away_cal, taiyi=taiyi, skyeyes=skyeyes,
    )
    layer2 = three_doors_five_generals_layer(three_doors, five_generals)
    layer3 = zhuke_dongjing_layer(layer2)
    layer4 = jiangshuai_xianfou_layer(
        home_state=home_general_state,
        away_state=away_general_state,
        home_palace=home_general_palace,
        away_palace=away_general_palace,
    )
    result = {
        "schema_version": "1.0",
        "canonical": C8_VERSION,
        "category": "military_composite",
        "name": "卷五军事实战综合",
        "source_profile": "volume5_strict",
        "cross_volume_merge": False,
        "source_variants": [],
        "layers": {
            "eight_divinations": layer1,
            "three_doors_five_generals": layer2,
            "host_guest_movement": layer3,
            "commanders": layer4,
        },
        "composition_policy": [
            "基础术各自保留 rule_id/source 语义，综合层不得复制公式。",
            "三门五将是独立输入事实，不得由八占结果反推。",
            "主客动静只判角色与行动姿态，不覆盖多少胜负。",
            "将帅贤否不借七术 Mode B、十二长生或卷十七格局补算。",
        ],
        "excluded_from_default": [
            {"name": "孤虚对照", "reason": "旧实现混入卷十七求索规则；须独立来源层后再组合"},
            {"name": "太乙助主客", "reason": "旧实现同时引用卷五/卷九语义；待拆成独立规则"},
            {"name": "辅相贤否", "reason": "应独立成辅相层，不能与将帅贤否同函数混算"},
            {"name": "诸将旺衰", "reason": "旺衰计算应由独立规则层提供，C8只消费结果"},
            {"name": "郡国进贤/出师略地", "reason": "属卷五其他篇目，不属于军事胜负综合主链"},
        ],
    }
    result["legacy_projection"] = legacy_projection(result)
    return result
