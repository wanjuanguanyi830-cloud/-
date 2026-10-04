"""Canonical coordinate systems and five-state rules; no calendar or UI imports."""

SIXTEEN = tuple("子 丑 艮 寅 卯 辰 巽 巳 午 未 坤 申 酉 戌 乾 亥".split())
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
GODS = tuple("地主 阳德 和德 吕申 高丛 太阳 大炅 大神 大威 天道 大武 武德 太簇 阴主 阴德 大义".split())
ELEMENTS = tuple("水 土 土 木 木 土 木 火 火 土 土 金 金 土 金 水".split())
SECTOR_GODS = dict(zip(SIXTEEN, GODS))
GOD_SECTORS = dict(zip(GODS, SIXTEEN))
SECTOR_ELEMENTS = dict(zip(SIXTEEN, ELEMENTS))
SIXTEEN_GOD_ELEMENTS = dict(zip(GODS, ELEMENTS))
GOD_ALIASES = {"太炅": "大炅", "太神": "大神"}
NINE_PALACES = {
    i: {"palace_id": i, "trigram": trigram, "sector": sector,
        "element": element, "yin_yang": polarity}
    for i, trigram, sector, element, polarity in (
        (1, "乾", "乾", "金", "阴"), (2, "离", "午", "火", "阴"),
        (3, "艮", "艮", "土", "阳"), (4, "震", "卯", "木", "阳"),
        (5, "中", None, "土", None), (6, "兑", "酉", "金", "阴"),
        (7, "坤", "坤", "土", "阴"), (8, "坎", "子", "水", "阳"),
        (9, "巽", "巽", "木", "阳"),
    )
}
# This projection is lossy: two Sector16 coordinates share each outer Palace9.
SECTOR_TO_NINE_PALACE = dict(zip(SIXTEEN, (8, 3, 3, 4, 4, 9, 9, 2, 2, 7, 7, 6, 6, 1, 1, 8)))
YANG_PALACES = frozenset((8, 3, 4, 9))
YIN_PALACES = frozenset((2, 7, 6, 1))
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
OVERCOMES = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
GENERAL_ELEMENTS = {"太乙": "木", "始击": "火", "文昌": "土", "主大将": "金",
                    "主参将": "水", "客大将": "水", "客参将": "木"}
ROLE_ELEMENTS = {"home_general": "金", "home_assistant": "水", "home_vassal": "水",
                 "away_general": "水", "away_assistant": "木", "away_vassal": "木"}
FIRE_STAGES = dict(zip(tuple("寅卯辰巳午未申酉戌亥子丑"),
                       "长生 沐浴 冠带 临官 帝旺 衰 病 死 墓 绝 胎 养".split()))
CORNER_SECTORS = {"艮": frozenset("丑艮寅"), "巽": frozenset("辰巽巳"),
                  "坤": frozenset("未坤申"), "乾": frozenset("戌乾亥")}


def integer(value, minimum=0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("须为整数")
    if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        raise ValueError("数值超出范围")
    return value


def validate_sector(sector):
    if not isinstance(sector, str) or sector not in SIXTEEN:
        raise ValueError("须为十六辰坐标")
    return sector


def sector_to_nine_palace(sector):
    """Lossy Sector16 -> Palace9 projection, never an invertible conversion."""
    return SECTOR_TO_NINE_PALACE[validate_sector(sector)]


def nine_palace_to_trigram(palace):
    return NINE_PALACES[integer(palace, 1, 9)]["trigram"]


def nine_palace_representative_sector(palace):
    sector = NINE_PALACES[integer(palace, 1, 9)]["sector"]
    if sector is None:
        raise ValueError("中五无十六辰代表点（杜塞）")
    return sector


def nine_palace_element(palace):
    return NINE_PALACES[integer(palace, 1, 9)]["element"]


def rotate_sixteen(sector, steps):
    integer(steps, None)
    return SIXTEEN[(SIXTEEN.index(validate_sector(sector)) + steps) % 16]


def dashen_from_sector(sector):
    return rotate_sixteen(sector, 4)


def dashen_from_nine_palace(palace):
    return dashen_from_sector(nine_palace_representative_sector(palace))


def qi_relation(subject, environment):
    if subject not in GENERATES or environment not in GENERATES:
        raise ValueError("须为木火土金水")
    if subject == environment:
        relation, state = "比和", "旺"
    elif GENERATES[environment] == subject:
        relation, state = "生我", "相"
    elif OVERCOMES[environment] == subject:
        relation, state = "克我", "死"
    elif OVERCOMES[subject] == environment:
        relation, state = "我克", "囚"
    else:
        relation, state = "我生", "休"
    return {"subject": subject, "environment": environment, "relation": relation, "state": state}


def sector_detail(sector):
    sector = validate_sector(sector)
    palace = sector_to_nine_palace(sector)
    return {"sector": sector, "god": SECTOR_GODS[sector], "element": SECTOR_ELEMENTS[sector],
            "sector_element": SECTOR_ELEMENTS[sector], "nine_palace": palace,
            "nine_palace_trigram": nine_palace_to_trigram(palace),
            "nine_palace_element": nine_palace_element(palace), "projection_lossy": True}


def fire_twelve_stage(sector):
    return FIRE_STAGES.get(validate_sector(sector))


def dashen_self_qi(landing_sector):
    detail = sector_detail(landing_sector)
    return {**qi_relation("火", detail["element"]), "landing": detail, "model": "A",
            "fire_stage": fire_twelve_stage(landing_sector), "fire_stage_provenance": "derived"}


def general_palace_qi(general_palace, dashen_sector):
    detail = sector_detail(dashen_sector)
    element = nine_palace_element(general_palace)
    return {**qi_relation(element, detail["element"]), "palace_id": general_palace,
            "palace_element": element, "landing": detail, "model": "B"}
