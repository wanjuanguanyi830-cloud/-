"""四库本《太乙金镜式经》卷四军事十二法的来源限定实现。

本模块只实现卷四正文及明确古籍参校能够支持的 source-specific 规则，
不借用《太乙统宗宝鉴》卷五、旧项目卷十五或现代重构近名公式静默补缺。

当前状态：J4M-01..J4M-12 全部已有 runtime（12 complete / 0 partial / 0 pending）。

实现入口：
- J4M-01 推三门具不具：sanmen_jubu / zhimen_from_cycle_count
- J4M-02 推五将发不发：wujiang_fabu
- J4M-03 推主客相关法：j4m03_eye_element_from_god / zhuke_xiangguan
- J4M-04 推主客：zhuke_fa
- J4M-05 推出师法：chushi_fa
- J4M-06 推陈兵向背：chenbing_xiangbei
- J4M-07 推制阵随地法：zhizhen_suidi
- J4M-08 推随地制变：suidi_zhibian
- J4M-09 推太乙在天外地内法：taiyi_tianwai_dinei
- J4M-10 推奇伏法：qifu_fa
- J4M-11 推太乙风云飞鸟助战法：fengyun_feiniao_zhuzhan
- J4M-12 推阵有风云气定胜负：yunqi_dingshengfu

重要边界：
- J4M-03 ≠ J4M-04；
- J4M-07 ≠ J4M-08；
- J4M-09 的《金镜》与《统宗》宫组差异必须分 profile；
- J4M-11/12 必须由外部观测驱动，不得从盘内事实伪造。
"""

from .taiyi_rules import GOD_ALIASES as _GLOBAL_GOD_ALIASES

J4M_RULESET = "jinjing-siku-v4-military-12"
J4M_SOURCE_PROFILE = "jinjing_siku_volume4"


_WUXING_KE = {
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金",
    "金": "木",
}

_WUXING_SHENG = {
    "木": "火",
    "火": "土",
    "土": "金",
    "金": "水",
    "水": "木",
}

# 《太乙淘金歌》“定胜负”注所列二目纳音/十六神五行。
# 这里只用于 J4M-03 的古籍参校与输入归一化，不等于现代“双纳音”重构体系。
_J4M03_GOD_ELEMENT = {
    "武德": "金", "太簇": "金", "阴德": "金",
    "吕申": "木", "高丛": "木", "大炅": "木",
    "大义": "水", "地主": "水",
    "大神": "火", "大威": "火",
    "和德": "土", "太阳": "土", "天道": "土",
    "大武": "土", "阴主": "土", "阳德": "土",
}

