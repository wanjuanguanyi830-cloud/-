# C111 NCL-06604 明钞本 J4M-07《推制阵随地法》正文校勘

日期：2026-10-05

## 证据

用户提供的 NCL-06604 卷四页图直接包含 J4M-07 正文。本轮逐栏视觉核读，重点核：

- 五阵五行；
- 主客置阵五行相克；
- 五类地形对应阵形；
- 地顺/地反吉凶；
- 收尾“观方置变”。

不以四库或《景祐太乙福应经》补字。

## 五阵五行

明钞本写：

- 曲阵为水
- 锐阵为火
- 直阵为木
- 方阵为金
- 圆阵为土

并明确：

“皆取主客置阵，次以五行相克而取胜负。”

这与四库 J4M-07 的核心结构相同。

## 地形表

明钞本直接可读：

- 后高前下 -> 锐阵；利以进战，以溃其敌
- 前高后下 -> 直阵；不便进退，利以近斗；宜以守之，以疲敌力
- 地跨邪 -> 圆阵；不便於战者，宜为圆阵，利以坚守
- 地高而平 -> 方阵；利以四向，以通敌
- 左右势高 -> 曲阵；以吞敌

其中关键异文是：

**地跨邪**

四库 canonical 当前保存：

**地洿邪**

《景祐太乙福应经》现存转录另有“地形跨斜”。

因此 NCL“地跨邪”作为明钞本 direct reading 单独保存；它与《福应经》“跨斜”近似，但不据此合并来源。

## 顺逆

明钞本写：

- 地顺其向则吉
- 地反其向则凶

与四库结构一致。

## 收尾异文

明钞本收尾直接可见：

“太乙兵起於鄉，陣隨其地，觀方置變，皆算掩神，此用兵之法也。”

其中：

**观方置变**

值得保留为明钞本文字。

四库 profile 仍按其自身正文，不以“置变”覆盖 canonical。

## 与四库的关系

本轮没有推翻四库 J4M-07 的算法结构：

- 五阵五行一致；
- 五类地形到阵形的对应结构一致；
- 顺逆吉凶一致。

差异主要在：

- terrain wording：地跨邪 vs 地洿邪；
- closing wording：观方置变；
- 明钞本自身正文词形。

因此只登记 manuscript reading，不改 jinjing_siku_volume4 runtime。

## 仓库修改

rules/jinjing_v4_military.json：

- J4M-07 manuscript_readings.NCL-06604 增加
  - formation_elements
  - host_guest_rule
  - terrain_table
  - direction_rule
  - closing_text
  - textual_relation
- source.ncl_volume4_collation_version = c111-ncl06604-j4m07-body-v1

rules/jinjing_v4_witness_matrix.json：

- J4M-07 更新为 body_structure_direct_visual_verified_C111
- difference_class 增加 terrain_wording / closing_wording

测试锁定 NCL“地跨邪”和“观方置变”，同时明确不覆盖四库 canonical。
