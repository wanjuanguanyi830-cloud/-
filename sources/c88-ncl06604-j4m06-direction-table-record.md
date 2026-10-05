# C88 NCL-06604 明钞本 J4M-06 陈兵向背数表异文

## 目标

继续 NCL-06604 卷四逐条校勘。本轮只处理 J4M-06“推陈兵向背”的明钞本数表骨架，避免把四库本、明钞本与《景祐太乙福应经》三种传本互相补数。

底本定位：

- NCL-06604 明钞本
- J4M-06：digital scan p.59-p.60

## NCL 明钞本直接图像读法

明钞本依次列出算数：

- 1
- 2
- 3
- 4
- 6
- 7
- 8
- 9

未见 5。

对应出军方向骨架为：

| 算 | 出军方向 |
|---|---|
| 1 | 西北 |
| 2 | 正南 |
| 3 | 东北 |
| 4 | 正东 |
| 6 | 正西 |
| 7 | 西南 |
| 8 | 正北 |
| 9 | 东南 |

本轮只把“算数 + 出军方向”登记为 direct visual verified。背地、阵形、旗色的完整逐行转录仍继续校勘，不在尚未逐字确认前扩写。

## 与四库本的差异

四库 jinjing_siku_volume4 当前本条明确列：

**1 / 2 / 4 / 5 / 6 / 9**

NCL 明钞本则列：

**1 / 2 / 3 / 4 / 6 / 7 / 8 / 9**

因此：

- NCL 比四库多 3、7、8；
- NCL 少四库的 5；
- 两表不能互补成 1～9 的“完整表”。

## 与《景祐太乙福应经》的关系

仓库已记录《福应经》“释陈兵向背”：

- 1 -> 西北
- 2 -> 正南
- 3 -> 东北
- 4 -> 正东
- 6 -> 正西
- 7 -> 西南
- 8 -> 正北
- 9 -> 东南

这一“数值 + 方向”骨架与 NCL 明钞本一致。

所以现在至少可以确认：

- 四库本系统：1/2/4/5/6/9，并有完整战利/背地/阵/旗结构；
- NCL 明钞本系统：1/2/3/4/6/7/8/9；
- 《福应经》系统：1/2/3/4/6/7/8/9。

这说明 3/7/8 不是后世《统宗》才出现的补数，而有明钞《金镜》与《福应经》双重古本见证。

但仍不得因此回填四库本。

## Source-specific 政策

J4M-06 的 canonical 继续是四库 profile：

- 接受 1/2/4/5/6/9；
- 不把任意算数取个位；
- 不从 NCL / 《福应经》补 3/7/8。

NCL manuscript reading：

- explicit_calculation_values = [1,2,3,4,6,7,8,9]
- omitted_vs_siku = [5]
- extra_vs_siku = [3,7,8]
- canonical_override = false

也不得反过来拿四库的 5 去补 NCL。

## 仓库契约

rules/jinjing_v4_military.json：

- J4M-06 manuscript_readings.NCL-06604.direction_table
- explicit_calculation_values
- omitted_vs_siku / extra_vs_siku
- source_boundary_evidence.ncl_06604_ming_manuscript
- source.ncl_volume4_collation_version = c88-ncl06604-j4m06-direction-table-v1

tests/test_jinjing_v4_military_record.py：

- 锁定 NCL 1/2/3/4/6/7/8/9；
- 锁定 NCL 无5；
- 锁定四库仍为1/2/4/5/6/9；
- 锁定“不得互补缺数”。

## 未决

继续逐字核 NCL p.59-p.60 的：

- 战利方向；
- 背地地形；
- 阵形；
- 旗色。

在这些细项逐行确认完成前，不根据四库结构自动复制到 NCL。
