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


## C57–C59 旧 yunqi 综合包装器隔离

进一步审计旧 `yunqi.py` 后，新增以下 quarantine。

### yunqi._YUNQI_COLOR

不只白云一项有问题。旧整表还混入：

- 黄5；
- 黑6；
- 红2/7；

等当前“太乙初移宫云色时变”直接条文未支持的独立计数 / 色名。

因此整表不得整体升格。

replacement：

- `C58-CLOUD-TIMING`
- `C58-WEATHER-OBSERVATION`

### yunqi._shu_duanyu

旧特殊数断语同时存在：

- 数10独立“大风”无直接条文；
- 数5独立“地数”无直接天气条文；
- 把数40的黄雾混入数50；
- 没有保存数50句读异文。

replacement：

`C59-TAIYI-NUMBER-OMEN`

### yunqi._JING_HEHUI

旧表：

- 使用“地符”旧名；
- 多条合会 / 宫位断语被压缩或错配；
- 缺旺相、阴阳宫与异文条件。

replacement：

`C57-TEN-ESSENCE-CLOUD-CONJUNCTION`

### yunqi.shijing_luo

该 wrapper 直接遍历错误旧 `_TEN_JING_FN`，继承：

- 地符 / 帝符名称问题；
- 太岁替代太乙数；
- 多项旧位置公式。

因此不得作为十精位置真源。

replacement 由 C52/C53/C55/C56 分层承担。

### yunqi.yunqi_hehui

旧函数仅因“宫号相等”就自动制造“合太乙”。

C57 已固定：

- 合会必须显式输入；
- `auto_position_lookup_used=False`。

因此旧自动同宫推断整体 quarantine。

### yunqi.yunqi_zongduan / yunqi.zonghe

两者会把以下内容重新揉成一个旧综合层：

- 旧十精落宫；
- 太乙数；
- 自动同宫；
- 旧云色表；
- 子房总诀；
- 天气断语。

C52–C59 已明确拆层，所以这两个 wrapper 只能作为历史展示/兼容参考，不能再作为 canonical 真源。

对应 replacement：

- C57 合会层；
- C58 观察层；
- C59 数值天气层；
- 必要时由 C52/C53/C55/C56 提供位置与注册事实。

## 最新验证

C60 扩展后的全量 CI：

```
1197 passed in 1.47s
```


## C70 补充隔离：config.wenchang_nine_stars

旧实现虽采用：

- 大周2700；
- 小周270；
- 30年一星；

这一周期核心可与统宗 NGJ 见证参校，但整体并不等价。

已确认问题：

- 星名表混入“文曲 / 昭摇 / 立华”等非 C70-NGJ 读法；
- 丁旧落巽9，直接表应落离2；
- 壬旧落中5，直接表应落乾1；
- 旧九星分布循环计算 `gong` 后未使用，实际仍输出固定星宫表；
- 没有保存 CADAL 10/30 内部冲突；
- 没有保存紫庭附篇正文未取得的来源边界。

因此：

- `canonical_equivalent=False`
- `promotion_allowed=False`
- replacement → `C70-TONGZONG-WENCHANG-NINE-STARS`

C70 只替代统宗 NGJ source profile，不替代紫庭 primary。


## C97 / C98 周期兼容层补充隔离

### 五福 C97

新增：

- `kintaiyi.cycles.wufu.project`
- `config.wufu_default`

原因：

旧 `project +250` 曾被阶段性实现标作 canonical，但 C67 已按来源拆为：

- 统宗 +115；
- 金镜无该盈差。

旧 +250 只能保留数值兼容，不能升格。

### 大游 C98

新增：

- `kintaiyi.cycles.bigyo.jinjing_tongzong`
- `config.bigyo_default`

原因：

旧默认 profile 名本身即：

`jinjing_tongzong`

把金镜宫序与统宗 +34 盈差合并成一个实现层。2026-10-04 恢复记录已经明确旧 `config.bigyo()` 只作实现参照，不作为规则真源。

因此：

- 数值兼容保留；
- `canonical=None`
- `canonical_equivalent=False`
- `promotion_allowed=False`

replacement 暂不指向猜测的新 runtime，等待 source-specific 行宫层独立重接。

### 大游天目 C98

新增：

- `kintaiyi.cycles.bigyo_tianmu.tongzong`
- `config.bigyo_tianmu_default`

2026-10-04 `rules/dayou/tianmu.json` 已明确：

- 金镜恢复工作采用 72→18 与18步路径；
- 旧 `%180 / +214` 实现只作 `deprecated_reference`。

因此默认旧 +214 wrapper 不能继续充当 canonical。

C98 保留兼容数值，但统一撤销 canonical 身份。
