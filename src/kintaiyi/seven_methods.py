"""Seven canonical methods. Mode A, Mode B and source variants stay separate."""
import warnings

from .taiyi_common import (
    BRANCHES, CORNER_SECTORS, OVERCOMES, ROLE_ELEMENTS, STEMS,
    dashen_from_nine_palace, dashen_from_sector, dashen_self_qi,
    general_palace_qi, integer, nine_palace_element, sexagenary_year,
)

NAMES = {"T7-01": "临津问道", "T7-02": "狮子反掷", "T7-03": "白云卷空",
         "T7-04": "猛虎相拒", "T7-05": "雷公入水", "T7-06": "白龙得云", "T7-07": "回军无言"}


def _wrap(rule_id, inputs, analysis=None, decision=None, missing=(), reason=None, variants=(), **legacy):
    available = not missing and reason is None
    return {"id": rule_id, "rule_id": rule_id, "name": NAMES[rule_id],
            "category": "seven_methods", "canonical": "taiyi-t7-d8-v1",
            "computable": available, "missing_inputs": list(missing), "missing": list(missing),
            "status": "ok" if available else "not_computable",
            "reason": reason or ("缺事件或将帅输入" if missing else None),
            "inputs": inputs, "analysis": analysis or {}, "decision": decision or {},
            "variants": list(variants), "source_variants": list(variants),
            "provenance": {"canonical": "project_canonical", "five_state": "R-QI",
                           "fire_twelve_stage": "derived"}, **legacy}


def _qi(landing):
    q = dashen_self_qi(landing)
    return {**q, "position": landing, "element": q["environment"],
            "palace": q["landing"]["nine_palace"], "stage": q["fire_stage"]}


def linjin_wendao(enemy_start_year_branch=None):
    inputs = {"enemy_start_year_branch": enemy_start_year_branch}
    if enemy_start_year_branch is None:
        return _wrap("T7-01", inputs, missing=["enemy_start_year_branch"])
    _, branch = sexagenary_year(enemy_start_year_branch)
    chain = [branch]
    for _ in range(4):
        chain.append(dashen_from_sector(chain[-1]))
    breaks = dict(zip(("year", "month", "day", "hour"), chain[1:]))
    return _wrap("T7-01", inputs, {"chain": chain}, {"breaks": breaks}, chain=chain,
                 break_year_branch=chain[1], break_month_branch=chain[2],
                 break_day_branch=chain[3], break_hour_branch=chain[4])


def lion_reverse_throw(enemy_start_year_branch=None):
    inputs = {"enemy_start_year_branch": enemy_start_year_branch}
    if enemy_start_year_branch is None:
        return _wrap("T7-02", inputs, missing=["enemy_start_year_branch"])
    index, branch = sexagenary_year(enemy_start_year_branch)
    qi = _qi(dashen_from_sector(branch))
    corner = next((s for s, points in CORNER_SECTORS.items() if qi["position"] in points), None)
    offset = 17 if corner else None
    year = None if index is None or offset is None else STEMS[(index + offset) % 10] + BRANCHES[(index + offset) % 12]
    timing = {"sector": corner, "year_number": 18 if corner else None, "offset": offset,
              "year": year, "candidate_branch": qi["position"] if corner is None else None}
    verdict = "不破" if qi["state"] in ("旺", "相") else "合破"
    return _wrap("T7-02", inputs, {"dashen": qi, "timing": timing}, {"verdict": verdict},
                 variants=[{"status": "source_variant", "note": "墓为易破"}],
                 dashen=qi, timing=timing, verdict=verdict,
                 pending=[] if corner else ["普通落支应期待校"])


