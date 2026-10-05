"""D8-01..08，独立于七术及卷17动态内外格局。"""

from .taiyi_rules import (GODS, GOD_POSITION, YANG_PALACES, YIN_PALACES,
                          calc_components, integer, position, result)

SANCAI_FULL_CLASSIC = frozenset(t * 10 + u for t in (1, 2, 3) for u in (6, 7, 8, 9))
SANCAI_NO_HEAVEN_CLASSIC = frozenset(range(1, 10))
SANCAI_NO_EARTH_CLASSIC = frozenset(
    t * 10 + u for t in (0, 1, 2, 3) for u in (1, 2, 3, 4)
)
SANCAI_NO_HUMAN_CLASSIC = frozenset((10, 20, 30, 40))
SANCAI_BLOCKED_CLASSIC = frozenset((5, 15, 25, 35))

GUDAN_SINGLE_YANG = frozenset((1, 3, 7, 9))
GUDAN_SINGLE_YIN = frozenset((2, 4, 6, 8))
GUDAN_ISOLATED_YANG = frozenset((10, 30))
GUDAN_ISOLATED_YIN = frozenset((20, 40))
GUDAN_DOUBLE_YANG = frozenset((11, 13, 17, 19, 31, 33, 37, 39))
GUDAN_DOUBLE_YIN = frozenset((22, 24, 26, 28))

INNER_GODS = frozenset("阴德 大义 地主 阳德 和德 吕申 高丛 太阳".split())
OUTER_GODS = frozenset(GODS) - INNER_GODS


def _sancai_classic_tags(n):
    """返回古典标签；与结构缺失字段严格分离。"""
    if n in SANCAI_BLOCKED_CLASSIC:
        return ["杜塞"]
    tags = []
    if n in SANCAI_NO_HEAVEN_CLASSIC:
        tags.append("无天")
    if n in SANCAI_NO_EARTH_CLASSIC:
        tags.append("无地")
    if n in SANCAI_NO_HUMAN_CLASSIC:
        tags.append("无人")
    if n in SANCAI_FULL_CLASSIC:
        tags.append("三才俱足")
    return tags


def sancai(n):
    parts = calc_components(n)
    names = {"ten": "天", "five": "地", "one": "人"}
    structural_missing = [names[k] for k, present in parts.items() if not present]
    classic_tags = _sancai_classic_tags(n)
    return result(
        "D8-01",
        calc=n,
        components=parts,
        structural_missing=structural_missing,
        # 兼容旧消费者；语义等同 structural_missing。
        missing=list(structural_missing),
        classic_tags=classic_tags,
        sancai_full_classic="三才俱足" in classic_tags,
        blocked_classic="杜塞" in classic_tags,
        effects=[
            {"天": "天象异常", "地": "地灾", "人": "人事疾病迁徙"}[k]
            for k in structural_missing
        ],
        policy="结构缺失与古典标签分层；杜塞数不得按结构缺失改写为无天/无人等 classic 标签。",
    )


def cal_des(home_cal, away_cal=None, set_cal=None):
    if away_cal is None and set_cal is None:
        return sancai(home_cal)
    return {name: sancai(n) for name, n in (("home", home_cal), ("away", away_cal), ("set", set_cal)) if n is not None}


def calc_length(n):
    calc_components(n)
    return result("D8-02", calc=n, length="长" if n >= 11 else "短",
                  verdict="宜缓、深入" if n >= 11 else "宜急、浅入", source_profile="统宗")


