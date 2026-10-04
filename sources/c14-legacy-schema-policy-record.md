# C14 legacy schema policy 单一真源记录

## 目标

C12 adapter 与 C13 audit 原先各自维护 legacy 风险字段/映射，长期可能漂移。

新增：

- `src/kintaiyi/legacy_schema.py`
- `classify_legacy_field(...)`
- `replacement_path_for_legacy(...)`
- `legacy_field_manifest(...)`

并把 C12/C13 改为读取这一份 registry。

## 字段策略

每个旧顶层字段只能落入一种状态：

- `migrated_fact`
- `quarantined`
- `unported`
- `embedded_v2`

### migrated_fact

有明确 v2 目标路径，例如：

- `太乙落宮 -> board.taiyi.palace`
- `主算 -> board.calculations.home`
- `主將 -> board.generals.home_general`
- `八門分佈 -> board.doors.distribution`

### quarantined

只允许保留 compat，并声明新结构替代路径，例如：

- `軍事戰略 -> analysis.military`
- 旧七术断语 -> `analysis.seven_methods`
- 旧八占相关断语 -> `analysis.eight_divinations`
- `運籌博弈分析 -> modern.game_theory`

### unported

未知或尚未迁移的旧字段不猜测目标，保持 `target=None`。

## C12 重构

`pan_adapter.py` 不再自维护：

- META_MAP
- CALENDAR_MAP
- board/general/calc/cycle/door maps
- quarantined key set

全部从 C14 registry 导入。

## C13 重构

`migration_audit.py` 不再单独维护：

- old military set
- old seven methods set
- old eight-divinations set
- old game-theory set

replacement gap 直接调用：

`replacement_path_for_legacy(key)`

因此 adapter 与 audit 不会再因为名单不同步产生假状态。

## 原则

registry 只定义 schema 迁移策略，不读取字段值、不计算古法、不决定吉凶。
