"""R-* 公共 canonical。来源与异文见 rules/taiyi_v1.json。"""

SIXTEEN = tuple("子 丑 艮 寅 卯 辰 巽 巳 午 未 坤 申 酉 戌 乾 亥".split())
BRANCHES = tuple("子丑寅卯辰巳午未申酉戌亥")
STEMS = tuple("甲乙丙丁戊己庚辛壬癸")
GODS = tuple("地主 阳德 和德 吕申 高丛 太阳 大炅 大神 大威 天道 大武 武德 太簇 阴主 阴德 大义".split())
ELEMENTS = tuple("水 土 土 木 木 土 木 火 火 土 土 金 金 土 金 水".split())
POSITION_WX = dict(zip(SIXTEEN, ELEMENTS))
GOD_POSITION = dict(zip(GODS, SIXTEEN))
GOD_ALIASES = {
    "太炅": "大炅",
    "太神": "大神",
    "大旲": "大炅",
    "陽德": "阳德",
    "呂申": "吕申",
    "高叢": "高丛",
    "太陽": "太阳",
    "陰主": "阴主",
    "陰德": "阴德",
    "大義": "大义",
    "太蔟": "太簇",
}
SIXTEEN_GOD_WX = dict(zip(GODS, ELEMENTS))
PALACE_POINT = {1: "乾", 2: "午", 3: "艮", 4: "卯", 6: "酉", 7: "坤", 8: "子", 9: "巽"}
PALACE_WX = {1: "金", 2: "火", 3: "土", 4: "木", 5: "土", 6: "金", 7: "土", 8: "水", 9: "木"}
YANG_PALACES = frozenset((8, 3, 4, 9))
YIN_PALACES = frozenset((2, 7, 6, 1))
GENERATES = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CONTROLS = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
FIRE_STAGES = dict(zip(tuple("寅卯辰巳午未申酉戌亥子丑"),
                          "长生 沐浴 冠带 临官 帝旺 衰 病 死 墓 绝 胎 养".split()))
CORNER_SECTORS = {"艮": frozenset("丑艮寅"), "巽": frozenset("辰巽巳"),
                  "坤": frozenset("未坤申"), "乾": frozenset("戌乾亥")}

# C96: recovered from 2026-10-04 taiyi_common.py and crosschecked against
# current POSITION_WX / GOD_POSITION / PALACE_POINT. These are coordinate helpers,
# not independent formula sources.
SECTOR_GODS = {position: god for god, position in GOD_POSITION.items()}
SECTOR_TO_NINE_PALACE = dict(
    zip(SIXTEEN, (8, 3, 3, 4, 4, 9, 9, 2, 2, 7, 7, 6, 6, 1, 1, 8))
)
PALACE_TRIGRAM = {
    1: "乾", 2: "离", 3: "艮", 4: "震", 5: "中",
    6: "兑", 7: "坤", 8: "坎", 9: "巽",
}
OPPOSITE_PALACES = {1: 9, 9: 1, 3: 7, 7: 3, 2: 8, 8: 2, 4: 6, 6: 4}


