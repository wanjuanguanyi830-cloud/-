"""T7-01..07；大神自身气势(A)与将帅乘气(B)分开计算。"""

from .taiyi_rules import (BRANCHES, STEMS, CORNER_SECTORS, CONTROLS,
    dashen_from_lushen, dashen_qi, palace_element, qi_state, result, sexagenary_year)


def lijin(enemy_start_year):
    _, branch = sexagenary_year(enemy_start_year)
    chain = [branch]
    for _ in range(4):
        chain.append(dashen_from_lushen(chain[-1]))
    return result("T7-01", chain=chain, break_year_branch=chain[1],
                  break_month_branch=chain[2], break_day_branch=chain[3],
                  break_hour_branch=chain[4],
                  source_example_note="甲子古例破年丁卯、五月午；年干与月数仅存古例，不推为通用规则")


def lion(enemy_start_year):
    """T7-02 狮子反掷。

    《统宗》与《金钥匙》明言大神所临为破年；若落四维之方，则改用
    第十八年。十六环顺四格使普通情形只落子卯午酉四正，对应起兵年
    后第三年（含起年为第4年）；四维情形按古例取 +17。
    """
    cycle_index, branch = sexagenary_year(enemy_start_year)
    qi = dashen_qi(branch)
    sector = next(
        (s for s, points in CORNER_SECTORS.items() if qi["position"] in points),
        None,
    )
    offset = 17 if sector else 3
    year_number = offset + 1
    break_year_branch = BRANCHES[(BRANCHES.index(branch) + offset) % 12]
    year = (
        None
        if cycle_index is None
        else STEMS[(cycle_index + offset) % 10] + break_year_branch
    )
    return result(
        "T7-02",
        dashen=qi,
        verdict="不破" if qi["state"] in ("旺", "相") else "合破",
        timing={
            "mode": "corner_18_year" if sector else "direct_break_year",
            "source_marker": qi["position"],
            "sector": sector,
            "year_number": year_number,
            "offset": offset,
            "year": year,
            "break_year_branch": break_year_branch,
            # compatibility alias kept for older callers that consumed branch only
            "candidate_branch": break_year_branch if sector is None else None,
            "year_resolution": (
                "full_ganzhi"
                if cycle_index is not None
                else "branch_only_input_no_stem"
            ),
        },
        pending=[],
        source_variants=[
            "相关版本墓为易破",
            "《太乙金钥匙》补充：起兵年太乙杜塞则当年破；未并入四库canonical普通应期算法",
        ],
        collation_record="sources/t7-02-lion-collation.md",
    )

def _cloud_general(palace):
    qi = dashen_qi(palace)
    if qi["stage"] == "帝旺":
        verdict = "不可触犯"
    elif qi["stage"] in ("临官", "冠带"):
        verdict = "善战/精锐"
    elif qi["stage"] == "墓" or qi["state"] in ("休", "囚", "死"):
        verdict = "弱败"
    else:
        verdict = "强"
    return {"general_palace": palace, "dashen": qi, "verdict": verdict}


def cloud(home_general, away_general=None):
    if away_general is None:
        return result("T7-03", status="not_computable", missing=["away_general"])
    return result("T7-03", home=_cloud_general(home_general), away=_cloud_general(away_general))


def tiger(taiyi):
    qi = dashen_qi(taiyi)
    if qi["stage"] in ("衰", "死", "墓") or qi["state"] == "死":
        verdict = "敌营不久破/可攻"
    elif qi["state"] in ("旺", "相"):
        verdict = "不可攻"
    else:
        verdict = "无明确断语"
    return result("T7-04", dashen=qi, verdict=verdict,
                  source_variants=["部分版本囚可攻"],
                  pending=["五态休、囚的其他组合不自动归入可攻"] if verdict == "无明确断语" else [])


def _generals(taiyi, home_general, home_vassal, away_general, away_vassal):
    qi = dashen_qi(taiyi)
    generals = {}
    for name, palace in (("home_general", home_general), ("home_vassal", home_vassal),
                         ("away_general", away_general), ("away_vassal", away_vassal)):
        generals[name] = {"palace": palace, "state": qi_state(palace_element(palace), qi["element"])} if palace is not None else {"status": "not_computable"}
    # Model B deliberately excludes the fire subject/state used by model A.
    return {"environment": {k: qi[k] for k in ("position", "element", "palace")},
            "model": "B", "generals": generals,
            "missing": [name for name, data in generals.items() if "state" not in data]}


