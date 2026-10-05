# C104 大游天目：金镜 / 统宗来源分层

日期：2026-10-05

## 1. 为什么要纠正 C98 的阶段性判断

C98 在只依据 2026-10-04 恢复记录时，把旧 `%180/+214` wrapper 继续视作 deprecated compatibility。

进一步直接核源后发现：

《太乙统宗宝鉴》卷七“明太游天目所主术”明确有：

- 神盈差214；
- 大周180；
- 小周18；
- 顺行十六宫；
- 大武、阴德重留。

《易学象数论》也明确记录：

- 神周18；
- 神盈差214；
- 余起天道；
- 顺行十六神；
- 大武、阴德重留。

因此：

> 旧 wrapper 的“来源身份”判断需要修正；+214/180/18本身不是无源公式。

真正的问题是此前把它放在旧 compatibility 模块，没有 source-specific 契约。

## 2. 金镜 profile

《太乙金镜式经》卷五：

“推大游天目所在法”明确：

- 天目元法72；
- 天目周法18；
- 命起天道；
- 顺行十六神；
- 大武、阴德重留一算。

来源：

https://ctext.org/wiki.pl?chapter=606969&if=gb

## 3. 统宗 profile

《太乙统宗宝鉴》卷七：

- 神盈差214；
- 大周180；
- 小周18；
- 顺行十六宫；
- 大武、阴德重留。

来源：

https://www.shidianguji.com/book/CADAL02055529/chapter/1l5erk9igsxeb

参校《易学象数论》：

https://www.shidianguji.com/book/SK0122/chapter/1l9rdmvwzdrm7

该参校明确写“余起天道”。

统宗一电子转录起点处见“天通”类 OCR，C104 不把 OCR 字形另造第二条路径。

## 4. 18步路径

统一路径：

1. 天道
2. 大武
3. 大武
4. 武德
5. 太簇
6. 阴主
7. 阴德
8. 阴德
9. 大义
10. 地主
11. 阳德
12. 和德
13. 吕申
14. 高丛
15. 太阳
16. 大炅
17. 大神
18. 大威

重复点只来自：

- 大武；
- 阴德。

## 5. 来源不能乱合

金镜：

- surplus=0
- outer=72
- inner=18

统宗：

- surplus=214
- outer=180
- inner=18

C104 不设置 default profile。

调用必须显式：

`source_profile="jinjing" | "tongzong"`

## 6. 最近两天恢复关系

10月4日：

`rules/dayou/tianmu.json`

已经保存：

- 金镜72→18；
- 18步路径；
- 大武/阴德重留。

C104 采用该最近两天工作作为恢复线索，再用直接来源重核。

因此符合：

“只采用最近两天旧工作内容，但每项重新核来源”。

## 7. 与 C98 的关系

C98 对 `cycles.bigyo_tianmu` 的兼容隔离属于阶段性治理。

C104 建立后，应把 legacy wrapper 改成：

- 0基输入适配到 C104 1基输入；
- tongzong → C104 tongzong；
- jinjing → C104 jinjing。

随后：

- 不再把 tongzong +214 本身登记为错误公式；
- 只保留“旧 compatibility wrapper 不应成为独立真源”的接口层说明。