# 四库卷四 J4M-03 例文可见“太蔟”；项目规范词形沿用“太簇”。
# 这是同名异体/传本文字归一，不是另一个神名，也不改变五行。
_J4M03_GOD_ALIASES = {
    "太蔟": _GLOBAL_GOD_ALIASES["太蔟"],
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

_EIGHT_GATES = ["开", "休", "生", "伤", "杜", "景", "死", "惊"]
_SANMEN = {"开", "休", "生"}
_GATE_AUSPICE = {
    "开": "大吉",
    "休": "大吉",
    "生": "大吉",
    "景": "小吉",
    "死": "大凶",
    "惊": "大凶",
    "伤": "大凶",
    "杜": "大凶",
}

_TERRAIN_ARMS = {
    "沟堑山林川泽丘阜草木": {
        "利": "步兵",
        "不利": "车骑",
        "source_ratio_text": "车骑三不当一步兵",
        "source_scope": "五丈之沟、居堑之水、山林积石、川泽丘阜、草木所临",
    },
    "平陵平原广野": {
        "利": "车骑",
        "不利": "步兵",
        "source_ratio_text": "步兵十不当一车骑",
        "source_scope": "土水平陵、曼衍相属、平原广野",
    },
    "两阵相近平地浅草": {
        "利": "长戟",
        "不利": "剑楯",
        "source_ratio_text": "剑楯三不当一长戟",
        "source_scope": "两阵相近、平地浅草、可前可后",
    },
    "萑苇竹萧蒙笼草木": {
        "利": "矛鋋",
        "不利": "弓弩",
        "source_ratio_text": "弓弩三不当一矛鋋",
        "source_scope": "萑苇竹萧、草木蒙笼、枝叶接茂",
    },
    "平阳相远山谷幽涧仰高临下": {
        "利": "弓弩",
        "不利": "短兵",
        "source_ratio_text": "短兵百不当一弓弩",
        "source_scope": "平阳相远、山谷幽涧、仰高临下",
    },
}


_J4M11_ANCHORS = {"太乙所在宫", "大将宫", "主目", "客目", "主人形", "太岁", "太阴", "月建", "主人阵", "客阵", "阵中"}
_J4M11_PHENOMENA = {"风", "云", "飞鸟", "风云", "风云飞鸟"}

_ZHUKE_START_DEITIES = {
    "东": "阴德",
    "南": "和德",
    "西": "大炅",
    "北": "大武",
}

_YUNQI_TABLE = {
    "北": {
        "黑": {"verdict": "大胜", "qi_class": "胜气", "subject_mode": "formation", "day_stems_good": ["壬", "癸"]},
        "白": {"verdict": "欲罢阵求和", "qi_class": "和解", "subject_mode": "formation"},
        "青": {"verdict": "将宽缓，急击则平", "qi_class": "迟缓", "subject_mode": "formation_general"},
        "红": {"verdict": "客胜", "qi_class": "客胜", "subject_mode": "guest_role"},
        "黄": {"verdict": "大败", "qi_class": "败气", "subject_mode": "formation", "day_stems_bad": ["壬", "癸"]},
    },
    "南": {
        "赤": {"verdict": "大胜", "qi_class": "胜气", "subject_mode": "formation", "day_stems_good": ["丙", "丁"]},
        "青": {"verdict": "欲罢阵求解", "qi_class": "和解", "subject_mode": "formation"},
        "黄": {"verdict": "将迟钝，急击则平", "qi_class": "迟缓", "subject_mode": "formation_general"},
        "白": {"verdict": "失利", "qi_class": "不利", "subject_mode": "formation"},
        "黑": {"verdict": "大败", "qi_class": "败气", "subject_mode": "formation", "day_stems_bad": ["丙", "丁"]},
    },
    "西": {
        # 四库正文这里只写“庚辛日弥佳”，没有明写“大胜”。
        # 不按五行对称性补成胜气。
        "白": {
            "verdict": None,
            "qi_class": "基础胜负未明",
            "subject_mode": "formation",
            "day_stems_good": ["庚", "辛"],
            "source_note": "白云气在敌阵上，庚辛日弥佳；本句未明写基础胜负。",
        },
        "黄": {"verdict": "欲求解", "qi_class": "和解", "subject_mode": "formation"},
        "黑": {"verdict": "将宽缓，急击平", "qi_class": "迟缓", "subject_mode": "formation_general"},
        "青": {"verdict": "败", "qi_class": "败气", "subject_mode": "formation"},
        "赤": {"verdict": "大败", "qi_class": "败气", "subject_mode": "formation", "day_stems_bad": ["庚", "辛"]},
    },
    "东": {
        "青": {"verdict": "大胜", "qi_class": "胜气", "subject_mode": "formation", "day_stems_good": ["甲", "乙"]},
        "黑": {"verdict": "欲求和", "qi_class": "和解", "subject_mode": "formation"},
        "赤": {"verdict": "将迟钝，然不可击", "qi_class": "迟缓勿击", "subject_mode": "formation_general"},
        "黄": {"verdict": "大败", "qi_class": "败气", "subject_mode": "formation", "day_stems_bad": ["甲", "乙"]},
    },
}

def _base(rule_id, name):
    return {
        "ruleset": J4M_RULESET,
        "source_profile": J4M_SOURCE_PROFILE,
        "rule_id": rule_id,
        "name": name,
        "source_scope": "太乙金镜式经_四库本_卷四",
    }


def zhimen_from_cycle_count(period_count):
    """J4M-01 直门 240/30 轮转辅助。

    正文以二百四十为一周、每三十移一门，并明言上元甲子开门直使，
    满三十年后休门直使。这里只接收已经换算好的 1-based 周期计数，
    不在此函数中发明年/月/日/时的历法换算。
    """
    result = _base("J4M-01", "推三门具不具")
    if not isinstance(period_count, int) or isinstance(period_count, bool) or period_count <= 0:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "period_count": period_count,
            "policy": "须给出正整数的周期累计数；年月日时如何取得该数由各自上游历法层负责。",
        }

    within_cycle = (period_count - 1) % 240 + 1
    gate_index = (within_cycle - 1) // 30
    direct_gate = _EIGHT_GATES[gate_index]
    return {
        **result,
        "status": "ok",
        "computable": True,
        "period_count": period_count,
        "within_240_cycle": within_cycle,
        "block_of_30": gate_index + 1,
        "direct_gate": direct_gate,
        "gate_order": list(_EIGHT_GATES),
        "auspice": _GATE_AUSPICE[direct_gate],
        "policy": "只实现正文明确的240周、30一移；不替代第一卷时计八门算法。",
    }


def sanmen_jubu(*, taiyi_gate=None, tianmu_gate=None, direct_gate=None):
    """J4M-01 推三门具不具。

    原文明确覆盖的组合：
    - 太乙、天目分临开/生二门 -> 两门不具；
    - 太乙或天目临休门 -> 三门不具。

    对同落开、同落生、只给一端等原文未在本句展开的组合，不自行类推。
    direct_gate 仅用于保存州郡岁计直门吉凶，不替代门具判定。
    """
    result = _base("J4M-01", "推三门具不具")

    if direct_gate is None:
        direct_gate_auspice = None
    elif direct_gate in _GATE_AUSPICE:
        direct_gate_auspice = _GATE_AUSPICE[direct_gate]
    else:
        direct_gate_auspice = "unknown_gate"

    known_gates = set(_EIGHT_GATES)
    if taiyi_gate is not None and taiyi_gate not in known_gates:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "taiyi_gate": taiyi_gate,
            "tianmu_gate": tianmu_gate,
            "valid_gates": list(_EIGHT_GATES),
            "policy": "太乙所临门名无效；不从宫位自动反推八门。",
        }
    if tianmu_gate is not None and tianmu_gate not in known_gates:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "taiyi_gate": taiyi_gate,
            "tianmu_gate": tianmu_gate,
            "valid_gates": list(_EIGHT_GATES),
            "policy": "天目所临门名无效；不从神名或其他卷次自动反推八门。",
        }

    gates = {g for g in (taiyi_gate, tianmu_gate) if g is not None}
    if "休" in gates:
        status = "three_doors_not_ready"
        not_ready_count = 3
        three_doors_ready = False
        source_case = "临休门"
    elif taiyi_gate is not None and tianmu_gate is not None and gates == {"开", "生"}:
        status = "two_doors_not_ready"
        not_ready_count = 2
        three_doors_ready = False
        source_case = "太乙天目分临开生二门"
    elif taiyi_gate is None or tianmu_gate is None:
        status = "not_computable"
        not_ready_count = None
        three_doors_ready = None
        source_case = "缺太乙或天目所临门"
    else:
        status = "not_defined_by_source_passage"
        not_ready_count = None
        three_doors_ready = None
        source_case = "本句未展开该组合"

    return {
        **result,
        "status": status,
        "computable": three_doors_ready is not None,
        "taiyi_gate": taiyi_gate,
        "tianmu_gate": tianmu_gate,
        "three_doors": ["开", "休", "生"],
        "three_doors_ready": three_doors_ready,
        "not_ready_count": not_ready_count,
        "source_case": source_case,
        "direct_gate": direct_gate,
        "direct_gate_auspice": direct_gate_auspice,
        "auspice_table": dict(_GATE_AUSPICE),
        "policy": "只判正文明确组合；州郡岁计直门吉凶与门具事实分栏。",
    }


