# 现代 production 时计：二至半岁相对积时

## 永久规则标识

- `MODERN-TAIYI-TIME-UNIT`
- `MODERN-TAIYI-SOLSTICE-RELATIVE-TIME`
- `MODERN-TAIYI-TIME-COUNT`
- runtime: `kintaiyi.taiyi_modern_time_count`

## 原典核心

《太乙金镜式经》卷一“推冬夏二至以后太乙所在法”明确以：

> 冬夏二至以来，并今日所求日减一，以十二乘之……加所求时数

求“冬夏二至后时实”。

《太乙统宗宝鉴》卷一亦写：

> 置冬至、夏至所求日减一，以十二乘之……加所求时为实。

因此production时计不能使用“梁代日计锚点以来的绝对积日 × 12”。

## production公式

先由现代天文求当前半岁的精确起点：

- 冬至瞬间 -> 冬至后 / 阳局；
- 夏至瞬间 -> 夏至后 / 阴局。

再按 Asia/Shanghai 民用日期：

`day_index = 所求民用日 - 二至所在民用日 + 1`

日内时序按已校定的“夜半/子正”口径：

- 00:00–01:59 = 第1时；
- …
- 22:00–23:59 = 第12时。

于是：

`entry_count = (day_index - 1) * 12 + time_unit`

二至精确瞬间进入新的半岁profile，因此entry_count回到该二至所在日的1..12范围，不保持跨二至连续。

## 与日计分离

日计可以使用历史原典积日锚点形成连续日编号。

时计则是另一条原法：

> 从当前冬至/夏至半岁重新起算。

所以时计不得再消费 `modern_day_count().accumulated_day` 作为绝对底数。

## entry_count 与 C119 duty_time_real

当前production adapter把同一“二至半岁相对12时编号”同时送给：

- 四计G2..G7的 `entry_count`；
- C119八门的 `duty_time_real`。

两个API字段仍独立保存，因为《金镜》C119和《统宗》四计属于不同source profile；未来若进一步校出差异，可以分开而不破坏接口。

## 与另一种“二至间甲子日起元”法

《太白兵备统宗》等平行书另保存：

> 二至间逢甲子日为起元之首。

这是另一source profile，不与本production canonical静默合并。

如后续实现，应另立variant，并用其局例回归。
