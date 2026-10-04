"""T7-01..07: five-state qi (A/B) and stage interpretations stay separate."""

from .taiyi_rules import (
    BRANCHES, STEMS, CORNER_SECTORS, CONTROLS, GENERAL_INTRINSIC_WX, GENERAL_NAME_ALIASES,
    dashen_from_sector, dashen_qi_from_nine_palace, dashen_qi_from_sector,
    integer, not_computable, palace_element, qi_relation, result,
    sexagenary_year,
)


def lijin(enemy_start_year=None):
    """T7-01: four consecutive Lüshen additions produce year/month/day/hour."""
    if enemy_start_year is None:
        return not_computable("T7-01", ["enemy_start_year"], "缺敌军起兵年支")
    _, branch = sexagenary_year(enemy_start_year)
    chain = [branch]
    for _ in range(4):
        chain.append(dashen_from_sector(chain[-1]))
    return result("T7-01", chain=chain, break_year_branch=chain[1],
                  break_month_branch=chain[2], break_day_branch=chain[3],
                  break_hour_branch=chain[4],
                  source_example_note="甲子古例破年丁卯、五月午；年干与月数仅存古例，不推为通用规则")


def lion(enemy_start_year=None):
    """T7-02: calculate the 16-sector Great God, then test Mode A."""
    if enemy_start_year is None:
        return not_computable("T7-02", ["enemy_start_year"], "缺敌军起兵年支")
    cycle_index, branch = sexagenary_year(enemy_start_year)
    qi = dashen_qi_from_sector(branch)
    sector = next((name for name, points in CORNER_SECTORS.items()
                   if qi["sector"] in points), None)
    year_number = 18 if sector else None
    offset = 17 if sector else None
    year = (None if cycle_index is None or offset is None else
            STEMS[(cycle_index + offset) % 10] + BRANCHES[(cycle_index + offset) % 12])
    return result("T7-02", dashen=qi,
                  verdict="不破" if qi["state"] in ("旺", "相") else "合破",
                  break_predicate=qi["state"] not in ("旺", "相"),
                  timing={"sector": sector, "corner_sector": sector,
                          "sector_type": "four_dimensional" if sector else None,
                          "year_number": year_number, "offset": offset, "year": year,
                          "candidate_branch": qi["sector"] if sector is None else None},
                  source_variants=["普通支的应期候选仅作派生；墓/废差异保留来源层"],
                  pending=[] if sector else ["普通落支应期缺第二古籍实例"])


def _cloud_general(palace, side="主"):
    """Internal T7-03 evaluator. Stage advice never overwrites Mode A qi."""
    if palace is None:
        name = "home_general" if side == "主" else "away_general"
        return not_computable("T7-03", [name], "缺大将九宫")
    try:
        qi = dashen_qi_from_nine_palace(integer(palace, 1, 9))
    except (TypeError, ValueError) as exc:
        if palace == 5:
            return not_computable("T7-03", ["sixteen_sector_for_palace_5"],
                                  "中五无十六辰对应；杜塞，不强行映射",
                                  general_palace=5, verdict=None, classic_note="杜塞")
        raise exc
    strong = qi["state"] in ("旺", "相")
    special_stage = {
        "帝旺": "不可触犯",
        "临官": "善战/精锐",
        "冠带": "善战/精锐",
    }.get(qi["stage"])
    return {
        "computable": True,
        "general_palace": palace,
        "dashen": qi,
        "qi_strength": "强" if strong else "弱",
        "outcome": f"{side}胜" if strong else f"{side}败",
        "verdict": f"{side}胜" if strong else f"{side}败",
        "stage_advice": special_stage,
        "stage_profile": "项目canonical倾向善战；帝旺不可触犯",
        "source_variants": ["四库：冠带士卒战死", "景祐：临官冠带士卒战善"]
        if qi["stage"] in ("临官", "冠带") else [],
    }


