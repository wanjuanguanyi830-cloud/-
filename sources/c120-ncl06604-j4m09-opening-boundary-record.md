# C120 NCL-06604 明钞本 J4M-09 开头与页内边界校勘

日期：2026-10-05

## 证据

用户提供的 NCL-06604 卷四页图，在 J4M-08 收尾之后直接进入 J4M-09。

页内可连续确认：

- J4M-08 收尾：**此之要也**
- 下一标题：**推太乙在天外地内法**
- J4M-09 首句：**古法曰太乙在一八三四宫者为地内宫助主人**

本轮只补这个页内边界与首句，不重复建立 C86 已完成的宫组校勘。

## 与 C86 的关系

C86 已直接核得 NCL 明钞本 J4M-09：

- 地内助主人：[1,8,3,4]
- 天外助客：[9,2,7,6]

C120 的新证据是：

1. J4M-08 与 J4M-09 在同页上的真实衔接；
2. J4M-09 首句明确写“一八三四宫”；
3. 该“1宫”不是后续整理补入，而是明钞本正文开句直接存在。

因此 C120 **不重算** C86 的宫组，只把首句和页内边界补进证据链。

## 四库 canonical 仍不改变

四库 jinjing_siku_volume4 当前 J4M-09：

- 地内：[8,3,4]
- 天外：[9,2,7,6]

NCL-06604 明钞本：

- 地内：[1,8,3,4]
- 天外：[9,2,7,6]

C120 再次确认 NCL 首句确实含“1”，但：

**不得以 NCL 的 1宫补四库 canonical。**

## 仓库字段

rules/jinjing_v4_military.json：

- J4M-09 manuscript_readings.NCL-06604.opening_direct_visual
- cycle = C120
- previous_rule_closing = 此之要也
- body_title = 推太乙在天外地内法
- opening_text = 古法曰太乙在一八三四宫者为地内宫助主人
- source.ncl_volume4_collation_version = c120-ncl06604-j4m09-opening-boundary-v1

rules/jinjing_v4_witness_matrix.json：

- J4M-09 boundary_status = J4M-08_to_J4M-09_direct_visual_verified_C120
- palace_group_status 继续标为 direct_visual_verified_C86
- C120 只补 boundary/opening，不重建宫组。

## 结论

NCL 明钞本卷四现在不仅有 J4M-09 的宫组结果，也有页内首句证据：

**古法曰太乙在一八三四宫者为地内宫助主人。**

这进一步确认 [1,8,3,4] 是传本文字，而不是后世按对称性补出的组合。
