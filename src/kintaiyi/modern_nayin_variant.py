"""现代《太乙数纳音体系（修正版）》的独立重构 variant。

该模块不是《太乙金镜式经》J4M-03 canonical。
只实现材料明确给出的现代构造：
- 太乙五音顺序：宫徵羽商角；
- 五音纳天干：宫徵羽商角 -> 甲丙戊庚壬，并按阴阳取成对阴干；
- 星神本五行 -> 五音；
- 所落地支 -> 十二律，并据阴阳生成干支；
- 六十甲子纳音表；
- 日干对应的“变音顺序”仅返回序列，不擅自替作者决定某星神如何取变音；
- 四维可显式选用材料提出的 branch_proxy：乾亥、艮寅、坤申、巽巳。

禁止把本模块结果回写 J4M-03 canonical。
"""

MODERN_NAYIN_PROFILE = "modern_liunian_nayin_2026"
MODERN_NAYIN_VARIANT_ID = "J4M03-MODERN-LIUNIAN-NAYIN"

TONE_ORDER = ["宫", "徵", "羽", "商", "角"]
TONE_ELEMENT = {"宫": "土", "徵": "火", "羽": "水", "商": "金", "角": "木"}
ELEMENT_TONE = {v: k for k, v in TONE_ELEMENT.items()}

# 材料：“宫徵羽商角纳甲丙戊庚壬”；结合其“子取阳干壬、丑取阴干癸”示例，
# 用成对阴干补齐。
TONE_STEM_PAIR = {
    "宫": ("甲", "乙"),
    "徵": ("丙", "丁"),
    "羽": ("戊", "己"),
    "商": ("庚", "辛"),
    "角": ("壬", "癸"),
}

BRANCH_POLARITY = {
    "子": "阳", "丑": "阴", "寅": "阳", "卯": "阴",
    "辰": "阳", "巳": "阴", "午": "阳", "未": "阴",
    "申": "阳", "酉": "阴", "戌": "阳", "亥": "阴",
}

# 十二地支配十二律：古典律历背景依赖；材料自身明确使用此配合并举若干实例。
BRANCH_LU = {
    "子": "黄钟", "丑": "大吕", "寅": "太簇", "卯": "夹钟",
    "辰": "姑洗", "巳": "仲吕", "午": "蕤宾", "未": "林钟",
    "申": "夷则", "酉": "南吕", "戌": "无射", "亥": "应钟",
}

# 材料另给四维的一种“按照历法”取支法。
DIMENSION_BRANCH_PROXY = {"乾": "亥", "艮": "寅", "坤": "申", "巽": "巳"}

DAY_TONE_SEQUENCE = {
    "甲": ["宫", "徵", "羽", "商", "角"],
    "己": ["宫", "徵", "羽", "商", "角"],
    "乙": ["徵", "羽", "商", "角", "宫"],
    "庚": ["徵", "羽", "商", "角", "宫"],
    "丙": ["羽", "商", "角", "宫", "徵"],
    "辛": ["羽", "商", "角", "宫", "徵"],
    "壬": ["商", "角", "宫", "徵", "羽"],
    "丁": ["商", "角", "宫", "徵", "羽"],
    "癸": ["角", "宫", "徵", "羽", "商"],
    "戊": ["角", "宫", "徵", "羽", "商"],
}

JIAZI_NAYIN = {
    "甲子": "海中金", "乙丑": "海中金", "丙寅": "炉中火", "丁卯": "炉中火",
    "戊辰": "大林木", "己巳": "大林木", "庚午": "路旁土", "辛未": "路旁土",
    "壬申": "剑锋金", "癸酉": "剑锋金", "甲戌": "山头火", "乙亥": "山头火",
    "丙子": "涧下水", "丁丑": "涧下水", "戊寅": "城头土", "己卯": "城头土",
    "庚辰": "白蜡金", "辛巳": "白蜡金", "壬午": "杨柳木", "癸未": "杨柳木",
    "甲申": "泉中水", "乙酉": "泉中水", "丙戌": "屋上土", "丁亥": "屋上土",
    "戊子": "霹雳火", "己丑": "霹雳火", "庚寅": "松柏木", "辛卯": "松柏木",
    "壬辰": "长流水", "癸巳": "长流水", "甲午": "沙中金", "乙未": "沙中金",
    "丙申": "山下火", "丁酉": "山下火", "戊戌": "平地木", "己亥": "平地木",
    "庚子": "壁上土", "辛丑": "壁上土", "壬寅": "金箔金", "癸卯": "金箔金",
    "甲辰": "覆灯火", "乙巳": "覆灯火", "丙午": "天河水", "丁未": "天河水",
    "戊申": "大驿土", "己酉": "大驿土", "庚戌": "钗钏金", "辛亥": "钗钏金",
    "壬子": "桑柘木", "癸丑": "桑柘木", "甲寅": "大溪水", "乙卯": "大溪水",
    "丙辰": "沙中土", "丁巳": "沙中土", "戊午": "天上火", "己未": "天上火",
    "庚申": "石榴木", "辛酉": "石榴木", "壬戌": "大海水", "癸亥": "大海水",
}

NAYIN_ELEMENT = {}
for _jiazi, _name in JIAZI_NAYIN.items():
    NAYIN_ELEMENT[_jiazi] = _name[-1]

WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


def _base():
    return {
        "variant_id": MODERN_NAYIN_VARIANT_ID,
        "profile": MODERN_NAYIN_PROFILE,
        "source_class": "modern_reconstruction",
        "canonical": False,
        "policy": "独立现代重构 variant；不得回写 J4M-03 canonical。",
    }


