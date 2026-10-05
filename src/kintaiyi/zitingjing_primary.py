"""C19 《太乙紫庭经》第一批可直接定位的主来源结构。

这里只结构化已能在在线古籍见证中直接定位的内容。
未定位到《太乙紫庭经》直接条文的项目保持 pending，不借统宗参校本补成主来源。
"""

from __future__ import annotations

import copy
from typing import Any

from .taiyi_rules import integer

C19_VERSION = "taiyi-c19-zitingjing-primary-v1"
C125_VERSION = "taiyi-c125-ziting-taiyi-nine-stars-cycle-v1"
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
        "status": "prior_scan_confirmed_page_record_pending",
        "section": "附太乙文昌九星值宫术",
        "url": None,
        "legacy_scan_recovery": {
            "asset": "terminology/zitingjing-legacy-scan-recovery.json",
            "status": "manuscript_previously_scanned_original_page_record_not_reattached",
            "user_confirmed_manuscript": "研易楼藏《太乙紫庭祕訣》明钞本",
            "local_copy_status": "E盘仍存，当前执行环境未挂载",
            "code_residue_note": "旧config.py九星段明确标注来源为《太乙统宗宝鉴》卷六，因此其中词形不能直接认定为研易楼本逐字扫描结果。",
        },
        "catalog_witness": {
            "title": "太乙紫庭秘诀（现代整理本目录）",
            "urls": [
                "https://www.chinyuan.com.tw/all_book/more?id=7195",
                "https://www.xinyi.hk/goods-7102.html",
            ],
            "evidence": "两处现代整理本目录均列“附太乙文昌九星值宫术”",
        },
        "scan_share_leads": [
            {
                "site": "书格",
                "title": "太乙紫庭祕訣 研易樓藏明鈔本",
                "url": "https://www.shuge.org/meet/topic/96517/",
                "reported_extent": "181单页灰度，328M",
                "status": "share_page_located_scan_not_inspected",
                "note": "分享帖称文本与北大本可互补，并列出多个网盘转存；当前未取得可逐页核读的扫描正文。",
            },
        ],
        "witness_context": "该术附属于《太乙紫庭秘诀》传本系统；用户确认研易楼明钞本此前已在术语库整理阶段扫描且E盘仍有原件，但原扫描页/旧terminology.json尚未在本执行环境重新挂载。旧config.py九星残留明确标注为统宗卷六来源，不作为研易楼本逐字见证。",
    },
    "three_banners": {
        "status": "project_primary_attribution_unverified",
        "section": None,
        "url": None,
        "catalog_check": {
            "ziting_mijue_catalog_result": "not_found",
            "checked_catalogs": [
                "https://www.chinyuan.com.tw/all_book/more?id=7195",
                "https://www.xinyi.hk/goods-7102.html",
            ],
            "note": "已查《太乙紫庭秘诀》十二卷及附录目录未见“三旗行宫”题名。",
        },
        "collation_locator": {
            "source": "太乙统宗宝鉴卷十",
            "section": "明太乙与三旗行宫会合术",
            "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec",
        },
        "witness_context": "项目曾指定《太乙紫庭经》为主来源目标，但当前未取得目录或正文归属证据；统宗卷十有直接可定位文本。",
    },
    "nine_palace_nobles": {
        "status": "project_primary_attribution_unverified",
        "section": None,
        "url": None,
        "catalog_check": {
            "ziting_mijue_catalog_result": "not_found",
            "checked_catalogs": [
                "https://www.chinyuan.com.tw/all_book/more?id=7195",
                "https://www.xinyi.hk/goods-7102.html",
            ],
            "note": "已查《太乙紫庭秘诀》十二卷及附录目录未见“九宫贵神”题名。",
        },
        "collation_locator": {
            "source": "太乙统宗宝鉴卷十",
            "section": "明太乙九宫贵神术",
            "url": "https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec",
        },
        "witness_context": "项目曾指定《太乙紫庭经》为主来源目标，但当前未取得目录或正文归属证据；统宗卷十有直接可定位文本。",
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


TAIYI_NINE_STARS_PRIMARY_CYCLE_EVIDENCE = {
    "rule_id": "C125-ZITING-TAIYI-NINE-STARS-CYCLE",
    "section": "释九宫所值九星",
    "url": "https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u4tgl",
    "normalized_facts": [
        "九星按十年一换直符。",
        "开元十二年原例积算为1937281，九星循环余31。",
        "余31按天蓬、天芮、天冲各十年后，天辅为直符且入星第1年。",
        "正文另记甲年、乙年分别加六甲、六乙；完整十干动态布星暂不由OCR残文外推。",
    ],
    "derived_cycle": {
        "years_per_star": 10,
        "star_count": 9,
        "cycle_years": 90,
        "derivation": "九星×每星十年；且1937281 mod 90 = 31，与原例天辅直符第1年吻合。",
    },
    "example": {
        "accumulated_count": 1937281,
        "cycle_remainder": 31,
        "direct_star": "天辅",
        "year_in_star": 1,
    },
    "boundary": {
        "direct_star_cycle_supported": True,
        "full_year_stem_distribution_supported": False,
        "reason": "主来源目前足以固定十年一星与直符循环；六甲/六乙加宫句存在，但未在本层从OCR残文强推完整十干九星动态排布。",
    },
}


def taiyi_nine_stars_primary_cycle(accumulated_count: int) -> dict[str, Any]:
    """按《紫庭经》〈释九宫所值九星〉直接正文计算太乙九星直符周期。

    当前只实现直接文本足以支持的 90 年循环 / 10 年一星。
    年干加宫仅保留为文本证据，不在本函数强推完整九星动态分布。
    """
    count = integer(accumulated_count, 1)
    remainder = count % 90
    cycle_count = remainder or 90
    zero_index = cycle_count - 1
    star_index = zero_index // 10
    year_in_star = zero_index % 10 + 1
    star = TAIYI_NINE_STARS_PRIMARY[star_index]
    return {
        "schema_version": "1.0",
        "canonical": C125_VERSION,
        "rule_id": "C125-ZITING-TAIYI-NINE-STARS-CYCLE",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "source_locator": copy.deepcopy(PRIMARY_LOCATORS["taiyi_nine_stars"]),
        "accumulated_count": count,
        "cycle_years": 90,
        "cycle_remainder": remainder,
        "cycle_count": cycle_count,
        "years_per_star": 10,
        "direct_star_number": star_index + 1,
        "direct_star": star["star"],
        "year_in_star": year_in_star,
        "full_dynamic_distribution": None,
        "source_evidence": copy.deepcopy(TAIYI_NINE_STARS_PRIMARY_CYCLE_EVIDENCE),
        "policy": (
            "只使用《紫庭经》直接正文足以固定的十年一星循环；"
            "不借C124《统宗》十干加宫表补成本来源完整动态排布。"
        ),
    }


def taiyi_nine_stars_primary() -> dict[str, Any]:
    """返回《太乙紫庭经》〈释九宫所值九星〉的静态九宫表。

    本篇另有十年一星的直符周期，已由 taiyi_nine_stars_primary_cycle 独立实现；
    十干完整动态布星仍不从参校本反填。
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
            "direct_cycle_supported": True,
            "direct_cycle_runtime": "kintaiyi.zitingjing_primary.taiyi_nine_stars_primary_cycle",
            "years_per_star": 10,
            "cycle_years": 90,
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
        "detailed_year_stem_element_table_status": "collated_with_preserved_variants",
        "year_element_collation": shiji_year_element_collation(),
        "policy": (
            "逐岁干×五行已形成25项正规化表；"
            "OCR校字保留原读法，真正内容异文继续并列，不无痕统一。"
        ),
    }


# C31 〈始击变化〉逐岁干×五行灾应的校勘层。
# 只保存当前在线见证可辨读的结构事实；OCR冲突项不得静默正规化。
SHIJI_YEAR_ELEMENT_COLLATION = {
    "甲乙": {
        "rows": [
            {"witness_label": "水", "element": "水", "status": "stable",
             "effects": ["北方兵动", "算和则冬有和亲", "岁稔", "大水"]},
            {"witness_label": "金", "element": "金", "status": "stable",
             "effects": ["西方兵起", "东方有败"]},
            {"witness_label": "木", "element": "木", "status": "stable_with_minor_ocr_gap",
             "effects": ["东方兵起", "舟车事兴"],
             "collation_note": "主见证末字缺；《太乙秘书》参校作岁丰。"},
            {"witness_label": "火", "element": "火", "status": "stable",
             "effects": ["南方兵动", "夏旱火热", "民流亡", "疾病", "所临分野多灾"]},
            {"witness_label": "土", "element": "土", "status": "stable_across_collation",
             "effects": ["中宫兵动", "与太乙掩迫格则臣下谋上", "废将辅", "土工兴作"],
             "collation_note": "该句接在甲乙火项后的下一段，非丙丁组。"},
        ],
        "missing_elements": [],
        "status": "complete_five_elements",
    },
    "丙丁": {
        "rows": [
            {"witness_label": "水", "element": "水", "status": "stable_with_minor_ocr_noise",
             "effects": ["东北兵起", "夏大水", "民流亡"]},
            {"witness_label": "火", "element": "火", "status": "stable",
             "effects": ["南方有变", "兵动", "大旱", "民饥", "疾病", "兵革"]},
            {"witness_label": "土", "element": "土", "status": "stable_with_wording_variants",
             "effects": ["中宫相关兵忧"],
             "collation_note": "各见证在“东夷/东京/中宫忧变”等字句有差异，暂只保留共同核心。"},
            {"witness_label": "木", "element": "木", "status": "stable",
             "effects": ["春冬东方有和亲"]},
            {"witness_label": "金", "element": "金", "status": "stable",
             "effects": ["西方兵动", "金银贵", "重臣被诛"]},
        ],
        "missing_elements": [],
        "status": "complete_five_elements_with_wording_variants",
    },
    "戊己": {
        "rows": [
            {"witness_label": "水", "element": "木", "status": "ocr_corrected_by_collation",
             "effects": ["东方兵动"],
             "collation_witnesses": ["太乙秘书", "太乙统宗宝鉴卷六"],
             "correction": "识典《太乙紫庭经》OCR首字作水；两参校见证均作木，且本组随后另有水项。"},
            {"witness_label": "火", "element": "火", "status": "stable",
             "effects": ["南方有兵", "蝗虫", "谷贵", "大旱", "民流移"]},
            {"witness_label": "土", "element": "土", "status": "stable",
             "effects": ["中宫忧", "土工", "山崩地动"]},
            {"witness_label": "金", "element": "金", "status": "stable",
             "effects": ["西方兵起", "与北方相争"]},
            {"witness_label": "水", "element": "水", "status": "stable",
             "effects": ["征伐北方", "大臣被诛", "夏旱", "冬大水雨雪"]},
        ],
        "missing_elements": [],
        "status": "complete_after_ocr_collation",
    },
    "庚辛": {
        "rows": [
            {"witness_label": "木", "element": "木", "status": "stable",
             "effects": ["东方兵兴", "民流移"]},
            {"witness_label": "金", "element": "金", "status": "stable",
             "effects": ["西方兵动"]},
            {"witness_label": "水", "element": "水", "status": "stable",
             "effects": ["北方兵起"]},
            {"witness_label": "火", "element": "火", "status": "stable_with_minor_ocr_noise",
             "effects": ["南方兵动", "中国火灾", "掩捕袭夺", "岁旱", "金银贵"]},
            {"witness_label": "土", "element": "土", "status": "textual_variant",
             "effects": ["中国或邻国兵兴", "民丰"],
             "variants": {
                 "taiyi_zitingjing_online": "夏大旱",
                 "taiyi_mishu_and_tongzong_collation": "夏大水",
             },
             "resolution": "preserve_both_no_silent_merge"},
        ],
        "missing_elements": [],
        "status": "complete_five_elements_with_textual_variant",
    },
    "壬癸": {
        "rows": [
            {"witness_label": "水", "element": "水", "status": "stable_with_wording_variants",
             "effects": ["北方或西北有兵", "冬寒霜雪"]},
            {"witness_label": "金", "element": "金", "status": "stable",
             "effects": ["西方进宝", "大丰", "民和"]},
            {"witness_label": "火", "element": "火", "status": "stable_with_minor_ocr_noise",
             "effects": ["南方多灾", "夏旱", "秋冬大水霜雪"]},
            {"witness_label": "木", "element": "木", "status": "stable_with_wording_variants",
             "effects": ["东方兵事", "疾病"]},
            {"witness_label": "王", "element": "土", "status": "ocr_corrected_by_collation",
             "effects": ["中国有兵"],
             "collation_witnesses": ["太乙秘书", "太乙统宗宝鉴卷六", "太白兵备统宗宝鉴另一识典见证"],
             "correction": "主在线OCR作王；多参校见证均作土。"},
        ],
        "missing_elements": [],
        "status": "complete_after_ocr_collation",
    },
}


def shiji_year_element_collation() -> dict[str, Any]:
    """返回〈始击变化〉逐岁干×五行灾应的校勘表。

    OCR字符误识可用多见证参校纠正；真正内容异文则必须并列保留。
    """
    normalized_rows = 0
    ocr_corrections = []
    textual_variants = []
    for stem_group, group in SHIJI_YEAR_ELEMENT_COLLATION.items():
        for row in group["rows"]:
            if row.get("element"):
                normalized_rows += 1
            if row["status"] == "ocr_corrected_by_collation":
                ocr_corrections.append({
                    "stem_group": stem_group,
                    "witness_label": row["witness_label"],
                    "normalized_element": row["element"],
                    "collation_witnesses": copy.deepcopy(row["collation_witnesses"]),
                })
            if row["status"] == "textual_variant":
                textual_variants.append({
                    "stem_group": stem_group,
                    "element": row["element"],
                    "variants": copy.deepcopy(row["variants"]),
                    "resolution": row["resolution"],
                })
    complete = (
        normalized_rows == 25
        and all(not group["missing_elements"] for group in SHIJI_YEAR_ELEMENT_COLLATION.values())
    )
    return {
        "canonical": C19_VERSION,
        "rule_key": "shiji_changes",
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "source_locator": copy.deepcopy(PRIMARY_LOCATORS["shiji_changes"]),
        "source_status": "direct_primary_text_collated",
        "stem_groups": copy.deepcopy(SHIJI_YEAR_ELEMENT_COLLATION),
        "normalized_row_count": normalized_rows,
        "ocr_corrections": ocr_corrections,
        "textual_variants": textual_variants,
        "normalization_complete": complete,
        "policy": (
            "明确OCR误识可在多见证一致时校正并保留原witness_label；"
            "内容层异文不得以多数表决静默覆盖，必须并列保存。"
        ),
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
