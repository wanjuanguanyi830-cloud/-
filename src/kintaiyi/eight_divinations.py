"""D8-01..08, kept independent from Seven Methods and dynamic realm rules."""

from .taiyi_rules import (
    GODS, GOD_POSITION, YANG_PALACES, YIN_PALACES,
    calc_components, integer, not_computable, position, result,
)

NO_SKY = frozenset(range(1, 10))
NO_EARTH = frozenset(
    (1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34)
)
NO_HUMAN = frozenset((10, 20, 30, 40))
SANCAI_FULL_CLASSIC = frozenset(
    10 * ten + unit for ten in (1, 2, 3) for unit in (6, 7, 8, 9)
)
DU_SE = frozenset((5, 15, 25, 35))
INNER_GODS = frozenset("阴德 大义 地主 阳德 和德 吕申 高丛 太阳".split())
OUTER_GODS = frozenset(GODS) - INNER_GODS

SINGLE_YANG = frozenset((1, 3, 7, 9))
SINGLE_YIN = frozenset((2, 4, 6, 8))
ISOLATED_YANG = frozenset((10, 30))
ISOLATED_YIN = frozenset((20, 40))
DOUBLE_YANG = frozenset((11, 13, 17, 19, 31, 33, 37, 39))
DOUBLE_YIN = frozenset((22, 24, 26, 28))


def sancai(n=None):
    """D8-01: structural components and classic tags are separate layers."""
    if n is None:
        return not_computable("D8-01", ["calc"], "缺算数")
    parts = calc_components(n)
    names = {"ten": "天", "five": "地", "one": "人"}
    missing = [names[k] for k, present in parts.items() if not present]
    tags = []
    if n in NO_SKY:
        tags.append("无天")
    if n in NO_EARTH:
        tags.append("无地")
    if n in NO_HUMAN:
        tags.append("无人")
    if n in SANCAI_FULL_CLASSIC:
        tags.append("三才俱足")
    if n in DU_SE:
        tags.append("杜塞")
    effects = [
        {"天": "天象异常", "地": "地灾", "人": "人事疾病迁徙"}[name]
        for name in missing
    ]
    return result(
        "D8-01", calc=n, components=parts, missing_components=missing,
        missing=missing, classic_tags=tags,
        sancai_full_classic="三才俱足" in tags, effects=effects,
    )


def cal_des(home_cal, away_cal=None, set_cal=None):
    """Deprecated compatibility wrapper; new code calls each D8 rule directly."""
    if away_cal is None and set_cal is None:
        return sancai(home_cal)
    return {
        name: sancai(n)
        for name, n in (("home", home_cal), ("away", away_cal), ("set", set_cal))
        if n is not None
    }


def calc_length(n=None, *, source_profile="统宗"):
    """D8-02: 11 and above is long; source variants remain descriptive only."""
    if n is None:
        return not_computable("D8-02", ["calc"], "缺算数")
    calc_components(n)
    return result(
        "D8-02", calc=n, length="长" if n >= 11 else "短",
        verdict="缓动、可深入" if n >= 11 else "急动、不宜深入",
        source_profile=source_profile,
        source_variants=["四库异文：十一以上长，单九以下短"],
    )


def wuyin_from_calc(n=None):
    """D8-03: last digit selects the topic; it does not independently judge luck."""
    if n is None:
        return not_computable("D8-03", ["calc"], "缺算数")
    calc_components(n)
    tail = n % 10 or 10
    pair_index = (tail - 1) // 2
    tone, element, first_subject, second_subject = (
        ("宫", "土", "人君", "人君"),
        ("徵", "火", "宗庙", "宗庙"),
        ("羽", "水", "后妃", "后妃"),
        ("商", "金", "子孙", "太子"),
        ("角", "木", "疾病", "疾病"),
    )[pair_index]
    tone_kind = "正音" if tail % 2 else "比音"
    return result(
        "D8-03", calc=n, last_digit=tail, tone=tone,
        element=element,
        subject=first_subject if tone_kind == "正音" else second_subject,
        tone_kind=tone_kind, verdict="只定位所主，不单独判凶",
    )


