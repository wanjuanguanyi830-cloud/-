# 2026-10-05 C32 cross-volume Guxu helper

- 新增 src/kintaiyi/cross_volume_helpers.py。
- V17-D1 固定为 derived_cross_volume_helper。
- helper 只消费 D8-05 与 V17-09 结构化结果。
- V17-09 增加 inputs 回显用于来源一致性审计。
- 输入 rule_id 不匹配直接拒绝。
- 内外输入冲突输出 input_conflict，不自行重算。
- mixed_evidence 保持原样。
- canonical_source_rule_count 固定为 0。
- 新增 tests/test_cross_volume_helpers.py。