def cloud(home_general=None, away_general=None):
    """T7-03: input each general's 9-palace, not intrinsic five-element."""
    missing = ["away_general"] if away_general is None else []
    home = _cloud_general(home_general, "主")
    away = _cloud_general(away_general, "客") if away_general is not None else None
    missing.extend(f"home:{x}" for x in home.get("missing_inputs", []))
    if away:
        missing.extend(f"away:{x}" for x in away.get("missing_inputs", []))
    computable = away is not None and home.get("computable", True) and away.get("computable", True)
    return result("T7-03", computable=computable,
                  status="ok" if computable else "not_computable",
                  missing_inputs=missing, missing=missing,
                  reason=None if computable else "须提供可计算的主客大将九宫；中五无十六辰对应",
                  home=home, away=away)


def tiger(enemy_camp_day_taiyi=None):
    """T7-04: input is the Taiyi 9-palace on the day the enemy camped."""
    if enemy_camp_day_taiyi is None:
        return not_computable("T7-04", ["enemy_camp_day_taiyi"], "缺敌军下营日太乙九宫")
    try:
        qi = dashen_qi_from_nine_palace(integer(enemy_camp_day_taiyi, 1, 9))
    except (TypeError, ValueError):
        if enemy_camp_day_taiyi == 5:
            return not_computable("T7-04", ["enemy_camp_day_taiyi_sector"],
                                  "中五无十六辰对应；杜塞，不强行映射")
        raise
    if qi["stage"] in ("衰", "死", "墓") or qi["state"] == "死":
        verdict = "可攻"
    elif qi["state"] in ("旺", "相"):
        verdict = "不可攻"
    else:
        verdict = "原典未明言"
    return result("T7-04", enemy_camp_day_taiyi=enemy_camp_day_taiyi,
                  dashen=qi, verdict=verdict, attackable=verdict == "可攻",
                  source_variants=["部分版本囚可攻"],
                  pending=["五态休、囚的其他组合无明确断语"] if verdict == "原典未明言" else [])


def _generals(taiyi, home_general, home_vassal, away_general, away_vassal, *,
              required=("home_general", "home_assistant", "away_general", "away_assistant"),
              mound_blocks_suitability=False):
    """Mode B: subject is a general's current palace element."""
    try:
        environment = dashen_qi_from_nine_palace(integer(taiyi, 1, 9))
    except (TypeError, ValueError):
        if taiyi is None:
            blocked = not_computable("T7-05", ["taiyi_nine_palace"], "缺太乙九宫")
            return {key: value for key, value in blocked.items()
                    if key not in ("rule_id", "category", "canonical")}
        if taiyi == 5:
            blocked = not_computable("T7-05", ["sixteen_sector_for_palace_5"],
                                      "太乙中五没有十六辰对应；大神不可强行映射")
            return {key: value for key, value in blocked.items()
                    if key not in ("rule_id", "category", "canonical")}
        raise

    general_values = (
        ("home_general", home_general), ("home_assistant", home_vassal),
        ("away_general", away_general), ("away_assistant", away_vassal),
    )
    generals = {}
    missing = []
    for raw_name, palace in general_values:
        name = GENERAL_NAME_ALIASES.get(raw_name, raw_name)
        if palace is None:
            generals[name] = {"computable": False, "palace_id": None,
                              "intrinsic_element": GENERAL_INTRINSIC_WX[name],
                              "palace_element": None, "status": "not_computable"}
            if name in required:
                missing.append(name)
            continue
        palace_id = integer(palace, 1, 9)
        element = palace_element(palace_id)
        state = qi_relation(element, environment["sector_element"])
        has_qi = state in ("旺", "相")
        suitable = has_qi and not (mound_blocks_suitability and environment["stage"] == "墓")
        generals[name] = {
            "computable": True,
            "palace_id": palace_id,
            "intrinsic_element": GENERAL_INTRINSIC_WX[name],
            "palace_element": element,
            "state": state,
            "has_qi": state in ("旺", "相"),
            "military_suitable": suitable,
            "verdict": "宜出军/下营" if suitable else "不宜出军/下营",
            "death_risk": state == "死",
        }
    return {
        "computable": not missing,
        "status": "ok" if not missing else "not_computable",
        "environment": {
            "position": environment["position"],
            "element": environment["element"],
            **{k: environment[k] for k in
               ("sector", "sector_element", "nine_palace", "nine_palace_element", "stage")},
        },
        "model": "B",
        "generals": generals,
        "missing_inputs": missing,
        "missing": missing,
    }


