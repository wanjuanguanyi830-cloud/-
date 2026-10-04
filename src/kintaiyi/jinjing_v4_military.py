"""四库本《太乙金镜式经》卷四军事十二法的来源限定实现。

本模块只实现已经能从卷四正文直接结构化、且不需要借用其他卷次公式的规则。
当前已实现：
- J4M-03 推主客相关法：五行相制核心；“日计纳音”的具体附加角色保留 pending。
- J4M-05 推出师法。
- J4M-06 推陈兵向背。
- J4M-07 推制阵随地法。
- J4M-09 推太乙在天外地内法。
- J4M-10 推奇伏法。

禁止把《太乙统宗宝鉴》卷五或旧项目卷十五的近名函数静默并入本模块。
"""

J4M_RULESET = "jinjing-siku-v4-military-12"
J4M_SOURCE_PROFILE = "jinjing_siku_volume4"


_WUXING_KE = {
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金",
    "金": "木",
}

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

_CHUSHI_CALCS = {12, 22, 32}
_THREE_LUCKY_GATES = {"开", "休", "生"}
_FUBING_CALCS = {12, 22, 32}
_HIDDEN_CALCS = {11, 21, 31}


def _base(rule_id, name):
    return {
        "ruleset": J4M_RULESET,
        "source_profile": J4M_SOURCE_PROFILE,
        "rule_id": rule_id,
        "name": name,
        "source_scope": "太乙金镜式经_四库本_卷四",
    }


def zhuke_xiangguan(host_eye_element, guest_eye_element, *, day_nayin_element=None):
    """J4M-03 推主客相关法。

    正文明确：
    - 客目五行克主目五行 -> 客关得主人，客胜。
    - 主目五行克客目五行 -> 主人关得客，主胜。

    正文同时说“皆用日计纳音以决之”，但本段没有展开纳音如何参与上述
    五行关系。故本函数保留 day_nayin_element 为来源输入，却不擅自用它
    改写胜负。待后续找到明确公式后再升级。
    """
    result = _base("J4M-03", "推主客相关法")
    valid = set(_WUXING_KE)

    if host_eye_element not in valid or guest_eye_element not in valid:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "host_eye_element": host_eye_element,
            "guest_eye_element": guest_eye_element,
            "valid_elements": sorted(valid),
            "policy": "只接受明确五行；不从神名或其他卷次自动反推。",
        }

    if _WUXING_KE[guest_eye_element] == host_eye_element:
        relation = "客关得主人"
        winner = "客"
        loser = "主"
    elif _WUXING_KE[host_eye_element] == guest_eye_element:
        relation = "主人关得客"
        winner = "主"
        loser = "客"
    else:
        relation = None
        winner = None
        loser = None

    if day_nayin_element is None:
        nayin = {
            "value": None,
            "status": "missing",
            "role": "正文要求日计纳音以决之；本段未展开具体接法",
        }
    elif day_nayin_element not in valid:
        nayin = {
            "value": day_nayin_element,
            "status": "invalid",
            "role": "只接受木火土金水；不猜测其他标签",
        }
    else:
        nayin = {
            "value": day_nayin_element,
            "status": "provided_role_pending",
            "role": "已保留来源输入，但不在无明确公式时擅自修改主客胜负",
        }

    return {
        **result,
        "status": "partial_source_specific" if relation else "no_control_relation_defined",
        "computable": True,
        "fully_computable": False,
        "host_eye_element": host_eye_element,
        "guest_eye_element": guest_eye_element,
        "relation": relation,
        "winner": winner,
        "loser": loser,
        "day_nayin": nayin,
        "policy": "五行相制核心按正文与古例实现；日计纳音的具体附加作用保持 pending。",
    }


