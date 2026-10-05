# C77 — 建立《景祐太乙福应经》卷四独立 JF4M profile

日期：2026-10-05

新增 rules/jingyou_fuying_v4_military.json，把《福应经》卷四十一条军事/主客术法从 J4M 内嵌异文提升为独立古籍 source profile。

核心原则：

- JF4M 与 J4M 各自编号；
- parallel_jinjing_rule 只做比较，不做字段继承；
- 当前全部 source_record_only；
- 不把 J4M runtime 冒充《福应经》算法；
- source_profiles 允许 jingyou_fuying_volume4 与其他来源并列保存，但 cross_source_merge 仍为 false。
