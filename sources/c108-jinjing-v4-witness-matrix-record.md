# C108 《太乙金镜式经》卷四三见证机器对勘矩阵

日期：2026-10-05

## 目的

把当前已经直接核实的三条证据链放入同一机器可读矩阵：

1. 四库本：CADAL06056494
2. 明钞本：NCL-06604
3. 《景祐太乙福应经》卷四 parallel source

文件：

`rules/jinjing_v4_witness_matrix.json`

该文件不是新的推法 runtime，而是 source-collation contract。

## 核心政策

canonical profile 仍是：

`jinjing_siku_volume4`

NCL 和《福应经》能够证明古代异文真实存在，但：

- 不得静默补四库；
- 不得把所有差异都降格成 alias；
- 未直接图像核实的 NCL 细项继续 pending；
- 差异按 heading / numeric / table_structure / palace_group / event_verdict / verdict / glyph 等类型保存。

## 当前最重要的实质差异

### J4M-05

四库：
- 12 / 22 / 32

NCL：
- 12 / 22
- 未见 32

类型：numeric variant。

### J4M-06

四库：
- 1 / 2 / 4 / 5 / 6 / 9

NCL：
- 1 / 2 / 3 / 4 / 6 / 7 / 8 / 9
- 方向骨架已核

《福应经》：
- 1 / 2 / 3 / 4 / 6 / 7 / 8 / 9
- 方向骨架与 NCL 同构

但 NCL 的以下细项仍保持 pending：

- 战利方向逐项
- 背地逐项
- 阵形逐项
- 旗色逐项

因此明确禁止：

**因为 NCL 数表与《福应经》一致，就把《福应经》细项复制进 NCL。**

### J4M-09

四库地内：
- 8 / 3 / 4

NCL 与《福应经》：
- 1 / 8 / 3 / 4

类型：palace_group variant。

1宫不得补进四库 canonical。

### J4M-11

四库当前读法：
- 主人形上来 -> 客败

NCL：
- 主人刑上来 -> 主人败
- 客刑上来 -> 客败

《福应经》：
- 主人刑上来 -> 主人败
- 客刑上来 -> 客败

类型：event_verdict substantive variant。

### J4M-12

四库西方白云：
- 基础胜负未明
- 庚辛日弥佳

NCL：
- 大胜
- 庚辛日弥佳

类型：verdict variant。

NCL 的“大胜”证明另一古传本文字确实存在，但仍不能作为“按对称性补四库”的理由。

## 标题与顺序差异

矩阵同时保存：

- J4M-06/07/08：NCL 正文标题支持四库正文，不支持四库目录异题；
- J4M-10：NCL 正文作“推奇兵伏兵法”；
- J4M-11：NCL 正文作“推太乙风云飞鸟助阵法”，正文起句仍“助战之法”；
- J4M-12：NCL 正文作“推对阵有云气定胜负”。

目录/正文顺序继续以正文实际出现顺序为 J4M 编号依据。

## 测试

`tests/test_c108_jinjing_v4_witness_matrix.py`

锁定：

- 四库 profile 是唯一 canonical；
- NCL/Jingyou 均 canonical_override=false；
- J4M-06 pending 细项不能跨见证回填；
- J4M-05/06/09/11/12 的实质差异必须按类型保存；
- J4M-12 四库 null 与 NCL 大胜同时存在，互不覆盖。