def integer(value, minimum=0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("须为整数")
    if value < minimum or (maximum is not None and value > maximum):
        raise ValueError("数值超出范围")
    return value


def palace_element(palace):
    return PALACE_WX[integer(palace, 1, 9)]


def position(anchor):
    if isinstance(anchor, int) and not isinstance(anchor, bool):
        integer(anchor, 1, 9)
        if anchor == 5:
            raise ValueError("中五无十六宫代表点")
        return PALACE_POINT[anchor]
    anchor = GOD_ALIASES.get(anchor, anchor)
    anchor = GOD_POSITION.get(anchor, anchor)
    if anchor not in SIXTEEN:
        raise ValueError("须为十六宫位置、十六神或外八宫数")
    return anchor


def dashen_from_lushen(anchor):
    """R-LS-01：十六环顺行四格，内部0基。"""
    return SIXTEEN[(SIXTEEN.index(position(anchor)) + 4) % 16]


def qi_state(subject, environment):
    """R-QI：同旺，生我相，克我死，我克囚，我生休。"""
    if subject not in GENERATES or environment not in GENERATES:
        raise ValueError("须为木火土金水")
    if subject == environment:
        return "旺"
    if GENERATES[environment] == subject:
        return "相"
    if CONTROLS[environment] == subject:
        return "死"
    if CONTROLS[subject] == environment:
        return "囚"
    return "休"


def dashen_qi(anchor):
    landing = dashen_from_lushen(anchor)
    return {"position": landing, "element": POSITION_WX[landing],
            "palace": next((p for p, point in PALACE_POINT.items() if point == landing), None),
            "state": qi_state("火", POSITION_WX[landing]),
            "stage": FIRE_STAGES.get(landing), "model": "A"}



def _signed_integer(value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("须为整数")
    return value


def validate_sector(sector):
    if not isinstance(sector, str) or sector not in SIXTEEN:
        raise ValueError("须为十六宫位置")
    return sector


def sector_to_nine_palace(sector):
    """C96：十六辰/四维 -> 九宫的有损投影。"""
    return SECTOR_TO_NINE_PALACE[validate_sector(sector)]


def nine_palace_to_trigram(palace):
    return PALACE_TRIGRAM[integer(palace, 1, 9)]


def nine_palace_representative_sector(palace):
    palace = integer(palace, 1, 9)
    if palace == 5:
        raise ValueError("中五无十六宫代表点")
    return PALACE_POINT[palace]


def rotate_sixteen(sector, steps):
    """C96：十六环可正负步旋转；不附加任何术义。"""
    sector = validate_sector(sector)
    steps = _signed_integer(steps)
    return SIXTEEN[(SIXTEEN.index(sector) + steps) % len(SIXTEEN)]


def sector_detail(sector):
    sector = validate_sector(sector)
    palace = sector_to_nine_palace(sector)
    god = SECTOR_GODS[sector]
    return {
        "sector": sector,
        "god": god,
        "element": POSITION_WX[sector],
        "sector_element": POSITION_WX[sector],
        "nine_palace": palace,
        "nine_palace_trigram": nine_palace_to_trigram(palace),
        "nine_palace_element": PALACE_WX[palace],
        "projection_lossy": True,
    }


def sector_opposition(sector):
    return rotate_sixteen(sector, 8)


def nine_palace_opposition(palace):
    palace = integer(palace, 1, 9)
    if palace == 5:
        return {
            "computable": False,
            "missing_inputs": [],
            "reason": "中宫对冲来源待校",
            "status": "pending",
        }
    return {
        "computable": True,
        "palace_id": palace,
        "opposite_palace_id": OPPOSITE_PALACES[palace],
    }


def qi_relation(subject, environment):
    """C96：在现行 qi_state 上恢复关系名包装，不改变五态公式。"""
    state = qi_state(subject, environment)
    if subject == environment:
        relation = "比和"
    elif GENERATES[environment] == subject:
        relation = "生我"
    elif CONTROLS[environment] == subject:
        relation = "克我"
    elif CONTROLS[subject] == environment:
        relation = "我克"
    else:
        relation = "我生"
    return {
        "subject": subject,
        "environment": environment,
        "relation": relation,
        "state": state,
    }


def general_palace_qi(general_palace, landing_sector):
    """C96：显式九宫五行 vs 落点五行关系；不计算落点来源。"""
    detail = sector_detail(landing_sector)
    element = PALACE_WX[integer(general_palace, 1, 9)]
    return {
        **qi_relation(element, detail["element"]),
        "palace_id": general_palace,
        "palace_element": element,
        "landing": detail,
        "model": "B",
    }

def calc_components(n):
    """R-CAL-01：十/五/一存在结构，不自动赋予古籍俱足标签。"""
    integer(n, 1, 40)
    unit = n % 10
    return {"ten": n >= 10, "five": unit >= 5, "one": unit % 5 != 0}


def sexagenary_year(value):
    if value in BRANCHES:
        return None, value
    if not isinstance(value, str) or len(value) != 2 or value[0] not in STEMS or value[1] not in BRANCHES:
        raise ValueError("须为年支或有效干支年")
    cycle = [STEMS[i % 10] + BRANCHES[i % 12] for i in range(60)]
    if value not in cycle:
        raise ValueError("无效干支配对")
    return cycle.index(value), value[1]


def result(rule_id, **fields):
    return {"rule_id": rule_id, "category": "seven_methods" if rule_id.startswith("T7") else "eight_divinations",
            "canonical": "taiyi-t7-d8-v1", **fields}
