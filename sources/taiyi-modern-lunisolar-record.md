# 现代中国农历/干支事实层

## 永久规则标识

- `MODERN-CHINESE-LUNISOLAR-FACTS`
- runtime: `kintaiyi.taiyi_modern_lunisolar`
- provider: `lunar_python 1.4.8`

## 目的

production 已确定：

- 太乙岁：真实冬至瞬间换年；
- 现代农历：仍需要真实农历年月日、闰月等事实；
- 两者不能互相替代。

因此本层只提供现代中国农历/干支事实，不直接生成太乙月计、日计积数。

## 日历时区

现代中国农历统一按：

`Asia/Shanghai`

即中国标准时间解释。

输入datetime可来自任意时区，只要带timezone；程序先转换到同一绝对瞬间对应的中国标准时间，再交给现代农历库。

这与太乙冬至换年并不冲突：

- 冬至边界比较的是绝对天文瞬间；
- 农历年月日按中国标准日历时区呈现。

## 明确分离三种“年”

结果同时允许出现：

1. `taiyi_year`：太乙岁，冬至换；
2. `lunar.year` / `ganzhi.lunar_year`：现代农历春节换；
3. `ganzhi.jieqi_year_exact`：节气/立春体系。

后两种都不得改写第一种。

### 典型例子

2027-01-01：

- 2026冬至已经过去，所以太乙已进入2027岁；
- 2027春节要到2月6日，所以现代农历仍是2026年。

这正是项目要求避免“元旦/春节/立春/春分和太乙换年混淆”的场景。

## 闰月

`lunar_python` 用负月号表示闰月。

项目输出同时保存：

- `month=abs(signed_month)`
- `signed_month`
- `is_leap_month`

例如2025-07-25为闰六月初一：

- month=6
- signed_month=-6
- is_leap_month=True

后续太乙月计如何让闰月进入连续计数，将在月计production映射层单独定义；本层不偷做决定。

## 日干支边界

库同时提供两套日干支精确口径：

- `getDayInGanZhiExact()`
- `getDayInGanZhiExact2()`

当前均保存为事实：

- `day_exact`
- `day_exact_zi`

在太乙日计边界正式确定前，不擅自选其中之一。

## production依赖

PyPI：

- package: `lunar_python`
- pinned range: `>=1.4.8,<2`

该库负责现代中国农历/干支事实；太乙业务边界仍由本项目规则层决定。
