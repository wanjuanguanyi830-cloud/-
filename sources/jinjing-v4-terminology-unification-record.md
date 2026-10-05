# 《太乙金镜式经》卷四术语统一记录

## 1. 目录拆分

稳定术语目录：

- terminology/military-p0.json
- terminology/military-jinjing-v4.json

P0：

- J4M-01 推三门具不具
- J4M-02 推五将发不发
- J4M-03 推主客相关法

扩展：

- J4M-04 推主客
- J4M-05 推出师法
- J4M-06 推陈兵向背
- J4M-07 推制阵随地法
- J4M-08 推随地制变
- J4M-09 推太乙在天外地内法
- J4M-10 推奇伏法
- J4M-11 推太乙风云飞鸟助战法
- J4M-12 推阵有风云气定胜负

拆目录只是仓库组织方式，不改变《金镜》卷四正文顺序。

## 2. Canonical / witness

当前 canonical source profile：

jinjing_siku_volume4

NCL-06604 明钞本：

independent manuscript witness

规则：

- 明钞本不覆盖四库 canonical；
- 四库与明钞冲突时并列保存；
- old terminology.json 恢复后，manuscript_form/source_page 挂 witness，不回写 stable preferred term。

## 3. 高风险异文

### J4M-05

四库：12 / 22 / 32。

NCL：当前直接核只见 12 / 22，未见 32。

### J4M-06

四库 canonical：1 / 2 / 4 / 5 / 6 / 9。

NCL：1 / 2 / 3 / 4 / 6 / 7 / 8 / 9 完整表。

不得互补成一个“完整版”。

### J4M-09

四库：8 / 3 / 4 地内助主；9 / 2 / 7 / 6 天外助客；1宫未列。

NCL：1 / 8 / 3 / 4 地内助主。

1宫必须保持 source variant。

### J4M-11

NCL 的主人刑 / 客刑败方读法与四库相关句冲突。

必须分 witness 保存，不能用“语义更顺”做静默修正。

### J4M-12

NCL 西方白云明写“大胜，庚辛日弥佳”。

四库当前 canonical 只锁定“庚辛日弥佳”，基础胜负不按表格对称性补出。

## 4. 其他边界

- J4M-03 主客相关五行相制 != J4M-04 主客先后动静。
- J4M-07 地形制阵 != J4M-08 随地制变。
- J4M-10 不借卷十五近名奇兵伏兵算法。
- J4M-11 必须消费外部观测，不得使用十精飞鸟位置替代。
- J4M-12 未列组合不按五行常识或表格对称性补表。
- 三门/五将与 C117 太公考时的 ready 接线属于 cross-source integration，不改变卷一/卷四原文身份。