def leigong(taiyi, home_general=None, home_vassal=None, away_general=None, away_vassal=None):
    return result("T7-05", **_generals(taiyi, home_general, home_vassal, away_general, away_vassal))


def general_conflict(home_general, away_general, home_vassal=None, *, xing_pairs=None):
    """T7-06 canonical only executes the source-supported five-element 克 relation.

    xing_pairs is retained as an explicit compatibility extension. The three
    checked witnesses do not supply an independent general-palace 刑 mapping, and
    the Siku parallel clause abbreviates the small-general case to 克. Therefore
    caller-supplied 刑 pairs are reported separately and never alter the canonical
    severe/verdict fields.
    """
    enemy_wx = palace_element(away_general)
    events = []
    external_xing_events = []
    targets = (("home_general", home_general), ("home_vassal", home_vassal))
    for target, palace in targets:
        if palace is not None and CONTROLS[enemy_wx] == palace_element(palace):
            events.append({"relation": "克", "target": target})
        if (
            palace is not None
            and xing_pairs is not None
            and (away_general, palace) in xing_pairs
        ):
            external_xing_events.append({
                "relation": "刑",
                "target": target,
                "source_role": "explicit_external_extension",
            })
    return {
        "severe": bool(events),
        "events": events,
        "verdict": "出战必死" if events else None,
        "canonical_relation": "五行克",
        "xing_evidence_status": (
            "explicit_external_extension_not_canonical"
            if xing_pairs is not None
            else "no_independent_xing_operator_from_source"
        ),
        "external_xing_events": external_xing_events,
        "external_extension_severe": bool(external_xing_events),
        "pending": [],
        "source_interpretation": (
            "三源均无独立将宫刑表；四库本大将句用‘刑克’，"
            "平行小将句简作‘克小将亦然’，故canonical仅执行九宫五行克。"
        ),
        "collation_record": "sources/t7-06-white-dragon-xing-collation.md",
    }

def dragon(taiyi, home_general=None, home_vassal=None, away_general=None, away_vassal=None, *, xing_pairs=None):
    data = _generals(taiyi, home_general, home_vassal, away_general, away_vassal)
    for general in data["generals"].values():
        if "state" in general:
            general["has_qi"] = general["state"] in ("旺", "相")
            general["verdict"] = "宜出军/下营/屯军" if general["has_qi"] else "不宜"
    conflicts = {}
    if home_general is not None and away_general is not None:
        conflicts["home"] = general_conflict(home_general, away_general, home_vassal, xing_pairs=xing_pairs)
        conflicts["away"] = general_conflict(away_general, home_general, away_vassal, xing_pairs=xing_pairs)
        for side, conflict in conflicts.items():
            if conflict["severe"]:
                data["generals"][side + "_general"]["verdict"] = conflict["verdict"]
    return result("T7-06", **data, conflicts=conflicts, priority="五行克严重条件优先于乘气；外部刑扩展不改写canonical判定")


def returnarmy(ag_num=None, *, enemy_arrival_taiyi=None, home_general=None, away_general=None):
    """旧单参数 ag_num 仅视作客将；绝不代替敌初来太乙。"""
    if away_general is None:
        away_general = ag_num
    missing = [name for name, value in (("enemy_arrival_taiyi", enemy_arrival_taiyi),
               ("home_general", home_general), ("away_general", away_general)) if value is None]
    if missing:
        return result("T7-07", name="回军无言", aliases=["回车无言"], status="not_computable", missing=missing)
    data = _generals(enemy_arrival_taiyi, home_general, None, away_general, None)
    data.pop("missing")
    data["generals"] = {k: v for k, v in data["generals"].items() if k.endswith("general")}
    enemy_qi = data["generals"]["away_general"]["state"] in ("旺", "相")
    return result("T7-07", name="回军无言", aliases=["回车无言"], status="ok", **data,
                  enemy_verdict="有伏兵须防" if enemy_qi else "无伏、自破、可攻",
                  home_verdict="宜自设伏" if data["generals"]["home_general"]["state"] in ("旺", "相") else "无明确断语",
                  source_variants=["四库囚死休废", "其他本休囚死墓"])
