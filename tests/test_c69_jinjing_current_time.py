import pytest

from kintaiyi.jinjing_current_time import (
    DAY_PERIOD_RULERS,
    EXCLUDED_BRANCHES,
    FULL_FORMULA_BOUNDARY,
    GENERAL_RULES,
    c69_catalog,
    current_time_core,
    general_omen,
    tianyi_period_ruler,
)


@pytest.mark.parametrize(
    "stem,morning,evening",
    [
        ("甲", "小吉", "大吉"),
        ("戊", "大吉", "小吉"),
        ("庚", "大吉", "小吉"),
        ("己", "神后", "传送"),
        ("乙", "传送", "神后"),
        ("丁", "登明", "从魁"),
        ("丙", "从魁", "登明"),
        ("癸", "太乙", "太冲"),
        ("壬", "太冲", "太乙"),
        ("辛", "功曹", "胜光"),
    ],
)
def test_c69_day_stem_morning_evening_table(stem, morning, evening):
    assert tianyi_period_ruler(stem, "朝")["ruler"] == morning
    assert tianyi_period_ruler(stem, "暮")["ruler"] == evening


def test_c69_ruler_branches_never_use_chen_or_xu():
    used = {
        tianyi_period_ruler(stem, period)["branch"]
        for stem in DAY_PERIOD_RULERS
        for period in ("朝", "暮")
    }
    assert "辰" not in used
    assert "戌" not in used
    assert EXCLUDED_BRANCHES["辰"]["designation"] == "天庭"
    assert EXCLUDED_BRANCHES["戌"]["designation"] == "天狱"
    assert EXCLUDED_BRANCHES["戌"]["source_form"] == "戍"


@pytest.mark.parametrize(
    "general,element,verdict",
    [
        ("螣蛇", "火", "凶"),
        ("朱雀", "火", "凶"),
        ("六合", "木", "吉"),
        ("勾陈", "土", "凶"),
        ("青龙", "木", "吉"),
        ("太阴", "金", "吉"),
        ("玄武", "水", "凶"),
        ("太常", "土", "吉"),
        ("白虎", "金", "凶"),
        ("天空", "土", "凶"),
    ],
)
def test_c69_direct_general_verdicts(general, element, verdict):
    data = general_omen(general)
    assert data["element"] == element
    assert data["verdict"] == verdict


def test_c69_tianhou_has_no_invented_verdict():
    data = general_omen("天后")
    assert data["verdict"] is None
    assert data["source_status"] == "direct_no_explicit_verdict"
    assert data["matters"] == ["蔽匿", "妇人", "淫乱事"]


def test_c69_tianyi_verdict_requires_explicit_qi_state():
    missing = general_omen("天乙贵神")
    assert missing["verdict"] is None
    assert "须显式给王相/囚死" in "；".join(missing["pending"])

    assert general_omen("天乙贵神", tianyi_qi_state="王相")["verdict"] == "吉"
    assert general_omen("天乙贵神", tianyi_qi_state="囚死")["verdict"] == "凶"

    with pytest.raises(ValueError, match="王相/囚死"):
        general_omen("天乙贵神", tianyi_qi_state="旺")


def test_c69_qi_state_cannot_be_silently_applied_to_other_generals():
    with pytest.raises(ValueError, match="只用于天乙贵神"):
        general_omen("六合", tianyi_qi_state="王相")


def test_c69_rejects_unknown_stem_period_and_general():
    with pytest.raises(ValueError, match="十天干"):
        tianyi_period_ruler("甲子", "朝")
    with pytest.raises(ValueError, match="朝/暮"):
        tianyi_period_ruler("甲", "昼")
    with pytest.raises(ValueError, match="未知C69天将"):
        general_omen("值符")


def test_c69_core_is_explicitly_partial_not_full_current_time_formula():
    data = current_time_core(day_stem="甲", period="朝", general="六合")
    assert data["tianyi_ruler"]["ruler"] == "小吉"
    assert data["general_omen"]["verdict"] == "吉"
    assert data["complete_current_time_formula"] is False
    assert data["full_formula_boundary"] == FULL_FORMULA_BOUNDARY
    assert "日度" in "；".join(FULL_FORMULA_BOUNDARY["pending_upstream"])


def test_c69_catalog_locks_twelve_generals_and_partial_boundary():
    data = c69_catalog()
    assert len(GENERAL_RULES) == 12
    assert len(data["day_period_rulers"]) == 10
    assert data["full_formula_boundary"]["complete_current_time_formula"] is False
    assert data["source_profile"] == "jinjing_volume1_current_time"
