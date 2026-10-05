# C68 《景祐太乙福应经》卷四独立军事规则 profile

日期：2026-10-05

## 为什么另建 JF4M

C67 已证明《景祐太乙福应经》卷四与四库《太乙金镜式经》卷四并非“同文小异”：

- 陈兵向背数表不同；
- 随地制变引文数字、兵器段落不同；
- 太乙地内宫是否含一宫不同；
- 风云飞鸟有实质胜负方向差异；
- 奇伏有“伏兵必败”与“奇兵必从”的实质异文。

继续只把这些差异嵌在 J4M 的 source_variants 中，容易让后续消费者误认为可以从不同书中挑字段拼成一条最佳规则。

因此 C68 新建：

rules/jingyou_fuying_v4_military.json

ruleset：

jingyou-fuying-v4-military-11

source profile：

jingyou_fuying_volume4

规则编号：

- JF4M-01 释三门具不具第四十四
- JF4M-02 释五将发不发第四十五
- JF4M-03 释主客相关第四十六
- JF4M-04 释主客第四十七
- JF4M-05 释出师略地第四十八
- JF4M-06 释陈兵向背第四十九
- JF4M-07 释置阵随地第五十
- JF4M-08 释随地形制变第五十一
- JF4M-09 释太乙在天外地内宫第五十二
- JF4M-10 释太乙风云飞鸟置战第五十三
- JF4M-11 释奇伏第五十四

《福应经》卷四没有《金镜》J4M-12“推阵有风云气定胜负”的直接同条，因此本 profile 只建十一条，不人为补第十二条。

## 编号政策

JF4M 是《福应经》自身编号空间，不复用 J4M。

parallel_jinjing_rule 只做比较索引：

- JF4M-01 -> J4M-01
- ...
- JF4M-09 -> J4M-09
- JF4M-10 -> J4M-11（风云飞鸟）
- JF4M-11 -> J4M-10（奇伏）

后两条顺序与《金镜》正文顺序不同，正说明独立编号是必要的。

## 执行状态

当前十一条统一：

implementation_status = source_record_only

原因：

- 现在目标是先建立古籍真源层；
- 尚未为《福应经》复制一套 runtime；
- 不允许拿 J4M runtime 冒充 JF4M；
- 只有将来逐条实现并通过 source-specific tests 后，才能升级为 executable profile。

## 来源状态

当前在线全文来自识典古籍所载《景祐太乙福应经》卷四，书目 ID CADAL02094381。

本轮已经做文本级交叉校勘，但还没有把该书每条规则绑定到可直接复核的扫描页，因此：

source_status = ancient_parallel_text_transcription_scan_locator_pending

含可疑 OCR 的字继续保留 pending，例如：

- JF4M-02 “大小将不相开”
- JF4M-07 “地形跨斜”
- JF4M-07 “地形高而不平”
- JF4M-08 矛类兵器异体字

不得把这些转录字形升级为 verified glyph。

## source_profiles 接入

C68 将 jingyou_fuying_volume4 加入 MILITARY_PROFILE_KEYS。

P0 三项 crosswalk 同时记录：

- J4M-01 / JF4M-01
- J4M-02 / JF4M-02
- J4M-03 / JF4M-03

不同 profile 继续：

- canonical_selected = None
- cross_source_merge = False

C8 仍只是上游事实/组合层，不成为任何古籍公式替身。

## 测试

新增：

tests/test_jingyou_v4_military_record.py

锁定：

- 恰好 11 条；
- 独立 JF4M 编号；
- 陈兵方向表；
- 地内宫组；
- 风云飞鸟与奇伏关键异文；
- source_record_only 不得伪装 runtime。
