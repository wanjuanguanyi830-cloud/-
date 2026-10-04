"""Eight independent canonical divinations, consuming only taiyi_common."""
from .taiyi_common import (
    GOD_ALIASES,
    GOD_SECTORS,
    GODS,
    SECTOR_GODS,
    YANG_PALACES,
    YIN_PALACES,
    integer,
    validate_sector,
)

SANCAI_FULL_CLASSIC = frozenset(t * 10 + u for t in (1, 2, 3) for u in (6, 7, 8, 9))
INNER_GODS = frozenset(["阴德", "大义", "地主", "阳德", "和德", "吕申", "高丛", "太阳"])
OUTER_GODS = frozenset(GODS) - INNER_GODS
GUDAN_SETS = {
    "单阳": {1, 3, 7, 9}, "单阴": {2, 4, 6, 8}, "孤阳": {10, 30},
    "孤阴": {20, 40}, "重阳": {11, 13, 17, 19, 31, 33, 37, 39},
    "重阴": {22, 24, 26, 28},
}


def _result(rule_id, **fields):
    return {"id": rule_id, "rule_id": rule_id, "category": "eight_divinations",
            "canonical": "taiyi-t7-d8-v1", "computable": True,
            "missing_inputs": [], "reason": None, **fields}


def calc_components(n):
    integer(n, 1, 40)
    unit = n % 10
    return {"ten": n >= 10, "five": unit >= 5, "one": unit % 5 != 0}


def sancai_analysis(n):
    parts = calc_components(n)
    names = {"ten": "天", "five": "地", "one": "人"}
    missing = [names[k] for k, present in parts.items() if not present]
    tags = []
    if n <= 9:
        tags.append("无天")
    if n % 10 in (1, 2, 3, 4):
        tags.append("无地")
    if n % 10 == 0:
        tags.append("无人")
    if n in SANCAI_FULL_CLASSIC:
        tags.append("三才俱足")
    if n in (5, 15, 25, 35):
        tags.append("杜塞")
    return _result("D8-01", calc=n, components=parts, missing=missing,
                   missing_components=missing, classic_tags=tags,
                   sancai_full_classic=n in SANCAI_FULL_CLASSIC,
                   effects=[{"天": "天象异常", "地": "地灾", "人": "人事疾病迁徙"}[k] for k in missing])


sancai = sancai_analysis


def cal_des(home_cal, away_cal=None, set_cal=None):
    if away_cal is None and set_cal is None:
        return sancai_analysis(home_cal)
    return {name: sancai_analysis(n) for name, n in
            (("home", home_cal), ("away", away_cal), ("set", set_cal)) if n is not None}


def calc_length(n):
    calc_components(n)
    variant = {"id": "VAR-D8-LENGTH-SIKU", "status": "source_ambiguous" if n == 10 else "source_variant",
               "length": "长" if n >= 11 else "短" if n <= 9 else None}
    return _result("D8-02", calc=n, length="长" if n >= 11 else "短",
                   verdict="宜缓、深入" if n >= 11 else "宜急、浅入",
                   source_profile="project_canonical", variants=[variant])


