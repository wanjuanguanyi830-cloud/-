# C22 military rule-unit 验证报告

日期：2026-10-05

验证：

- 卷十五 source rules：14
- 卷十七 source rules：11
- 跨卷 helper：1
- 总 source rules：25
- 每个旧 payload key 都有唯一 rule_id
- 孤虚对照不进入卷十七 source rule 集
- J4M/C8 overlap 只作为 metadata
- 外部风云规则显式声明 external_inputs
- C21 profiles 已暴露 rule_id crosswalk

完整 CI：

```
373 passed in 0.65s
```

当前基线：373 passed / 0 failed。
