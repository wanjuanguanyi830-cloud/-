"""四库本《太乙金镜式经》卷四军事十二法的来源限定实现。

本模块只实现已经能从卷四正文直接结构化、且不需要借用其他卷次公式的规则。
当前第一批：J4M-06 推陈兵向背、J4M-07 推制阵随地法、J4M-09 推太乙在天外地内法。

禁止把《太乙统宗宝鉴》卷五或旧项目卷十五的近名函数静默并入本模块。
"""

J4M_RULESET = "jinjing-siku-v4-military-12"
J4M_SOURCE_PROFILE = "jinjing_siku_volume4"


_CHENBING_XIANGBEI = {
    1: {"出军": "西北", "战利": "东南", "背地": "深涧隐匿之地", "阵": "方阵", "旗": "白旗"},
    2: {"出军": "正南", "战利": "正北", "邪道": "西南", "背地": "山邑火光耀耀焦之地", "阵": "直阵", "旗": "青旗"},
    4: {"出军": "正东", "战利": "正西", "背地": "林木穷道曲堤之地", "阵": "锐阵", "旗": "赤旗"},
    5: {"出军": "正北", "战利": "正南", "背地": "积土负城邑山林之地", "阵": "曲阵", "旗": "黑旗", "附注": "不然深沟高垒，固守吉"},
    6: {"出军": "正西", "战利": "正东", "背地": "水泽堑于丘墟之地", "阵": "方阵", "旗": "白旗"},
    9: {"出军": "东南", "战利": "西北", "背地": "高山丘陵积土之地", "阵": "锐阵", "旗": "赤旗"},
}

_FORMATION_ELEMENTS = {
    "曲阵": "水",
    "锐阵": "火",
    "直阵": "木",
    "方阵": "金",
    "圆阵": "土",
}

_TERRAIN_FORMATIONS = {
    "后高前下": {"宜阵": "锐阵", "所利": "利以进战，以溃其敌"},
    "前高后下": {"宜阵": "直阵", "所利": "不便进退，利以近斗；宜守以疲敌力"},
    "地洿邪": {"宜阵": "圆阵", "所利": "不便于战，利以坚守"},
    "地高而平": {"宜阵": "方阵", "所利": "利以四向，以通敌"},
    "左右势高": {"宜阵": "曲阵", "所利": "利以吞敌"},
}


def _base(rule_id, name):
    return {
        "ruleset": J4M_RULESET,
        "source_profile": J4M_SOURCE_PROFILE,
        "rule_id": rule_id,
        "name": name,
        "source_scope": "太乙金镜式经_四库本_卷四",
    }


def chenbing_xiangbei(rule_number):
    """J4M-06 推陈兵向背。

    rule_number 是本条正文明确列出的算类编号 1/2/4/5/6/9。
    这里不擅自把任意 1..40 算数化为个位；若上游需要这种归类，须另立来源规则。
    """
    result = _base("J4M-06", "推陈兵向背")
    if rule_number not in _CHENBING_XIANGBEI:
        return {
            **result,
            "status": "not_defined_by_source_passage",
            "computable": False,
            "input": rule_number,
            "defined_rule_numbers": list(_CHENBING_XIANGBEI),
            "policy": "正文仅列 1/2/4/5/6/9；不自动取个位、不借旧卷十五陈兵出乡补表。",
        }
    return {
        **result,
        "status": "ok",
        "computable": True,
        "input": rule_number,
        **_CHENBING_XIANGBEI[rule_number],
        "policy": "直接按《金镜》卷四正文表读取；不等同于陈兵出乡。",
    }


def zhizhen_suidi(terrain):
    """J4M-07 推制阵随地法：地形 -> 阵形 -> 五行。"""
    result = _base("J4M-07", "推制阵随地法")
    if terrain not in _TERRAIN_FORMATIONS:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "terrain": terrain,
            "known_terrains": list(_TERRAIN_FORMATIONS),
            "formation_elements": dict(_FORMATION_ELEMENTS),
            "policy": "未知地形不类推；J4M-07 不与 J4M-08 随地制变合并。",
        }
    item = _TERRAIN_FORMATIONS[terrain]
    formation = item["宜阵"]
    return {
        **result,
        "status": "ok",
        "computable": True,
        "terrain": terrain,
        "宜阵": formation,
        "五行": _FORMATION_ELEMENTS[formation],
        "所利": item["所利"],
        "formation_elements": dict(_FORMATION_ELEMENTS),
        "direction_relation": {"顺其向": "吉", "反其向": "凶"},
        "policy": "只实现本条地形制阵；兵种器械随地应变属于 J4M-08。",
    }


def taiyi_tianwai_dinei(taiyi_palace, *, three_doors_ready=None,
                        five_generals_released=None):
    """J4M-09 推太乙在天外地内法（仅《金镜》卷四 profile）。

    四库本卷四本段：8/3/4 地内助主，9/2/7/6 天外助客。
    1 宫（以及中五）不在本段两组中，必须保留未定义状态。
    """
    result = _base("J4M-09", "推太乙在天外地内法")

    if taiyi_palace in (8, 3, 4):
        realm = "地内"
        assists = "主"
        movement = "助主人之时，原野不利先起"
    elif taiyi_palace in (9, 2, 7, 6):
        realm = "天外"
        assists = "客"
        movement = "助客之时，安居不利先起"
    else:
        return {
            **result,
            "status": "not_defined_by_source_passage",
            "computable": False,
            "taiyi_palace": taiyi_palace,
            "realm": None,
            "assists": None,
            "canonical_groups": {"地内助主": [8, 3, 4], "天外助客": [9, 2, 7, 6]},
            "policy": "不得把《统宗》卷五的一宫助主规则静默写入《金镜》卷四 canonical。",
        }

    if three_doors_ready is False or five_generals_released is False:
        decisive_ready = False
    elif three_doors_ready is True and five_generals_released is True:
        decisive_ready = True
    else:
        decisive_ready = None

    return {
        **result,
        "status": "ok",
        "computable": True,
        "taiyi_palace": taiyi_palace,
        "realm": realm,
        "assists": assists,
        "movement_note": movement,
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
        "decisive_ready": decisive_ready,
        "canonical_groups": {"地内助主": [8, 3, 4], "天外助客": [9, 2, 7, 6]},
        "policy": "助主客与门具将发分栏；未同时门具将发时不宣称决胜。",
    }


def j4m_low_dependency_catalog():
    """供文档/UI 查询的第一批已实现规则，不参与自动综合胜负。"""
    return {
        "ruleset": J4M_RULESET,
        "source_profile": J4M_SOURCE_PROFILE,
        "implemented": ["J4M-06", "J4M-07", "J4M-09"],
        "pending": [
            "J4M-01", "J4M-02", "J4M-03", "J4M-04", "J4M-05",
            "J4M-08", "J4M-10", "J4M-11", "J4M-12",
        ],
    }
