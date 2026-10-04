# C11 pan v2 builder 验证报告

日期：2026-10-05

## 完成内容

- 新增 `src/kintaiyi/pan_v2.py`。
- `build_pan_v2(...)` 生成完整 schema 2.0。
- `validate_pan_v2(...)` 验证结构和表示层不变量。
- builder 不导入 `Taiyi`，不重复古法算法。
- builder 输出可直接交给 C10 `v2_consumer.py`。

## 关键测试

新增测试证明：

1. 根结构与 board/cycles/analysis 必需子层完整。
2. 太乙/诸将/计算对象只要 `palace=5`，其 `sector` 强制为 null。
3. 天目 `sector_element` 与 `nine_palace_element` 同时保留。
4. 将帅 `intrinsic_element` 与 `palace_element` 同时保留。
5. scenario 只允许三个 canonical 事件输入。
6. 非 canonical scenario 字段直接拒绝。
7. tuple/set 可规范成 JSON-safe list。
8. 未知对象不会被自动 `str(...)`，而是 TypeError。
9. builder 输出能被 C10 strict consumer 直接读取。
10. general 五行层缺字段时 validator 给 warning，不自行猜值。

## CI

加入 C11 测试后：

- 237 passed
- 2 failed

两条失败仍只来自旧 `tests/test_eight_divinations_classics.py` 对 15 的过时预期：

- 旧预期：15 无缺项；
- canonical：15 缺兵卒 / 无人算。

- 旧预期：15 三才结构全具；
- canonical：15 仅天算+地算。

没有 C9/C10/C11 新失败。

## 阶段结论

C9 第一阶段：通过。
C10 第一阶段：通过。
C11 第一阶段：通过。

目标仓库现在已经具备：

```
古法结构化结果
    ↓
C8 military composite
    ↓
C9 modern game-theory projection
    ↓
C11 pan_v2 builder
    ↓
C10 strict v2 consumer
    ↓
未来 Taiyi.pan() / CLI / UI
```

后续真实主程序接线时，禁止绕过 builder/consumer 再直接混读旧 flat schema。