def modern_day_tone_sequence(day_stem):
    """返回材料明确给出的日干变音顺序，不进一步替作者选某星神的变音。"""
    sequence = DAY_TONE_SEQUENCE.get(day_stem)
    if sequence is None:
        return {
            **_base(),
            "status": "not_computable",
            "computable": False,
            "day_stem": day_stem,
            "valid_day_stems": list(DAY_TONE_SEQUENCE),
        }
    return {
        **_base(),
        "status": "ok",
        "computable": True,
        "day_stem": day_stem,
        "tone_sequence": list(sequence),
        "tone_to_position": {tone: i + 1 for i, tone in enumerate(sequence)},
        "policy_detail": "只返回材料的变音顺序；“星神如何由该顺序取得变五行”未在材料中写成唯一算法。",
    }


def _resolve_location(location, *, dimension_mode=None):
    if location in BRANCH_LU:
        return {
            "branch": location,
            "lu": BRANCH_LU[location],
            "location_kind": "branch",
            "location_method": "direct_branch",
        }

    if location in DIMENSION_BRANCH_PROXY:
        if dimension_mode != "branch_proxy":
            return {
                "error": "dimension_requires_explicit_mode",
                "location": location,
                "supported_dimension_mode": "branch_proxy",
                "policy": "四维存在多种取法；必须显式选择材料提出的乾亥/艮寅/坤申/巽巳 branch_proxy。",
            }
        branch = DIMENSION_BRANCH_PROXY[location]
        return {
            "branch": branch,
            "lu": BRANCH_LU[branch],
            "location_kind": "dimension",
            "location_method": "branch_proxy",
            "original_location": location,
        }

    return {"error": "unknown_location", "location": location}


def modern_star_base_nayin(star_element, location, *, dimension_mode=None):
    """按现代材料构造一个星神的“本五行纳音”。

    只实现材料可明确复现的链：
    星神本五行 -> 五音 -> 纳天干；所落地支/四维 -> 律吕/阴阳 -> 干支 -> 六十甲子纳音。
    """
    if star_element not in ELEMENT_TONE:
        return {
            **_base(),
            "status": "not_computable",
            "computable": False,
            "star_element": star_element,
            "valid_elements": sorted(ELEMENT_TONE),
        }

    loc = _resolve_location(location, dimension_mode=dimension_mode)
    if "error" in loc:
        return {
            **_base(),
            "status": "not_computable",
            "computable": False,
            **loc,
        }

    tone = ELEMENT_TONE[star_element]
    yang_stem, yin_stem = TONE_STEM_PAIR[tone]
    polarity = BRANCH_POLARITY[loc["branch"]]
    stem = yang_stem if polarity == "阳" else yin_stem
    jiazi = stem + loc["branch"]
    nayin_name = JIAZI_NAYIN.get(jiazi)

    if nayin_name is None:
        return {
            **_base(),
            "status": "not_computable",
            "computable": False,
            "star_element": star_element,
            "tone": tone,
            "stem": stem,
            **loc,
            "jiazi": jiazi,
            "policy_detail": "按材料构造出的干支未落入标准六十甲子纳音表；不自行纠正。",
        }

    return {
        **_base(),
        "status": "ok",
        "computable": True,
        "star_element": star_element,
        "tone": tone,
        "stem_pair": [yang_stem, yin_stem],
        "selected_stem": stem,
        "polarity": polarity,
        **loc,
        "jiazi": jiazi,
        "nayin_name": nayin_name,
        "nayin_element": NAYIN_ELEMENT[jiazi],
    }


def modern_star_transformed_nayin(transformed_tone, location, *, dimension_mode=None, day_stem=None):
    """构造“变音”纳音。

    材料明确给出日干的变音顺序，但没有给出一个无歧义的函数说明
    “某星神本五行在该日究竟映射到序列中的哪一变音”。
    因此 transformed_tone 必须由上游显式给出；day_stem 只用于验证该音是否在当日序列中。
    """
    if transformed_tone not in TONE_STEM_PAIR:
        return {
            **_base(),
            "status": "not_computable",
            "computable": False,
            "transformed_tone": transformed_tone,
            "valid_tones": list(TONE_STEM_PAIR),
        }

    day_sequence = None
    if day_stem is not None:
        day = modern_day_tone_sequence(day_stem)
        if not day["computable"]:
            return day
        day_sequence = day["tone_sequence"]

    element = TONE_ELEMENT[transformed_tone]
    data = modern_star_base_nayin(element, location, dimension_mode=dimension_mode)
    if not data.get("computable"):
        return data

    return {
        **data,
        "construction": "transformed_tone_explicit",
        "transformed_tone": transformed_tone,
        "day_stem": day_stem,
        "day_tone_sequence": day_sequence,
        "policy_detail": "变音由调用者显式指定；本函数不从日干序列擅自推导星神变五行。",
    }


def compare_modern_nayin_elements(first_element, second_element):
    """只返回五行关系，不把现代材料未明示的关系自动翻成吉凶/胜负。"""
    valid = set(WUXING_SHENG)
    if first_element not in valid or second_element not in valid:
        return {
            **_base(),
            "status": "not_computable",
            "computable": False,
            "first_element": first_element,
            "second_element": second_element,
        }

    if first_element == second_element:
        relation = "比和"
    elif WUXING_KE[first_element] == second_element:
        relation = "一克二"
    elif WUXING_KE[second_element] == first_element:
        relation = "二克一"
    elif WUXING_SHENG[first_element] == second_element:
        relation = "一生二"
    else:
        relation = "二生一"

    return {
        **_base(),
        "status": "ok",
        "computable": True,
        "first_element": first_element,
        "second_element": second_element,
        "relation": relation,
        "verdict": None,
        "policy_detail": "材料只说本/变纳音可以关系比较，未给统一吉凶公式，因此只返回关系。",
    }