def wujiang_fabu(*, shiji_yanji=None, wenchang_qiupo=None,
                 major_minor_generals_related=None, three_doors_ready=None):
    """J4M-02 推五将发不发。

    五将本体阻断条件：
    - 始击有掩击；
    - 文昌有囚迫；
    - 主客大小将有相关。

    三门具/不具作为独立上游事实保留，不用它覆盖三组五将条件。
    """
    result = _base("J4M-02", "推五将发不发")
    facts = {
        "shiji_yanji": shiji_yanji,
        "wenchang_qiupo": wenchang_qiupo,
        "major_minor_generals_related": major_minor_generals_related,
    }
    if any(v is not None and not isinstance(v, bool) for v in facts.values()):
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            **facts,
            "three_doors_ready": three_doors_ready,
            "policy": "掩击、囚迫、大小将相关必须是显式布尔事实；不解析旧字符串格局。",
        }

    all_known = all(isinstance(v, bool) for v in facts.values())
    if all_known:
        blockers = []
        if shiji_yanji:
            blockers.append("始击有掩击")
        if wenchang_qiupo:
            blockers.append("文昌有囚迫")
        if major_minor_generals_related:
            blockers.append("主客大小将有相关")
        five_generals_released = not blockers
    else:
        blockers = None
        five_generals_released = None

    if three_doors_ready is False or five_generals_released is False:
        combined_ready = False
    elif three_doors_ready is True and five_generals_released is True:
        combined_ready = True
    else:
        combined_ready = None

    return {
        **result,
        "status": "ok" if all_known else "not_computable",
        "computable": all_known,
        **facts,
        "blockers": blockers,
        "five_generals_released": five_generals_released,
        "three_doors_ready": three_doors_ready,
        "combined_ready": combined_ready,
        "deployment_allowed_by_doors": three_doors_ready if isinstance(three_doors_ready, bool) else None,
        "engagement_allowed_by_generals": five_generals_released,
        "source_notes": {
            "三门不具": "不可出兵",
            "五将不发": "不可临战",
            "三门具": "五将自然相会（保存为原文说明，不覆盖三组阻断事实）",
        },
        "policy": "五将条件与三门条件分栏；不照搬旧 fivegenerals() 的字符串/中五混合判断。",
    }


def suidi_zhibian(terrain_class, *, soldiers_trained=None,
                  equipment_serviceable=None, general_knows_warfare=None,
                  ruler_selects_generals=None):
    """J4M-08 推随地制变。

    只按正文保存五类地形与优势兵种/兵器，以及训练、器械、将、君四层警告。
    “三不当一/十不当一/百不当一”保留原文比例文字，不强行解释为现代战力倍数。
    """
    result = _base("J4M-08", "推随地制变")
    terrain = _TERRAIN_ARMS.get(terrain_class)

    if terrain is None:
        terrain_status = "unknown"
        terrain_payload = {
            "terrain_class": terrain_class,
            "known_terrain_classes": list(_TERRAIN_ARMS),
            "favored": None,
            "disfavored": None,
            "source_ratio_text": None,
        }
    else:
        terrain_status = "known"
        terrain_payload = {
            "terrain_class": terrain_class,
            "known_terrain_classes": list(_TERRAIN_ARMS),
            "favored": terrain["利"],
            "disfavored": terrain["不利"],
            "source_ratio_text": terrain["source_ratio_text"],
            "source_scope": terrain["source_scope"],
        }

    facts = {
        "soldiers_trained": soldiers_trained,
        "equipment_serviceable": equipment_serviceable,
        "general_knows_warfare": general_knows_warfare,
        "ruler_selects_generals": ruler_selects_generals,
    }
    invalid = [k for k, v in facts.items() if v is not None and not isinstance(v, bool)]
    if invalid:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            **terrain_payload,
            "invalid_facts": invalid,
            "policy": "训练、器械、将知兵、君择将均须显式布尔事实。",
        }

    warnings = []
    if soldiers_trained is False:
        warnings.append("士不选练、卒不服习：原文列为百不当一之失")
    if equipment_serviceable is False:
        warnings.append("器械不利：以其卒与敌")
    if general_knows_warfare is False:
        warnings.append("将不知兵：以其主与敌")
    if ruler_selects_generals is False:
        warnings.append("君不择将：以其国与敌")

    return {
        **result,
        "status": "ok" if terrain_status == "known" else "not_computable",
        "computable": terrain_status == "known",
        **terrain_payload,
        **facts,
        "urgent_requirements": ["士卒服习", "随其地形", "善用兵器"],
        "warnings": warnings,
        "doctrine_chain": [
            "器械不利，以其卒与敌",
            "卒不可用，以其将与敌",
            "将不知兵，以其主与敌",
            "君不择将，以其国与敌",
        ],
        "quotation_collation": {
            "status": "jinjing_quote_diverges_from_jingyou_and_hanshu",
            "canonical_for_this_profile": "太乙金镜式经_四库本_卷四实际引文",
            "external_witness": "汉书_爰盎晁错传",
            "notable_differences": [
                "金镜步兵地作车骑三不当一；汉书作车骑二不当一",
                "金镜与汉书此处兵器名同为矛鋋；差异在金镜作弓弩三不当一、汉书作长戟二不当一",
                "汉书另有曲道相伏、险厄相薄之剑楯地；金镜本段未录",
                "金镜士卒不练作百不当一、将不习兵作十不当一；汉书分别作百不当十、五不当一",
            ],
            "do_not_silent_emend": True,
        },
        "policy": (
            "J4M-08 是地形—兵种/兵器—训练器械层；不得并入 J4M-07 阵形五行。"
            "C79 已按 CADAL06056494 p.136 将旧误读“矛锤”改回“矛鋋”；《汉书》《福应经》只作异文校勘见证，不静默改写《金镜》source profile。"
        ),
    }


