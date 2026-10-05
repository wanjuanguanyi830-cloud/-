"""C93 直符太乙火神：已见证宫位火气状态表。

本层仅回收 2026-10-04 旧分支 four_taiyi.py 中
`zhifu_known_state()` 的三条已见证状态，并用《太乙秘书》正文重新核定：

- 二宫：火旺；
- 三宫：火长生；
- 四宫：火败。

未知宫位不按十二长生常识自动补齐。
"""

from __future__ import annotations

import copy
from typing import Any

C93_VERSION = "taiyi-c93-zhifu-known-fire-states-v1"

KNOWN_STATES = {
    2: {
        "state": "旺",
        "source_phrase": "辛卯三年入二宫，火旺",
    },
    3: {
        "state": "长生",
        "source_phrase": "甲午三年入三宫，火长生",
    },
    4: {
        "state": "败",
        "source_phrase": "丁酉三年临四宫，火败",
    },
}

SOURCE_WITNESS = {
    "primary": {
        "work": "太乙秘书",
        "section": "四神天乙地乙直符",
        "spirit": "直符太乙",
        "element": "火",
        "direct_states": copy.deepcopy(KNOWN_STATES),
        "context": (
            "正文以历史例说明二宫火旺、三宫火长生、四宫火败，"
            "并另述直符行宫与四神同法、上元五宫、中元一宫、下元九宫。"
        ),
    },
    "collation": {
        "work": "古今图书集成太乙神数相关汇编",
        "status": "supports_zhifu_fire_identity_and_36_year_cycle",
        "note": "只作后期参校，不用来补齐未见证宫位的火气状态。",
    },
}

LEGACY_RECOVERY = {
    "branch": "codex/c1-c7-canonical",
    "file": "src/kintaiyi/four_taiyi.py",
    "file_commit": "f02c052ae88e",
    "file_commit_date": "2026-10-04T19:52:53Z",
    "legacy_function": "zhifu_known_state",
    "legacy_table": {2: "旺", 3: "长生", 4: "败"},
    "recovery_status": "recovered_after_direct_source_recheck",
    "time_window_policy": "only_2026-10-04_and_2026-10-05_prior_work",
}

POSITION_BOUNDARY = {
    "position_runtime": "C64-ZHIFU",
    "auto_position_lookup_used": False,
    "policy": (
        "C93不从积年自动调用直符位置；调用方须显式提供宫位。"
        "位置公式与火气状态解释保持分层。"
    ),
}


def zhifu_known_fire_state(palace: int) -> dict[str, Any]:
    """返回正文明确见证的直符火气状态；未知宫位保持 source_pending。"""
    if isinstance(palace, bool) or not isinstance(palace, int):
        raise TypeError("palace须为整数宫位")
    if not 1 <= palace <= 12:
        raise ValueError("palace须为1..12")

    record = KNOWN_STATES.get(palace)
    if record is None:
        return {
            "schema_version": "1.0",
            "canonical": C93_VERSION,
            "rule_id": "C93-ZHIFU-KNOWN-FIRE-STATE",
            "source_profile": "taiyi_mishu_zhifu_fire_examples",
            "palace": palace,
            "state": None,
            "source_phrase": None,
            "status": "source_pending",
            "pending": [
                "当前直接见证只锁定二宫旺、三宫长生、四宫败；"
                "该宫不得按十二长生或五行常识自动补齐"
            ],
            "source_witness": copy.deepcopy(SOURCE_WITNESS),
            "legacy_recovery": copy.deepcopy(LEGACY_RECOVERY),
            "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
        }

    return {
        "schema_version": "1.0",
        "canonical": C93_VERSION,
        "rule_id": "C93-ZHIFU-KNOWN-FIRE-STATE",
        "source_profile": "taiyi_mishu_zhifu_fire_examples",
        "palace": palace,
        "state": record["state"],
        "source_phrase": record["source_phrase"],
        "status": "direct_source_state",
        "pending": [],
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_recovery": copy.deepcopy(LEGACY_RECOVERY),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
    }


def c93_catalog() -> dict[str, Any]:
    return {
        "canonical": C93_VERSION,
        "rule_id": "C93-ZHIFU-KNOWN-FIRE-STATE",
        "source_profile": "taiyi_mishu_zhifu_fire_examples",
        "known_states": copy.deepcopy(KNOWN_STATES),
        "known_palaces": sorted(KNOWN_STATES),
        "full_twelve_palace_state_table_ready": False,
        "source_witness": copy.deepcopy(SOURCE_WITNESS),
        "legacy_recovery": copy.deepcopy(LEGACY_RECOVERY),
        "position_boundary": copy.deepcopy(POSITION_BOUNDARY),
    }
