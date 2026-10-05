# 现代历法上游安全契约

## 规则标识

- `CORE-CALENDAR-UPSTREAM-CONTRACT`
- `CORE-RESOLVED-CALENDAR-COUNT`
- `CORE-CALENDAR-AUTOMATION-STATUS`
- runtime: `kintaiyi.taiyi_calendar_upstream`

## 为什么暂不直接接受Gregorian datetime

当前核心公式层已经闭合，但“现代日期时间 -> 古法积数”仍有source-specific历法问题。

### 岁计

《金镜》《统宗》明确给出积年历元，并把上元定在：

> 甲子年、甲子月、甲子日、甲子时，天正冬至。

《统宗》又用：

> 所求岁前天正十一月
> 所求岁前天正冬至

作为月日历法基准。

这些足以说明冬至是历法计算的重要锚点，但尚不足以在本项目无校勘地宣布：

- 现代民用日期在春节换岁计；
- 或立春换；
- 或冬至瞬间换。

因此岁计现代日期入口先要求上游明确给 `resolved_historical_year`。

### 月计

《金镜》保存章岁/章月/闰余体系；

《统宗》另有“积年减一、十二乘之”等历法表述。

两者必须拆成source profile，并需要进一步校常数/闰月处理。

所以现在月计只接受已经求好的 `accumulated_count`。

### 日计

依赖：

- 气朔积日；
- 经朔；
- 朓肭；
- 定朔等历法步骤。

不能拿Unix epoch或儒略日直接当太乙日计积日。

### 时计

原文明确以真实冬至、夏至气应为阴阳遁边界。

所以时计要求上游给：

- `entry_count`
- `solstice_half`
- 若需要C119八门，再给 `duty_time_real`

不得用“公历6月以后就是阴局、12月以后就是阳局”这类近似。

## 设计原则

统一入口 `run_resolved_calendar_count()` 只做：

> 已解析历法事实 -> 已校定太乙核心。

它故意拒绝跨层方便参数。

目标是防止未来UI为了“能跑”而把未经来源验证的现代日期换算静默写进canonical。
