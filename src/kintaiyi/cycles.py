"""Three bases, Five Blessings, Great/Small Wander, and Four Taiyi cycles."""

from .taiyi_rules import (
    BRANCHES, GOD_POSITION, integer, not_computable, result,
)

WUFU_PATH = (1, 3, 9, 7, 5)
WUFU_NAMES = ("乾黄秘", "艮黄始", "巽黄室", "坤黄庭", "中玄室")
WUFU_DOMAINS = {
    "乾": frozenset("戌乾亥"),
    "艮": frozenset("丑艮寅"),
    "巽": frozenset("辰巽巳"),
    "坤": frozenset("未坤申"),
    "中": frozenset("子午卯酉"),
}
WUFU_PALACE_NAMES = dict(zip(WUFU_PATH, WUFU_NAMES))
DAYOU_PATH = (7, 8, 9, 1, 2, 3, 4, 6)
DAYOU_TAOJIN_PATH = (7, 6, 4, 3, 2, 1, 9, 8)
SMALL_WANDER_PATH = (1, 2, 3, 4, 6, 7, 8, 9)
DAYOU_TM_PATH = tuple(
    "天道 大武 大武 武德 太簇 阴主 阴德 阴德 大义 地主 阳德 和德 吕申 高丛 太阳 大炅 大神 大威".split()
)
NUMBER_SUBJECTS = ("士卒", "君王", "王侯臣宰", "后妃", "太子",
                   "民庶", "师帅", "上将军", "中将军", "下将军")
WUFU_PROFILES = {
    "project": {"offset": 250, "source": "项目canonical"},
    "source_115": {"offset": 115, "source": "文献+115，仅source profile"},
}
DAYOU_PROFILES = {
    "jinjing_tongzong": {
        "path": DAYOU_PATH, "offset": 34, "source": "金镜/统宗宫序；宫盈差34",
    },
    "taojin": {
        "path": DAYOU_TAOJIN_PATH, "offset": None, "source": "淘金歌宫序；历元盈差未确认",
    },
}
TM_PROFILES = {
    "tongzong": {"offset": 214, "outer_cycle": 180, "source": "统宗/易学象数"},
    "jinjing": {"offset": None, "yuan": 72, "core_cycle": 18,
                 "source": "金镜元法72/周法18；历元盈差未确认"},
}
BASE_SPECS = {
    "jun_ji": {"name": "君基", "start": "午", "stay": 30, "cycle": 360, "outer_cycle": 3600},
    "chen_ji": {"name": "臣基", "start": "午", "stay": 3, "cycle": 36, "outer_cycle": 360},
    "min_ji": {"name": "民基", "start": "戌", "stay": 1, "cycle": 12, "outer_cycle": 360},
}

FOUR_TAIYI_START = {"四神": 1, "天乙": 6, "地乙": 9, "直符": 5}
FOUR_TAIYI_PALACES = {
    1: {"palace_name": "乾", "sector": "乾", "element": "金"},
    2: {"palace_name": "离", "sector": "午", "element": "火"},
    3: {"palace_name": "艮", "sector": "艮", "element": "土"},
    4: {"palace_name": "震", "sector": "卯", "element": "木"},
    5: {"palace_name": "中", "sector": None, "element": "土"},
    6: {"palace_name": "兑", "sector": "酉", "element": "金"},
    7: {"palace_name": "坤", "sector": "坤", "element": "土"},
    8: {"palace_name": "坎", "sector": "子", "element": "水"},
    9: {"palace_name": "巽", "sector": "巽", "element": "木"},
    10: {"palace_name": "绛宫", "sector": "巳", "element": "火"},
    11: {"palace_name": "明堂", "sector": "申", "element": "金"},
    12: {"palace_name": "玉堂", "sector": "寅", "element": "木"},
}
FOUR_TAIYI_PAIRS = (
    ("天乙", "地乙"), ("天乙", "直符"), ("天乙", "四神"),
    ("地乙", "直符"), ("地乙", "四神"), ("直符", "四神"),
)


def _number_subject(year_number, maximum):
    integer(year_number, 1, maximum)
    return NUMBER_SUBJECTS[year_number % 10]