def chushi_fa(calc_value, *, three_doors_ready=None,
              five_generals_released=None, exit_gate=None):
    """J4M-05 推出师法。

    正文条件分栏：
    - 算十二、二十二、三十二；
    - 五将发；
    - 三门具；
    - 出军取开、休、生三吉门。
    """
    result = _base("J4M-05", "推出师法")
    calc_ready = calc_value in _CHUSHI_CALCS

    if exit_gate is None:
        gate_valid = None
    else:
        gate_valid = exit_gate in _THREE_LUCKY_GATES

    known_prerequisites = (
        isinstance(three_doors_ready, bool)
        and isinstance(five_generals_released, bool)
    )
    source_prerequisites_ready = (
        calc_ready
        and three_doors_ready is True
        and five_generals_released is True
    ) if known_prerequisites else None

    if calc_ready is False:
        status = "hold"
        deployment_ready = False
        verdict = "算非十二、二十二、三十二，本条不据此许出师略地"
    elif three_doors_ready is False or five_generals_released is False:
        status = "hold"
        deployment_ready = False
        verdict = "三门不具或五将不发，不可据本法出兵略地"
    elif not known_prerequisites:
        status = "not_computable"
        deployment_ready = None
        verdict = "缺三门具/五将发的上游事实"
    elif gate_valid is False:
        status = "hold"
        deployment_ready = False
        verdict = "出军门不在开、休、生三吉门"
    elif gate_valid is None:
        status = "ready_pending_gate"
        deployment_ready = None
        verdict = "算、三门、五将条件已具；仍须择开、休、生三吉门出军"
    else:
        status = "ready"
        deployment_ready = True
        verdict = "可依本法出兵略地"

    return {
        **result,
        "status": status,
        "computable": status != "not_computable",
        "calc_value": calc_value,
        "eligible_calcs": sorted(_CHUSHI_CALCS),
        "calc_ready": calc_ready,
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
        "source_prerequisites_ready": source_prerequisites_ready,
        "exit_gate": exit_gate,
        "lucky_gates": ["开", "休", "生"],
        "exit_gate_valid": gate_valid,
        "deployment_ready": deployment_ready,
        "verdict": verdict,
        "policy": "不得以《统宗》卷五人君出师略地的兵额表替代本法。",
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


def qifu_fa(*, army_size=None, calc_value=None, tianmu_location=None,
            yanpo=None, terrain=None, enemy_urgent=False):
    """J4M-10 推奇伏法。

    分别保存：
    - 奇兵约三成；
    - 天目所临为大煞定位输入；
    - 12/22/32 为伏兵时；
    - 11/21/31 为伏藏隐迹、山林沟涧之时；
    - 伏兵取掩迫之时；
    - 敌急则伏于要害。

    不调用旧卷十五 qibing_fubing。
    """
    result = _base("J4M-10", "推奇伏法")

    if army_size is None:
        odd_force_count = None
        odd_force_count_status = "not_requested"
    elif not isinstance(army_size, int) or isinstance(army_size, bool) or army_size <= 0:
        odd_force_count = None
        odd_force_count_status = "invalid_army_size"
    elif army_size % 10 == 0:
        odd_force_count = army_size * 3 // 10
        odd_force_count_status = "exact_from_three_tenths"
    else:
        odd_force_count = None
        odd_force_count_status = "ratio_known_rounding_unspecified"

    ambush_time = calc_value in _FUBING_CALCS if calc_value is not None else None
    concealment_time = calc_value in _HIDDEN_CALCS if calc_value is not None else None

    if yanpo is True:
        yanpo_status = "favorable_required_timing_present"
    elif yanpo is False:
        yanpo_status = "required_timing_absent"
    else:
        yanpo_status = "unknown"

    recommendations = []
    if concealment_time is True:
        recommendations.append("藏于山林沟涧")
    if enemy_urgent:
        recommendations.append("伏于要害")

    return {
        **result,
        "status": "ok",
        "computable": True,
        "army_size": army_size,
        "odd_force_ratio": {"numerator": 3, "denominator": 10},
        "odd_force_count": odd_force_count,
        "odd_force_count_status": odd_force_count_status,
        "calc_value": calc_value,
        "ambush_calcs": sorted(_FUBING_CALCS),
        "concealment_calcs": sorted(_HIDDEN_CALCS),
        "ambush_time": ambush_time,
        "concealment_time": concealment_time,
        "tianmu_location": tianmu_location,
        "great_kill_location": tianmu_location,
        "great_kill_location_note": "正文以天目所临之下为大煞之地",
        "yanpo": yanpo,
        "yanpo_status": yanpo_status,
        "terrain": terrain,
        "enemy_urgent": bool(enemy_urgent),
        "recommendations": recommendations,
        "policy": "奇兵比例、伏兵时、隐迹时、大煞位、掩迫与要害分栏；不借卷十五近名算法补充。",
    }


def j4m_low_dependency_catalog():
    """供文档/UI 查询的已实现规则，不参与自动综合胜负。"""
    return {
        "ruleset": J4M_RULESET,
        "source_profile": J4M_SOURCE_PROFILE,
        "implemented": ["J4M-05", "J4M-06", "J4M-07", "J4M-09", "J4M-10"],
        "partial": ["J4M-03", "J4M-04"],
        "pending": ["J4M-01", "J4M-02", "J4M-08", "J4M-11", "J4M-12"],
    }
