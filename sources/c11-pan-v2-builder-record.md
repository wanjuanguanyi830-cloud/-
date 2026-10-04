# C11 pan v2 producer / builder 记录

## 目标

补齐目标仓库此前只有 v2 规格、没有实际 producer 的缺口。

新增 `src/kintaiyi/pan_v2.py`。该模块只组装已经算出的事实，不导入 `Taiyi`，不复制八占、七术、周期、军事公式。

## 根结构

builder 固定输出：

- `schema_version="2.0"`
- `meta`
- `calendar`
- `board`
- `cycles`
- `analysis`
- `modern`
- `source_variants`
- `compat`

并补齐所需子层：

### board

- taiyi
- eyes
- calculations
- generals
- doors

### cycles

- three_bases
- five_blessings
- big_wander
- small_wander
- four_taiyi

### analysis

- patterns
- eight_divinations
- seven_methods
- military

## 中五规则

中五没有 Sector16。

只要以下对象明确 `palace=5`，builder 就强制 `sector=None`：

- `board.taiyi`
- `board.generals.*`
- `board.calculations.*`

这只是表示层规范化，不重新计算宫位。

## 双层五行

builder 不合并：

- 天目 `sector_element` 与 `nine_palace_element`
- 将帅 `intrinsic_element` 与 `palace_element`

若 general 已给 intrinsic_element 却缺 palace_element，validator 仅 warning，不自行猜值。

## scenario

只接受：

- `enemy_start_year_branch`
- `enemy_camp_day_taiyi_palace`
- `enemy_first_arrival_taiyi_palace`

任何其他键直接拒绝，避免再次把客大将等字段偷换成敌军初来太乙。

## JSON-safe

tuple/set 会规范成 JSON-safe list；未知自定义对象直接 TypeError。

不得用 `str(object)` 伪造 JSON-safe。

## validator

`validate_pan_v2(...)` 验证结构和表示层不变量，不验证古法答案本身。

## 与 C10 接合

builder 输出可直接被 `v2_consumer.py` 严格消费；legacy flat 字段仍不会参与 v2 读取。
