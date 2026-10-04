# C35 有效迁移状态验证

日期：2026-10-05

验证：

1. J4M-11 legacy flat 字段为 quarantined。
2. replacement 必须精确到 jinjing_siku_volume4 profile。
3. 错 rule_id 的结果拒绝进入 weather-bird profile。
4. 结构化 J4M-11 profile 可清除 legacy replacement gap。
5. 旧 flybird_wl 文本不会自动进入 analysis。
6. 六项统宗 legacy flat 使用 tongzong_volume6/10 collation 路径。
7. collation 可完成 legacy migration，但不会把 pending/unverified 紫庭条目改成 primary_ready。
8. 文昌九星继续 primary_text_pending。

完整 CI：

```
655 passed in 1.07s
```