def j4m03_eye_element_from_god(god):
    """按古籍参校表把二目所临十六神归一为五行。

    《太乙金镜式经》卷二在“上下二目”配对义中：
    - 上目 = 始击 = 客；
    - 下目 = 文昌 = 主。

    J4M-03 正文例称“地目/天目”，此处为避免“天目”一词多义，
    运行接口统一使用 host/guest，不再用天目/地目作参数名。
    """
    if god is None:
        return None
    normalized = _J4M03_GOD_ALIASES.get(god, god)
    return _J4M03_GOD_ELEMENT.get(normalized)


def zhuke_xiangguan(host_eye_element=None, guest_eye_element=None, *,
                    host_eye_god=None, guest_eye_god=None,
                    calculation_scope="日计", day_nayin_element=None):
    """J4M-03 推主客相关法。

    经重新校勘：
    - 《金镜》卷四写“皆用日计纳音以决之”；
    - 《景祐太乙福应经》对应条文作“日计二目纳音”；
    - 《太乙淘金歌》“定胜负”明确说“以二目纳音决之，取五行生克为用”，
      并列十六神所属金木水火土。

    因此 canonical 不再把 day_nayin_element 解释成“当天干支的六十甲子纳音”。
    它保留为旧 API 兼容字段，但不参与 J4M-03 判定。

    canonical 明确部分：
    - 客目五行克主目五行 -> 客关得主人，客胜；
    - 主目五行克客目五行 -> 主人关得客，主胜；
    - 无相制时，J4M-03 本条不强宣主客胜负。

    《淘金歌》另有“同音二阵平”以及相生“战必和解”的参校说明，
    只作为 collation_hint 返回，不反写《金镜》本条的 winner。
    """
    result = _base("J4M-03", "推主客相关法")
    valid = set(_WUXING_KE)

    if calculation_scope != "日计":
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "calculation_scope": calculation_scope,
            "required_scope": "日计",
            "policy": "《金镜》本条明言用日计二目纳音；其他计层不得自动套用本 canonical。",
        }

    host_eye_god_canonical = _J4M03_GOD_ALIASES.get(host_eye_god, host_eye_god)
    guest_eye_god_canonical = _J4M03_GOD_ALIASES.get(guest_eye_god, guest_eye_god)
    host_from_god = j4m03_eye_element_from_god(host_eye_god)
    guest_from_god = j4m03_eye_element_from_god(guest_eye_god)

    if host_eye_element is None:
        host_eye_element = host_from_god
    elif host_from_god is not None and host_eye_element != host_from_god:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "host_eye_element": host_eye_element,
            "host_eye_god": host_eye_god,
            "god_resolved_element": host_from_god,
            "policy": "主目显式五行与古籍参校神名五行冲突；不自动择一。",
        }

    if guest_eye_element is None:
        guest_eye_element = guest_from_god
    elif guest_from_god is not None and guest_eye_element != guest_from_god:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "guest_eye_element": guest_eye_element,
            "guest_eye_god": guest_eye_god,
            "god_resolved_element": guest_from_god,
            "policy": "客目显式五行与古籍参校神名五行冲突；不自动择一。",
        }

    if host_eye_element not in valid or guest_eye_element not in valid:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "host_eye_element": host_eye_element,
            "guest_eye_element": guest_eye_element,
            "host_eye_god": host_eye_god,
            "guest_eye_god": guest_eye_god,
            "valid_elements": sorted(valid),
            "known_gods": sorted(_J4M03_GOD_ELEMENT),
            "policy": "必须给出主客二目五行，或给出可由古籍十六神表归一的神名。",
        }

    if _WUXING_KE[guest_eye_element] == host_eye_element:
        relation = "客关得主人"
        winner = "客"
        loser = "主"
        canonical_outcome = "客胜"
    elif _WUXING_KE[host_eye_element] == guest_eye_element:
        relation = "主人关得客"
        winner = "主"
        loser = "客"
        canonical_outcome = "主胜"
    else:
        relation = None
        winner = None
        loser = None
        canonical_outcome = "本条无相制关关系"

    if host_eye_element == guest_eye_element:
        collation_hint = {
            "source": "太乙淘金歌",
            "kind": "same_element",
            "verdict": "二阵平",
            "canonical_override": False,
        }
    elif (_WUXING_SHENG[host_eye_element] == guest_eye_element
          or _WUXING_SHENG[guest_eye_element] == host_eye_element):
        collation_hint = {
            "source": "太乙淘金歌注",
            "kind": "generating_relation",
            "verdict": "相生则和解",
            "canonical_override": False,
        }
    else:
        collation_hint = None

    legacy_day_nayin = {
        "value": day_nayin_element,
        "status": "legacy_input_ignored" if day_nayin_element is not None else "not_used",
        "role": (
            "旧版接口曾把“日计纳音”误建模为独立当天干支纳音五行；"
            "现按《福应经》“日计二目纳音”与《淘金歌》二目五行参校，不再参与判定。"
        ),
    }

    return {
        **result,
        "status": "ok",
        "computable": True,
        "fully_computable": True,
        "calculation_scope": "日计",
        "host_eye_element": host_eye_element,
        "guest_eye_element": guest_eye_element,
        "host_eye_god": host_eye_god,
        "guest_eye_god": guest_eye_god,
        "host_eye_god_canonical": host_eye_god_canonical,
        "guest_eye_god_canonical": guest_eye_god_canonical,
        "relation": relation,
        "winner": winner,
        "loser": loser,
        "canonical_outcome": canonical_outcome,
        "collation_hint": collation_hint,
        "legacy_day_nayin": legacy_day_nayin,
        "eye_role_convention": {
            "主": ["文昌", "下目", "地目（本条配对义）"],
            "客": ["始击", "上目", "天目（本条配对义）"],
            "warning": "“天目”在太乙文献中有多义；J4M-03 接口只用主目/客目避免歧义。",
        },
        "god_element_table": dict(_J4M03_GOD_ELEMENT),
        "god_name_aliases": dict(_J4M03_GOD_ALIASES),
        "policy": "canonical 只以日计主客二目所临神五行相制判关胜负；太蔟按四库例文归一为规范词形太簇；淘金歌同音/相生只作参校提示。",
    }

