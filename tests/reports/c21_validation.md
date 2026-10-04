# C21 军事 derived profile 验证报告

日期：2026-10-05

验证：

- 卷十五 14 个旧综合术目形状锁定。
- 卷十七 12 个旧综合术目形状锁定。
- partial profile 不冒充 complete。
- unknown topic 不静默提升。
- cross_volume/C8/J4M merge 全部为 false。
- legacy 军事应用/占断转为 quarantined。
- 空 profile 不能清除 replacement gap。
- 显式独立 payload 只清自己的 gap。
- profile 不会写入 `analysis.military`。

完整 CI：

```
362 passed in 0.35s
```

当前基线：362 passed / 0 failed。
