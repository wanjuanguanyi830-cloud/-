# C22 卷十五 / 卷十七军事 rule-unit 目录

## 目标

C21 已把卷十五/卷十七从 flat schema 拆成两个独立 derived profile。

C22 再把两个综合 payload 拆成独立 source_rule_id，避免后续继续依赖“整卷 dict”。

新增：

- `src/kintaiyi/military_rule_units.py`
- `rule_unit(...)`
- `units_for_profile(...)`
- `payload_key_to_rule_id(...)`
- `low_dependency_candidates(...)`

## 卷十五

14 条 source rules：

- V15-01 奇兵伏兵
- V15-02 五阵置旗
- V15-03 出兵称神
- V15-04 陈兵出乡
- V15-05 选将之术
- V15-06 教兵之术
- V15-07 随地制变
- V15-08 分合用兵
- V15-09 五音风
- V15-10 五音观风察将
- V15-11 安营置阵
- V15-12 风从八卦
- V15-13 云气逆顺
- V15-14 军势胜负

每条记录：

- source_rule_id
- source_title
- reference function
- inputs
- dependency_class
- external_inputs
- overlaps
- notes

## 卷十七

11 条 source rules：

- V17-01 出兵用时
- V17-02 敌国动静
- V17-03 间谍虚实
- V17-04 敌使虚实
- V17-05 敌兵来方
- V17-06 见闻虚实
- V17-07 讨捕叛亡
- V17-08 执囚对吏
- V17-09 求索所得
- V17-10 时计诸事
- V17-11 占望行人

## V17-D1 孤虚对照

旧综合 payload 中的“孤虚对照”并非独立卷十七原法。

参考代码明确由：

- 卷五“内外占攻击”
- 卷十七“求索所得”

组合产生。

因此单列：

`V17-D1`

并固定：

- source_status = `derived_cross_volume_helper`
- volume_profile = `cross_volume_helper`

不得分配卷十七 canonical source rule 身份。

## 下一批低依赖

C22 自动列出：

- V15-02 五阵置旗
- V15-03 出兵称神
- V15-04 陈兵出乡
- V15-05 选将之术
- V15-06 教兵之术
- V15-09 五音风
- V15-12 风从八卦
- V15-13 云气逆顺

其中外部风云观测类仍须保留 external_inputs，不应自动推断。

## C21 接线

C21 profile 现在附带：

`rule_units: payload_key -> source_rule_id`

所以旧综合 payload 仍可兼容，但新实现可以逐条替换。
