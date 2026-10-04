"""《太乙紫庭经 / 紫庭秘诀》传本与馆藏见证目录。

本模块只记录“哪一条传本/目录/在线转录能证明什么”：
- 不把馆藏存在等同于已读正文；
- 不自动判断各传本同源同内容；
- 不生成任何术法 canonical result。
"""

from __future__ import annotations

import copy
from typing import Any

ZITINGJING_WITNESS_VERSION = "zitingjing-manuscript-witnesses-v1"

WITNESSES = {
    "taibai_bingbei_harvard_qing_copy": {
        "witness_type": "manuscript_in_compilation",
        "title": "太白兵备统宗宝鉴",
        "copy_description": "清咸丰十年前后抄本 / 顾氏重抄系统",
        "holding": "Harvard-Yenching Library",
        "holding_evidence": "secondary_catalog_and_resource_description",
        "online_transcription": {
            "provider": "识典古籍",
            "book_id": "HY5849",
            "volume1_url": "https://www.shidianguji.com/book/HY5849/chapter/1l1bukbn18088",
            "catalog_url": "https://www.shidianguji.com/book/HY5849/chapter/1l1bujx4cdszk",
        },
        "ziting_text_evidence": {
            "level": "direct_online_transcription",
            "attested_titles": [
                "太乙紫庭经表",
                "太乙紫庭序",
                "释九宫所值九星",
                "释天目变化",
                "始击变化",
            ],
        },
        "wenchang_nine_star_appendix": {
            "status": "not_located_in_current_online_search",
            "policy": "未检出不等于该抄本绝无此文；只能记当前在线检索未定位。",
        },
    },
    "shanghai_yanyilou_ming_copy": {
        "witness_type": "reported_manuscript_base",
        "title": "太乙紫庭秘诀",
        "copy_description": "研易楼藏明钞本（现代整理本出版说明及二级资源页如此称）",
        "holding": "上海图书馆",
        "holding_evidence": "publisher_description_secondary",
        "user_previously_provided_manuscript_file": True,
        "current_session_file_index_status": "not_retrievable_in_current_file_index",
        "direct_text_reinspection_status": "pending_reinspection_from_previously_provided_file",
        "prior_terminology_extraction_status": "preliminary_completed_locally",
        "prior_terminology_repository_status": "local_terminology_json_not_migrated",
        "modern_edition": {
            "title": "太乙紫庭秘诀",
            "editor": "吴炜维",
            "publisher": "香港星易图书有限公司",
            "year": 2015,
            "isbn": "9789881412058",
            "catalog_url": "https://www.xinyi.hk/goods-7102.html",
        },
        "catalog_attestation": {
            "appendix_title": "附太乙文昌九星值宫术",
            "evidence_level": "catalog_attested_text_pending",
        },
        "resource_report": {
            "reported_pages": 181,
            "reported_size": "328MB",
            "status": "previously_user_provided_file_not_currently_retrievable",
        },
    },
    "peking_university_reported_copy": {
        "witness_type": "reported_holding",
        "title": "太乙紫庭经 / 紫庭秘诀（题名待馆藏目录核实）",
        "holding": "北京大学图书馆",
        "holding_evidence": "secondary_article_report_only",
        "direct_catalog_record_found": False,
        "online_resource_found": False,
        "policy": "未找到馆方可核目录前不得升级为verified holding。",
    },
    "qianqingtang_bibliographic_entry": {
        "witness_type": "historical_bibliographic_attestation",
        "title": "紫庭秘诀",
        "source": "千顷堂书目 卷十三",
        "url": "https://www.zhonghuashu.com/wiki/千頃堂書目_(四庫全書本)/卷13",
        "evidence_level": "title_attested_only",
        "identity_resolution": "not_proven_identical_to_current_ziting_mijue_copy",
        "policy": "历史书目题名可证明有同名书著录，但不能单独证明现存抄本的卷次、附篇或作者。",
    },
}


def zitingjing_manuscript_witnesses() -> dict[str, Any]:
    """返回传本见证目录；不选择 canonical manuscript。"""
    return {
        "schema_version": "1.0",
        "canonical": ZITINGJING_WITNESS_VERSION,
        "witnesses": copy.deepcopy(WITNESSES),
        "canonical_manuscript_selected": None,
        "cross_witness_identity_assumed": False,
        "policy": (
            "哈佛清抄汇编、上海研易楼本、北大报道线索及历史书目必须分开。"
            "馆藏/目录证据不能替代直接正文，不能假设不同传本附录完全相同。"
        ),
    }


def wenchang_nine_star_appendix_locator_status() -> dict[str, Any]:
    """聚合“附太乙文昌九星值宫术”当前定位状态。"""
    return {
        "rule_key": "wenchang_nine_stars",
        "target_title": "附太乙文昌九星值宫术",
        "status": "catalog_attested_primary_text_pending",
        "shanghai_yanyilou": {
            "catalog_attested": True,
            "user_previously_provided_file": True,
            "direct_text_reinspection_status": "pending",
        },
        "harvard_qing_compilation": {
            "ziting_text_present": True,
            "appendix_direct_text_located": False,
            "result_scope": "current_online_search_only",
        },
        "peking_university": {
            "holding_reported": True,
            "holding_verified_by_library_catalog": False,
            "direct_text_obtained": False,
        },
        "primary_result_allowed": False,
        "next_action": (
            "优先重新定位用户此前提供的上海研易楼明抄本并直接校读附篇；"
            "其次核哈佛抄本是否另有同术异题；"
            "再核北京大学馆藏目录。"
        ),
    }
