# C30 pan v2 aggregation contract 验证报告

日期：2026-10-05

## 验证

- analysis 固定四区段。
- legacy flat 键进入 analysis 会被拒绝。
- derived military profile 进入 analysis.military 会被拒绝。
- source_variants 固定 patterns/military/zitingjing/military_derived。
- modern.game_theory 必须有 derived_modern_feature=True。
- C11 中五 sector=null 约束继续生效。
- 未知 source_variants 根槽会被 validator 拒绝。
- 普通 C11 payload 未标 C30 contract 时给 warning，不破坏兼容。
- compat 中的 legacy quarantine 不会自动重建 analysis。

## CI

```
626 passed in 0.59s
```

当前 C30 基线：626 passed / 0 failed。
