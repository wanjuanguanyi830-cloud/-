"""太乙术语、规则、历史source profiles与modern production入口。

核心项目约束：
- 古籍规则按来源分层，不因同名静默合并；
- modern production 使用现代天文/现代历法事实；
- 太乙岁唯一换年点是真实天文冬至交节瞬间；
- 元旦、春节、立春、春分均不改变太乙岁。
"""

RULESET_VERSION = "taiyi-t7-d8-v1"

PRODUCTION_CALENDAR_MODE = "modern_astronomy_lunisolar"
TAIYI_YEAR_BOUNDARY = "astronomical_winter_solstice"
TAIYI_YEAR_LABEL_RULE = "Gregorian Y winter solstice instant => Taiyi Y+1"
NON_TAIYI_YEAR_BOUNDARIES = ("元旦", "春节", "立春", "春分")

PUBLIC_MODERN_ENTRYPOINTS = {
    "calendar_context": "kintaiyi.taiyi_modern_calendar.production_calendar_context",
    "pan_v2": "kintaiyi.taiyi_modern_pan.build_modern_pan_v2",
}