def _cloud_side(palace, label):
    if palace is not None:
        integer(palace, 1, 9)
    if palace is None or palace == 5:
        return {"computable": False, "general_palace": palace, "reason": "缺大将" if palace is None else "杜塞",
                "strength": None}
    qi = _qi(dashen_from_nine_palace(palace))
    strong = qi["state"] in ("旺", "相")
    special = {"stage": qi["stage"], "provenance": "derived",
               "cannot_offend": qi["stage"] == "帝旺",
               "skilled": qi["stage"] in ("临官", "冠带")}
    return {"computable": True, "general_palace": palace, "role": label,
            "intrinsic_element": ROLE_ELEMENTS[label], "palace_element": nine_palace_element(palace),
            "dashen": qi, "strength": "强" if strong else "弱", "special": special,
            "verdict": "不可触犯" if special["cannot_offend"] else "善战/精锐" if special["skilled"] else "强" if strong else "弱败"}


def white_cloud(home_general=None, away_general=None):
    inputs = {"home_general": home_general, "away_general": away_general}
    home = _cloud_side(home_general, "home_general")
    away = _cloud_side(away_general, "away_general")
    complete = home["computable"] and away["computable"]
    winner = None
    if complete and home["strength"] != away["strength"]:
        winner = "home" if home["strength"] == "强" else "away"
    comparison = {"status": "完整" if complete else "不完整", "winner": winner}
    missing = [k for k, v in inputs.items() if v is None]
    reason = "杜塞：大将中五无十六辰" if 5 in inputs.values() else None
    return _wrap("T7-03", inputs, {"home": home, "away": away}, comparison, missing, reason,
                 variants=[{"status": "source_variant", "source": "四库", "note": "冠带士卒战死"},
                           {"status": "project_canonical", "source": "景祐", "note": "临官冠带善战"}],
                 home=home, away=away, comparison=comparison)


def fierce_tiger(enemy_camp_day_taiyi_palace=None):
    inputs = {"enemy_camp_day_taiyi_palace": enemy_camp_day_taiyi_palace}
    if enemy_camp_day_taiyi_palace is None:
        return _wrap("T7-04", inputs, missing=["enemy_camp_day_taiyi_palace"])
    integer(enemy_camp_day_taiyi_palace, 1, 9)
    if enemy_camp_day_taiyi_palace == 5:
        return _wrap("T7-04", inputs, reason="杜塞：中五无大神落辰")
    qi = _qi(dashen_from_nine_palace(enemy_camp_day_taiyi_palace))
    attack = False if qi["state"] in ("旺", "相") else True if qi["state"] == "死" or qi["stage"] in ("衰", "墓") else None
    verdict = "不可攻" if attack is False else "敌营不久破/可攻" if attack else "无明确断语"
    return _wrap("T7-04", inputs, {"dashen": qi}, {"can_attack": attack, "verdict": verdict},
                 variants=[{"status": "source_variant", "note": "部分版本囚可攻"}],
                 dashen=qi, verdict=verdict, pending=["休囚待校"] if attack is None else [])


def _mode_b(rule_id, event_name, taiyi, generals):
    inputs = {event_name: taiyi, **generals}
    missing = [k for k, v in inputs.items() if v is None]
    if taiyi is None:
        return inputs, {}, {}, missing, None
    integer(taiyi, 1, 9)
    if taiyi == 5:
        return inputs, {}, {}, missing, "杜塞：中五无大神落辰"
    landing = dashen_from_nine_palace(taiyi)
    qi = _qi(landing)
    states = {}
    for role, palace in generals.items():
        if palace is None:
            states[role] = {"computable": False, "reason": "缺将宫"}
        else:
            states[role] = {**general_palace_qi(palace, landing), "palace": palace,
                            "intrinsic_element": ROLE_ELEMENTS[role], "computable": True}
    environment = {k: qi[k] for k in ("position", "element", "palace")}
    return inputs, states, environment, missing, None


