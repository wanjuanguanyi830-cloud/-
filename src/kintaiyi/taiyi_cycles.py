"""One-based cycle arithmetic. Epoch offsets are applied exactly once here."""
from .taiyi_common import BRANCHES, SECTOR_GODS, integer, validate_sector

WUFU_PATH = (1, 3, 9, 7, 5)
DAYOU_PATH = (7, 8, 9, 1, 2, 3, 4, 6)
DAYOU_TAOJIN_PATH = (7, 6, 4, 3, 2, 1, 9, 8)
DAYOU_TM_SECTORS = ("未", "坤", "坤", "申", "酉", "戌", "乾", "乾", "亥", "子", "丑", "艮", "寅", "卯", "辰", "巽", "巳", "午")
DAYOU_TM_PATH = tuple(SECTOR_GODS[s] for s in DAYOU_TM_SECTORS)
NUMBER_SUBJECTS = ("士卒", "君王", "王侯臣宰", "后妃", "太子", "民庶", "师帅", "上将军", "中将军", "下将军")
FIVE_DOMAINS = {"乾": frozenset("戌乾亥"), "艮": frozenset("丑艮寅"), "巽": frozenset("辰巽巳"),
                "坤": frozenset("未坤申"), "中": frozenset("子午卯酉")}
PALACE_DOMAINS = {1: "乾", 3: "艮", 9: "巽", 7: "坤", 5: "中", 2: "中", 4: "中", 6: "中", 8: "中"}
WUFU_NAMES = {"乾": "黄秘", "艮": "黄始", "巽": "黄室", "坤": "黄庭", "中": "玄室"}
OPPOSITE_PALACES = {1: 9, 9: 1, 3: 7, 7: 3, 2: 8, 8: 2, 4: 6, 6: 4}


def cycle_position(value, cycle, stay=1, offset=0):
    integer(value, 1)
    integer(cycle, 1)
    integer(stay, 1)
    integer(offset, None)
    if cycle % stay:
        raise ValueError("周期须整除驻留年数")
    year = ((value + offset - 1) % cycle) + 1
    return {"accumulated_year": value, "cycle": cycle, "offset": offset, "cycle_year": year,
            "index": (year - 1) // stay, "year_in_palace": (year - 1) % stay + 1,
            "computable": True, "missing_inputs": [], "reason": None}


def _base(value, start, stay, outer_cycle, profile):
    if profile not in ("project_canonical", "siku"):
        raise ValueError("未知三基profile")
    start = "戌" if profile == "siku" else start
    data = cycle_position(value, 12 * stay, stay, 250)
    return {**data, "branch": BRANCHES[(BRANCHES.index(start) + data["index"]) % 12],
            "start_branch": start, "source_outer_cycle": outer_cycle, "profile": profile,
            "provenance": "source_variant" if profile == "siku" else "project_canonical",
            "variants": [{"id": "VAR-3BASE-01", "start_branch": "戌", "status": "source_variant"}]}


def ruler_base(accumulated_year, *, profile="project_canonical"):
    return _base(accumulated_year, "午", 30, 3600, profile)


def minister_base(accumulated_year, *, profile="project_canonical"):
    return _base(accumulated_year, "午", 3, 360, profile)


def people_base(accumulated_year, *, profile="project_canonical"):
    return _base(accumulated_year, "戌", 1, 360, profile)


def number_subject(year_in_palace, maximum):
    integer(year_in_palace, 1, maximum)
    return {"value": year_in_palace, "last_digit": year_in_palace % 10,
            "subject": NUMBER_SUBJECTS[year_in_palace % 10]}


def five_blessings_lucky_calc(year_in_palace):
    return number_subject(year_in_palace, 45)


def sector_to_five_domain(sector):
    validate_sector(sector)
    return next(domain for domain, sectors in FIVE_DOMAINS.items() if sector in sectors)


def nine_palace_to_five_domain(palace):
    return PALACE_DOMAINS[integer(palace, 1, 9)]