def gudan_state(n=None):
    """D8-04: explicit number sets only; mixed values gain no global verdict."""
    if n is None:
        return not_computable("D8-04", ["calc"], "缺算数")
    calc_components(n)
    if n in DOUBLE_YANG:
        state = "重阳"
    elif n in DOUBLE_YIN:
        state = "重阴"
    elif n in SINGLE_YANG:
        state = "单阳"
    elif n in SINGLE_YIN:
        state = "单阴"
    elif n in ISOLATED_YANG:
        state = "孤阳"
    elif n in ISOLATED_YIN:
        state = "孤阴"
    else:
        state = None
    disadvantaged = "主" if state in ("单阳", "孤阳", "重阳") else (
        "客" if state in ("单阴", "孤阴", "重阴") else None
    )
    danger = "火厄" if state == "重阳" else "水厄" if state == "重阴" else None
    tags = [state] if state else []
    if n in DU_SE:
        tags = ["杜塞"]
    return result(
        "D8-04", calc=n, state=state, classic_tags=tags,
        disadvantaged=disadvantaged, danger=danger,
        pending=[] if state or n in DU_SE else ["本术未给该算值单独标签，不推全局无不利"],
    )


def attack_realm(skyeyes=None):
    """D8-05: fixed inner/outer sets, independent from Taiyi's moving palace."""
    if skyeyes is None:
        return not_computable("D8-05", ["skyeyes"], "缺天目")
    point = position(skyeyes)
    god = next(god for god, sector in GOD_POSITION.items() if sector == point)
    realm = "内" if god in INNER_GODS else "外"
    return result(
        "D8-05", skyeyes=god, sector=point, realm=realm,
        verdict="内虚、攻外" if realm == "内" else "外孤、攻内",
        inner_gods=sorted(INNER_GODS), outer_gods=sorted(OUTER_GODS),
    )


def suenwl(home_cal=None, away_cal=None, *, pattern_corrections=None):
    """D8-06: compare only the two numbers; equal is explicitly unresolved."""
    missing = [name for name, value in (("home_cal", home_cal), ("away_cal", away_cal))
               if value is None]
    if missing:
        return not_computable("D8-06", missing, "缺主客算")
    calc_components(home_cal)
    calc_components(away_cal)
    if away_cal > home_cal:
        winner, status, verdict = "away", "resolved", "客胜"
    elif away_cal < home_cal:
        winner, status, verdict = "home", "resolved", "主胜"
    else:
        winner, status, verdict = None, "original_unclear", "原典未明言"
    return result(
        "D8-06",
        base={"home_cal": home_cal, "away_cal": away_cal,
              "winner": winner, "status": status, "verdict": verdict},
        winner=winner, status=status, verdict=verdict,
        pattern_corrections=pattern_corrections or [],
        corrections_applied=False,
    )


def tui_danger(taiyi=None, home_cal=None, away_cal=None):
    """D8-07: palace yin/yang and each side's parity are evaluated independently."""
    missing = [name for name, value in (("taiyi_nine_palace", taiyi), ("home_cal", home_cal))
               if value is None]
    if missing:
        return not_computable("D8-07", missing, "缺太乙九宫或主算")
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
    return result(
        "D8-07", taiyi_nine_palace=taiyi, events=events,
        status="adversity_found" if events else "no_adversity",
        verdict=None if events else "本术无此厄",
    )


def calc_preparedness(n=None):
    """D8-08: role presence reuses D8-01 components, without a forced classic label."""
    if n is None:
        return not_computable("D8-08", ["calc"], "缺算数")
    parts = calc_components(n)
    names = {"ten": "将军", "five": "吏士", "one": "兵卒"}
    present = [names[k] for k, value in parts.items() if value]
    missing = [names[k] for k, value in parts.items() if not value]
    return result(
        "D8-08", calc=n, components=parts,
        present=present, missing=missing, missing_components=missing,
        components_all=all(parts.values()),
        source_note="金镜有‘十六以上皆具’说法；本函数按十/五/一结构计算，不按n>=16强制俱备",
    )


gudan = gudan_state
gudan_zhanlue = gudan_state
neiwai_gongji = attack_realm
