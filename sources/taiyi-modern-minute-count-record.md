# 现代 production 分计扩展 V1

## 身份

- rule: `MODERN-TAIYI-MINUTE-COUNT`
- runtime: `kintaiyi.taiyi_modern_minute_count.modern_minute_count`
- source profile: `production_modern_solstice_relative_minute_extension_v1`
- status: stable modern extension
- public API target: `kintaiyi.api.build_pan(moment, count_type="分计")`

## 来源边界

《太乙统宗宝鉴》卷一明确的是岁/月/日/时“四计”，当前仓库继续保持这一古法边界，
不把分计伪写成第五种古籍四计。

上游开源 Kintaiyi 的公开文档把 `ji_style=4 / 分計` 明确标为 **Modern extension**，
其仓库长期提供分钟级盘式。这证明“分计”作为现代软件扩展已有明确上游使用史，但不证明
古籍存在统一的分钟公式。

本仓库不直接移植旧实现中的经验常数或难以解释的 legacy minute arithmetic。V1 改用一个
透明、可测试、版本化的扩展定义，并明确记录它是项目现代规则。

上游参考：
- repository: `kentang2017/kintaiyi`
- observed commit: `11f78555d5e77c81ac8af69d243a981c22934733`
- public wiki: `wiki/Calculation-Modes.md`，将分計标为 `Modern extension, precise timing`

## V1 定义

分计继承现有 production 时计已经冻结的真实二至边界：

- 冬至瞬间起阳半岁；
- 夏至瞬间起阴半岁。

对 timezone-aware 输入时刻：

```text
elapsed_whole_minutes =
floor((input_utc - current_half_start_utc) / 60 seconds)

entry_count = elapsed_whole_minutes + 1
```

于是：

- 二至精确瞬间 = 第1分；
- +59.999秒仍为第1分；
- +60秒进入第2分；
- 任意相隔60秒的两个时刻，entry_count恰差1；
- 同一绝对瞬间无论输入时区如何，得到同一分计。

随后只把 `entry_count + dun` 送入已经来源冻结的 G2..G7：
太乙、文昌、计神、始击、主客算、主客大小将。分计不复制这些公式。

## 与時計分离

分计不是把一个时辰内的120分钟都当作同一盤，也不是把C119的“30时一门”改成
“30分一门”。因此：

- 分计不自动生成 C119 直门；
- `board.doors.direct` 在分计盘中保持缺省/空；
- 若未来需要“分计八门”，必须另立来源或另立项目扩展版本。

## 为什么不用旧经验常数

旧 Kintaiyi minute runtime 曾存在基于 `708011105`、`*23`、`hour*10500` 与分干支
余数校正的 legacy arithmetic。当前仓库的现代日计已经明确淘汰 `708011105` 一类经验
常数并改用来源锚点，因此不应为赛事需求把该 legacy 公式重新静默引入 canonical
production。

V1 的取舍是：

> 宁可把“现代扩展”身份写清楚，也不伪造古籍来源或恢复不透明经验常数。

## 使用场景

该 profile 为需要分钟级区分度的上层应用提供稳定事实盘；它不规定上层如何选择某一分钟。
例如赛事系统可在赛前窗口内做可复现随机选局，但“随机/去重/锁定”属于赛事仓库业务规则，
不属于本传统太乙仓库。