def thunder_in_water(day_taiyi_palace=None, home_general=None, home_assistant=None,
                     away_general=None, away_assistant=None):
    generals = {"home_general": home_general, "home_vassal": home_assistant,
                "away_general": away_general, "away_vassal": away_assistant}
    inputs, states, environment, missing, reason = _mode_b("T7-05", "day_taiyi_palace", day_taiyi_palace, generals)
    for data in states.values():
        if data["computable"]:
            data["death_risk"] = data["state"] == "死"
    return _wrap("T7-05", inputs, {"environment": environment, "generals": states, "model": "B"},
                 {"death_risks": [k for k, d in states.items() if d.get("death_risk")]}, missing, reason,
                 variants=[{"id": "VAR-T7-LS-01", "status": "source_variant",
                            "note": "统宗电子转录太乙6→乾；canonical为6→子"}],
                 environment=environment, generals=states, model="B")


def general_conflict(home_general, away_general, home_vassal=None, *, xing_pairs=None):
    enemy_wx = nine_palace_element(away_general)
    events = []
    for target, palace in (("home_general", home_general), ("home_vassal", home_vassal)):
        if palace is not None and OVERCOMES[enemy_wx] == nine_palace_element(palace):
            events.append({"relation": "克", "target": target})
    if xing_pairs is not None and (away_general, home_general) in xing_pairs:
        events.append({"relation": "刑", "target": "home_general"})
    return {"severe": bool(events), "events": events, "death_risk": bool(events),
            "verdict": "出战必死" if events else None,
            "pending": ["九宫刑关系未标准化"] if xing_pairs is None else []}


def white_dragon(day_taiyi_palace=None, home_general=None, home_assistant=None,
                 away_general=None, away_assistant=None, *, xing_pairs=None):
    generals = {"home_general": home_general, "home_vassal": home_assistant,
                "away_general": away_general, "away_vassal": away_assistant}
    inputs, states, environment, missing, reason = _mode_b("T7-06", "day_taiyi_palace", day_taiyi_palace, generals)
    for data in states.values():
        if data["computable"]:
            data["has_qi"] = data["state"] in ("旺", "相")
            data["deployment_suitable"] = data["has_qi"]
            data["verdict"] = "宜出军/下营/屯军" if data["has_qi"] else "不宜"
    conflicts = {}
    if home_general is not None and away_general is not None:
        conflicts["home"] = general_conflict(home_general, away_general, home_assistant, xing_pairs=xing_pairs)
        conflicts["away"] = general_conflict(away_general, home_general, away_assistant, xing_pairs=xing_pairs)
    return _wrap("T7-06", inputs, {"environment": environment, "generals": states,
                                  "model": "B", "direct_conflict": conflicts},
                 {"deployment": {k: d.get("deployment_suitable") for k, d in states.items()}},
                 missing, reason, environment=environment, generals=states, model="B", conflicts=conflicts)


def return_army(enemy_first_arrival_taiyi_palace=None, home_general=None, away_general=None):
    generals = {"home_general": home_general, "away_general": away_general}
    inputs, states, environment, missing, reason = _mode_b(
        "T7-07", "enemy_first_arrival_taiyi_palace", enemy_first_arrival_taiyi_palace, generals)
    enemy_strong = states.get("away_general", {}).get("state") in ("旺", "相") if away_general is not None and environment else None
    own_strong = states.get("home_general", {}).get("state") in ("旺", "相") if home_general is not None and environment else None
    verdict = "有伏兵须防" if enemy_strong is True else "无伏、自破、可攻" if enemy_strong is False else None
    return _wrap("T7-07", inputs, {"environment": environment, "generals": states, "model": "B"},
                 {"enemy_has_ambush": enemy_strong, "enemy_self_break": enemy_strong is False if enemy_strong is not None else None,
                  "can_attack": not enemy_strong if enemy_strong is not None else None, "own_should_ambush": own_strong},
                 missing, reason, variants=[{"status": "source_variant", "note": "墓/废不并入五态"}],
                 aliases=["回车无言"], environment=environment, generals=states, model="B",
                 enemy_verdict=verdict, home_verdict="宜自设伏" if own_strong else "无明确断语")