def wufu_gb(year_in_palace):
    """吉算是当前入宫第几年；不读取主算或客算。"""
    return _number_subject(year_in_palace, 45)


def wufu(accumulated_year=None, *, profile="project"):
    """R-WF: 1-based year formula; 45 years per domain, 225-year period."""
    if accumulated_year is None:
        return not_computable("R-WF", ["accumulated_year"], "缺历元累计年", profile=profile)
    integer(accumulated_year)
    spec = WUFU_PROFILES[profile]
    relative = (accumulated_year + spec["offset"] - 1) % 225 + 1
    index = (relative - 1) // 45
    palace_id = WUFU_PATH[index]
    name = WUFU_PALACE_NAMES[palace_id]
    year = (relative - 1) % 45 + 1
    domain = name[0]
    return result(
        "R-WF", canonical="taiyi-cycles-v2", coordinate="wufu_domain", profile=profile,
        source=spec["source"], offset=spec["offset"], accumulated_year=accumulated_year,
        cycle_index=relative - 1, relative_year=relative,
        palace_id=palace_id, palace=palace_id, palace_name=name,
        domain=domain, domain_sectors=sorted(WUFU_DOMAINS[domain]),
        year_in_palace=year,
        realm=("理天", "理地", "理人")[(year - 1) // 15],
        auspicious_subject=wufu_gb(year),
        source_variants=["文献+115偏移保留为source_115 profile"],
    )


def dayou_xiong(year_in_palace):
    """大游凶算：入宫年末位对应十类，不沿用旧六类。"""
    return _number_subject(year_in_palace, 36)


def bigyo(accumulated_year=None, *, profile="jinjing_tongzong", epoch_offset=None):
    """R-DY: 8-palace route, 36 years per palace, 288-year period."""
    if accumulated_year is None:
        return not_computable("R-DY", ["accumulated_year"], "缺历元累计年", profile=profile)
    integer(accumulated_year)
    spec = DAYOU_PROFILES[profile]
    offset = spec["offset"] if epoch_offset is None else integer(epoch_offset)
    if offset is None:
        return not_computable("R-DY", ["epoch_offset"],
                              "该profile历元盈差未确认；须显式提供epoch_offset",
                              canonical="taiyi-cycles-v2", profile=profile)
    relative = (accumulated_year + offset - 1) % 288 + 1
    index = (relative - 1) // 36
    year = (relative - 1) % 36 + 1
    palace_id = spec["path"][index]
    return result(
        "R-DY", canonical="taiyi-cycles-v2", coordinate="nine_palace", profile=profile,
        source=spec["source"], offset=offset, accumulated_year=accumulated_year,
        cycle_index=relative - 1,
        relative_year=relative, palace_id=palace_id, palace=palace_id,
        year_in_palace=year,
        realm=("治天", "治地", "治人")[(year - 1) // 12],
        inauspicious_subject=dayou_xiong(year),
        source_variants=["淘金歌反向宫序保留为taojin profile"],
    )


def bigyo_tianmu(accumulated_year=None, *, profile="tongzong", epoch_offset=None):
    """R-DY-TM: 18-step god sequence with explicit source offset profiles."""
    if accumulated_year is None:
        return not_computable("R-DY-TM", ["accumulated_year"], "缺历元累计年", profile=profile)
    integer(accumulated_year)
    spec = TM_PROFILES[profile]
    offset = spec["offset"] if epoch_offset is None else integer(epoch_offset)
    if offset is None:
        return not_computable("R-DY-TM", ["epoch_offset"],
                              "金镜历元盈差待校；须显式提供epoch_offset",
                              canonical="taiyi-cycles-v2", profile=profile,
                              profile_metadata=dict(spec))
    index = (accumulated_year + offset - 1) % 18
    god = DAYOU_TM_PATH[index]
    return result(
        "R-DY-TM", canonical="taiyi-cycles-v2", profile=profile,
        source=spec["source"], offset=offset, accumulated_year=accumulated_year,
        cycle_index=index,
        step_number=index + 1, god=god, position=GOD_POSITION[god],
        profile_metadata=dict(spec),
    )


def smyo(accumulated_year=None):
    """Small Wander: 3 years per palace; 24-year loop, no palace 5."""
    if accumulated_year is None:
        return not_computable("R-SY", ["accumulated_year"], "缺历元累计年")
    integer(accumulated_year, 1)
    relative = (accumulated_year - 1) % 24 + 1
    index = (relative - 1) // 3
    year = (relative - 1) % 3 + 1
    return result(
        "R-SY", canonical="taiyi-cycles-v2", coordinate="nine_palace",
        accumulated_year=accumulated_year, cycle_index=relative - 1,
        relative_year=relative, palace_id=SMALL_WANDER_PATH[index],
        palace=SMALL_WANDER_PATH[index], year_in_palace=year,
        realm=("治天", "治地", "治人")[year - 1],
    )


def three_bases(accumulated_year=None, *, profile="project"):
    """Three bases share +250 offset but have distinct stay and effective periods."""
    if accumulated_year is None:
        return not_computable("R-3B", ["accumulated_year"], "缺历元累计年", profile=profile)
    integer(accumulated_year, 1)
    if profile != "project":
        raise ValueError("未知三基profile；四库皆起戌仅为source variant")
    outputs = {}
    for key, spec in BASE_SPECS.items():
        relative = (accumulated_year + 250 - 1) % spec["cycle"] + 1
        index = (relative - 1) // spec["stay"]
        year_in_position = (relative - 1) % spec["stay"] + 1
        sector = BRANCHES[(BRANCHES.index(spec["start"]) + index) % 12]
        outputs[key] = {
            "coordinate": "twelve_branch", "name": spec["name"], "start": spec["start"],
            "sector": sector, "position": sector,
            "relative_year": relative, "cycle_index": relative - 1,
            "year_in_position": year_in_position,
            "stay_years": spec["stay"], "cycle_years": spec["cycle"],
            "outer_cycle_years": spec["outer_cycle"],
        }
    return result(
        "R-3B", canonical="taiyi-cycles-v2", profile=profile,
        accumulated_year=accumulated_year,
        offset=250, bases=outputs,
        source_variants=["四库三基皆起戌；项目canonical用明代/统宗体系"],
    )


def kingbase(accumulated_year):
    return three_bases(accumulated_year)["bases"]["jun_ji"]


def officerbase(accumulated_year):
    return three_bases(accumulated_year)["bases"]["chen_ji"]


def pplbase(accumulated_year):
    return three_bases(accumulated_year)["bases"]["min_ji"]


def four_taiyi(accumulated_year=None):
    """Four Taiyi each keep their independent 12-palace id and sector."""
    if accumulated_year is None:
        return not_computable("R-4T", ["accumulated_year"], "缺历元累计年")
    integer(accumulated_year, 1)
    cycle_year = (accumulated_year - 1) % 36 + 1
    step = (cycle_year - 1) // 3
    year_in_palace = (cycle_year - 1) % 3 + 1
    yuan_index = (accumulated_year - 1) // 60
    results = {}
    for name, start in FOUR_TAIYI_START.items():
        # The 36-year loop and the 60-year +8 offset agree; applying both
        # independently would double-count the 三元 shift.
        palace_id = (start - 1 + step) % 12 + 1
        details = FOUR_TAIYI_PALACES[palace_id]
        results[name] = {
            "coordinate": "four_taiyi_palace",
            "palace_id": palace_id,
            **details,
            "year_in_palace": year_in_palace,
            "three_year_step": step,
            "yuan_index": yuan_index,
            "computable": True,
        }
    return result(
        "R-4T", canonical="taiyi-cycles-v2", accumulated_year=accumulated_year,
        relative_year=cycle_year, taiyi=results,
        source_note="3年一宫；第1年天/第2年地/第3年人未见明确原典，不生成phase",
    )


def four_taiyi_central_matrix(four_taiyi_result=None):
    """Central matrix for six same-12-palace pairs; interpretation remains pending."""
    positions = (four_taiyi_result or {}).get("taiyi", {})
    rows = []
    for left, right in FOUR_TAIYI_PAIRS:
        a, b = positions.get(left), positions.get(right)
        same = (a is not None and b is not None
                and a.get("palace_id") == b.get("palace_id"))
        rows.append({
            "members": [left, right],
            "computable": a is not None and b is not None,
            "same_four_taiyi_palace": same if a is not None and b is not None else None,
            "interpretation_status": "pending",
            "reason": "同宫断语待来源校定；不由宫位相同推衍吉凶",
        })
    return {"coordinate": "four_taiyi_palace", "pairs": rows}


def four_god_water_conflict(sector, nine_palace_id):
    """Known Four-God water conflict combinations only; other pairs stay pending."""
    integer(nine_palace_id, 1, 9)
    if sector not in BRANCHES:
        raise ValueError("四神水判定须输入十二支位置")
    if sector in ("辰", "戌") and nine_palace_id in (5, 9):
        state = "克贼"
    elif sector in ("丑", "未") and nine_palace_id in (7, 3):
        state = "克贼"
    elif sector in ("巳", "午") and nine_palace_id in (2, 9):
        state = "战克"
    else:
        state = None
    return {
        "computable": state is not None,
        "status": "known_conflict" if state else "pending",
        "four_taiyi_sector": sector, "nine_palace_id": nine_palace_id,
        "state": state,
        "reason": None if state else "未列明组合保持pending；不推演生旺",
    }


XIAOYOU_EFFECTS = {
    "五福": {"德": "德昌", "失德": "失德受殃"},
    "君基": {"default": "双君之象、争夺兵革"},
    "臣基": {"default": "下凌上"},
    "民基": {"default": "兴兵役", "variant": "收成说法保留异文"},
    "天乙": {"default": "下凌上"},
    "地乙": {"default": "土工、暴政、兵盗"},
    "直符": {"default": "风火兵革"},
    "四神": {"default": "人民不安、水涝、疾疫"},
    "大游": {"default": "兵丧、水旱、凶暴"},
}


def xiaoyou_suozhu(small_wander, *, co_located=(), virtue=None):
    """Interpret explicit named co-location inputs; never compare unlike id spaces."""
    if isinstance(small_wander, int):
        wander = smyo(small_wander)
    else:
        wander = dict(small_wander)
    if not wander.get("computable", True):
        return {"computable": False, "status": "not_computable",
                "missing_inputs": wander.get("missing_inputs", []),
                "reason": "小游本身不可计算"}
    effects = []
    for name in co_located:
        if name not in XIAOYOU_EFFECTS:
            raise ValueError(f"未知小游同临对象: {name}")
        spec = XIAOYOU_EFFECTS[name]
        if name == "五福":
            key = "德" if virtue is True else "失德" if virtue is False else None
            effects.append({
                "source": name,
                "effect": spec[key] if key else None,
                "status": "resolved" if key else "pending_virtue",
            })
        else:
            effects.append({
                "source": name, "effect": spec["default"],
                "variant": spec.get("variant"), "status": "resolved",
            })
    return {
        "computable": True, "status": "resolved" if effects else "no_matching_rule",
        "rule_id": "R-SY-INTERACTION", "small_wander": wander,
        "co_located_names": list(co_located), "effects": effects,
        "coordinate_note": "调用方先用对应坐标系确认同临；本函数不直接比较不同宫环的数字",
    }


def wufu_interaction(*, big_wander_co_located=None, opposite_domain=None,
                     small_wander_co_located=None, virtue=None):
    """Apply stated Five-Blessings modifiers only when co-location is explicit."""
    effects = []
    if big_wander_co_located is True:
        effects.append({
            "source": "大游", "effect": "福减半",
            "opposite_domain": opposite_domain,
            "disaster_effect": "兵革灾降对冲分野",
        })
    elif big_wander_co_located is None:
        effects.append({"source": "大游", "status": "pending_co_location"})
    if small_wander_co_located is True:
        label = "有德者昌" if virtue is True else "失德者殃" if virtue is False else None
        effects.append({
            "source": "小游", "effect": label,
            "status": "resolved" if label else "pending_virtue",
        })
    elif small_wander_co_located is None:
        effects.append({"source": "小游", "status": "pending_co_location"})
    return {"computable": True, "effects": effects,
            "coordinate_note": "不把五福五域与九宫宫号当作同一坐标"}


# Compatibility names for older callers.
small_wander = smyo
four_taiyi_cycle = four_taiyi
