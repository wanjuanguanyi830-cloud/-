"""C19 《太乙紫庭经》第一批可直接定位的主来源结构。

这里只结构化已能在在线古籍见证中直接定位的内容。
未定位到《太乙紫庭经》直接条文的项目保持 pending，不借统宗参校本补成主来源。
"""

from __future__ import annotations

import copy
from typing import Any

C19_VERSION = "taiyi-c19-zitingjing-primary-v1"
PRIMARY_SOURCE_TITLE = "太乙紫庭经"
PRIMARY_SOURCE_ID = "zitingjing"

SHIDIAN_BOOK_ID = "SDZJ0646"
SHIDIAN_BOOK_WITNESS = {
    "title": "太白兵备统宗宝鉴",
    "role": "online_witness_containing_taiyi_zitingjing",
    "book_id": SHIDIAN_BOOK_ID,
    "zitingjing_entry": "https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u3291",
}

PRIMARY_LOCATORS = {
    "taiyi_nine_stars": {
        "status": "verified_direct",
        "section": "释九宫所值九星",
        "url": "https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u4tgl",
        "witness_context": "《太乙紫庭经》表、序之后的卷一首段",
    },
    "wenchang_changes": {
        "status": "verified_direct",
        "section": "释天目变化",
        "url": "https://www.shidianguji.com/book/SDZJ0646/chapter/1kg32q85u5vdx",
        "witness_context": "《太乙紫庭经》卷一段落",
    },
    "shiji_changes": {
        "status": "verified_direct",
        "section": "始击变化",
        "url": "https://www.shidianguji.com/book/SDZJ0646/chapter/1kg32q85u6811",
        "witness_context": "《太乙紫庭经》卷一段落",
    },
    "wenchang_nine_stars": {
        "status": "catalog_attested_primary_text_pending",
        "section": "附太乙文昌九星值宫术",
        "url": None,
        "catalog_witness": {
            "title": "太乙紫庭秘诀（现代整理本目录）",
            "url": "https://www.chinyuan.com.tw/all_book/more?id=7195",
            "evidence": "目录列“附太乙文昌九星值宫术”",
        },
        "witness_context": "已有《太乙紫庭秘诀》目录级证据，但尚未取得可逐条校读的直接正文。",
    },
    "three_banners": {
        "status": "project_primary_attribution_direct_text_pending",
        "section": None,
        "url": None,
        "collation_locator": {
            "source": "太乙统宗宝鉴卷十",
            "section": "明太乙与三旗行宫会合术",
            "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec",
        },
        "witness_context": "《太乙紫庭经》主来源身份按项目校勘原则保留；当前直接可定位的是统宗参校文本。",
    },
    "nine_palace_nobles": {
        "status": "project_primary_attribution_direct_text_pending",
        "section": None,
        "url": None,
        "collation_locator": {
            "source": "太乙统宗宝鉴卷十",
            "section": "明太乙九宫贵神术",
            "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec",
        },
        "witness_context": "《太乙紫庭经》主来源身份按项目校勘原则保留；当前直接可定位的是统宗参校文本。",
    },
}


# 〈释九宫所值九星〉的主来源表。
# “吉凶”按当前在线见证文字记录；若其他古本异文，进入 variant_note，不静默改表。
TAIYI_NINE_STARS_PRIMARY = (
    {"palace": 1, "star": "天蓬", "region": "冀州", "fortune": "凶"},
    {"palace": 2, "star": "天芮", "region": "荆州", "fortune": "凶"},
    {"palace": 3, "star": "天冲", "region": "青州", "fortune": "凶"},
    {"palace": 4, "star": "天辅", "region": "徐州", "fortune": "吉"},
    {"palace": 5, "star": "天禽", "region": "豫州", "fortune": "吉"},
    {"palace": 6, "star": "天心", "region": "雍州", "fortune": "吉"},
    {"palace": 7, "star": "天柱", "region": "梁益州", "fortune": "凶"},
    {"palace": 8, "star": "天任", "region": "兖州", "fortune": "吉"},
    {"palace": 9, "star": "天英", "region": "扬州", "fortune": "凶"},
)


def taiyi_nine_stars_primary() -> dict[str, Any]:
    """返回《太乙紫庭经》〈释九宫所值九星〉的第一层静态表。

    不在这里实现后世卷次中的九十/三百六十年推步算法。
    """
    return {
        "canonical": C19_VERSION,
        "rule_key": "taiyi_nine_stars",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "source_locator": copy.deepcopy(PRIMARY_LOCATORS["taiyi_nine_stars"]),
        "source_status": "verified_direct",
        "computable": True,
        "table": copy.deepcopy(list(TAIYI_NINE_STARS_PRIMARY)),
        "source_summary": {
            "two_hidden_seven_visible": True,
            "nine_palaces": True,
            "four_auspicious_five_inauspicious": True,
        },
        "known_variants": [
            {
                "field": "palace_3_tianchong_fortune",
                "primary_witness": "凶",
                "collation_witness": "吉",
                "collation_source": "太白兵备统宗宝鉴卷十·明太乙九星所主术",
                "collation_url": "https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32qffweib7",
                "resolution": "preserve_both_no_silent_merge",
            },
        ],
        "variant_policy": (
            "本表按当前在线见证记录；其他古本或统宗参校若有异文，"
            "必须另记variant_note/source_variant。"
        ),
    }


