# C76 — 《太乙金镜式经》十二推法底本与引文异文

日期：2026-10-05

本轮新增四类来源边界：

- 锁定四库扫描 witness：CADAL06056494（浙江大学图书馆，卷一~卷四，144页）；
- 登记 NCL-06604 明钞本为独立校字 witness；
- 明确四库目录与正文标题/顺序差异，J4M 编号继续按正文顺序；
- 发现 J4M-08 “晁错曰”与《汉书·爰盎晁错传》存在实质异文，禁止以《汉书》静默改写《金镜》runtime。

同时登记另一 CText 转录把同组内容标作“卷三”的卷次 variant；在底本未确认前不覆盖四库卷四 canonical。

新增：

- sources/c76-jinjing-v4-witness-collation-record.md

更新：

- rules/jinjing_v4_military.json
- src/kintaiyi/jinjing_v4_military.py
- tests/test_jinjing_v4_military.py
- tests/test_jinjing_v4_military_record.py


## C79 后续状态

C79 已直接核 CADAL06056494 图像页并 supersede C76 的两个 provisional 项：

- 十二法逐条数字扫描 locator 已完成（p.128-p.143）；
- J4M-08 旧转录“矛锤”已按 p.136 纠正为“矛鋋”。

C76 的来源边界原则不变；仅上述 locator 状态与字形读法被后续影印核验更新。
