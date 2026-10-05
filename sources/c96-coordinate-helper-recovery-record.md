# C96 10月4日 taiyi_common.py 纯坐标 helper 回收

日期：2026-10-05

## 1. 时间边界

只采用 2026-10-04 / 2026-10-05 已做工作。

来源文件：

`codex/c1-c7-canonical/src/kintaiyi/taiyi_common.py`

该文件相关提交均在 2026-10-04：

- C1 坐标公共层；
- C2 八占；
- C3 七术；
- C7 pan 聚合。

C96 不恢复整个旧 common 模块，而是把仍缺失的纯 helper 并回现行：

`src/kintaiyi/taiyi_rules.py`

这样公共真源仍只有一处。

## 2. 已有现行覆盖

现行 `taiyi_rules.py` 已有：

- SIXTEEN；
- BRANCHES / STEMS；
- GODS / GOD_POSITION；
- POSITION_WX；
- PALACE_POINT；
- PALACE_WX；
- 阴阳宫；
- 生克；
- FIRE_STAGES；
- 大神顺四格；
- qi_state；
- sexagenary_year。

因此这些不复制第二份。

## 3. C96 恢复项

### 十六辰 -> 九宫

恢复：

`SECTOR_TO_NINE_PALACE`

这是有损投影：

- 子 / 亥 -> 8；
- 丑 / 艮 -> 3；
- 寅 / 卯 -> 4；
- 辰 / 巽 -> 9；
- 巳 / 午 -> 2；
- 未 / 坤 -> 7；
- 申 / 酉 -> 6；
- 戌 / 乾 -> 1。

中五没有十六辰输入。

### 九宫基本 helper

恢复：

- `PALACE_TRIGRAM`
- `nine_palace_to_trigram()`
- `nine_palace_representative_sector()`

中五：

`nine_palace_representative_sector(5)`

继续拒绝，因为中五没有十六宫代表点。

### 十六环通用旋转 / 对冲

恢复：

- `rotate_sixteen()`
- `sector_opposition()`

与现有：

`dashen_from_lushen()`

不同，前者只是通用坐标 helper，不带大神术义。

### 九宫对冲

恢复：

`nine_palace_opposition()`

外八宫：

- 1 <-> 9
- 3 <-> 7
- 2 <-> 8
- 4 <-> 6

中五继续：

`pending`

不造中宫对冲。

### sector_detail

恢复十六辰细节包装：

- sector；
- god；
- sector element；
- nine palace；
- trigram；
- palace element；
- projection_lossy=true。

用于防止“辰土”与“九宫9木”之类坐标层混淆。

### qi_relation

现行已有：

`qi_state()`

C96 只恢复旧关系名称包装：

- 比和；
- 生我；
- 克我；
- 我克；
- 我生。

底层五态仍调用现行 `qi_state`，不复制第二套五行公式。

### general_palace_qi

恢复为显式：

`九宫五行 vs 已给落点五行`

关系 helper。

它不计算落点来源，只解释已经给定的坐标。

## 4. 不恢复

旧 `taiyi_common.py` 中任何可能形成重复真源的整套常量不另建模块。

C96 原则：

> helper 可以恢复；canonical 常量与公式不得复制成第二份。