def zhuke_fa(context, *, three_doors_ready=None, five_generals_released=None,
             yin_yang_harmonious=None, direction=None,
             host_calc=None, guest_calc=None):
    """J4M-04 推主客。

    将正文拆成四层：
    1. 陈兵原野 / 安居之势的主客角色；
    2. 三门、五将、阴阳和不和的行动姿态；
    3. 东南西北四方始发神；
    4. 客欲知主、主人欲知客时“视其算”的互查关系。

    “先胜后负”经《武经总要》《太乙秘书》同段参校，明确为
    “先起则胜，后起则败”；仅在三门具、五将发、阴阳和的有利三项中
    按当前场景的先起/后应角色落实胜负。
    """
    result = _base("J4M-04", "推主客")

    contexts = {
        "陈兵原野": {"first_mover": "客", "responder": "主"},
        "field_battle": {"first_mover": "客", "responder": "主"},
        "安居之势": {"first_mover": "主", "responder": "客"},
        "settled_context": {"first_mover": "主", "responder": "客"},
    }
    if context not in contexts:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "context": context,
            "valid_contexts": ["陈兵原野", "安居之势"],
            "policy": "只接受正文明确的陈兵原野/安居之势；不把其他场景自动映射为主客。",
        }

    role = contexts[context]
    role_context = "陈兵原野" if context in {"陈兵原野", "field_battle"} else "安居之势"

    readiness = {
        "three_doors_ready": three_doors_ready,
        "five_generals_released": five_generals_released,
        "yin_yang_harmonious": yin_yang_harmonious,
    }
    invalid = [k for k, v in readiness.items() if v is not None and not isinstance(v, bool)]
    if invalid:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "context": role_context,
            "roles": dict(role),
            **readiness,
            "invalid_readiness_fields": invalid,
            "policy": "三门、五将、阴阳和不和必须作为显式布尔事实输入。",
        }

    all_known = all(isinstance(v, bool) for v in readiness.values())
    all_favorable = all_known and all(readiness.values())
    all_unfavorable = all_known and not any(readiness.values())

    blockers = []
    if three_doors_ready is False:
        blockers.append("三门不具：不可出兵")
    if five_generals_released is False:
        blockers.append("五将不发：不可临战")
    if yin_yang_harmonious is False:
        blockers.append("阴阳不和")

    if all_favorable:
        action_status = "raise_forces_favorable"
        action_advice = "称兵"
        source_campaign_verdict = "所向必克"
        source_temporal_outcome = "先起者胜，后起者负"
        source_combination_status = "explicit_favorable_triad"
        winner = role["first_mover"]
        loser = role["responder"]
        winner_basis = (
            "《金镜》本句“先胜后负”经《武经总要》与《太乙秘书》"
            "同段“先起则胜，后起则败”参校，按本场景先起/后应角色落实。"
        )
    elif all_unfavorable:
        action_status = "hold_and_defend"
        action_advice = "不利举兵，宜固守吉"
        source_campaign_verdict = None
        source_temporal_outcome = None
        source_combination_status = "explicit_unfavorable_triad"
        winner = None
        loser = None
        winner_basis = None
    elif blockers:
        action_status = "blocked_or_mixed"
        action_advice = blockers[0] if len(blockers) == 1 else "；".join(blockers)
        source_campaign_verdict = None
        source_temporal_outcome = None
        source_combination_status = "mixed_combination_not_fully_expanded_by_j4m04"
        winner = None
        loser = None
        winner_basis = None
    elif not all_known:
        action_status = "not_computable"
        action_advice = "缺三门、五将或阴阳和不和事实"
        source_campaign_verdict = None
        source_temporal_outcome = None
        source_combination_status = "missing_inputs"
        winner = None
        loser = None
        winner_basis = None
    else:
        action_status = "mixed_combination_not_defined"
        action_advice = "正文只明确三项皆和与三项皆不和；该混合组合不扩写。"
        source_campaign_verdict = None
        source_temporal_outcome = None
        source_combination_status = "mixed_combination_not_fully_expanded_by_j4m04"
        winner = None
        loser = None
        winner_basis = None

    if direction is None:
        start_deity = None
        direction_status = "not_requested"
    elif direction in _ZHUKE_START_DEITIES:
        start_deity = _ZHUKE_START_DEITIES[direction]
        direction_status = "ok"
    else:
        start_deity = None
        direction_status = "not_defined_by_source_passage"

    return {
        **result,
        "status": "ok" if action_status not in {"not_computable", "mixed_combination_not_defined"} else action_status,
        "computable": action_status != "not_computable",
        "role_computable": True,
        "source_combination_computable": all_favorable or all_unfavorable,
        "hard_constraints_computable": bool(blockers),
        "context": role_context,
        "roles": {
            "first_mover": role["first_mover"],
            "responder": role["responder"],
        },
        **readiness,
        "blockers": blockers,
        "action_status": action_status,
        "action_advice": action_advice,
        "source_combination_status": source_combination_status,
        "source_campaign_verdict": source_campaign_verdict,
        "source_temporal_outcome": source_temporal_outcome,
        "winner": winner,
        "loser": loser,
        "winner_basis": winner_basis,
        "temporal_outcome_policy": (
            "“先胜后负”已由《武经总要》《太乙秘书》同段明确句读为"
            "“先起则胜，后起则败”；只在三门具、五将发、阴阳和的明确有利三项时落实胜负。"
            "《金镜》不利三项只明言不利举兵、宜固守，其他传本的“先起者败后起者胜”不自动回写。"
        ),
        "direction": direction,
        "start_deity": start_deity,
        "direction_status": direction_status,
        "start_deity_table": dict(_ZHUKE_START_DEITIES),
        "origin_return_method": "以始发之神定主客所起归之神；本段未展开进一步推步公式。",
        "host_calc": host_calc,
        "guest_calc": guest_calc,
        "cross_side_calc_reference": {
            "客欲知主": {"source_text": "视其算所知也", "target_calc": "主算", "value": host_calc},
            "主人欲知客": {"source_text": "亦视其算所知也", "target_calc": "客算", "value": guest_calc},
        },
        "policy": "J4M-04 不覆盖 J4M-03 五行相关胜负，也不覆盖 D8-06 多少胜负；角色、行动、始发神、互视其算分栏。",
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


def _formation_control_outcome(host_formation=None, guest_formation=None):
    """J4M-07 主客阵形五行相克胜负。

    原文只明言“次以五行相克而取胜负”，因此只在一方阵形五行明确克
    另一方时给出胜负；同五行或相生关系不补断。
    """
    valid = set(_FORMATION_ELEMENTS)
    if host_formation is None and guest_formation is None:
        return {
            "status": "not_requested",
            "computable": False,
            "host_formation": None,
            "guest_formation": None,
            "winner": None,
            "loser": None,
        }
    if host_formation not in valid or guest_formation not in valid:
        return {
            "status": "not_computable",
            "computable": False,
            "host_formation": host_formation,
            "guest_formation": guest_formation,
            "valid_formations": list(_FORMATION_ELEMENTS),
            "winner": None,
            "loser": None,
        }

    host_element = _FORMATION_ELEMENTS[host_formation]
    guest_element = _FORMATION_ELEMENTS[guest_formation]
    if _WUXING_KE[host_element] == guest_element:
        winner, loser, relation = "主", "客", "主阵五行克客阵五行"
    elif _WUXING_KE[guest_element] == host_element:
        winner, loser, relation = "客", "主", "客阵五行克主阵五行"
    else:
        winner, loser, relation = None, None, "本条无五行相克关系"

    return {
        "status": "ok",
        "computable": True,
        "host_formation": host_formation,
        "host_element": host_element,
        "guest_formation": guest_formation,
        "guest_element": guest_element,
        "relation": relation,
        "winner": winner,
        "loser": loser,
        "policy": "只按阵形五行相克取胜负；同类或相生不以常识补出胜负。",
    }


def zhizhen_suidi(terrain, *, host_formation=None, guest_formation=None):
    """J4M-07 推制阵随地法。

    分两层保存原文：
    1. 地形 -> 宜阵 -> 阵形五行；
    2. 主客已经置阵时，以两阵五行相克取胜负。

    第二层不要求把同一个 terrain 同时强配给主客双方。
    """
    result = _base("J4M-07", "推制阵随地法")
    contest = _formation_control_outcome(host_formation, guest_formation)

    if terrain not in _TERRAIN_FORMATIONS:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "terrain": terrain,
            "known_terrains": list(_TERRAIN_FORMATIONS),
            "formation_elements": dict(_FORMATION_ELEMENTS),
            "formation_contest": contest,
            "policy": (
                "未知地形不类推；若已显式给出主客阵形，五行相克结果仍独立保存在"
                "formation_contest。J4M-07 不与 J4M-08 随地制变合并。"
            ),
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
        "formation_contest": contest,
        "direction_relation": {"顺其向": "吉", "反其向": "凶"},
        "policy": (
            "本条同时保留地形制阵与主客阵形五行相克两层；兵种器械随地应变属于 J4M-08。"
            "阵形同类或相生时原文未给本条胜负，不扩写。"
        ),
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



def fengyun_feiniao_zhuzhan(events):
    """J4M-11 推太乙风云飞鸟助战法。

    events 必须是外部观测事实列表；每条只匹配正文明确事件。
    不从太乙盘位、天气 API 或旧 flybird_wl 自动伪造观测。
    """
    result = _base("J4M-11", "推太乙风云飞鸟助战法")
    if not events:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "events": events,
            "judgments": [],
            "policy": "无风、云、飞鸟外部观测时不得从盘内字段推造结果。",
        }
    if not isinstance(events, list) or any(not isinstance(e, dict) for e in events):
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "events": events,
            "judgments": [],
            "policy": "events 必须是观测字典列表。",
        }

    judgments = []
    for index, event in enumerate(events):
        phenomenon = event.get("phenomenon")
        action = event.get("action")
        source_anchor = event.get("source_anchor")
        target = event.get("target")
        flag_broken = event.get("flag_broken")
        birds_circling = event.get("birds_circling")
        returning_wind = event.get("returning_wind")
        crowd_noisy = event.get("crowd_noisy")

        judgment = {
            "index": index,
            "phenomenon": phenomenon,
            "action": action,
            "source_anchor": source_anchor,
            "target": target,
            "matched": True,
            "winner": None,
            "loser": None,
            "omen": None,
            "source_case": None,
        }

        if phenomenon not in _J4M11_PHENOMENA:
            judgment.update(
                matched=False,
                source_case="缺失或未知观测类型",
                note="必须明确记录风、云、飞鸟及其组合；缺失 phenomenon 也不得仅凭动作字段生成古籍断语。",
            )
        elif source_anchor == "太乙所在宫" and target == "太乙" and action in {"冲格", "迫击", "冲格迫击"}:
            judgment.update(
                omen="大败之兆",
                source_case="太乙所在宫风云飞鸟冲格迫击太乙",
            )
        elif target == "大将宫" and action == "迫击":
            judgment.update(
                loser="主",
                source_case="迫击大将宫",
            )
        elif source_anchor == "主目" and target == "客" and action in {"击", "去击"}:
            judgment.update(
                loser="客",
                source_case="从主目上去击客",
            )
        elif source_anchor == "客目" and target == "主" and action == "击":
            judgment.update(
                loser="主",
                source_case="从客目上击主",
            )
        elif source_anchor == "主人形" and action in {"来", "上来"}:
            judgment.update(
                loser="客",
                source_case="从主人形上来",
            )
        elif source_anchor in {"太岁", "太阴", "月建"} and action == "击" and target in {"主人", "主"}:
            judgment.update(
                loser="主",
                source_case=f"从{source_anchor}上来击主人",
            )
        elif source_anchor in {"太岁", "太阴", "月建"} and action == "击" and target == "客":
            judgment.update(
                loser="客",
                source_case=f"从{source_anchor}上来击客",
            )
        elif action == "扶" and target in {"主人阵", "主阵"}:
            judgment.update(
                winner="主",
                source_case="扶主人阵",
            )
        elif action == "扶" and target == "客阵":
            judgment.update(
                winner="客",
                source_case="扶客阵",
            )
        elif returning_wind is True and birds_circling is True and flag_broken is True:
            judgment.update(
                omen="大败之兆",
                source_case="回风起伏、飞鸟旋转阵中且旗折",
            )
        elif action == "冲突" and target in {"主人阵", "主阵"}:
            judgment.update(
                loser="主",
                source_case="风云冲突主人阵",
            )
        elif action == "冲突" and target == "客阵":
            judgment.update(
                loser="客",
                source_case="风云冲突客阵",
            )
        elif crowd_noisy is True or action == "噪阵":
            judgment.update(
                matched=False,
                source_case="众来噪阵",
                note="正文提及众来噪阵，但本句未单独明示其独立胜负结果，故只记观测不补断。",
            )
        else:
            judgment.update(
                matched=False,
                source_case="正文未覆盖该观测组合",
                note="不把旧 flybird_wl 或近似空间关系补入《金镜》卷四 canonical。",
            )

        judgments.append(judgment)

    matched = [j for j in judgments if j["matched"]]
    return {
        **result,
        "status": "ok" if matched else "not_defined_by_source_passage",
        "computable": bool(matched),
        "events": events,
        "judgments": judgments,
        "observation_schema": {
            "phenomenon": sorted(_J4M11_PHENOMENA),
            "source_anchor": sorted(_J4M11_ANCHORS),
            "fields": [
                "phenomenon", "action", "source_anchor", "target",
                "returning_wind", "birds_circling", "flag_broken", "crowd_noisy",
            ],
        },
        "policy": (
            "逐条解释外部观测；每条必须明确 phenomenon 为风/云/飞鸟类，"
            "动作词只接受《金镜》本条明写值，不把近义词自动视作等价。"
            "允许同日多事件并存，不强制折算为单一总胜负。"
        ),
    }


