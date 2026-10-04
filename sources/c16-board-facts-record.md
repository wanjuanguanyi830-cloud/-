# C16 P0 第一批：board 结构事实迁移记录

## 目标

落实 C15 P0 中最低风险的一批：

- 十六宫分布进入 `board.sixteen_palaces`
- 天乙 / 地乙 / 四神 / 直符 / 合神 / 计神进入 `board.generals`

本批只迁移旧 snapshot 已存在的盘面事实，不重新计算这些值。

## 1. 十六宫分布

参考旧 `Taiyi.pan()`：

`十六宮分佈 = self.sixteen_gong(...)`

参考代码注释明确标为《太乙统宗宝鉴》卷二。

C16 新位置：

`board.sixteen_palaces`

规则：

- adapter 只搬运旧 dict；
- 不重新调用 `sixteen_gong(...)`；
- 保留 sector -> 星将列表结构；
- C11 builder 默认创建空 `sixteen_palaces={}`；
- C11 validator 将其作为 board 必需子区段。

## 2. 六个基础神将

旧盘字段：

- 天乙
- 地乙
- 四神
- 直符
- 合神
- 计神

参考实现返回十六神/支位文字，而不是主客大将那类 1-9 九宫数字。

因此 C16 统一迁移为：

- `board.generals.tianyi.sector`
- `board.generals.diyi.sector`
- `board.generals.four_spirits.sector`
- `board.generals.zhifu.sector`
- `board.generals.hegod.sector`
- `board.generals.jigod.sector`

禁止把这些值存成 `palace`。

## 3. C14 状态变化

上述 7 个字段从：

`status=unported`

变为：

`status=migrated_fact`

C15 目录仍保留它们作为“当时的迁移候选历史记录”，但 C14 当前状态优先。

## 4. C13 审计变化

C13 不再把这 7 个字段统计为 unported，也不会继续把“十六宫分布”放进 next migration candidates。

## 5. 边界

本批没有：

- 迁移帝符/太尊/飞鸟/三风/五风/八风；
- 实现十六宫算法；
- 计算基础神将；
- 改变 J4M / C8 军事结论；
- 把旧断语提升为 canonical。
