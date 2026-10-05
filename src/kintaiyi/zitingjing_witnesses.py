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
        "witness_type": "user_provided_manuscript_scan",
        "title": "太乙紫庭祕訣",
        "copy_description": "研易楼藏明钞本",
        "holding": "上海图书馆",
        "holding_evidence": "publisher_description_secondary",
        "user_previously_provided_manuscript_file": True,
        "current_session_file_index_status": "reattached_current_conversation",
        "direct_text_reinspection_status": "toc_inspected",
        "current_uploaded_pdf_pages": 150,
        "prior_terminology_extraction_status": "preliminary_completed_locally",
        "prior_terminology_repository_status": "local_terminology_json_not_migrated",
        "manuscript_toc_evidence": {
            "pdf_pages": [5, 6],
            "volumes_one_to_twelve_attested": True,
            "wenchang_nine_stars_title_attested": False,
            "note": "目录列卷一至卷十二及后附项目，未见“文昌九星值宫术”题名；目录未见不外推为全文绝对不存在。",
        },
        "modern_edition": {
            "title": "太乙紫庭秘诀",
            "editor": "吴炜维",
            "publisher": "香港星易图书有限公司",
            "year": 2015,
            "isbn": "9789881412058",
            "catalog_url": "https://www.xinyi.hk/goods-7102.html",
            "appendix_title": "附太乙文昌九星值宫术",
            "appendix_provenance": "unresolved",
            "note": "现代整理本收录同名附篇，不证明研易楼原钞目录含该题；是否由统宗材料增补目前只作来源假说。",
        },
        "public_resource_report": {
            "reported_pages": 181,
            "reported_size": "328MB",
            "status": "secondary_public_share_report_not_identical_to_current_150_page_upload_claimed",
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
    """聚合现代整理本“附太乙文昌九星值宫术”的当前来源状态。"""
    return {
        "rule_key": "wenchang_nine_stars",
        "target_title": "附太乙文昌九星值宫术",
        "status": "manuscript_toc_not_attested_modern_appendix_provenance_unresolved",
        "shanghai_yanyilou": {
            "manuscript_scan_reattached": True,
            "toc_pages": [5, 6],
            "toc_title_attested": False,
            "direct_text_reinspection_status": "toc_inspected",
        },
        "modern_edition": {
            "appendix_title_attested": True,
            "provenance": "unresolved",
            "tongzong_addition_hypothesis": "plausible_not_proven",
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
        "ziting_primary_result_allowed": False,
        "current_rule_source_gap": False,
        "known_executable_rule_id": "C70-TONGZONG-WENCHANG-NINE-STARS",
        "known_executable_source_profile": "tongzong_volume6_ngj_wenchang_nine_stars",
        "next_action": (
            "如需继续研究，应追现代整理本编辑来源/附篇底本；"
            "这属于编辑史与来源问题，不再阻塞C70文昌九星算法。"
        ),
    }

