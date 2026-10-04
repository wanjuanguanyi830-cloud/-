# 2026-10-05 C22 military rule units

- 卷十五综合 payload 拆为 V15-01..14。
- 卷十七真正 source rules 拆为 V17-01..11。
- “孤虚对照”识别为跨卷 derived helper，编号 V17-D1。
- 每条规则记录输入依赖、外部输入、overlap 与来源标题。
- 自动给出低依赖候选批次。
- C21 profile 增加 payload key → source_rule_id crosswalk。
- 新增 `tests/test_military_rule_units.py`。
