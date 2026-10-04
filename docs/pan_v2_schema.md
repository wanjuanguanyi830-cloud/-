# pan v2 canonical snapshot API

本次执行依据为用户提供的自包含 C1–C7 规格；未读取其它聊天。唯一写入仓库为 `wanjuanguanyi830-cloud/-`。

目标仓库此前已有规则模块、纯 `build_pan_v2`、legacy snapshot 搬运器和 v2 消费者，**没有日期排盘引擎、原版 Taiyi 类、Streamlit 或 CLI 应用**。本批保留这些接口，新增 `build_pan_v2_from_snapshot` 与 `Taiyi(snapshot).pan(...)`。这不是参考项目日期构造器的替代品；年、月、日、时的历法计算仍须由调用方提供。

## 入口与依赖

`taiyi_common` 不依赖 config、Taiyi、game_theory、jieqi。八占、七术依赖公共核心；周期与四太乙各自拥有明确坐标。`pan_v2` 不导入 Taiyi；`kintaiyi.py` 收集 snapshot，再调用 builder。旧 `taiyi_rules` 与 `config` 只做别名、输入或显示适配。

```python
from kintaiyi import Taiyi

snapshot = {
    "accumulated_year": 10154821,
    "year_accumulated_year": 10154821,
    "ji_style": 0, "taiyi_acumyear": 0,
    "taiyi_palace": 7,
    "wenchang_sector": "辰", "shiji_sector": "戌", "dingmu_sector": "巳",
    "home_cal": 15, "away_cal": 26, "fixed_cal": 40,
    "home_general": 7, "home_assistant": 8,
    "away_general": 3, "away_assistant": 4,
    "day_taiyi_palace": 6,
    "four_taiyi_yuan": 1,
}
pan = Taiyi(snapshot).pan(0, 0, scenario={
    "enemy_start_year_branch": "甲戌",
    "enemy_camp_day_taiyi_palace": 3,
    "enemy_first_arrival_taiyi_palace": 2,
})
```

`pan(ji_style, taiyi_acumyear, enable_game_theory=False, *, scenario=None)` 保留参考项目的位置参数形式。snapshot 的计式和积年法若已声明，必须与调用参数一致。此仓库新增的 Taiyi 以 snapshot 构造；没有声称支持日期构造器。

原日期引擎接入时可复用 `TaiyiCanonicalMixin` 的三基／四太乙方法及 `collect_core_snapshot(engine, style, profile)`。collector 对每个计式的核心方法只调用一次；日计太乙显式调用 `ty(2, profile)`，年计积年显式调用 `accnum(0, profile)`。调用方须在原 pan 内共享这一 snapshot，避免旧盘与 v2 各自重起盘。

## 根结构

| 区段 | 内容 |
|---|---|
| `schema_version` | 字符串 `2.0` |
| `meta` | 当前／年计积年、计式、source profile、四太乙三元输入依据 |
| `calendar` | 调用方提供的历法事实，不补造日期 |
| `board` | taiyi、eyes、calculations、generals、doors |
| `cycles` | three_bases、five_blessings、big_wander、small_wander、four_taiyi |
| `analysis` | patterns、eight_divinations、seven_methods、military |
| `modern` | 默认空；显式启用才加入现有现代特征投影，不宣称 Nash 求解 |
| `source_variants` | 版本异文独立存放 |
| `compat` | legacy_top_level=true、legacy_schema=pan-v1-flat |

太乙使用 `palace_id/trigram/sector/element/yin_yang`。中五的 sector 为 null。眼使用 `sector/god/sector_element/nine_palace/nine_palace_trigram/nine_palace_element`，辰土／九宫9木、戌土／九宫1金同时保留，投影标记 `projection_lossy=true`。

算数使用 `value/components/missing_components/classic_tags/parity/last_digit`。components 的 `ten/five/one` 对应天／地／人；15 等结构缺人，但古典标签为杜塞，不自动变成“无人”。四将使用 `role/palace_id/trigram/representative_sector/palace_element/intrinsic_element`。四太乙在独立十二宫运动，10／11／12 不投影为 2／6／4，不输出未确认的天地人 phase。

## 周期与缺输入

新 `taiyi_cycles` 与根 `config` 的周期入口使用 **1-based 积年**。旧 `kintaiyi.cycles` 保留此前公开的零基 elapsed-year 接口，先显式 `+1` 转换，再调用同一核心；没有第二套公式。勿将该 adapter 再用于真实 1-based 积年。

五福默认 +250，+115 为异文。大游无移位 profile 为 project_canonical，统宗 profile 才施加 +34；snapshot builder 默认统宗 profile，并记录实际采用的 offset。大游使用年计积年，非年盘缺 `year_accumulated_year` 时返回不可算；不会借月／日／时积年。金镜大游天目 offset0、统宗 +214。四太乙默认使用已确认基础起宫，显式 `four_taiyi_yuan` 才选择三元；元法依据记录在 meta，不反推三元。

七术外壳统一含 `id/name/computable/missing_inputs/reason/inputs/analysis/decision/variants/provenance`。无 scenario 时临津、狮子、猛虎、回军不可算；雷公、白龙必须有明确 `day_taiyi_palace`。白云可用现盘两大将。大将中五导致该侧不可算，总比较不完整，不强判另一方胜。五态与火十二长生分层；白龙的 direct_conflict 不覆盖 deployment 层。

任何缺失 snapshot 事实返回结构化不可算对象。patterns／doors 未提供时亦标记缺输入。`build_pan_v2` 仍是已有的纯事实组装器；`pan_adapter` 仍只搬运旧事实，两者不自动把旧断语提升为 canonical。需要规则计算时使用新增 canonical snapshot builder。

## 旧盘与 JSON

`Taiyi.pan` 先从 v2 facts 投影太乙落宮、主／客／定算、文昌、始擊、定目、四将、三基、五福、大游、小游和四太乙，再附加 `v2`，随后处理 enable_game_theory。已有 legacy snapshot 的其它中文 key 保留；已确认错误值按新事实更新。五福／大小游旧值为字典时保留字典容器并更新宫号。

v2 输出可以直接 `json.dumps`。strict assembler 拒绝非字符串键；旧八门分布整数键只在明确的 legacy adapter 中转为字符串，且拒绝转换冲突。内部 frozenset pair 不进入输出，四太乙同宫结果输出字符串列表。

## 来源与后续边界

本批规则来自本次完整规格，古籍卷页与影印证据仍 pending；参考仓库只核接口与积年 adapter。三基古例与四太乙古例测试显式使用年积年 `10153917 + 公元年`，没有修改运动公式配合例子。五福三基初会按 same_now and not same_previous；九宫、十六辰对冲各自独立，中宫对冲 pending。

目标仓库没有 jieqi.py 与 ming_pplbase 原实现，因此没有可直接修改的季节八态／民基断语。君基＋天乙新增事实接口使用天乙，不借普通太乙；完整断语仍 pending。卷五将帅旺衰未借七术 Mode B 补算。已有 C8+ 模块保留，本批不扩张其来源规则。
