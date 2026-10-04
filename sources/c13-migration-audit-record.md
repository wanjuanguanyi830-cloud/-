# C13 legacy flat schema 迁移审计记录

## 目标

为真正接入旧 `Taiyi.pan()` 前提供可量化迁移状态，不通过删除旧字段制造“迁移完成”的假象。

新增：

- `src/kintaiyi/migration_audit.py`
- `audit_legacy_snapshot(...)`
- `audit_snapshot_collection(...)`

## 单盘审计

输出：

- legacy key 总数
- 已迁移事实 key 数/比例
- quarantined key 数/比例
- unported key 数/比例
- v2 是否存在
- v2 是否通过 C11 validator
- structured replacement gaps
- 是否可供 v2 core consumer 使用

## structured replacement gaps

当旧 snapshot 存在风险字段时，必须确认 v2 中已有对应新结构：

- 旧军事战略 → `analysis.military`
- 旧七术顶层断语 → `analysis.seven_methods`
- 旧八占相关顶层断语 → `analysis.eight_divinations`
- 旧运筹博弈分析 → `modern.game_theory`

若旧字段存在但新结构为空，则状态为：

`v2_partial_replacements`

不得因为 `result["v2"]` 已存在就宣称迁移完成。

## 状态

- `legacy_only`
- `v2_invalid`
- `v2_partial_replacements`
- `v2_core_ready_with_unported_legacy`
- `v2_core_ready`

其中 `v2_core_ready_with_unported_legacy` 表示核心新结构已具备，但仍有卷次/字段尚未迁移；旧 compat 仍可保留。

## 批量审计

`audit_snapshot_collection(...)` 汇总：

- 各状态数量
- ready 数量
- 平均迁移/隔离/未迁移比例
- 各字段出现频率
- replacement gap 频率

用于后续真实盘样本回归和迁移优先级排序。

## 原则

审计结果标：

`derived_migration_metadata=True`

它只描述 schema 状态，不生成古法断语，也不参与 C8/C9。
