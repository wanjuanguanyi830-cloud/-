"""Four Taiyi occupy Palace12, retaining IDs 10, 11 and 12 without projection."""
from .taiyi_common import BRANCHES, integer
from .taiyi_cycles import cycle_position, sector_to_five_domain

TWELVE_PALACES = {
    i: {"palace_id": i, "name": name, "sector": sector, "coordinate_system": "four_taiyi_palace12"}
    for i, name, sector in (
        (1,"乾","乾"),(2,"离","午"),(3,"艮","艮"),(4,"震","卯"),(5,"中",None),
        (6,"兑","酉"),(7,"坤","坤"),(8,"坎","子"),(9,"巽","巽"),
        (10,"绛宫","巳"),(11,"明堂","申"),(12,"玉堂","寅"),
    )
}
FOUR_ATTRIBUTES = {"天乙": {"element": "金", "start_palace": 6},
                   "地乙": {"element": "土", "start_palace": 9},
                   "直符": {"element": "火", "start_palace": 5},
                   "四神": {"element": "水", "start_palace": 1}}
PAIR_EFFECTS = {
    frozenset(("天乙","地乙")): ("兵戈","土工","农伤"),
    frozenset(("天乙","直符")): ("火旱","刀兵","饥疾"),
    frozenset(("天乙","四神")): ("水涝","霜雪","兵盗","舟车不通"),
    frozenset(("地乙","直符")): ("火旱","兵盗","土工"),
    frozenset(("地乙","四神")): ("水旱失调","民灾"),
    frozenset(("直符","四神")): ("水旱","饥疫","兵盗"),
}
FIVE_MEETING_EFFECTS = {"天乙": ("兵","盗"), "地乙": ("疫疠","民灾"),
                        "直符": ("旱","蝗"), "四神": ("淫雨","川溃")}


def rotate_twelve(start, steps):
    integer(start, 1, 12)
    integer(steps, None)
    return ((start + steps - 1) % 12) + 1


def four_taiyi_position(name, accumulated_year, *, yuan=1):
    if name not in FOUR_ATTRIBUTES:
        raise ValueError("未知四太乙名称")
    integer(yuan, 1, 3)
    data = cycle_position(accumulated_year, 36, 3)
    attributes = FOUR_ATTRIBUTES[name]
    start = rotate_twelve(attributes["start_palace"], (yuan - 1) * 8)
    palace = rotate_twelve(start, data["index"])
    return {**data, **TWELVE_PALACES[palace], "name": name,
            "palace_name": TWELVE_PALACES[palace]["name"], "palace": palace,
            "intrinsic_element": attributes["element"], "yuan": yuan,
            "yuan_start_palace": start, "provenance": "project_canonical",
            "source_note": "三年一宫；未确认每宫三年天地人阶段，不设phase"}


def four_taiyi_positions(accumulated_year, *, yuan=1):
    return {name: four_taiyi_position(name, accumulated_year, yuan=yuan) for name in FOUR_ATTRIBUTES}


def same_palace_effects(positions):
    effects = []
    for pair, dangers in PAIR_EFFECTS.items():
        names = sorted(pair)
        if all(name in positions for name in names):
            a, b = (positions[name] for name in names)
            if a["palace_id"] == b["palace_id"]:
                effects.append({"pair": names, "palace_id": a["palace_id"], "effects": list(dangers)})
    return effects


def five_blessings_four_taiyi_effects(five, positions):
    effects = []
    for name, position in positions.items():
        palace = integer(position["palace_id"], 1, 12)
        sector = TWELVE_PALACES[palace]["sector"]
        domain = "中" if palace == 5 else sector_to_five_domain(sector)
        if domain == five["domain"]:
            effects.append({"name": name, "palace_id": palace, "domain": domain,
                            "effects": list(FIVE_MEETING_EFFECTS[name]), "rule": "same_five_domain"})
    return effects


def four_gods_water_special(year_branch=None, palace_id=None):
    missing = [k for k, v in (("year_branch", year_branch), ("palace_id", palace_id)) if v is None]
    if missing:
        return {"computable": False, "missing_inputs": missing, "reason": "缺四神水事件输入"}
    if not isinstance(year_branch, str) or year_branch not in BRANCHES:
        raise ValueError("须为十二支")
    integer(palace_id, 1, 12)
    known = "克贼" if (year_branch in "辰戌" and palace_id in (5,9)) or (year_branch in "丑未" and palace_id in (7,3)) else "战克" if year_branch in "巳午" and palace_id in (2,9) else None
    return {"computable": known is not None, "missing_inputs": [],
            "status": "ok" if known else "pending", "reason": None if known else "原文未覆盖，不外推",
            "year_branch": year_branch, "palace_id": palace_id, "classification": known}


def zhifu_known_state(palace_id):
    integer(palace_id, 1, 12)
    state = {2: "旺", 3: "长生", 4: "败"}.get(palace_id)
    return {"computable": state is not None, "missing_inputs": [], "palace_id": palace_id,
            "state": state, "status": "ok" if state else "source_pending",
            "reason": None if state else "直符该宫来源未确认"}
