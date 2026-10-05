# C85 — J4M-11～12 影印规则边界补齐

日期：2026-10-05

本轮将 J4M-11、J4M-12 补入统一 `scan_rule_audit`：

- J4M-11：外部观测必需、动作按正文词面、众来噪阵不补胜负、福应经冲突读法不回写；
- J4M-12：方位×颜色逐项保存、西方白云不补大胜、cloud_bearer 与 verdict_subject 分离、不做五行/对称性补表。

完成后十二法 scan audit 覆盖为：

- J4M-01..04：C83
- J4M-05..10：C80
- J4M-11..12：C85

新增：
- sources/c85-j4m11-12-scan-rule-audit-record.md

更新：
- rules/jinjing_v4_military.json
- tests/test_jinjing_v4_military_record.py
