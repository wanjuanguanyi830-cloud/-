"""Legacy public names delegated to the canonical coordinate core."""
from . import taiyi_common as _c

SIXTEEN = _c.SIXTEEN
BRANCHES = _c.BRANCHES
STEMS = _c.STEMS
GODS = _c.GODS
ELEMENTS = _c.ELEMENTS
POSITION_WX = _c.SECTOR_ELEMENTS
GOD_POSITION = _c.GOD_SECTORS
GOD_ALIASES = _c.GOD_ALIASES
SIXTEEN_GOD_WX = _c.SIXTEEN_GOD_ELEMENTS
PALACE_POINT = {i: d["sector"] for i, d in _c.NINE_PALACES.items() if i != 5}
PALACE_WX = {i: d["element"] for i, d in _c.NINE_PALACES.items()}
YANG_PALACES = _c.YANG_PALACES
YIN_PALACES = _c.YIN_PALACES
GENERATES = _c.GENERATES
CONTROLS = _c.OVERCOMES
FIRE_STAGES = _c.FIRE_STAGES
CORNER_SECTORS = _c.CORNER_SECTORS
integer = _c.integer
palace_element = _c.nine_palace_element


def position(anchor):
    if isinstance(anchor, int) and not isinstance(anchor, bool):
        return _c.nine_palace_representative_sector(anchor)
    anchor = GOD_ALIASES.get(anchor, anchor)
    return _c.validate_sector(GOD_POSITION.get(anchor, anchor))


def dashen_from_lushen(anchor):
    return _c.dashen_from_sector(position(anchor))


def qi_state(subject, environment):
    return _c.qi_relation(subject, environment)["state"]


def dashen_qi(anchor):
    landing = dashen_from_lushen(anchor)
    qi = _c.dashen_self_qi(landing)
    return {"position": landing, "element": qi["environment"],
            "palace": qi["landing"]["nine_palace"], "state": qi["state"],
            "stage": qi["fire_stage"], "model": "A"}


def calc_components(n):
    integer(n, 1, 40)
    unit = n % 10
    return {"ten": n >= 10, "five": unit >= 5, "one": unit % 5 != 0}


def sexagenary_year(value):
    if value in BRANCHES:
        return None, value
    if not isinstance(value, str) or len(value) != 2:
        raise ValueError("须为年支或有效干支年")
    cycle = [STEMS[i % 10] + BRANCHES[i % 12] for i in range(60)]
    if value not in cycle:
        raise ValueError("无效干支配对")
    return cycle.index(value), value[1]


def result(rule_id, **fields):
    return {"rule_id": rule_id,
            "category": "seven_methods" if rule_id.startswith("T7") else "eight_divinations",
            "canonical": "taiyi-t7-d8-v1", **fields}
