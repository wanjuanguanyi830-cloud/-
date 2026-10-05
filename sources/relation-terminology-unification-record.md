# 太乙显式关系层术语统一记录

## 目标

把已经完成来源重核的“同宫 / 同域 / 条件关系”从位置周期中独立出来，建立统一术语入口：

- terminology/relations.json

## 总原则

位置事实 != 自动关系断语。

所有关系层都固定：

- auto_position_lookup_used = false
- auto_same_palace_inference_used = false（适用处）
- 调用方显式提供关系证据
- 未列 pair 不类推

## C65 三神同宫

对象：

- 天乙
- 地乙
- 直符
- 四神
- 大游
- 小游

只解释卷七天乙 / 地乙 / 直符条下直接列出的12个 pair。

“值符”不是默认 canonical 名，兼容时才映射为“直符”。

## C74 三基五福

六个 pair：

- 君基×臣基
- 君基×民基
- 臣基×民基
- 君基×五福
- 臣基×五福
- 民基×五福

含五福的 pair 若涉及“同宫在初交之始”，必须显式 initial_conjunction=True 才应用附加断语。

五福与君基“相冲”不是同宫，不在 C74 自动应用。

## C90 三基×三神

九个 pair：

三基（君/臣/民） × 天乙/地乙/直符。

君基三条保留原文行为条件 -> 吉凶双分支；没有 conduct branch 时不能压成单一结论。

臣基、民基六条按直接灾应保存。

## C91 三基×四神/大小游

九个 pair：

三基（君/臣/民） × 四神/大游/小游。

君基：

- 四神：条件治理；
- 大游：条件应对；
- 小游：争象 + 原文规定应对。

臣基/民基按直接灾应保存。

## C94 五福×四太乙

四太乙：

- 天乙金
- 地乙土
- 直符火
- 四神水

这是2026-10-04恢复解释层，来源序列支持金/土/火/水灾应映射，但坐标解释不是原文无歧义公式。

因此必须显式：

- interpretation_profile = oct4_recovered_four_taiyi_elemental
- same_wufu_domain = True / False / None

不得从 C64/C92/C67 或 terminology/wufu_domains.json 自动制造关系。

## C113 遗留大小游关系

恢复并重新按统宗卷七核定：

- 五福×大游
- 五福×小游
- 四神×小游
- 大游×小游

边界：

- 五福×大游保留五福条 / 大游条双层；
- 五福×小游必须显式 virtue；
- 四神×小游、大游×小游按直接灾应；
- 不自动计算具体对冲分野；
- C65/C90/C91/C94 已覆盖的 pair 不重复实现。

## 数据模型建议

任何关系输出至少区分：

- position evidence
- relation evidence
- source section
- condition branch
- applied effects
- pending / unchecked

这样可避免未来 UI 或聚合器把“位置相同”偷换成“古籍已判同宫灾应”。