def leigong(taiyi=None, home_general=None, home_vassal=None, away_general=None, away_vassal=None):
    """T7-05: four separate Mode B qi readings; death risk is state 死."""
    data = _generals(taiyi, home_general, home_vassal, away_general, away_vassal)
    return result("T7-05", **data)


def general_conflict(home_general, away_general, home_vassal=None, *, xing_pairs=None):
    """Direct conflict layer, separate from Mode B乘气."""
    enemy_wx = palace_element(integer(away_general, 1, 9))
    events = []
    for target, palace in (("home_general", home_general), ("home_assistant", home_vassal)):
        if palace is not None and CONTROLS[enemy_wx] == palace_element(integer(palace, 1, 9)):
            events.append({"relation": "克", "target": target})
        if (target == "home_general" and xing_pairs is not None
                and (away_general, home_general) in xing_pairs):
            events.append({"relation": "刑", "target": target})
    return {
        "computable": True,
        "severe": bool(events),
        "death_risk": bool(events),
        "events": events,
        "verdict": "出战有死亡风险" if events else None,
        "pending": ["将宫刑关系表待校；未提供时仅计算克"] if xing_pairs is None else [],
    }


def dragon(taiyi=None, home_general=None, home_vassal=None, away_general=None, away_vassal=None, *, xing_pairs=None):
    """T7-06: Mode B suitability and direct conflict remain independent layers."""
    data = _generals(taiyi, home_general, home_vassal, away_general, away_vassal,
                     mound_blocks_suitability=True)
    direct_conflict = {}
    if home_general is not None and away_general is not None:
        direct_conflict["home"] = general_conflict(
            home_general, away_general, home_vassal, xing_pairs=xing_pairs)
        direct_conflict["away"] = general_conflict(
            away_general, home_general, away_vassal, xing_pairs=xing_pairs)
    return result("T7-06", **data, direct_conflict=direct_conflict,
                  conflicts=direct_conflict,
                  source_variants=["刑表未校时仅报告五行克，不合并进乘气层"])


def returnarmy(ag_num=None, *, enemy_arrival_taiyi=None, home_general=None, away_general=None):
    """T7-07: ag_num remains an away-general compatibility alias only."""
    if away_general is None:
        away_general = ag_num
    missing = [name for name, value in (
        ("enemy_arrival_taiyi", enemy_arrival_taiyi),
        ("home_general", home_general),
        ("away_general", away_general),
    ) if value is None]
    if missing:
        return not_computable("T7-07", missing,
                              "必须输入敌军初来时日太乙九宫及双方大将")
    try:
        data = _generals(enemy_arrival_taiyi, home_general, None, away_general, None,
                         required=("home_general", "away_general"))
    except (TypeError, ValueError):
        if enemy_arrival_taiyi == 5:
            return not_computable("T7-07", ["enemy_arrival_taiyi_sector"],
                                  "敌军初来太乙中五没有十六辰对应")
        raise
    if not data.get("computable"):
        return not_computable("T7-07", data.get("missing_inputs", []),
                              "大神或双方将宫输入不可计算", environment=data.get("environment"))
    enemy_has_qi = data["generals"]["away_general"]["state"] in ("旺", "相")
    home_has_qi = data["generals"]["home_general"]["state"] in ("旺", "相")
    return result("T7-07", name="回军无言", aliases=["回车无言"],
                  enemy_arrival_taiyi=enemy_arrival_taiyi,
                  environment=data["environment"], model="B",
                  generals={k: v for k, v in data["generals"].items()
                            if k in ("home_general", "away_general")},
                  enemy_verdict="有伏兵须防" if enemy_has_qi else "无伏兵、自破、可攻",
                  home_verdict="本军宜伏" if home_has_qi else "原典未明言",
                  source_variants=["四库囚死休废", "其他本休囚死墓"])


# Historical callable names are retained as wrappers above.
