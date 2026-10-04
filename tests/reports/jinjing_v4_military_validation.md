# J4M 《太乙金镜式经》卷四军事十二法验证报告

日期：2026-10-05

## 范围

J4M 是四库本《太乙金镜式经》卷四军事十二法的独立来源层：

- ruleset: `jinjing-siku-v4-military-12`
- source profile: `jinjing_siku_volume4`
- rule ids: `J4M-01..J4M-12`

C8 `volume5_strict` 只与本层做 crosswalk，不把近名规则自动并入总胜负链。

## 十二法固定顺序

1. J4M-01 推三门具不具
2. J4M-02 推五将发不发
3. J4M-03 推主客相关法
4. J4M-04 推主客
5. J4M-05 推出师法
6. J4M-06 推陈兵向背
7. J4M-07 推制阵随地法
8. J4M-08 推随地制变
9. J4M-09 推太乙在天外地内法
10. J4M-10 推奇伏法
11. J4M-11 推太乙风云飞鸟助战法
12. J4M-12 推阵有风云气定胜负

正文小标题为 canonical，卷首目录异写只作 aliases。

## 第三批新增 runtime

### J4M-01 推三门具不具

运行入口：

- `sanmen_jubu(...)`
- `zhimen_from_cycle_count(...)`

正文明确三门为开、休、生，并明确：

- 太乙、天目分临开/生二门：两门不具；
- 临休门：三门不具。

实现只覆盖以上来源明确组合；两者同落开/生、只给一端等情况保持 `not_defined_by_source_passage` / `not_computable`，不照搬旧 `threedoors` 只看太乙值门的简化逻辑。

直门辅助实现：

- 240 为一周；
- 每 30 移一门；
- 顺序：开、休、生、伤、杜、景、死、惊；
- 第 1..30 为开，第 31..60 为休，……第 211..240 为惊，第 241 重新回开。

州郡岁计直门吉凶独立保存：

- 开/休/生：大吉
- 景：小吉
- 死/惊/伤/杜：大凶

不把“门具”与“直门吉凶”合成单一布尔值。

### J4M-02 推五将发不发

运行入口：`wujiang_fabu(...)`。

五将阻断条件分成三栏：

- 始击有掩击；
- 文昌有囚迫；
- 主客大小将有相关。

三者均无时，`five_generals_released=True`。

J4M-01 的 `three_doors_ready` 作为独立上游事实输入，输出继续分开：

- `five_generals_released`
- `three_doors_ready`
- `combined_ready`
- `deployment_allowed_by_doors`
- `engagement_allowed_by_generals`

保存正文边界：

- 三门不具：不可出兵；
- 五将不发：不可临战。

旧 `fivegenerals` 的格局字符串、中五等混合逻辑不直接进入本 profile。

### J4M-08 推随地制变

运行入口：`suidi_zhibian(...)`。

正文三项临战急务：

1. 士卒服习
2. 随其地形
3. 善用兵器

五类 terrain/arms 映射：

- 沟堑、山林、川泽、丘阜、草木：利步兵；原文“车骑三不当一”
- 平陵、平原、广野：利车骑；原文“步兵十不当一”
- 两阵相近、平地浅草、可前可后：利长戟；原文“剑楯三不当一”
- 萑苇竹萧、草木蒙笼：利矛锤；原文“弓弩三不当一”
- 平阳相远、山谷幽涧、仰高临下：利弓弩；原文“短兵百不当一”

比例只保存为 `source_ratio_text`，不转成现代战力倍率。

另外保存：

- 士卒是否服习
- 器械是否完利
- 将是否知兵
- 君是否择将

这些只形成 readiness/warning，不自动决定胜负。

## 之前已完成

完整 source-specific：

- J4M-05 推出师法
- J4M-06 推陈兵向背
- J4M-07 推制阵随地法
- J4M-09 推太乙在天外地内法
- J4M-10 推奇伏法

partial source-specific：

- J4M-03 推主客相关法：主客目五行相制已实现；“日计纳音以决之”的具体接法仍 pending。
- J4M-04 推主客：C8-L3 已覆盖先后/动静角色子层，仍非整条完成。

## 当前完成度

完整 source-specific runtime：

- J4M-01
- J4M-02
- J4M-05
- J4M-06
- J4M-07
- J4M-08
- J4M-09
- J4M-10

partial：

- J4M-03
- J4M-04

待实现：

- J4M-11 推太乙风云飞鸟助战法
- J4M-12 推阵有风云气定胜负

即十二法中已有 **8 条完整、2 条 partial、2 条 pending**。

## 防混法断言

测试持续锁定：

- J4M-01 不退化成旧 `threedoors` 的“只看太乙值门”逻辑。
- J4M-02 不解析旧 `fivegenerals` 混合字符串结果。
- J4M-03 ≠ J4M-04。
- J4M-05 ≠ 《统宗》卷五兵额表。
- J4M-06 ≠ 旧卷十五陈兵出乡。
- J4M-07 ≠ J4M-08。
- J4M-08 原文比例不转现代战力分数。
- J4M-09 《金镜》profile ≠ 《统宗》profile。
- J4M-10 不调用旧卷十五近名奇伏算法。
- J4M-11/12 必须由外部观测事实驱动，不得从盘内字段伪造。

## CI

第三批修正与 metadata 锁定后，GitHub Actions run `37229118725`：

- workflow: `tests`
- job: `pytest`
- conclusion: `success`
- result: **313 passed in 0.52s**

run 101 / 102 的失败来自第三批代码插入时三个常量表与 catalog 未同步写入，表现为 `NameError` 与旧 catalog 断言；修正提交 `d06cc807da08d12e43224c3a7aaab9af2232e6ee` 后恢复全绿。规则判定断言本身未发生语义冲突。

## 下一批

下一步只剩卷四最依赖“外部观测事实”的两条：

1. J4M-11 推太乙风云飞鸟助战法
2. J4M-12 推阵有风云气定胜负

应先建立 observation schema（来源、方向、目标、颜色、形态、动态、所临将位等），然后再实现判读；没有观测输入时必须返回 `not_computable`。
