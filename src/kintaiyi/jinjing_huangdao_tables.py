"""C118 《太乙金镜式经》卷一黄道日度 / 宿度 / 十二分野上游表。

本层为 C69“推太乙当时法”的上游事实层，只实现卷一直接列出的：
- 二十四气黄道日度所在立成；
- 二十八宿黄道度数立成；
- 列宿十二分野立成；
- 由节气锚点按“一日一度”推进的可审计日度 helper。

边界：
- 不计算现代天文黄经；
- 不把后世宿度表覆盖《金镜》卷一；
- “虚”宿度当前转录存在缺字 / 分数歧义，不强造数值；
- 日度推进若必须跨越“虚”宿未定边界，则返回 not_computable；
- 不在本层安天乙前后诸将，C69 仍负责天乙朝暮与十二天将表。
"""

from __future__ import annotations

import copy
from fractions import Fraction
from typing import Any

C118_VERSION = "taiyi-c118-jinjing-huangdao-upstream-v1"

MANSION_ORDER = (
    "斗", "牛", "女", "虚", "危", "室", "壁",
    "奎", "娄", "胃", "昴", "毕", "觜", "参",
    "井", "鬼", "柳", "星", "张", "翼", "轸",
    "角", "亢", "氐", "房", "心", "尾", "箕",
)

SOLAR_TERM_ANCHORS: dict[str, dict[str, Any]] = {
    "冬至": {"mansion": "斗", "degree": Fraction(9, 1)},
    "小寒": {"mansion": "斗", "degree": Fraction(24, 1)},
    "大寒": {"mansion": "女", "degree": Fraction(8, 1)},
    "立春": {"mansion": "危", "degree": Fraction(2, 1)},
    "雨水": {"mansion": "室", "degree": Fraction(1, 1)},
    "惊蛰": {"mansion": "室", "degree": Fraction(1, 1)},
    "春分": {"mansion": "奎", "degree": Fraction(4, 1)},
    "清明": {"mansion": "娄", "degree": Fraction(2, 1)},
    "谷雨": {"mansion": "胃", "degree": Fraction(4, 1)},
    "立夏": {"mansion": "昴", "degree": Fraction(4, 1)},
    "小满": {"mansion": "毕", "degree": Fraction(8, 1)},
    "芒种": {"mansion": "参", "degree": Fraction(6, 1)},
    "夏至": {"mansion": "井", "degree": Fraction(1, 1)},
    "小暑": {"mansion": "井", "degree": Fraction(27, 1)},
    "大暑": {"mansion": "柳", "degree": Fraction(8, 1)},
    "立秋": {"mansion": "张", "degree": Fraction(3, 1)},
    "处暑": {"mansion": "翼", "degree": Fraction(1, 1)},
    "白露": {"mansion": "翼", "degree": Fraction(16, 1)},
    "秋分": {"mansion": "轸", "degree": Fraction(13, 1)},
    "寒露": {"mansion": "角", "degree": Fraction(9, 1)},
    "霜降": {"mansion": "氐", "degree": Fraction(2, 1)},
    "立冬": {"mansion": "房", "degree": Fraction(1, 1)},
    "小雪": {"mansion": "尾", "degree": Fraction(6, 1)},
    "大雪": {"mansion": "箕", "degree": Fraction(3, 1)},
}

