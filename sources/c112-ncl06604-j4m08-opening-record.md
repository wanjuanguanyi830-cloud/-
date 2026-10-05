# C112 NCL-06604 明钞本 J4M-08《推随地制变》开头“三急”校勘

日期：2026-10-05

## 证据范围

用户提供的 NCL-06604 卷四页图直接露出 J4M-08 开头。

本轮只登记本图能够完整确认的连续文字，不把被裁切的后文扩成“全文已核”。

## 标题

明钞本正文标题：

**推随地制变**

与此前 C86 已登记标题一致。

## 开头总纲

页图可直接读出：

**晁错曰：用兵临战合用之急者有三：一曰士卒服习，二曰随其地形，三曰善用兵器。**

因此“三急”明确为：

1. 士卒服习
2. 随其地形
3. 善用兵器

这一结构与四库 J4M-08 当前理解一致。

## 后续可见范围

“三曰善用兵器”后，页图继续露出：

**五丈之沟居堑之水山林**

但该页图在此处被裁切，不能仅凭这张图完成“五丈之沟”以下连续段落的逐字转录。

因此机器状态明确区分：

- opening triplet：direct visual verified
- later selected reading：“矛鋋 / 弓弩三不当一”此前 C86 已由后页直接核实
- 中间连续正文：仍待完整页图

## 为什么不直接拿《汉书》或《福应经》补中段

J4M-08 已知《金镜》与《汉书》《福应经》在比例、段落结构等处存在实质差异。

所以即使晁错引文主题相同，也不能用其他古籍补齐 NCL 明钞本被裁掉的连续文字。

## 仓库状态

rules/jinjing_v4_military.json：

- J4M-08 manuscript_readings.NCL-06604.opening_direct_visual
- source_attribution = 晁错
- three_urgencies = [士卒服习, 随其地形, 善用兵器]
- continuation_visible_only = 五丈之沟居堑之水山林
- scope_policy 明确“不据本图声明已核后续全文”
- source.ncl_volume4_collation_version = c112-ncl06604-j4m08-opening-v1

rules/jinjing_v4_witness_matrix.json：

- schema_version = 1.4
- C112 update
- J4M-08 verification_scope 标为非连续两端已核
- pending 保留“五丈之沟以下至矛鋋段之间的连续逐字转录”

## 结论

NCL J4M-08 当前已经有：

- 正文标题
- 开头三急总纲
- 后段“矛鋋 / 弓弩三不当一”

三类直接页图证据。

但仍不宣称整条 J4M-08 连续正文已经逐字核完。


## C112 v2 用户校读补充

用户进一步确认该页在“三曰善用兵器”之后可连续读到：

**五丈之沟居堑之水山林**

因此 C112 的直接可见范围由“仅五丈之沟起句”向后延长至上述完整字串。

仍不补其后的文字；pending 从“该字串之后”继续。


## C115 后续升级

C112 的“开头已核、中段连续正文 pending”状态已被 C115 supersede。

用户后续补充的连续页图已经从“**五丈之沟居堑之水山林**”一直核到 J4M-08 收尾，并直接见下一标题“推太乙在天外地内法”。

因此：
- C112 继续保留为历史阶段；
- 当前 J4M-08 NCL 状态为 full_contiguous_body_direct_visual_verified；
- 当前详情以 sources/c115-ncl06604-j4m08-full-body-record.md 为准。
