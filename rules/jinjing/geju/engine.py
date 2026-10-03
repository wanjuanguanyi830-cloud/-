"""《太乙金鏡式經》卷三 source-limited pattern engine."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Mapping

from ..eight_door import eight_door


GEJU_RULESET = "jinjing"
GEJU_RULESET_VERSION = "jinjing-geju-1.0.0"
RULE_SOURCE = "《太乙金鏡式經》卷三"
DOOR_RULE_SOURCE = "《太乙金鏡式經》卷四"

SIXTEEN_RING = (
    "子", "丑", "艮", "寅", "卯", "辰", "巽", "巳",
    "午", "未", "坤", "申", "酉", "戌", "乾", "亥",
)
PALACE_RING = (8, 3, 4, 9, 2, 7, 6, 1)

TY_CENTER = {
    8: "子",
    3: "艮",
    4: "卯",
    9: "巽",
    2: "午",
    7: "坤",
    6: "酉",
    1: "乾",
}
JIAN_SHEN = {
    8: "亥",
    3: "丑",
    4: "寅",
    9: "辰",
    2: "巳",
    7: "未",
    6: "申",
    1: "戌",
}
JIAN_SHEN_POSITIONS = frozenset(JIAN_SHEN.values())
CHEN_TO_PALACE = {
    "子": 8, "亥": 8,
    "丑": 3, "艮": 3,
    "寅": 4, "卯": 4,
    "辰": 9, "巽": 9,
    "巳": 2, "午": 2,
    "未": 7, "坤": 7,
    "申": 6, "酉": 6,
    "戌": 1, "乾": 1,
}

_SIXTEEN_INDEX = {chen: index for index, chen in enumerate(SIXTEEN_RING)}
_PALACE_INDEX = {palace: index for index, palace in enumerate(PALACE_RING)}
_CHEN_RELATIONS = {
    0: "正宮",
    1: "外辰",
    2: "外宮",
    8: "對宮",
    14: "內宮",
    15: "內辰",
}

@dataclass(frozen=True)
class GejuContext:
    """同一盤面快照中的格局輸入。將位使用九宮數，目位使用十六神名稱。"""

    taiyi: int
    wenchang: str
    shiji: str
    home_big: int
    home_vassal: int
    away_big: int
    away_vassal: int
    dingmu: str | None = None
    duty_door: str | None = None
    doors: Mapping[int, str] | None = None
    accumulated_year: int | None = None


def chen_relation_to_taiyi(chen: str, taiyi_palace: int) -> str:
    """回傳目在太乙周圍的十六神精確位置關係。"""
    center = TY_CENTER.get(taiyi_palace)
    chen_index = _SIXTEEN_INDEX.get(chen)
    if center is None or chen_index is None:
        return "其他"
    diff = (chen_index - _SIXTEEN_INDEX[center]) % len(SIXTEEN_RING)
    return _CHEN_RELATIONS.get(diff, "其他")


def palace_relation_to_taiyi(palace: int, taiyi_palace: int) -> str:
    """按空間宮環 8→3→4→9→2→7→6→1 判斷將與太乙的關係。"""
    p_index = _PALACE_INDEX.get(palace)
    ty_index = _PALACE_INDEX.get(taiyi_palace)
    if p_index is None or ty_index is None:
        return "其他"
    diff = (p_index - ty_index) % len(PALACE_RING)
    return {0: "同宮", 1: "外宮", 4: "對宮", 7: "內宮"}.get(diff, "其他")


def is_palace_flanked(target: int, actor_a: int, actor_b: int) -> bool:
    """兩個位置是否在八宮環上夾住目標。"""
    target_index = _PALACE_INDEX.get(target)
    a_index = _PALACE_INDEX.get(actor_a)
    b_index = _PALACE_INDEX.get(actor_b)
    if target_index is None or a_index is None or b_index is None:
        return False
    return {
        (a_index - target_index) % 8,
        (b_index - target_index) % 8,
    } == {1, 7}


def _is_chen_flanked(target: str, actor_a: str, actor_b: str) -> bool:
    """兩個十六神位置是否分居目標兩側。"""
    target_index = _SIXTEEN_INDEX.get(target)
    a_index = _SIXTEEN_INDEX.get(actor_a)
    b_index = _SIXTEEN_INDEX.get(actor_b)
    if target_index is None or a_index is None or b_index is None:
        return False
    a_distance = (a_index - target_index) % 16
    b_distance = (b_index - target_index) % 16
    return 0 < a_distance < 8 < b_distance < 16 or 0 < b_distance < 8 < a_distance < 16


def _is_palace_center(chen: str) -> bool:
    index = _SIXTEEN_INDEX.get(chen)
    return index is not None and index % 2 == 0


def _opposite_palace(palace: int) -> int | None:
    index = _PALACE_INDEX.get(palace)
    return PALACE_RING[(index + 4) % 8] if index is not None else None


def _non_center_general_pair(generals: Mapping[str, int]) -> list[tuple[str, str]]:
    return [
        (left_name, right_name)
        for (left_name, left), (right_name, right) in combinations(generals.items(), 2)
        if left != 5 and right != 5 and left == right
    ]


def analyze_geju(context: GejuContext) -> dict:
    """執行《金鏡式經》主算法並回傳結構化事件與舊式字典。"""
    ty = context.taiyi
    if ty not in TY_CENTER:
        raise ValueError(f"太乙宮必須是八個正宮之一，收到: {ty!r}")

    wc = context.wenchang
    sj = context.shiji
    if wc not in _SIXTEEN_INDEX or sj not in _SIXTEEN_INDEX:
        raise ValueError("文昌與始擊必須使用十六神精確位置，不接受未歸一化的星名")
    wc_relation = chen_relation_to_taiyi(wc, ty)
    sj_relation = chen_relation_to_taiyi(sj, ty)
    wc_palace = CHEN_TO_PALACE.get(wc)
    sj_palace = CHEN_TO_PALACE.get(sj)
    opposite = _opposite_palace(ty)
    generals = {
        "主大": context.home_big,
        "主參": context.home_vassal,
        "客大": context.away_big,
        "客參": context.away_vassal,
    }
    events: list[dict] = []
    legacy: dict[str, str] = {}

    def add_event(
        category: str,
        legacy_key: str,
        subjects: list[str],
        target: str | None,
        relation: str,
        evidence: str,
        interpretation: str,
        source: str = RULE_SOURCE,
    ) -> None:
        if legacy_key in legacy:
            return
        events.append({
            "格局": category,
            "主體": subjects,
            "目標": target,
            "位置": relation,
            "成格依據": evidence,
            "斷語": interpretation,
            "出處": source,
            "舊式鍵": legacy_key,
        })
        legacy[legacy_key] = interpretation

    # 始擊專主掩、擊、格；上目不納迫。
    if sj_relation == "正宮":
        add_event("掩", "掩", ["始擊"], "太乙", "正宮", "始擊與太乙同處正宮。", "始擊臨太乙正宮，陰盛陽衰、君弱臣強之象")
    hit_keys = {
        "外辰": ("擊(外辰)", "始擊在太乙前一辰，外辰擊，諸侯侵凌"),
        "內辰": ("擊(內辰)", "始擊在太乙後一辰，內辰擊，親王后妃憑凌"),
        "外宮": ("擊(外宮)", "始擊在太乙前一宮，外宮擊"),
        "內宮": ("擊(內宮)", "始擊在太乙後一宮，內宮擊"),
    }
    if sj_relation in hit_keys:
        key, interpretation = hit_keys[sj_relation]
        add_event("擊", key, ["始擊"], "太乙", sj_relation, f"始擊相對太乙為{sj_relation}。", interpretation)

    # 文昌主囚、迫、對。間神雖映射同一宮，仍不算同正宮囚。
    if wc_relation == "正宮":
        add_event("囚", "囚(文昌)", ["文昌"], "太乙", "正宮", "文昌與太乙同處正宮，非僅映射同宮。", "文昌囚太乙，拘繫執正，不利為主")

    for name, relation in (("文昌", wc_relation),):
        chen_po = {
            "外辰": ("外", "辰迫", "在太乙前一辰，外辰迫，災急而重"),
            "內辰": ("內", "辰迫", "在太乙後一辰，內辰迫，災尤速"),
        }.get(relation)
        if chen_po:
            direction, kind, text = chen_po
            add_event("迫", f"{kind}({direction}、{name})", [name], "太乙", relation, f"{name}與太乙相隔一辰。", f"{name}{text}")
        elif relation in ("外宮", "內宮"):
            direction = "外" if relation == "外宮" else "內"
            add_event(
                "迫", f"宮迫({direction}、{name})", [name], "太乙", relation,
                f"{name}在太乙{relation}。", f"{name}在太乙{('前' if direction == '外' else '後')}一宮，{direction}宮迫",
            )

    for name, palace in generals.items():
        relation = palace_relation_to_taiyi(palace, ty)
        if palace == ty and palace != 5:
            add_event("囚", f"囚({name})", [name], "太乙", "同宮", f"{name}與太乙同宮。", f"{name}與太乙同宮為囚，下犯上之象")
        if relation in ("外宮", "內宮"):
            direction = "外" if relation == "外宮" else "內"
            add_event("迫", f"宮迫({direction}、{name})", [name], "太乙", relation, f"{name}位於太乙{relation}。", f"{name}在太乙{('前' if direction == '外' else '後')}一宮，{direction}宮迫")

    for left_name, right_name in _non_center_general_pair(generals):
        add_event(
            "關", f"關({left_name}、{right_name})", [left_name, right_name], None, "同宮",
            f"{left_name}與{right_name}同宮。", "主客將同宮相持，不利有為",
        )

    if opposite is not None:
        if sj_palace == opposite:
            add_event("格", "格(始擊)", ["始擊"], "太乙", "對宮", "始擊所在宮與太乙對宮相同。", "始擊在太乙對宮，政事上下相格、盜侮其君")
        for name in ("客大", "客參"):
            if generals[name] == opposite:
                add_event("格", f"格({name})", [name], "太乙", "對宮", f"{name}在太乙對宮。", f"{name}在太乙對宮為格")
        if wc_palace == opposite:
            add_event("對", "對", ["文昌"], "太乙", "對宮", "文昌所在宮與太乙對宮相同。", "文昌與太乙相對，大臣懷二、將吏挾奸")

    # 正宮提挾：通用枚舉「太乙＋四將」的夹持关系；
    # 目只能作为正宫目标，间神目标留给挟闭判断。
    locations = {"太乙": ty, **generals, "文昌": wc_palace, "始擊": sj_palace}
    chen_locations = {"文昌": wc, "始擊": sj}
    flank_points = {"太乙": ty, **generals}
    targets = ("太乙", *generals.keys(), "文昌", "始擊")
    for target in targets:
        target_palace = locations.get(target)
        if target_palace is None:
            continue
        if target in chen_locations and not _is_palace_center(chen_locations[target]):
            continue
        for actor_a, actor_b in combinations(flank_points, 2):
            if target in (actor_a, actor_b):
                continue
            if is_palace_flanked(target_palace, flank_points[actor_a], flank_points[actor_b]):
                add_event(
                    "提挾", f"提挾({actor_a}、{actor_b}夾{target})", [actor_a, actor_b], target, "正宮",
                    f"{target}在正宮位置；{actor_a}與{actor_b}位於八宮環相鄰兩側。",
                    f"{actor_a}、{actor_b}挾{target}，推勢挾持之象",
                )

    # 挾閉：二目均臨間神；太乙與一主將、一客將共同構成夾持點。
    if wc in JIAN_SHEN_POSITIONS and sj in JIAN_SHEN_POSITIONS:
        home_points = [
            (name, TY_CENTER[generals[name]])
            for name in ("主大", "主參")
            if generals[name] in TY_CENTER
        ]
        away_points = [
            (name, TY_CENTER[generals[name]])
            for name in ("客大", "客參")
            if generals[name] in TY_CENTER
        ]
        support = None
        for home_actor in home_points:
            for away_actor in away_points:
                actor_points = [("太乙", TY_CENTER[ty]), home_actor, away_actor]
                wc_pairs = [pair for pair in combinations(actor_points, 2) if _is_chen_flanked(wc, pair[0][1], pair[1][1])]
                sj_pairs = [pair for pair in combinations(actor_points, 2) if _is_chen_flanked(sj, pair[0][1], pair[1][1])]
                if wc_pairs and sj_pairs:
                    support = (wc_pairs[0], sj_pairs[0])
                    break
            if support:
                break
        if support:
            wc_pair, sj_pair = support
            participants = {name for name, _ in (*wc_pair, *sj_pair)}
            wc_actors = "、".join(name for name, _ in wc_pair)
            sj_actors = "、".join(name for name, _ in sj_pair)
            add_event(
                "挾閉", "挾閉", sorted(participants), "文昌、始擊", "間神",
                f"文昌、始擊皆臨間神；{wc_actors}夾文昌，{sj_actors}夾始擊，並見太乙與主客將。",
                "二目臨間神而受夾，挾閉之象",
            )

    # 執提、提格只看當值之開門或生門，不看盤上其他開、生門。
    if context.duty_door is not None and context.accumulated_year is not None:
        calculated_door = eight_door(context.accumulated_year)
        if context.duty_door != calculated_door:
            raise ValueError("duty_door conflicts with the 《金鏡》 accumulated-year cycle")
    duty_door = context.duty_door or (
        eight_door(context.accumulated_year) if context.accumulated_year is not None else None
    )
    if duty_door is not None and duty_door not in {"開", "休", "生", "傷", "杜", "景", "死", "驚"}:
        raise ValueError(f"unsupported duty door: {duty_door!r}")
    if duty_door in ("開", "生") and context.doors:
        duty_palace = next((palace for palace, door in context.doors.items() if door == duty_door), None)
        if duty_palace == ty:
            add_event(
                "執提", "執(開生門合)", [duty_door], "太乙", "同宮",
                f"值事門為{duty_door}，且與太乙同宮。", f"值事{duty_door}門與太乙合，執提之象，不可舉事", DOOR_RULE_SOURCE,
            )
        elif duty_palace == opposite:
            add_event(
                "提格", "提格(開生門衝)", [duty_door], "太乙", "對宮",
                f"值事門為{duty_door}，且與太乙對宮相衝。", f"值事{duty_door}門與太乙衝，提格之象", DOOR_RULE_SOURCE,
            )

    # 四郭固、四郭杜是基於基本事件的復合格局。
    general_pairs = _non_center_general_pair(generals)
    if wc_relation == "正宮" and general_pairs:
        add_event(
            "四郭固", "四郭固", ["文昌", *general_pairs[0]], "太乙", "復合",
            f"文昌囚太乙，並見大小將同宮（{general_pairs[0][0]}、{general_pairs[0][1]}）。",
            "文昌囚太乙，兼大小將相關，四郭固，堅壁固守，不可有為",
        )
    elif sj_palace == ty and (
        context.away_big == context.away_vassal
        or context.away_big == ty
        or context.away_vassal == ty
        or context.away_big == context.home_big
        or context.away_vassal == context.home_vassal
    ):
        add_event(
            "四郭固", "四郭固", ["始擊", "客大", "客參"], "太乙", "復合",
            "客目與太乙同宮位（可在間神），並見客將或主客同類將相關。", "客目臨太乙，兼客主將相關，四郭固，宜固守",
        )

    has_secondary = any(event["格局"] in {"掩", "迫", "關", "格", "提挾"} for event in events)
    if wc_palace == context.away_vassal and context.home_big == context.away_big and has_secondary:
        add_event(
            "四郭杜", "四郭杜", ["客參", "文昌", "主大", "客大"], None, "復合",
            "客參與文昌同宮、主大與客大同宮，且兼見掩／迫／關／格／提挾。",
            "客參與文昌並，主大與客大並，兼見掩、迫、關、格或提挾，四郭杜",
        )

    if not legacy:
        legacy["無格局"] = "太乙無《金鏡式經》所列格局，主客清明"

    return {
        "規則集": GEJU_RULESET,
        "規則版本": GEJU_RULESET_VERSION,
        "規則來源": RULE_SOURCE,
        "盤面": {
            "太乙": ty,
            "文昌": {"十六神": wc, "宮": wc_palace, "與太乙關係": wc_relation, "位置類型": "正宮" if _is_palace_center(wc) else "間神"},
            "始擊": {"十六神": sj, "宮": sj_palace, "與太乙關係": sj_relation, "位置類型": "正宮" if _is_palace_center(sj) else "間神"},
            "定目": context.dingmu,
            "主大": context.home_big,
            "主參": context.home_vassal,
            "客大": context.away_big,
            "客參": context.away_vassal,
            "積年": context.accumulated_year,
            "值事門": duty_door,
            "八門分布": dict(context.doors or {}),
        },
        "事件": events,
        "舊式": legacy,
    }


def to_legacy_dict(detail: Mapping) -> dict[str, str]:
    """保持 Taiyi.shi_geju() 的舊字典返回形态。"""
    return dict(detail["舊式"])

