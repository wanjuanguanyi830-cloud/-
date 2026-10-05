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

INNER_GODS = frozenset("阴德 大义 地主 阳德 和德 吕申 高丛 太阳".split())
OUTER_GODS = frozenset(GODS) - INNER_GODS


def _sancai_classic_tags(n):
    """返回古典标签；与结构缺失字段严格分离。"""
    tags = []
    if n in SANCAI_NO_HEAVEN_CLASSIC:
        tags.append("无天")
    if n in SANCAI_NO_EARTH_CLASSIC:
        tags.append("无地")
    if n in SANCAI_NO_HUMAN_CLASSIC:
        tags.append("无人")
    if n in SANCAI_FULL_CLASSIC:
        tags.append("三才俱足")
    if n in SANCAI_BLOCKED_CLASSIC:
        tags.append("杜塞")
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
    unit = n % 10
    single = "单阳" if unit in (1, 3, 7, 9) else "单阴" if unit in (2, 4, 6, 8) else None
    # Decimal tens component is the isolated number: 13 = 10 + 3.
    isolated = "孤阳" if n - unit in (10, 30) else "孤阴" if n - unit in (20, 40) else None
    state = "重阳" if (isolated, single) == ("孤阳", "单阳") else "重阴" if (isolated, single) == ("孤阴", "单阴") else isolated if unit == 0 else single if isolated is None else None
    basic_effects = [{"classification": label, "disadvantaged": "主" if label.endswith("阳") else "客"}
                     for label in (isolated, single) if label is not None]
    return result("D8-04", calc=n, single=single, isolated=isolated, state=state,
                  basic_effects=basic_effects,
                  disadvantaged="主" if state in ("单阳", "孤阳", "重阳") else "客" if state in ("单阴", "孤阴", "重阴") else None,
                  danger="火厄" if state == "重阳" else "水厄" if state == "重阴" else None,
                  pending=["尾数5及混合孤单组合无新增断语"] if state is None else [])


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
    events = []
    for side, n in (("主", home_cal), ("客", away_cal)):
        if n is None:
            continue
        calc_components(n)
        if taiyi in YANG_PALACES and n % 2:
            events.append({"side": side, "state": "重阳", "danger": "厄火"})
        elif taiyi in YIN_PALACES and n % 2 == 0:
            events.append({"side": side, "state": "重阴", "danger": "厄水"})
    return result("D8-07", taiyi=taiyi, events=events, verdict="无明确断语" if not events else None)


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
