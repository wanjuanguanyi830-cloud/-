# 现代 production 日计积数

## 永久规则标识

- `MODERN-TAIYI-DAY-COUNT`
- runtime: `kintaiyi.taiyi_modern_day_count`

## 原典数值锚点

《太乙金镜式经》卷一“推积日并朔法”保存一条直接实例：

> 梁天监三年甲申岁六月八日，积得七亿七百五十万一千六十一日。

项目取：

`707,501,061`

作为日计连续编号锚点。

不再使用旧代码：

`708011105`

等缺乏同等级来源的经验常数。

## 现代production重建

锚点日期本身是传统“甲申岁六月八日”。

production现代历法层使用 `lunar_python`：

`Lunar.fromYmd(504, 6, 8).getSolar()`

把该历史农历日转换为现代连续历日事实。

当前日期同样转为中国标准民用日。

两者日差：

`delta_days`

则：

`accumulated_day = 707,501,061 + delta_days`

这意味着古代朔策、月法、日法等近似历法常数不再承担现代production的日差计算。

## 日界

production日计统一：

> `Asia/Shanghai 00:00:00` 换日。

原因是本项目已经决定采用现代日历体系作为生产canonical。

现代干支库可能同时存在：

- 午夜换日；
- 子初23:00换干支日；

两种口径。

它们继续在 `taiyi_modern_lunisolar` 中并列保存，但不会反过来改变日计积日边界。

## 与月计、岁计

三个边界独立：

- 岁计：真实冬至瞬间；
- 月计：真实十二节交节瞬间；
- 日计：中国标准民用日00:00。

任何一个边界变化都不暗示另外两层同时变化。

## 下游

`modern_day_count(datetime)`

直接输出：

`accumulated_day -> 日计阳局 -> G2..G7`

因此production日计不再要求调用方手工提供积日。
