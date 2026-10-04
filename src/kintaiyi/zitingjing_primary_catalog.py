"""C19 《太乙紫庭经》主来源篇目索引。

这里只记录已核到的篇目关系与定位状态，不执行术法公式。
"""

from __future__ import annotations

import copy
from typing import Any

CATALOG_VERSION = "taiyi-c19-zitingjing-primary-catalog-v1"
PRIMARY_SOURCE_ID = "zitingjing"
PRIMARY_SOURCE_TITLE = "太乙紫庭经"
SHIDIAN_BOOK_ENTRY = "https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u3291"
SHIDIAN_TOC = "https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q452g7jm"

PRIMARY_CATALOG: dict[str, dict[str, Any]] = {
    "taiyi_nine_stars": {
        "legacy_name": "太乙九星",
        "primary_location_status": "direct_primary_chapter_located",
        "primary_chapter_title": "释九宫所值九星",
        "primary_chapter_url": "https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u4tgl",
        "relation": "primary_nine_star_foundation",
        "implementation_status": "source_extractable",
        "collation_sources": ["tongzong_volume6", "tongzong_volume10"],
        "notes": (
            "《太乙紫庭经》本体直接有〈释九宫所值九星〉，内容含九星名义、"
            "九宫配属、十年一易和值符等。旧代码所谓“太乙九星”不可仅凭统宗卷六注释定义。"
        ),
    },
    "wenchang_nine_stars": {
        "legacy_name": "文昌九星",
        "primary_location_status": "bibliographic_anchor_only",
        "primary_chapter_title": "附太乙文昌九星值宫术",
        "primary_chapter_url": None,
        "relation": "appendix_or_related_zitingjing_transmission",
        "implementation_status": "pending_direct_primary_text",
        "collation_sources": ["tongzong_volume6"],
        "notes": (
            "现已见《太乙紫庭秘诀》目录著录“附太乙文昌九星值宫术”，"
            "但识典当前《太乙紫庭经》在线正文尚未直接定位该篇全文；不得以统宗公式代替主来源。"
        ),
    },
    "wenchang_changes": {
        "legacy_name": "文昌变化",
        "primary_location_status": "direct_primary_chapter_located",
        "primary_chapter_title": "释天目变化",
        "primary_chapter_url": "https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u5vdx",
        "relation": "exact_semantic_alias",
        "implementation_status": "source_extractable",
        "collation_sources": ["tongzong_volume6"],
        "notes": (
            "〈释天目变化〉正文明确天目“在地号曰文昌”，故可作为文昌变化主来源对应。"
        ),
    },
    "shiji_changes": {
        "legacy_name": "始击变化",
        "primary_location_status": "toc_confirmed_primary_chapter",
        "primary_chapter_title": "始击变化",
        "primary_chapter_url": None,
        "relation": "exact_title",
        "implementation_status": "pending_direct_page_fetch",
        "collation_sources": ["tongzong_volume6"],
        "notes": "《太乙紫庭经》卷一目录已直接列〈始击变化〉；待补直接页面定位后再结构化。",
    },
    "three_banners": {
        "legacy_name": "三旗行宫",
        "primary_location_status": "pending_direct_primary_location",
        "primary_chapter_title": None,
        "primary_chapter_url": None,
        "relation": "user_confirmed_primary_tradition_exact_chapter_pending",
        "implementation_status": "pending_direct_primary_text",
        "collation_sources": ["tongzong_volume10"],
        "notes": (
            "按项目来源策略以《太乙紫庭经》为主要参考；当前在线检索尚未找到"
            "与“三旗行宫”同名的紫庭经直接篇目，因此只保留统宗卷十参校，不先实现主来源公式。"
        ),
    },
    "nine_palace_nobles": {
        "legacy_name": "九宫贵神",
        "primary_location_status": "pending_direct_primary_location",
        "primary_chapter_title": None,
        "primary_chapter_url": None,
        "relation": "user_confirmed_primary_tradition_exact_chapter_pending",
        "implementation_status": "pending_direct_primary_text",
        "collation_sources": ["tongzong_volume10"],
        "notes": (
            "按项目来源策略以《太乙紫庭经》为主要参考；当前在线检索尚未找到"
            "与“九宫贵神”同名的紫庭经直接篇目。统宗卷十及其他九宫资料仅作参校。"
        ),
    },
}


def primary_catalog_entry(rule_key: str) -> dict[str, Any]:
    if rule_key not in PRIMARY_CATALOG:
        raise ValueError(f"未知C19规则: {rule_key}")
    return {
        "catalog_version": CATALOG_VERSION,
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "book_entry_url": SHIDIAN_BOOK_ENTRY,
        "toc_url": SHIDIAN_TOC,
        "rule_key": rule_key,
        **copy.deepcopy(PRIMARY_CATALOG[rule_key]),
    }


def primary_catalog() -> dict[str, Any]:
    entries = {key: primary_catalog_entry(key) for key in PRIMARY_CATALOG}
    ready = [
        key for key, item in entries.items()
        if item["implementation_status"] == "source_extractable"
    ]
    pending = [key for key in entries if key not in ready]
    return {
        "canonical": CATALOG_VERSION,
        "primary_source": PRIMARY_SOURCE_ID,
        "primary_source_title": PRIMARY_SOURCE_TITLE,
        "book_entry_url": SHIDIAN_BOOK_ENTRY,
        "toc_url": SHIDIAN_TOC,
        "ready_for_source_extraction": ready,
        "pending_primary_location_or_text": pending,
        "rules": entries,
        "policy": (
            "只有已定位《太乙紫庭经》直接篇目正文的规则才可进入主来源结构化；"
            "目录确认、书目附录或统宗参校均不能单独替代主来源正文。"
        ),
    }
