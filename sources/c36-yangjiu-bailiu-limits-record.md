# C36 阳九 / 百六大小限来源记录

## 直接来源

识典《太乙统宗宝鉴》在线见证：

https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppwz3ep1yr

该见证题作卷十，并连续列：

- 明太乙阳九，百六厄会附
- 求阳九灾变之期大小限数
- 求百六灾变之期大小限数术
- 明阳九百六，太游行限观历术

项目旧资料曾把同组内容标作卷九。

C36 固定：

`volume_status="witness_volume_variant"`

卷号差异不复制算法。

## 阳九

直接数值：

- 大限：4560
- 小限：456
- 十个小限成一大限
- 阳盈差：130

结构公式：

`(accumulated_year + 130) mod 4560`

再按 456 分小限。

C36 不把“第一年”误当“数终”；只有小限第456年才标小限终，大限余数为0才标大限终。

## 百六

直接数值：

- 大限：4320
- 小限：288
- 十五个小限成一大限
- 阴盈差：2050

结构公式：

`(accumulated_year + 2050) mod 4320`

再按 288 分小限。

## 与旧 pan 的区别

旧参考 `config.yangjiu(year, month, day)` / `baliu(...)`：

- 把公历输入转农历年；
- 经过模数后映射为地支；
- pan 顶层只输出一个地支值。

这与古籍“灾变之期大小限数”不是同一数据结构。

因此旧：

- 陽九
- 百六

当前均为 legacy quarantine。

replacement：

- `cycles.limits.yangjiu`
- `cycles.limits.bailiu`

不得把旧地支值直接塞进 canonical limits。

## pan v2

C11 cycles 新增：

`cycles.limits`

C36：

`yangjiu_bailiu_limits(accumulated_year)`

可直接作为该区段。

## 尚未合并的相关规则

“明阳九百六太游行限观历术”还包含：

- 太游外卦十年一宫、八十年一竟；
- 太游内卦三十六年一宫、二百八十八年一竟；
- 即位年干支加大义等厄会法。

这些是后续独立规则，不因同篇相邻而塞进大小限函数。
