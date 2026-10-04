# C10 v2 消费层验证报告

日期：2026-10-05

## 完成内容

- 新增 `src/kintaiyi/v2_consumer.py`。
- 支持直接 v2 与 legacy pan 内嵌 `result["v2"]`。
- flat-only 输入不会被自动拼成 v2。
- analysis / board 子层缺失时显式返回 `not_computable`。
- 新增 `build_v2_view_model(...)`，供未来 UI/CLI 共用。
- view model 固定 `legacy_fallback_used=False`。

## 关键测试

新增测试证明：

1. 直接 v2 可解析。
2. 同时存在 flat 与 v2 时，消费层只读 v2。
3. 只有 `主算/客算/太乙/七式` 等旧字段时拒绝混读。
4. `analysis.military` 不会回退读取旧 `军事战略`。
5. `board.taiyi` 不会回退读取旧顶层 `太乙`。
6. 缺子层返回明确 missing path。
7. 缺根区段不会自动造值。
8. view model 明确报告未使用 legacy fallback。
9. 未知区段名直接拒绝。

## CI

加入 C10 测试后：

- 228 passed
- 2 failed

失败仍仅为旧 `tests/test_eight_divinations_classics.py` 对 15 的过时预期，与 C10 无关。

## 结论

C10 第一阶段通过。

由于目标仓库尚未有完整 pan v2 producer / `Taiyi.pan()` 主入口，下一阶段应补纯 builder，再由后续真实应用入口接线。
