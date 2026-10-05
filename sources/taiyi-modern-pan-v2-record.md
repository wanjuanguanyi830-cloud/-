# 现代 production 四计 -> pan v2 适配器

## 永久规则标识

- `MODERN-PAN-V2-ADAPTER`
- runtime: `kintaiyi.taiyi_modern_pan`

## 目的

现代日期层已经能从一个timezone-aware datetime生成：

- 岁计；
- 月计；
- 日计；
- 时计；

各自的核心太乙事实。

C11 `pan_v2.py` 的设计原则仍是：

> builder只组装事实，不计算古法。

所以新增独立adapter，而不把现代日历算法塞进builder。

## 显式四计选择

调用：

`build_modern_pan_v2(moment, count_type=...)`

必须明确选择：

- 岁计；
- 月计；
- 日计；
- 时计。

不会把四张不同时间尺度的盘合成一张。

## board映射

当前自动搬运：

- `board.taiyi.palace`
- `board.eyes.skyeyes`
- `board.eyes.shiji`
- `board.eyes.jishen`
- `board.calculations.host/guest`
- `board.generals.host/guest`

时计另外搬：

- `board.doors.direct` = C119直门。

## calendar

保存：

- 输入datetime ISO字符串；
- 太乙冬至岁；
- 现代农历事实；
- 干支并列事实；
- 十二节太阳月；
- 当前选择的四计完整计数上下文；
- 冬至岁界；
- 时计二至半岁。

datetime在adapter层转ISO，保证C11 JSON-safe不变量。

## 太乙岁与农历年

2027-01-01回归必须保持：

- Taiyi year = 2027（2026冬至已经换岁）；
- lunar year = 2026（春节尚未到）。

该差异在v2 calendar中同时保留，不得归一化成一个“year”。

## scenario

仍只允许C11规定的三个scenario字段。

现代日期事实不得推断：

- 敌起兵年；
- 敌下营日太乙；
- 敌初来太乙。

这些军事事件输入继续显式提供。


## 太乙岁界进入pan v2契约

`calendar.year_boundary_policy` 现在显式保存：

- `unique_boundary = 真实天文冬至交节瞬间`
- `label_rule = 公历Y年冬至瞬间起进入太乙Y+1岁`
- 比较规则：`< 冬至 => Y；>= 冬至 => Y+1`
- 明确忽略：元旦、春节、立春、春分
- 当前太乙岁起点UTC
- 下一太乙岁起点UTC

这样UI、CLI、导出器只需消费v2事实，不得自行重新定义换年规则。

回归测试覆盖：

- 冬至前1微秒仍属旧太乙岁；
- 冬至精确瞬间立即切下一太乙岁；
- 之后的公历元旦不再次换岁。


## validator硬约束

`validate_pan_v2()` 对任何：

- `meta.calendar_mode = production_modern`，或
- `compat.modern_production = true`

的payload强制检查：

1. 必须存在 `calendar.taiyi_year`；
2. 必须存在 `calendar.year_boundary_policy`；
3. `unique_boundary` 必须严格等于“真实天文冬至交节瞬间”；
4. 必须明确排除元旦、春节、立春、春分；
5. 必须保存当前与下一太乙岁的冬至起点。

因此后续任何UI、CLI、导出器或新adapter若试图把现代太乙换年改成元旦/春节/立春/春分，会直接使pan v2验证失败。