def five_blessings(accumulated_year, *, profile="project_canonical", offset=None):
    profiles = {"project_canonical": 250, "source_115": 115}
    if profile not in profiles:
        raise ValueError("未知五福profile")
    selected_offset = profiles[profile] if offset is None else integer(offset, None)
    data = cycle_position(accumulated_year, 225, 45, selected_offset)
    palace = WUFU_PATH[data["index"]]
    domain = PALACE_DOMAINS[palace]
    lucky = five_blessings_lucky_calc(data["year_in_palace"])
    return {**data, "rule_id": "R-WF", "palace_id": palace, "palace": palace,
            "domain": domain, "name": WUFU_NAMES[domain], "profile": profile,
            "phase": ("理天", "理地", "理人")[(data["year_in_palace"] - 1) // 15],
            "lucky_calc": lucky, "auspicious_subject": lucky["subject"],
            "provenance": "source_variant" if profile == "source_115" else "project_canonical"}


def big_wander(accumulated_year, *, profile="project_canonical", epoch_offset=None):
    profiles = {"project_canonical": (DAYOU_PATH, 0), "tongzong": (DAYOU_PATH, 34),
                "taojin": (DAYOU_TAOJIN_PATH, None)}
    if profile not in profiles:
        raise ValueError("未知大游profile")
    path, offset = profiles[profile]
    offset = offset if epoch_offset is None else integer(epoch_offset, None)
    integer(accumulated_year, 1)
    if offset is None:
        return {"computable": False, "missing_inputs": ["epoch_offset"], "reason": "该来源历元盈差待校",
                "status": "not_computable", "profile": profile, "path": list(path), "provenance": "source_variant"}
    data = cycle_position(accumulated_year, 288, 36, offset)
    palace = path[data["index"]]
    subject = number_subject(data["year_in_palace"], 36)
    return {**data, "rule_id": "R-DY", "palace_id": palace, "palace": palace, "profile": profile,
            "phase": ("治天", "治地", "治人")[(data["year_in_palace"] - 1) // 12],
            "inauspicious_calc": subject, "inauspicious_subject": subject["subject"],
            "provenance": "source_variant" if profile == "taojin" else "project_canonical"}


def big_wander_skyeyes(accumulated_year, *, profile="jinjing", epoch_offset=None):
    profiles = {"jinjing": 0, "tongzong": 214}
    if profile not in profiles:
        raise ValueError("未知大游天目profile")
    offset = profiles[profile] if epoch_offset is None else integer(epoch_offset, None)
    data = cycle_position(accumulated_year, 18, 1, offset)
    sector = DAYOU_TM_SECTORS[data["index"]]
    return {**data, "rule_id": "R-DY-TM", "step_number": data["cycle_year"],
            "sector": sector, "position": sector, "god": SECTOR_GODS[sector], "profile": profile}


def small_wander(accumulated_year):
    data = cycle_position(accumulated_year, 24, 3)
    palace = (1, 2, 3, 4, 6, 7, 8, 9)[data["index"]]
    return {**data, "rule_id": "R-SY", "palace_id": palace, "palace": palace,
            "phase": ("治天", "治地", "治人")[data["year_in_palace"] - 1]}


def five_blessings_wander_effect(five, *, big=None, small=None):
    effects = []
    if big and big.get("computable") and nine_palace_to_five_domain(big["palace_id"]) == five["domain"]:
        effects.append({"method": "big_wander", "fortune_fraction": 0.5,
                        "disaster_palace": OPPOSITE_PALACES[big["palace_id"]],
                        "residual": ["兵盗", "水旱"]})
    if small and small.get("computable") and nine_palace_to_five_domain(small["palace_id"]) == five["domain"]:
        effects.append({"method": "small_wander", "verdict": "有德昌、失德殃"})
    return effects


def five_blessings_base_meeting(accumulated_year, base_function):
    current = five_blessings(accumulated_year)
    same_now = sector_to_five_domain(base_function(accumulated_year)["branch"]) == current["domain"]
    if accumulated_year == 1:
        return {"same_now": same_now, "computable": False, "missing_inputs": ["previous_accumulated_year"],
                "reason": "积年第1年无前一年有效输入"}
    previous = five_blessings(accumulated_year - 1)
    same_previous = sector_to_five_domain(base_function(accumulated_year - 1)["branch"]) == previous["domain"]
    return {"computable": True, "same_now": same_now, "same_previous": same_previous,
            "first_meeting": same_now and not same_previous}