def wuyin_from_calc(n):
    calc_components(n)
    tail = n % 10 or 10
    tone, element, subject = (("宫", "土", "人君"), ("徵", "火", "宗庙"),
        ("羽", "水", "后妃"), ("商", "金", "子孙"), ("角", "木", "疾病"))[(tail - 1) // 2]
    tone_kind = "正音" if tail % 2 else "比音"
    return result("D8-03", calc=n, tail=tail, tone=tone, element=element, subject=subject,
                  tone_kind=tone_kind, pending=[],
                  policy="尾数0按10；1/3/5/7/9为正音，2/4/6/8/10为比音；五音本身不直接判吉凶。")


def gudan_state(n):
    calc_components(n)

    if n in GUDAN_SINGLE_YANG:
        state, single, isolated = "单阳", "单阳", None
    elif n in GUDAN_SINGLE_YIN:
        state, single, isolated = "单阴", "单阴", None
    elif n in GUDAN_ISOLATED_YANG:
        state, single, isolated = "孤阳", None, "孤阳"
    elif n in GUDAN_ISOLATED_YIN:
        state, single, isolated = "孤阴", None, "孤阴"
    elif n in GUDAN_DOUBLE_YANG:
        state, single, isolated = "重阳", "单阳", "孤阳"
    elif n in GUDAN_DOUBLE_YIN:
        state, single, isolated = "重阴", "单阴", "孤阴"
    else:
        state = single = isolated = None

    disadvantaged = (
        "主" if state in ("单阳", "孤阳", "重阳")
        else "客" if state in ("单阴", "孤阴", "重阴")
        else None
    )
    danger = "火厄" if state == "重阳" else "水厄" if state == "重阴" else None

    if n in SANCAI_BLOCKED_CLASSIC:
        pending = ["杜塞数不强塞孤单分类"]
    elif state is None:
        pending = ["该数不在 canonical 孤单/重阴阳明确数集"]
    else:
        pending = []

    return result(
        "D8-04",
        calc=n,
        single=single,
        isolated=isolated,
        state=state,
        disadvantaged=disadvantaged,
        danger=danger,
        basic_effects=(
            [{"classification": state, "disadvantaged": disadvantaged}]
            if state is not None
            else []
        ),
        blocked=n in SANCAI_BLOCKED_CLASSIC,
        pending=pending,
        policy="孤单按 canonical 明确数集分类；杜塞数与未列混合数不得由十位/尾数分解强行补类。",
    )


def attack_realm(skyeyes):
    point = position(skyeyes)
    god = next(god for god, p in GOD_POSITION.items() if p == point)
    realm = "内" if god in INNER_GODS else "外"
    return result("D8-05", skyeyes=god, realm=realm,
                  verdict="内虚、宜攻外" if realm == "内" else "外孤、宜攻内")


def suenwl(home_cal, away_cal, *, pattern_corrections=None):
    calc_components(home_cal)
    calc_components(away_cal)
    verdict = "主败/客胜" if away_cal > home_cal else "主胜" if away_cal < home_cal else "同数/无明确断语"
    return result("D8-06", base={"home_cal": home_cal, "away_cal": away_cal, "verdict": verdict},
                  pattern_corrections=pattern_corrections or [],
                  corrections_applied=False)


def tui_danger(taiyi, home_cal, away_cal=None):
    integer(taiyi, 1, 9)
    realm = "阳" if taiyi in YANG_PALACES else "阴" if taiyi in YIN_PALACES else None
    events = []

    for side, n in (("主", home_cal), ("客", away_cal)):
        if n is None:
            continue
        calc_components(n)
        if realm == "阳" and n % 2:
            events.append({"side": side, "state": "重阳", "danger": "火厄"})
        elif realm == "阴" and n % 2 == 0:
            events.append({"side": side, "state": "重阴", "danger": "水厄"})

    if taiyi == 5:
        verdict = "中五不参与本术"
    elif not events:
        verdict = "无厄"
    else:
        verdict = None

    return result(
        "D8-07",
        taiyi=taiyi,
        palace_yinyang=realm,
        participates=taiyi != 5,
        events=events,
        verdict=verdict,
        policy="D8-07只看太乙宫阴阳与算数奇偶；与D8-04孤单分类独立。",
    )


def calc_preparedness(n):
    parts = calc_components(n)
    names = {"ten": "将军", "five": "吏士", "one": "兵卒"}
    return result("D8-08", calc=n, components=parts,
                  present=[names[k] for k, v in parts.items() if v],
                  missing=[names[k] for k, v in parts.items() if not v],
                  components_all=all(parts.values()),
                  classic_label="将吏兵卒俱备" if n == 17 else None,
                  pending=[] if n == 17 else ["结构齐备不自动授予古籍俱备标签"])


gudan = gudan_state
gudan_zhanlue = gudan_state
neiwai_gongji = attack_realm
