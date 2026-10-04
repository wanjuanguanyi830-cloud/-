# C60 旧错误公式 / 非等价旧实现隔离注册表

日期：2026-10-05

## 1. 目标

C60 是治理层，不新增太乙算法。

唯一 registry：

`src/kintaiyi/legacy_formula_quarantine.py`

rule id：

`C60-LEGACY-QUARANTINE`

用途：

- 把已经有来源审计结论的错误公式集中登记；
- 把“周期表面相合但未证明公式等价”的旧实现集中登记；
- 给出明确 replacement rule / layer；
- 固定 `promotion_allowed=False`；
- 防止后续重构把旧函数重新提升成 canonical。

未知旧实现不会因为“不在清单”就自动视为正确；仍应保持待审。

## 2. 十精旧实现

已集中隔离：

- `config.flybird`：旧 %8，且八项路径漏中五 → `C53-FLYBIRD`；
- `config.fivewind`：旧 %29 → `C53-FIVEWIND`；
- `config.eightwind`：八项表漏中五 → `C53-EIGHTWIND`；
- `config.threewind`：八项表漏九步 → `C53-THREEWIND`；
- `config.taijun`：只保留旧mod4结果，不等价于完整40/4来源路径 → `C53-TAIZUN`；
- `config.wuxing`：周期相合但来源路径不完整 → `C53-WUXING`；
- `config.tian_wang`：周期相合但缺十六神四维重留等来源结构 → `C55-TIANHUANG`；
- `config.kingfu`：周期相合但缺四正重留/名称/盈差边界 → `C55-DIFU`；
- `config.tian_shi`：周期相合但未保存120/12、阳寅阴申与异文边界 → `C56-TIANSHI`；
- `yunqi._TEN_JING_FN`：把帝符写成地符，并以太岁替代太乙数 → C52 registry；
- `yunqi.shijing_shu`：数值核心可参校，但天气 wrapper 混层 → `C54-TAIYI-NUMBER`。

## 3. 卷九等已证实非等价旧实现

- `guiyun.yinyang_jiu_e`：把九段段长误当累计阈值 → `C46-YJ-9E`；
- `guiyun.ehui_xingxian`：只用年支+16位简单步数 → `C43-V9-EHUI`；
- `guiyun.guozheng_bianyi`：只收年支静态旋转六神 → `C44-V9-GOV`；
- `guiyun.suizhong_zaifa`：十六位offset且只做简化月层 → `C45-V9-DISASTER`；
- `guiyun.yunqi_zhanbo`：日支遗漏、云生辰语义错位、己数错误、多关系被if/elif压扁 → `C51-CLOUD-OMEN`；
- `guiyun.outer_hexagram_offset_50`：旧+50外卦偏移无直接明文 → `C41-DY-HEX`；
- `legacy.flybird_wl`：盘内飞鸟位置推断不能替代真实外部飞鸟观测 → `J4M-11`。

## 4. 现代材料不等于错误公式

现代：

- `modern_liunian_nayin_2026`
- `MODERN-LIUNIAN-NAYIN`

不进入 C60 quarantine。

它们属于合法但独立的：

`source_class="modern_reconstruction"`

正确策略是物理/命名空间隔离，不是把现代材料判为“错误”。

## 5. 验收语义

C60 每条记录必须：

- `promotion_allowed=False`
- `canonical_equivalent=False`
- 有具体 reason；
- 有来源模块；
- 有替代规则，或明确为何只能继续隔离。

C60 是“已证实问题清单”，不是“未审旧代码自动白名单”的反面。

新增旧公式时，若已有审计判定其不可直接升格，应同步进入本 registry。


## C58 / C59 补充隔离

新增：

### yunqi._YUNQI_COLOR.white

旧表：

- 白 7 / 6 → 亥子。

C58 校定：

- 白 7 / 6 → 申酉；
- 黑 1 / 8 → 亥子。

因此旧白云时支：

- `canonical_equivalent=False`
- replacement: `C58-CLOUD-TIMING`

### yunqi.shijing_shu

360 / 72 数值核心可以作为 C54 参校，但 wrapper 同时混入天气断语。

C59 又确认：

- 30 / 40 是直接天气数值；
- 50存在句读异文；
- 旧10 / 5不是当前直接条文的独立天气特例；
- 合天目 / 飞鸟 / 主计等必须显式关系证据。

因此 replacement 同时指向：

- `C54-TAIYI-NUMBER`
- `C59-TAIYI-NUMBER-OMEN`

不得只迁 C54 后保留旧天气 wrapper。