def analyze_seven_methods(*, home_general=None, home_assistant=None, away_general=None,
                          away_assistant=None, day_taiyi_palace=None, scenario=None):
    scenario = {} if scenario is None else scenario
    allowed = {"enemy_start_year_branch", "enemy_camp_day_taiyi_palace", "enemy_first_arrival_taiyi_palace"}
    if not isinstance(scenario, dict) or set(scenario) - allowed:
        raise ValueError("未知scenario字段")
    generals = (home_general, home_assistant, away_general, away_assistant)
    return {
        "T7-01": linjin_wendao(scenario.get("enemy_start_year_branch")),
        "T7-02": lion_reverse_throw(scenario.get("enemy_start_year_branch")),
        "T7-03": white_cloud(home_general, away_general),
        "T7-04": fierce_tiger(scenario.get("enemy_camp_day_taiyi_palace")),
        "T7-05": thunder_in_water(day_taiyi_palace, *generals),
        "T7-06": white_dragon(day_taiyi_palace, *generals),
        "T7-07": return_army(scenario.get("enemy_first_arrival_taiyi_palace"), home_general, away_general),
    }


# Legacy names delegate; display projections never become rule sources.
lijin = linjin_wendao
lion = lion_reverse_throw
cloud = white_cloud


def _cloud_general(anchor):
    # Historical API permitted a Sector16 anchor for examining fire stages.
    from .taiyi_common import validate_sector
    if isinstance(anchor, str):
        qi = _qi(dashen_from_sector(validate_sector(anchor)))
        special = qi["stage"] in ("临官", "冠带")
        return {"dashen": qi, "verdict": "善战/精锐" if special else "强" if qi["state"] in ("旺", "相") else "弱败"}
    return _cloud_side(anchor, "home_general")


def tiger(anchor):
    if isinstance(anchor, str):
        from .taiyi_common import validate_sector
        qi = _qi(dashen_from_sector(validate_sector(anchor)))
        verdict = "敌营不久破/可攻" if qi["state"] == "死" or qi["stage"] in ("衰", "墓") else "不可攻" if qi["state"] in ("旺", "相") else "无明确断语"
        return _wrap("T7-04", {"legacy_sector_anchor": anchor}, {"dashen": qi}, {"verdict": verdict}, dashen=qi, verdict=verdict)
    return fierce_tiger(anchor)


def leigong(taiyi, home_general=None, home_vassal=None, away_general=None, away_vassal=None):
    return thunder_in_water(taiyi, home_general, home_vassal, away_general, away_vassal)


def dragon(taiyi, home_general=None, home_vassal=None, away_general=None, away_vassal=None, *, xing_pairs=None):
    data = white_dragon(taiyi, home_general, home_vassal, away_general, away_vassal, xing_pairs=xing_pairs)
    # Retain the old combined display, while analysis retains separate layers.
    import copy
    data["generals"] = copy.deepcopy(data["generals"])
    for side, conflict in data["conflicts"].items():
        if conflict["severe"] and side + "_general" in data["generals"]:
            data["generals"][side + "_general"]["verdict"] = conflict["verdict"]
    return data


def returnarmy(ag_num=None, *, enemy_arrival_taiyi=None, home_general=None, away_general=None):
    if ag_num is not None:
        warnings.warn("returnarmy(away_general)已废弃；须显式提供敌初来时日太乙", DeprecationWarning, stacklevel=2)
    data = return_army(enemy_arrival_taiyi, home_general, away_general if away_general is not None else ag_num)
    if "enemy_first_arrival_taiyi_palace" in data["missing"]:
        data["missing"] = ["enemy_arrival_taiyi" if k == "enemy_first_arrival_taiyi_palace" else k for k in data["missing"]]
    if not data["environment"]:
        data.pop("environment")
    return data
