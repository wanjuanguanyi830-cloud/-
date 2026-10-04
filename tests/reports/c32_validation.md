# C32 V17-D1 跨卷 helper 验证报告

日期：2026-10-05

验证：

1. 只接受 D8-05 + V17-09。
2. 内虚时只读出宜攻外，并与 V17-09 正向求索作基础对照。
3. 外孤时只读出宜攻内，并与 V17-09 负向求索作基础对照。
4. V17-09 mixed_evidence 不被 helper 覆盖。
5. 两边 realm 不一致时返回 input_conflict。
6. helper 深拷贝来源结果，不反写源对象。
7. canonical_source_rule_count=0。

与 C31/最新证据测试合并后：

```
637 passed in 0.84s
```

当前基线：637 passed / 0 failed。
