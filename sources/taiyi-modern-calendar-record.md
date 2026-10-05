# 现代 production 太乙冬至换年与二至时计边界

## 永久规则标识

- `MODERN-TAIYI-YEAR-WINTER-SOLSTICE`
- `MODERN-TAIYI-TIME-SOLSTICE-HALF`
- `MODERN-TAIYI-ASTRONOMICAL-CALENDAR`
- runtime: `kintaiyi.taiyi_modern_calendar`

## 太乙岁唯一换年边界

项目 production 统一规定：

> **真实天文冬至交节瞬间，是太乙岁唯一换年边界。**

对于公历年 `Y`：

- 冬至前一瞬仍属太乙 `Y` 岁；
- 冬至精确瞬间起进入太乙 `Y+1` 岁。

所以：

`moment < winter_solstice(Y) -> Taiyi year Y`

`moment >= winter_solstice(Y) -> Taiyi year Y+1`

## 明确排除的换年点

以下都不得改变太乙岁：

- 元旦；
- 春节；
- 立春；
- 春分。

这些时间点可以作为其他历法或术数系统的边界，但不得污染太乙岁计。

## 时计二至半岁

时计继续采用已校定规则：

- 冬至瞬间起 -> 冬至后 -> 阳局；
- 夏至瞬间起 -> 夏至后 -> 阴局。

同样使用真实天文瞬间，不用固定公历日期近似。

## 现代天文引擎

当前 production 使用 PyPI `astronomy-engine 2.1.19`：

- Python import: `import astronomy`
- `astronomy.Seasons(year)`
- `SeasonInfo.jun_solstice`
- `SeasonInfo.dec_solstice`
- `Time.Utc()`

Astronomy Engine 官方说明：
- `Seasons(year)` 计算当年两分两至；
- 1800–2100年范围的两分两至已与USNO数据验证到2分钟内。

天文引擎只提供季节瞬间。

以下业务语义仍属于本项目自身规则：

- 冬至是太乙唯一换年边界；
- Y年冬至切入太乙Y+1岁；
- 冬至后时计阳局；
- 夏至后时计阴局。

## 时区

调用者必须提供 timezone-aware `datetime`。

程序先转换UTC，再与同一绝对天文瞬间比较，因此：

- 用户在中国；
- 美国；
- 日本；
- 其他时区；

看到的本地钟表日期可能不同，但换年发生在同一个绝对冬至瞬间。

不得先把冬至粗略换成本地“某一天0点”。

## 与古历profile

现代天文/现代历法是 production canonical。

《金镜》《统宗》的章岁、章月、气朔、闰余等算法继续保留为：

- source reconstruction；
- historical profile；
- 古法回归与比较。

不得再让古历常数成为现代production日期换算的隐藏依赖。


## production边界注册表

为了避免“太乙岁、农历年、立春干支年、公历年、月建”再次混淆，
`production_calendar_context()` 现在统一输出 `boundary_registry`：

| 字段 | 边界 | 是否改变太乙岁 |
|---|---|---|
| taiyi_year | 真实天文冬至瞬间 | **是，唯一** |
| gregorian_year | 元旦00:00 | 否 |
| lunar_year | 春节 | 否 |
| jieqi_ganzhi_year | 立春 | 否 |
| spring_equinox | 春分 | 否 |
| taiyi_solar_month | 十二节精确交节 | 只改月计月建 |
| taiyi_day | Asia/Shanghai 00:00 | 只改production日计 |
| taiyi_time_half | 冬至/夏至瞬间 | 只切时计阴阳局 |
| taiyi_time_unit | 子正/夜半起每2小时 | 只改时计时序 |

核心不变量：

> 只有 `boundary_registry.taiyi_year` 有权改变 `taiyi_year`。

### 月计公式年的命名

月计从大雪起进入子月，因此用于“(积年-1)×12+月序”的公式年，
可能在太乙冬至换岁之前就指向下一月计循环年。

该字段现在显式另名：

`month_formula_year`

它只服务积月公式，**绝不是太乙岁标签**。

太乙岁始终只读：

`year_boundary.taiyi_historical_year`

以及pan v2：

`calendar.taiyi_year`。
