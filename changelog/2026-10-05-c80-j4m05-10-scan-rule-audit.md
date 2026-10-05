# C80 — J4M-05～10 影印规则边界复扫

日期：2026-10-05

本轮依据已完成的 CADAL 四库扫描定位，复扫 J4M-05～J4M-10。

未发现除 C79“矛鋋”纠字之外的新核心公式硬错误。新增 machine-level scan_rule_audit，用于锁定：

- J4M-05：12/22/32 不扩成所有尾数2；
- J4M-06：1/2/4/5/6/9 不取个位补表；
- J4M-07：同类/相生不补胜负；
- J4M-08：矛鋋及原比例不转现代战力值；
- J4M-09：四库本不补1宫；
- J4M-10：“败/从”异文不造公式，非整十军数不自定取整。

新增：
- sources/c80-j4m05-10-scan-rule-audit-record.md

更新：
- rules/jinjing_v4_military.json
- tests/test_jinjing_v4_military_record.py