def wenchang_changes_primary() -> dict[str, Any]:
    """结构化〈释天目变化〉中可直接抽取的关系规则。"""
    return {
        "canonical": C19_VERSION,
        "rule_key": "wenchang_changes",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "source_locator": copy.deepcopy(PRIMARY_LOCATORS["wenchang_changes"]),
        "source_status": "verified_direct",
        "computable": True,
        "identity": {
            "name": "文昌",
            "role": "天目",
            "element": "土",
            "symbolic_role": "辅相",
        },
        "relations_to_taiyi": {
            "same_palace": {"pattern": "囚", "effect": "不利主人"},
            "one_palace_ahead": {"pattern": "外迫", "effect": "臣下有外谋"},
            "one_palace_behind": {"pattern": "内迫", "effect": "臣下有内谋或后宫之私"},
            "opposite": {"pattern": "对", "effect": "臣下失礼、王纲不振之象"},
        },
        "two_eyes_related": {
            "condition": "文昌与始击同宫",
            "name": "二目相关",
            "decision_basis": "旺相者胜",
            "home_favored_palaces": [1, 8, 3, 7],
            "away_favored_palaces": [4, 9, 6, 2],
        },
        "specific_oppositions": [
            {"taiyi_palace": 1, "wenchang_palace": 9, "subject": "辅相"},
            {"taiyi_palace": 2, "wenchang_palace": 8, "subject": "君父"},
            {"taiyi_palace": 6, "wenchang_palace": 4, "subject": "宰辅将相"},
        ],
        "policy": "只抽取本篇直接可见关系；五行旺相的具体计算仍由独立规则提供。",
    }


def shiji_changes_primary_core() -> dict[str, Any]:
    """结构化〈始击变化〉第一层身份与军事角色。

    岁干×五行的详细灾应表暂不在本批全量转录，避免OCR异文未校即固化。
    """
    return {
        "canonical": C19_VERSION,
        "rule_key": "shiji_changes",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "source_locator": copy.deepcopy(PRIMARY_LOCATORS["shiji_changes"]),
        "source_status": "verified_direct",
        "computable": True,
        "identity": {
            "name": "始击",
            "astral_correspondence": "荧惑之精",
            "direction": "南方",
            "season": "夏",
            "element": "火",
        },
        "military_role": {
            "side": "客",
            "role": "客目",
            "favors": "客",
            "initiative": "临军先举",
        },
        "relations": {
            "covers_taiyi": {
                "pattern": "掩",
                "effect": "掩袭篡夺之事",
            },
            "covers_wenchang": {
                "pattern": "关",
                "decision_basis": "旺宫者胜",
                "home_favored_palaces": [1, 8, 3, 7],
                "away_favored_palaces": [4, 9, 2, 6],
            },
            "covers_home_general_or_vassal": {
                "effect": "不论旺宫，必败死",
            },
            "adjacent_to_taiyi": {
                "pattern": "击",
                "effect": "有兵逼之灾",
            },
        },
        "observational_principles": [
            "出则有兵、入则兵散",
            "临分野可主乱、贼、疾、丧、兵、饥等灾应",
            "变化不可执一途而断",
        ],
        "detailed_year_stem_element_table_status": "pending_textual_collation",
        "policy": "本批只固化直接核心事实；逐岁五行灾应待完成OCR/异文校勘后再结构化。",
    }


def c19_primary_catalog() -> dict[str, Any]:
    """六项P1的主来源定位与当前结构化状态。"""
    implemented = {
        "taiyi_nine_stars": "verified_primary_table",
        "wenchang_changes": "verified_primary_rules",
        "shiji_changes": "verified_primary_core",
    }
    return {
        "canonical": C19_VERSION,
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "online_witness": copy.deepcopy(SHIDIAN_BOOK_WITNESS),
        "locators": copy.deepcopy(PRIMARY_LOCATORS),
        "implemented": implemented,
        "pending": [
            key for key in PRIMARY_LOCATORS if key not in implemented
        ],
        "policy": (
            "能直接定位《太乙紫庭经》文本的先结构化；未定位者保持pending，"
            "不得用统宗参校结果反填primary_result。"
        ),
    }


def build_c19_verified_primary_results() -> dict[str, dict[str, Any]]:
    """生成可送入 C18 source container 的已验证 primary_result 集合。"""
    return {
        "taiyi_nine_stars": {"primary_result": taiyi_nine_stars_primary()},
        "wenchang_changes": {"primary_result": wenchang_changes_primary()},
        "shiji_changes": {"primary_result": shiji_changes_primary_core()},
    }
