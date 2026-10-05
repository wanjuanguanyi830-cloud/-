"""C94 五福与四太乙五行同域关系：2026-10-04 工作回收层。

来源核心：《太乙统宗宝鉴》卷六/七五福条。
旧分支 four_taiyi.py 在 2026-10-04 已将原文
“金/土/火/水”四类灾应解释为：
- 天乙（金）→兵盗；
- 地乙（土）→疫疠、民灾；
- 直符（火）→旱蝗；
- 四神（水）→淋雨、川溃。

本层保留该最近两天工作解释，但把自动坐标推断移除：
调用方必须显式给 same_wufu_domain=True/False/None。
"""

from __future__ import annotations

import copy
from typing import Any

C94_VERSION = "taiyi-c94-wufu-four-taiyi-domain-relations-v1"

COUNTERPARTS = {
    "天乙": {
        "element": "金",
        "effects": ["兵盗"],
    },
    "地乙": {
        "element": "土",
        "effects": ["疫疠", "民灾"],
    },
    "直符": {
        "element": "火",
        "effects": ["旱蝗"],
    },
    "四神": {
        "element": "水",
        "effects": ["淋雨", "川溃"],
    },
}

ALIASES = {
    "值符": "直符",
    "四神水宿": "四神",
}

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙统宗宝鉴",
        "witness_volumes": [6, 7],
        "section": "明五福太乙所主术",
        "source_clause": (
            "五福与四神同宫，为福减损；金有兵盗，土有疫疠民灾，"
            "火有旱蝗，水有淋雨川溃。"
        ),
        "variants": {
            "福减": ["减省", "减损"],
            "火灾词": ["旱虫", "蝗旱", "旱蝗"],
            "水灾词": ["川溃", "川渍"],
        },
    },
    "collation": [
        {
            "work": "三才世纬",
            "status": "supports_four_element_sequence",
        }
    ],
}

RECENT_WORK_INTERPRETATION = {
    "profile": "oct4_recovered_four_taiyi_elemental",
    "status": "recent_work_interpretation_supported_by_source_sequence",
    "created_from": {
        "branch": "codex/c1-c7-canonical",
        "file": "src/kintaiyi/four_taiyi.py",
        "file_commit": "f02c052ae88e",
        "file_commit_date": "2026-10-04T19:52:53Z",
        "symbol": "FIVE_MEETING_EFFECTS",
    },
    "coordinate_basis": {
        "branch": "codex/c1-c7-canonical",
        "file": "src/kintaiyi/taiyi_cycles.py",
        "file_commit": "fadab7ee3fa8",
        "file_commit_date": "2026-10-04T19:52:22Z",
        "symbols": ["FIVE_DOMAINS", "PALACE_DOMAINS"],
        "recovered_asset": "terminology/wufu_domains.json",
    },
    "interpretation": (
        "原文连续列金/土/火/水四类灾应；2026-10-04 工作将其按四太乙"
        "固有五行映射到天乙/地乙/直符/四神。‘同宫’在旧实现中以五福五域"
        "坐标归一化后判断。C94保留此解释，但不再自动计算同域。"
    ),
    "time_window_policy": "only_2026-10-04_and_2026-10-05_prior_work",
}

COORDINATE_BOUNDARY = {
    "coordinate_reference": "terminology/wufu_domains.json",
    "source_term": "同宫",
    "project_interpretation": "same_wufu_domain",
    "auto_coordinate_lookup_used": False,
    "auto_relation_inference_used": False,
    "policy": (
        "C94不读取C64/C92位置，也不读取C67五福位置自动判断关系；"
        "是否处于同一五福域必须由调用方显式给出。"
    ),
}


def _counterpart(name: str, *, allow_legacy_zhifu_alias: bool) -> str:
    if not isinstance(name, str):
        raise TypeError("counterpart须为字符串")
    if name in COUNTERPARTS:
        return name
    if name == "值符":
        if allow_legacy_zhifu_alias:
            return "直符"
        raise ValueError("值符不是C94 canonical名称；兼容时显式开启alias")
    normalized = ALIASES.get(name)
    if normalized is not None:
        return normalized
    raise ValueError("counterpart须为天乙/地乙/直符/四神")


def wufu_four_taiyi_relation(
    counterpart: str,
    *,
    same_wufu_domain: bool | None,
    interpretation_profile: str,
    allow_legacy_zhifu_alias: bool = False,
) -> dict[str, Any]:
    """解释五福与四太乙的显式同五福域关系。

    interpretation_profile 必须显式指定为最近两天恢复的解释，
    防止把该坐标解释误当作原文无歧义的字面公式。
    """
    if interpretation_profile != RECENT_WORK_INTERPRETATION["profile"]:
        raise ValueError(
            "interpretation_profile须为oct4_recovered_four_taiyi_elemental"
        )
    if same_wufu_domain not in (None, True, False):
        raise TypeError("same_wufu_domain须为bool或None")

    name = _counterpart(
        counterpart,
        allow_legacy_zhifu_alias=allow_legacy_zhifu_alias,
    )
    spec = COUNTERPARTS[name]

    if same_wufu_domain is None:
        status = "same_wufu_domain_unchecked"
        effects: list[str] = []
        pending = [
            "须显式确认是否同一五福域；C94不从位置或五域坐标自动判断"
        ]
    elif same_wufu_domain is False:
        status = "not_same_wufu_domain"
        effects = []
        pending = []
    else:
        status = "explicit_same_wufu_domain_relation"
        effects = ["五福之福减损", *spec["effects"]]
        pending = []

    return {
        "schema_version": "1.0",
        "canonical": C94_VERSION,
        "rule_id": "C94-WUFU-FOUR-TAIYI-DOMAIN-RELATION",
        "source_profile": "tongzong_wufu_four_taiyi_element_sequence",
        "interpretation_profile": interpretation_profile,
        "counterpart": name,
        "counterpart_element": spec["element"],
        "same_wufu_domain": same_wufu_domain,
        "effects": effects,
        "status": status,
        "pending": pending,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "recent_work_interpretation": copy.deepcopy(RECENT_WORK_INTERPRETATION),
        "coordinate_boundary": copy.deepcopy(COORDINATE_BOUNDARY),
        "policy": (
            "保留2026-10-04四太乙五行映射解释，但不自动计算同域；"
            "原文异字只正规化为稳定灾应核心。"
        ),
    }


def c94_catalog() -> dict[str, Any]:
    return {
        "canonical": C94_VERSION,
        "rule_id": "C94-WUFU-FOUR-TAIYI-DOMAIN-RELATION",
        "counterparts": copy.deepcopy(COUNTERPARTS),
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "recent_work_interpretation": copy.deepcopy(RECENT_WORK_INTERPRETATION),
        "coordinate_boundary": copy.deepcopy(COORDINATE_BOUNDARY),
        "default_interpretation_profile": None,
        "interpretation_profile_required": True,
    }
