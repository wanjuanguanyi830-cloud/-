from kintaiyi.modern_nayin_variant import (
    MODERN_NAYIN_PROFILE,
    compare_modern_nayin_elements,
    modern_day_tone_sequence,
    modern_star_base_nayin,
    modern_star_transformed_nayin,
)


def test_modern_variant_is_explicitly_noncanonical():
    data = modern_star_base_nayin("木", "子")
    assert data["profile"] == MODERN_NAYIN_PROFILE
    assert data["source_class"] == "modern_reconstruction"
    assert data["canonical"] is False


def test_modern_base_nayin_reproduces_material_taiyi_example():
    # 材料示例：太乙木 -> 角音 -> 纳壬；落子 -> 壬子 -> 桑柘木
    data = modern_star_base_nayin("木", "子")
    assert data["tone"] == "角"
    assert data["selected_stem"] == "壬"
    assert data["lu"] == "黄钟"
    assert data["jiazi"] == "壬子"
    assert data["nayin_name"] == "桑柘木"
    assert data["nayin_element"] == "木"


def test_modern_base_nayin_uses_yin_stem_on_yin_branch():
    data = modern_star_base_nayin("木", "丑")
    assert data["tone"] == "角"
    assert data["selected_stem"] == "癸"
    assert data["lu"] == "大吕"
    assert data["jiazi"] == "癸丑"
    assert data["nayin_name"] == "桑柘木"


def test_modern_branch_lu_mapping_uses_classical_twelve_lu_background():
    expected = {
        "子": "黄钟", "丑": "大吕", "寅": "太簇", "卯": "夹钟",
        "辰": "姑洗", "巳": "仲吕", "午": "蕤宾", "未": "林钟",
        "申": "夷则", "酉": "南吕", "戌": "无射", "亥": "应钟",
    }
    for branch, lu in expected.items():
        data = modern_star_base_nayin("土", branch)
        assert data["lu"] == lu


def test_modern_dimensions_require_explicit_branch_proxy_mode():
    missing_mode = modern_star_base_nayin("木", "乾")
    assert missing_mode["computable"] is False
    assert missing_mode["error"] == "dimension_requires_explicit_mode"

    data = modern_star_base_nayin("木", "乾", dimension_mode="branch_proxy")
    assert data["branch"] == "亥"
    assert data["lu"] == "应钟"
    assert data["location_method"] == "branch_proxy"


def test_modern_day_tone_sequence_follows_material():
    assert modern_day_tone_sequence("甲")["tone_sequence"] == ["宫", "徵", "羽", "商", "角"]
    assert modern_day_tone_sequence("乙")["tone_sequence"] == ["徵", "羽", "商", "角", "宫"]
    assert modern_day_tone_sequence("丙")["tone_sequence"] == ["羽", "商", "角", "宫", "徵"]
    assert modern_day_tone_sequence("壬")["tone_sequence"] == ["商", "角", "宫", "徵", "羽"]
    assert modern_day_tone_sequence("癸")["tone_sequence"] == ["角", "宫", "徵", "羽", "商"]


def test_modern_transformed_nayin_requires_explicit_transformed_tone():
    data = modern_star_transformed_nayin("宫", "子", day_stem="乙")
    assert data["construction"] == "transformed_tone_explicit"
    assert data["transformed_tone"] == "宫"
    assert data["day_tone_sequence"] == ["徵", "羽", "商", "角", "宫"]
    assert "不从日干序列擅自推导" in data["policy_detail"]


def test_modern_nayin_comparison_returns_relation_not_verdict():
    control = compare_modern_nayin_elements("木", "土")
    assert control["relation"] == "一克二"
    assert control["verdict"] is None

    generate = compare_modern_nayin_elements("金", "水")
    assert generate["relation"] == "一生二"
    assert generate["verdict"] is None

    same = compare_modern_nayin_elements("火", "火")
    assert same["relation"] == "比和"
    assert same["verdict"] is None