def wuyin_from_calc(n):
    calc_components(n)
    tail = n % 10 or 10
    tone, element, subject = (("宫", "土", "人君"), ("徵", "火", "宗庙"),
                             ("羽", "水", "后妃"), ("商", "金", "子孙"),
                             ("角", "木", "疾病"))[(tail - 1) // 2]
    return _result("D8-03", calc=n, tone=tone, element=element, subject=subject,
                   tone_kind="正音" if tail % 2 else "比音", pending=[],
                   aliases=["太子"] if tone == "商" else [], judges_fortune=False)


def gudan_analysis(n):
    calc_components(n)
    state = next((label for label, values in GUDAN_SETS.items() if n in values), None)
    side = None if state is None else "主" if state.endswith("阳") else "客"
    return _result("D8-04", calc=n, state=state,
                   single=state if state in ("单阳", "单阴") else None,
                   isolated=state if state in ("孤阳", "孤阴") else None,
                   disadvantaged=side,
                   danger="火厄" if state == "重阳" else "水厄" if state == "重阴" else None,
                   basic_effects=[] if state is None else [{"classification": state, "disadvantaged": side}],
                   scope_note="本术无标签不代表全局无不利",
                   pending=["本术无明确标签"] if state is None else [])


gudan_state = gudan_analysis
gudan = gudan_analysis
gudan_zhanlue = gudan_analysis


def neiwai_attack(skyeyes_sector):
    point = validate_sector(skyeyes_sector)
    god = SECTOR_GODS[point]
    realm = "内" if god in INNER_GODS else "外"
    return _result("D8-05", skyeyes=god, sector=point, realm=realm,
                   emptiness="内虚" if realm == "内" else "外孤",
                   attack="外" if realm == "内" else "内",
                   verdict="内虚、宜攻外" if realm == "内" else "外孤、宜攻内")


def attack_realm(skyeyes):
    anchor = GOD_ALIASES.get(skyeyes, skyeyes)
    return neiwai_attack(GOD_SECTORS.get(anchor, anchor))


neiwai_gongji = attack_realm


def calc_amount_victory(home_cal, away_cal):
    calc_components(home_cal)
    calc_components(away_cal)
    winner = "away" if away_cal > home_cal else "home" if away_cal < home_cal else None
    verdict = "主败/客胜" if winner == "away" else "主胜" if winner == "home" else "同数/无明确断语"
    return _result("D8-06", home_cal=home_cal, away_cal=away_cal,
                   winner=winner, status="ok" if winner else "原典未明言",
                   comparison="客多主少" if winner == "away" else "主多客少" if winner == "home" else "同数",
                   base={"home_cal": home_cal, "away_cal": away_cal, "verdict": verdict})


def suenwl(home_cal, away_cal, *, pattern_corrections=None):
    return {**calc_amount_victory(home_cal, away_cal),
            "pattern_corrections": pattern_corrections or [], "corrections_applied": False}


def yinyang_adversity(taiyi, home_cal, away_cal=None):
    integer(taiyi, 1, 9)
    events = []
    for side, n in (("主", home_cal), ("客", away_cal)):
        if n is None:
            continue
        calc_components(n)
        if taiyi in YANG_PALACES and n % 2:
            events.append({"side": side, "state": "重阳", "danger": "厄火"})
        elif taiyi in YIN_PALACES and n % 2 == 0:
            events.append({"side": side, "state": "重阴", "danger": "厄水"})
    return _result("D8-07", taiyi=taiyi, events=events,
                   verdict="无明确断语" if not events else None)


tui_danger = yinyang_adversity


def calc_preparedness(n):
    parts = calc_components(n)
    names = {"ten": "将军", "five": "吏士", "one": "兵卒"}
    return _result("D8-08", calc=n, components=parts,
                   present=[names[k] for k, v in parts.items() if v],
                   missing=[names[k] for k, v in parts.items() if not v],
                   components_all=all(parts.values()),
                   classic_label="将吏兵卒俱备" if n == 17 else None,
                   source_note="十六以上皆具仅保留来源文字，不替代逐项结构计算",
                   pending=[])


def analyze_eight_divinations(taiyi_palace, skyeyes_sector, home_cal, away_cal,
                              source_profile="project_canonical"):
    if source_profile != "project_canonical":
        raise ValueError("未知source_profile；异文须显式选择")
    methods = (
        ("D8-01", lambda n: sancai_analysis(n)),
        ("D8-02", lambda n: calc_length(n)),
        ("D8-03", lambda n: wuyin_from_calc(n)),
        ("D8-04", lambda n: gudan_analysis(n)),
        ("D8-08", lambda n: calc_preparedness(n)),
    )
    def unavailable(rule_id, missing):
        return _result(rule_id, computable=False, missing_inputs=missing, reason="缺八占输入")

    missing_cal = [key for key, n in (("home_cal", home_cal), ("away_cal", away_cal)) if n is None]
    data = {key: _result(key, computable=not missing_cal, missing_inputs=missing_cal,
                        reason="缺八占算数" if missing_cal else None,
                        home=fn(home_cal) if home_cal is not None else unavailable(key, ["home_cal"]),
                        away=fn(away_cal) if away_cal is not None else unavailable(key, ["away_cal"]))
            for key, fn in methods}
    data["D8-05"] = neiwai_attack(skyeyes_sector) if skyeyes_sector is not None else unavailable("D8-05", ["skyeyes_sector"])
    data["D8-06"] = calc_amount_victory(home_cal, away_cal) if not missing_cal else unavailable("D8-06", missing_cal)
    missing_adversity = ["taiyi_palace"] if taiyi_palace is None else []
    missing_adversity += missing_cal
    data["D8-07"] = yinyang_adversity(taiyi_palace, home_cal, away_cal) if not missing_adversity else unavailable("D8-07", missing_adversity)
    return {key: data[key] for key in sorted(data)}
