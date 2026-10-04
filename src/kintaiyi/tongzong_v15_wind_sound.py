"""C25 卷十五“明五音观风察将术”来源限定实现。

本条看的是实际风声形态，而不是 V15-09 的风向五音。
"""

from __future__ import annotations

import copy
from typing import Any

C25_VERSION = "taiyi-c25-tongzong-v15-wind-sound-v1"
SOURCE_PROFILE = "tongzong_volume15"

WIND_SOUND_CLASSES = {
    "宫风": {
        "tone": "宫",
        "element": "土",
        "sound_profile": "沉厚隆隆，近车雷鼓声",
        "general_character": "宽和、有信",
    },
    "商风": {
        "tone": "商",
        "element": "金",
        "sound_profile": "清越铿然，近金石钟佩声",
        "general_character": "威猛、好杀",
    },
    "角风": {
        "tone": "角",
        "element": "木",
        "sound_profile": "肃习而动林木",
        "general_character": "仁恕、不易欺诈",
    },
    "徵风": {
        "tone": "徵",
        "element": "火",
        "sound_profile": "急烈奔腾，近奔马烈火",
        "general_character": "猛烈、难争锋",
    },
    "羽风": {
        "tone": "羽",
        "element": "水",
        "sound_profile": "流动扬波，近流水之声",
        "general_character": "贪暴、多奸诈",
    },
}

ONLINE_WITNESS = {
    "provider": "识典古籍",
    "url": "https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppxduthvru",
    "section": "明五音观风察将术",
}


def observe_general_from_wind_sound(
    wind_sound_class: str | None,
) -> dict[str, Any]:
    """V15-10 以显式风声类别察将。

    不接受 V15-09 的风向五音结果作为替代输入。
    """
    base = {
        "canonical": C25_VERSION,
        "source_profile": SOURCE_PROFILE,
        "source_rule_id": "V15-10",
        "name": "五音观风察将",
        "source_section": "明五音观风察将术",
        "online_witness": copy.deepcopy(ONLINE_WITNESS),
        "requires_external_observation": True,
        "cross_j4m_merge": False,
        "cross_c8_merge": False,
        "v15_09_direction_tone_substitute_allowed": False,
    }

    if wind_sound_class is None:
        return {
            **base,
            "status": "not_computable",
            "computable": False,
            "missing_inputs": ["wind_sound_class"],
            "known_classes": list(WIND_SOUND_CLASSES),
            "policy": "未实际观察风声，不得由风向五音或盘面推造风声类别。",
        }

    if not isinstance(wind_sound_class, str):
        raise TypeError("wind_sound_class须为str或None")
    if wind_sound_class not in WIND_SOUND_CLASSES:
        raise ValueError("wind_sound_class须为宫风/商风/角风/徵风/羽风")

    return {
        **base,
        "status": "ok",
        "computable": True,
        "wind_sound_class": wind_sound_class,
        **copy.deepcopy(WIND_SOUND_CLASSES[wind_sound_class]),
        "winner": None,
        "policy": (
            "本条只按风声五音描述将帅性情，不自动推成军事胜负；"
            "风向五音属于V15-09，二者不得互相替代。"
        ),
    }


def c25_catalog() -> dict[str, Any]:
    return {
        "canonical": C25_VERSION,
        "implemented": ["V15-10"],
        "external_observation": "wind_sound_class",
        "direction_rule_separate": "V15-09",
        "policy": "风声与风向分层。",
    }
