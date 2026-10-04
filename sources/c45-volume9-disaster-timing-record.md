# C45 岁中灾发月日之期严格来源模型

日期：2026-10-05

## 来源与卷次

当前在线《太乙统宗宝鉴》见证编在卷十；项目旧参考长期归入卷九。

固定：

- `online_witness_volume = 10`
- `project_legacy_volume_label = 9`
- `volume_status = witness_volume_variant`

对应术目：

《明岁中灾发月日之期术》

## 原文两阶段

本术不是单层“灾发月份”算法，而是连续两步：

### 第一阶段：岁 → 月

以太岁合神加岁支，视：

- 文昌所临；
- 天目所临；

定灾发之月，冲处亦然。

原文举例：

- 文昌临辰 → 三月；
- 冲处戌 → 九月亦然。

### 第二阶段：月 → 日期

再以当月合神加当月支，重新视：

- 文昌所临；
- 天目所临；

所临何位，即为日层之期，冲处亦然。

因此 C45 将月层、日层分开保存；不能把旧月层断语当成完整“月日之期”。

## C45-01 不在本层重算“合神加支”

runtime：

`src/kintaiyi/volume9_disaster_timing.py`

C45 只消费上游已经求得的：

- 岁层文昌落点；
- 岁层天目落点；
- 月层文昌落点；
- 月层天目落点。

固定：

`addition_formula_applied=False`

旧 `guiyun.suizhong_zaifa` 的十六位 offset 不视为 canonical 等价实现。

## C45-02 文昌与天目必须同时检查

原文明确并举“文昌、天目”。

因此月层要求：

- `wenchang_landing_after_year_addition`
- `tianmu_landing_after_year_addition`

日层要求：

- `wenchang_landing_after_month_addition`
- `tianmu_landing_after_month_addition`

任一阶段缺天目时：

`not_computable`

不得只凭文昌结果清除 legacy replacement gap。

## C45-03 月份换算

十二支对应月份：

- 寅 1
- 卯 2
- 辰 3
- 巳 4
- 午 5
- 未 6
- 申 7
- 酉 8
- 戌 9
- 亥 10
- 子 11
- 丑 12

冲处沿十六宫环取对位。

如果文昌或天目落在：

- 艮
- 巽
- 坤
- 乾

等四维位，当前直接条文没有给这些四维如何折成月份，因此：

- 保留十六宫落点；
- 月份字段为 null；
- 本阶段保持 not_computable；
- 不擅自折月。

## C45-04 日层保存“位”，不伪造成日期

第二阶段原文说“所临何位，即为期”。

因此 C45 首先保存：

- `disaster_day_point`
- `opposite_day_point`
- 天目对应 point / opposite point。

只有落点本身是十二支时，才同时填：

- `*_day_branch`

若落艮/巽/坤/乾：

- point 仍保存；
- branch = null。

固定：

`specific_calendar_day=None`

`specific_calendar_day_status=source_gives_sixteen_point_period_not_calendar_day_number`

没有另一步历法证据时，不生成某月某日的现代日期数字。

## C45-05 文昌宫阴阳与水旱

原文另说：

- 文昌临阳宫 → 岁旱；
- 文昌临阴宫 → 岁水。

因此：

`palace_polarity`

必须由上游显式提供。

禁止旧实现自造 `_YANG_GONG` 集合后从十六点名猜宫性。

## C45-06 年度不协/不稔证据

原文另列：

- 文昌加在太乙宫；
- 格；
- 掩；
- 迫；
- 击；
- 挟；
- 提；

等情况，主君臣不协、岁不丰稔。

C45 将这些作为独立年度证据：

- `wenchang_same_as_taiyi`
- `pattern_evidence`

它们不改写灾发月候选。

即使“无格局”，也必须显式传：

`pattern_evidence=[]`

避免“未检查”与“检查后没有”混为一谈。

## C45-07 完整 replacement 条件

组合层：

`disaster_timing_from_evidence(month_stage, day_stage)`

只有：

- 月层 computable；
- 日层 computable；

同时成立时：

`status=complete_month_day_timing`

并允许：

`source_variants.volume9.disaster_timing.legacy_replacement`

非空。

只有月层时：

`partial_month_only`

不能清除旧 `歲中災發` migration gap。

## C45-08 legacy 审计

旧：

`guiyun.suizhong_zaifa`

问题：

1. 以 year_zhi / hegod_zhi / skyeyes_chen 做简单 offset，未证明等价于“合神加支”原盘式；
2. 只实现月层，没有第二阶段月→日；
3. 只看单一 skyeyes / 文昌，不完整表达文昌与天目双目标；
4. 自建阳宫集合推水旱；
5. 未显式区分“未检查格局”与“检查后无格局”。

因此：

`canonical_equivalent=False`

旧 flat：

`歲中災發`

继续 quarantine，replacement 只认完整 C45 两阶段结果。