def yunqi_dingshengfu(*, formation_direction=None, cloud_color=None,
                      observed_formation="敌", day_stem=None,
                      cloud_present=True, continuity=None,
                      disorder=None, motion_advantage=None,
                      over_general=None):
    """J4M-12 推阵有风云气定胜负。

    以“云气所覆阵的方位 + 颜色”为基础表，再分栏保存日干、聚散动静、
    大将/参将位置修正。无云气时返回原文“无战或相匀”，不造胜负。
    """
    result = _base("J4M-12", "推阵有风云气定胜负")

    if cloud_present is False:
        return {
            **result,
            "status": "no_cloud",
            "computable": True,
            "cloud_present": False,
            "verdict": None,
            "source_note": "若都无云气，多少方分无战或复相匀",
            "policy": "无云气不强判胜负。",
        }

    if cloud_present is not True:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "cloud_present": cloud_present,
            "policy": "cloud_present 必须显式为 True/False。",
        }

    if observed_formation not in {"敌", "我"}:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "observed_formation": observed_formation,
            "valid_observed_formations": ["敌", "我"],
            "policy": "原文只比较敌阵与我阵；须显式标明云气所覆的是敌阵还是我阵。",
        }

    if formation_direction not in _YUNQI_TABLE:
        return {
            **result,
            "status": "not_computable",
            "computable": False,
            "formation_direction": formation_direction,
            "valid_directions": list(_YUNQI_TABLE),
            "policy": "须给出云气所覆阵的东/南/西/北方位。",
        }

    table = _YUNQI_TABLE[formation_direction]
    if cloud_color not in table:
        return {
            **result,
            "status": "not_defined_by_source_passage",
            "computable": False,
            "formation_direction": formation_direction,
            "cloud_color": cloud_color,
            "defined_colors": list(table),
            "policy": "该方位正文未列此颜色时保持未定义，不以五行生克补表。",
        }

    item = dict(table[cloud_color])

    subject_mode = item.get("subject_mode", "formation")
    if subject_mode == "guest_role":
        verdict_subject = "客"
    elif subject_mode == "formation_general":
        verdict_subject = f"{observed_formation}将"
    else:
        verdict_subject = observed_formation

    day_modifier = None
    if day_stem is not None:
        if day_stem in item.get("day_stems_good", []):
            day_modifier = "弥佳"
        elif day_stem in item.get("day_stems_bad", []):
            day_modifier = "弥恶"

    morphology = []
    effective_verdict = item.get("verdict")
    qi_class = item["qi_class"]

    if qi_class == "胜气":
        if motion_advantage is True:
            morphology.append("胜气动利：大胜")
        if continuity == "断续" or disorder in {"南北溃乱", "溃乱"}:
            morphology.append("虽得胜云气，断续不次或南北溃乱：反败")
            effective_verdict = "败"
    elif qi_class == "败气":
        if continuity == "坚实" and motion_advantage is True:
            morphology.append("败云气坚实而动利：保留原文修正，不擅自翻成确定胜负")
        if continuity == "断续" or disorder in {"溃乱", "断续溃乱"}:
            morphology.append("败气断续溃乱：不至全恶")

    general_modifier = None
    if over_general is not None:
        if over_general not in {"大将", "参将"}:
            general_modifier = "invalid_general_position"
        elif qi_class == "胜气" and over_general == "大将":
            general_modifier = "胜云气在大将上：大胜"
        elif qi_class == "胜气" and over_general == "参将":
            general_modifier = "胜云气在参将上：参将胜"
        elif qi_class == "败气":
            general_modifier = f"败云气在{over_general}上：原文曰反此，不扩写未明细节"
        else:
            general_modifier = f"{qi_class}不在正文“大将/参将胜败气”修正规则内"

    return {
        **result,
        "status": "ok",
        "computable": True,
        "cloud_present": True,
        "observed_formation": observed_formation,
        "cloud_bearer": observed_formation,
        "verdict_subject": verdict_subject,
        "subject_mode": subject_mode,
        "perspective_note": (
            f"云气所覆为{observed_formation}阵；原文云‘若在我阵上亦尔’，故沿用同一方位×颜色条目。"
            "但条文若明确写主客角色（如北方红云‘客胜’），断语主体仍保留原角色，"
            "不因云气在我阵/敌阵而机械换成我/敌。"
        ),
        "formation_direction": formation_direction,
        "cloud_color": cloud_color,
        "base_verdict": item.get("verdict"),
        "source_note": item.get("source_note"),
        "qi_class": qi_class,
        "day_stem": day_stem,
        "day_modifier": day_modifier,
        "continuity": continuity,
        "disorder": disorder,
        "motion_advantage": motion_advantage,
        "morphology_modifiers": morphology,
        "over_general": over_general,
        "general_modifier": general_modifier,
        "effective_verdict": effective_verdict,
        "defined_color_table": {k: v.get("verdict") for k, v in table.items()},
        "policy": (
            "基础颜色表、日干、云气聚散动静、所临将位分层；云气所在阵与断语主体分栏。"
            "未知颜色、原文未明基础胜负或未明反义，一律不以五行常识/表格对称性补齐。"
        ),
    }


def j4m_low_dependency_catalog():
    """供文档/UI 查询的已实现规则，不参与自动综合胜负。"""
    return {
        "ruleset": J4M_RULESET,
        "source_profile": J4M_SOURCE_PROFILE,
        "implemented": ["J4M-01", "J4M-02", "J4M-03", "J4M-04", "J4M-05", "J4M-06", "J4M-07", "J4M-08", "J4M-09", "J4M-10", "J4M-11", "J4M-12"],
        "partial": [],
        "pending": [],
    }