# numeric_span=None means the current primary transcription is not safe enough
# to normalize into a numeric degree without an additional facsimile witness.
MANSION_SPANS: dict[str, dict[str, Any]] = {
    "斗": {"raw": "二十四", "numeric_span": Fraction(24, 1), "status": "direct"},
    "牛": {"raw": "七", "numeric_span": Fraction(7, 1), "status": "direct"},
    "女": {"raw": "十一半", "numeric_span": Fraction(23, 2), "status": "direct"},
    "虚": {
        "raw": "〈二十五分半四分度之一〉",
        "numeric_span": None,
        "status": "transcription_ambiguous_confirmed_by_manuscript",
        "note": (
            "四库公开转录缺整数主体；NCL-06604明钞本PDF第21页直接影像"
            "同样只见虚宿旁小字“二十五分半 / 四分度之一”类分数说明，"
            "未见可安全补作整数主体的正文数字。不得据周天总和或后世宿度表反推。"
        ),
        "manuscript_witness": {
            "id": "NCL-06604",
            "edition": "明钞本",
            "pdf_page": 21,
            "section": "推黄道数立成",
            "evidence_level": "direct_visual_verified",
            "reading": "虚旁小字见二十五分半、四分度之一；整数主体未见",
            "relation_to_siku": "confirms_missing_integer_ambiguity",
            "canonical_effect": "none",
        },
    },
    "危": {"raw": "十八", "numeric_span": Fraction(18, 1), "status": "direct"},
    "室": {"raw": "十七", "numeric_span": Fraction(17, 1), "status": "direct"},
    "壁": {"raw": "十", "numeric_span": Fraction(10, 1), "status": "direct"},
    "奎": {"raw": "十七半", "numeric_span": Fraction(35, 2), "status": "direct"},
    "娄": {"raw": "十三", "numeric_span": Fraction(13, 1), "status": "direct"},
    "胃": {"raw": "十四半", "numeric_span": Fraction(29, 2), "status": "direct"},
    "昴": {"raw": "十一", "numeric_span": Fraction(11, 1), "status": "direct"},
    "毕": {"raw": "十六", "numeric_span": Fraction(16, 1), "status": "direct"},
    "觜": {"raw": "一", "numeric_span": Fraction(1, 1), "status": "direct"},
    "参": {"raw": "九", "numeric_span": Fraction(9, 1), "status": "direct"},
    "井": {"raw": "三十", "numeric_span": Fraction(30, 1), "status": "direct"},
    "鬼": {"raw": "三", "numeric_span": Fraction(3, 1), "status": "direct"},
    "柳": {"raw": "十四", "numeric_span": Fraction(14, 1), "status": "direct"},
    "星": {"raw": "七", "numeric_span": Fraction(7, 1), "status": "direct"},
    "张": {"raw": "十九", "numeric_span": Fraction(19, 1), "status": "direct"},
    "翼": {"raw": "十九", "numeric_span": Fraction(19, 1), "status": "direct"},
    "轸": {"raw": "十八半", "numeric_span": Fraction(37, 2), "status": "direct"},
    "角": {"raw": "十三", "numeric_span": Fraction(13, 1), "status": "direct"},
    "亢": {"raw": "九", "numeric_span": Fraction(9, 1), "status": "direct"},
    "氐": {"raw": "十六", "numeric_span": Fraction(16, 1), "status": "direct"},
    "房": {"raw": "五", "numeric_span": Fraction(5, 1), "status": "direct"},
    "心": {"raw": "五", "numeric_span": Fraction(5, 1), "status": "direct"},
    "尾": {"raw": "十七", "numeric_span": Fraction(17, 1), "status": "direct"},
    "箕": {"raw": "十半", "numeric_span": Fraction(21, 2), "status": "direct"},
}

DIVISIONS = (
    {"mansions": ("斗", "牛"), "state": "吴越", "regions": ("扬州", "交州"), "branch": "丑"},
    {"mansions": ("女", "虚", "危"), "state": "齐", "regions": ("青州",), "branch": "子"},
    {"mansions": ("室", "壁"), "state": "卫", "regions": ("并州",), "branch": "亥"},
    {"mansions": ("奎", "娄"), "state": "鲁", "regions": ("徐州",), "branch": "戌", "source_branch": "戍"},
    {"mansions": ("胃", "昴", "毕"), "state": "赵", "regions": ("冀州",), "branch": "酉"},
    {"mansions": ("觜", "参"), "state": "晋", "regions": ("益州",), "branch": "申"},
    {"mansions": ("井", "鬼"), "state": "秦", "regions": ("雍州",), "branch": "未"},
    {"mansions": ("柳", "星", "张"), "state": "周", "regions": ("三河",), "branch": "午"},
    {"mansions": ("翼", "轸"), "state": "楚", "regions": ("荆州",), "branch": "巳"},
    {"mansions": ("角", "亢"), "state": "郑", "regions": ("兖州",), "branch": "辰"},
    {"mansions": ("氐", "房", "心"), "state": "宋", "regions": ("豫州",), "branch": "卯"},
    {"mansions": ("尾", "箕"), "state": "燕", "regions": ("幽州",), "branch": "寅"},
)

SOURCE_WITNESS = {
    "work": "太乙金镜式经",
    "volume": 1,
    "sections": [
        "推二十四气黄道日度所在立成法",
        "推黄道数立成",
        "推列宿十二分野立成",
    ],
    "links": [
        "https://zh.wikisource.org/zh-hans/太乙金鏡式經_(四庫全書本)/卷01",
        "https://www.shidianguji.com/book/SK1615/chapter/1l9lir71oidda",
    ],
    "policy": (
        "卷一表格作为历史算法输入；不以现代天文学或后世宿度表改写。"
        "公开转录对虚宿度数存在缺字/分数歧义，保持 unresolved。"
    ),
}

C69_UPSTREAM = {
    "downstream": "C69 推太乙当时法",
    "direct_bridge_clause": "算日在何宿，计属何辰，以时加位，立贵前后，以论将之吉凶",
    "implemented_here": [
        "二十四气宿度锚点",
        "二十八宿黄道度数表（虚宿保留未定）",
        "宿->十二分野/地支",
        "节气第N日日度推进（遇虚宿未定边界则停止）",
    ],
    "still_pending_after_c118": [
        "以时加位到时支的完整位移规则",
        "依六壬式安天乙贵神及前五后六到十二支",
        "C69完整主客诸将落十二天将判定",
    ],
}


