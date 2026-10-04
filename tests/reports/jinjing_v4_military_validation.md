# J4M 《太乙金镜式经》卷四军事十二法验证报告

日期：2026-10-05

## 范围

本轮只完成“来源核对、术名规范、层级隔离、C8 crosswalk 与机器可读建档”，不把未校勘公式冒充为已实现算法。

canonical 来源层：

- ruleset: `jinjing-siku-v4-military-12`
- source profile: `jinjing_siku_volume4`
- rule ids: `J4M-01..J4M-12`

## 核对结论

用户给出的十二条是四库本《太乙金镜式经》卷四连续军事法，不应直接当作现有 C8 `volume5_strict` 的十二个子函数。

正文顺序固定为：

1. 推三门具不具
2. 推五将发不发
3. 推主客相关法
4. 推主客
5. 推出师法
6. 推陈兵向背
7. 推制阵随地法
8. 推随地制变
9. 推太乙在天外地内法
10. 推奇伏法
11. 推太乙风云飞鸟助战法
12. 推阵有风云气定胜负

卷首目录异题仅作 `toc_aliases`，不另建重复规则。

## 防混法断言

新增 `tests/test_jinjing_v4_military_record.py` 固定以下边界：

- J4M-03“推主客相关法”与 J4M-04“推主客”必须分开。
- J4M-07“推制阵随地法”与 J4M-08“推随地制变”必须分开。
- J4M-05“推出师法”不得以《统宗》卷五 `chushi_luedi` 兵额表替代。
- J4M-06“推陈兵向背”不得以旧卷十五“陈兵出乡”替代。
- J4M-09 必须保存《金镜》卷四与《统宗》卷五的来源差异。

## J4M-09 来源隔离

`jinjing_siku_volume4`：

- 地内助主：8/3/4
- 天外助客：9/2/7/6
- 1 宫：本段正文未列

`tongzong_volume5` variant：

- 天内助主：1/8/3/4
- 天外助客：9/2/7/6

因此旧参考代码使用 `[1,8,3,4]` 时，只能归入《统宗》型来源，不得覆盖《金镜》卷四 canonical。

## 当前实现状态

- J4M-01/02：C8-L2 有上游事实容器，公式仍 pending。
- J4M-04：C8-L3 已覆盖先后/动静角色子层，仍是 partial。
- J4M-06：已实现 `chenbing_xiangbei()`，只接收正文明确的 1/2/4/5/6/9 六类，不自动取任意算数个位。\n- J4M-07：已实现 `zhizhen_suidi()`，固定五阵五行与五类地形映射。\n- J4M-09：已实现 `taiyi_tianwai_dinei()`，只使用《金镜》卷四 8/3/4 与 9/2/7/6 两组；1 宫保持未定义。\n- J4M-03/05/08/10/11/12：尚无《金镜》卷四 source-specific runtime implementation。\n- 本轮仍未修改 `src/kintaiyi/junshi_zhanlue.py` 的综合计算行为，避免把独立来源规则提前并入总胜负。

## CI

GitHub Actions run `37227677720`，HEAD `de9c6d375737cb20a4fe11c36364b34c5254032a`：

- workflow: `tests`
- job: `pytest`
- conclusion: `success`
- result: **267 passed in 0.40s**

这表示新增规则表、测试、C8 crosswalk、工作规格与 package-data 配置均未破坏现有测试基线。

## 下一批

优先实现低依赖且边界清楚的：

1. J4M-06 推陈兵向背
2. J4M-07 推制阵随地法
3. J4M-09 推太乙在天外地内法（必须显式 source profile）

之后再做 J4M-05、10、03；J4M-11/12 需先设计外部风云飞鸟/云气观测输入模型。
