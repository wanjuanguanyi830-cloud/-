# C83 — J4M-01～04 影印边界与“太蔟/太簇”归一

日期：2026-10-05

本轮复扫《太乙金镜式经》四库本卷四 J4M-01～04。

新增：

- J4M-01～04 scan_rule_audit，机器化锁定不可补推边界；
- 四库原文字形“太蔟” -> 项目规范词形“太簇”的来源限定术语 alias；
- runtime 同时保存原始输入与 canonical god name；
- terminology/jinjing-v4-aliases.json。

未改变的关键原则：

- 三门未明组合不补判；
- 三门具不替代五将阻断事实；
- J4M-03 不恢复独立日干支纳音；
- J4M-04 不与 J4M-03 / D8-06 合并。

新增：
- sources/c83-j4m01-04-scan-rule-audit-record.md
- terminology/jinjing-v4-aliases.json

更新：
- rules/jinjing_v4_military.json
- src/kintaiyi/jinjing_v4_military.py
- tests/test_jinjing_v4_military.py
- tests/test_jinjing_v4_military_record.py
- terminology/README.md