def _fraction_payload(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def solar_term_anchor(term: str) -> dict[str, Any]:
    if term not in SOLAR_TERM_ANCHORS:
        raise ValueError("未知二十四气")
    data = SOLAR_TERM_ANCHORS[term]
    return {
        "schema_version": "1.0",
        "canonical": C118_VERSION,
        "rule_id": "C118-SOLAR-TERM-ANCHOR",
        "term": term,
        "mansion": data["mansion"],
        "degree": _fraction_payload(data["degree"]),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
    }


def mansion_span(mansion: str) -> dict[str, Any]:
    if mansion not in MANSION_SPANS:
        raise ValueError("未知二十八宿")
    data = MANSION_SPANS[mansion]
    numeric = data["numeric_span"]
    return {
        "schema_version": "1.0",
        "canonical": C118_VERSION,
        "rule_id": "C118-MANSION-SPAN",
        "mansion": mansion,
        "raw": data["raw"],
        "numeric_span": _fraction_payload(numeric) if numeric is not None else None,
        "status": data["status"],
        "note": data.get("note"),
        "manuscript_witness": copy.deepcopy(data.get("manuscript_witness")),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
    }


def mansion_division(mansion: str) -> dict[str, Any]:
    if mansion not in MANSION_ORDER:
        raise ValueError("未知二十八宿")
    row = next(item for item in DIVISIONS if mansion in item["mansions"])
    return {
        "schema_version": "1.0",
        "canonical": C118_VERSION,
        "rule_id": "C118-MANSION-DIVISION",
        "mansion": mansion,
        "division_mansions": list(row["mansions"]),
        "state": row["state"],
        "regions": list(row["regions"]),
        "branch": row["branch"],
        "source_branch": row.get("source_branch"),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
    }


def term_day_position(term: str, day_number: int) -> dict[str, Any]:
    """按卷一节气锚点推“第N日”日度。

    day_number=1 表示节气本日。推进采用一日一度；只有在所经宿度数
    都已可安全数字化时才继续。跨入“虚”可以定位到虚宿，但若还需从
    虚继续越界，则因虚宿度数未定而停止。
    """
    if isinstance(day_number, bool) or not isinstance(day_number, int):
        raise TypeError("day_number须为整数")
    if day_number < 1:
        raise ValueError("day_number须>=1")
    if term not in SOLAR_TERM_ANCHORS:
        raise ValueError("未知二十四气")

    anchor = SOLAR_TERM_ANCHORS[term]
    mansion = anchor["mansion"]
    degree = anchor["degree"]
    steps = Fraction(day_number - 1, 1)

    while steps > 0:
        span = MANSION_SPANS[mansion]["numeric_span"]
        if span is None:
            return {
                "schema_version": "1.0",
                "canonical": C118_VERSION,
                "rule_id": "C118-TERM-DAY-POSITION",
                "computable": False,
                "status": "blocked_ambiguous_mansion_span",
                "term": term,
                "day_number": day_number,
                "current_mansion": mansion,
                "current_degree": _fraction_payload(degree),
                "remaining_days": _fraction_payload(steps),
                "blocked_by": mansion,
                "pending": ["虚宿黄道度数须取得更可靠影印/转录后才能继续跨宿推进"],
                "source_witness": copy.deepcopy(SOURCE_WITNESS),
                "c69_upstream": copy.deepcopy(C69_UPSTREAM),
            }

        room = span - degree
        if steps <= room:
            degree += steps
            steps = Fraction(0, 1)
            break

        # 先走到本宿末界，再进入下一宿；进入新宿时从0度连续推进。
        # 例如立冬房一为第1日，第5日在房五，第6日进入心一。
        steps -= room
        mansion = MANSION_ORDER[(MANSION_ORDER.index(mansion) + 1) % len(MANSION_ORDER)]
        degree = Fraction(0, 1)

    division = mansion_division(mansion)
    return {
        "schema_version": "1.0",
        "canonical": C118_VERSION,
        "rule_id": "C118-TERM-DAY-POSITION",
        "computable": True,
        "status": "ok",
        "term": term,
        "day_number": day_number,
        "mansion": mansion,
        "degree": _fraction_payload(degree),
        "division": {
            "state": division["state"],
            "regions": division["regions"],
            "branch": division["branch"],
        },
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "c69_upstream": copy.deepcopy(C69_UPSTREAM),
    }


def c118_catalog() -> dict[str, Any]:
    return {
        "canonical": C118_VERSION,
        "rule_ids": [
            "C118-SOLAR-TERM-ANCHOR",
            "C118-MANSION-SPAN",
            "C118-MANSION-DIVISION",
            "C118-TERM-DAY-POSITION",
        ],
        "solar_term_anchors": {
            term: {
                "mansion": value["mansion"],
                "degree": _fraction_payload(value["degree"]),
            }
            for term, value in SOLAR_TERM_ANCHORS.items()
        },
        "mansion_spans": {
            mansion: {
                "raw": value["raw"],
                "numeric_span": (
                    _fraction_payload(value["numeric_span"])
                    if value["numeric_span"] is not None else None
                ),
                "status": value["status"],
                "note": value.get("note"),
                "manuscript_witness": copy.deepcopy(value.get("manuscript_witness")),
            }
            for mansion, value in MANSION_SPANS.items()
        },
        "divisions": [
            {
                **{k: copy.deepcopy(v) for k, v in row.items() if k != "mansions"},
                "mansions": list(row["mansions"]),
            }
            for row in DIVISIONS
        ],
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "c69_upstream": copy.deepcopy(C69_UPSTREAM),
    }
