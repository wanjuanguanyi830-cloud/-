# C14 legacy schema policy 验证报告

日期：2026-10-05

## 完成内容

- 新增 `src/kintaiyi/legacy_schema.py`。
- 建立 legacy 字段迁移策略单一真源。
- C12 adapter 改为读取 C14 registry。
- C13 migration audit 改为读取 C14 registry。
- 明确四态：
  - migrated_fact
  - quarantined
  - unported
  - embedded_v2
- quarantined 字段具备明确 structured replacement path。
- unknown 字段保持 unported，不猜目标。

## 关键回归

测试覆盖：

1. `太乙落宮 -> board.taiyi.palace`。
2. `軍事戰略 -> analysis.military`。
3. 旧七术 -> `analysis.seven_methods`。
4. 旧运筹博弈 -> `modern.game_theory`。
5. `卷十二` 等未知/未迁移字段保持 unported。
6. `v2` 识别为 embedded_v2。
7. 繁简体 aliases 使用同一迁移政策。
8. C12/C13 原有测试继续通过。

## CI

C14 registry 测试加入后：

```
263 passed in 0.32s
```

当前全套：

- 263 passed
- 0 failed

## 结论

C14 通过。

后续新增或迁移旧 pan 字段时，必须先更新 C14 registry，再由 C12/C13 自动获得一致行为，禁止重新在各模块复制字段名单。
