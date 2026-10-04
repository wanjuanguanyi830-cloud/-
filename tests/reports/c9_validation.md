# C9 现代博弈层验证报告

日期：2026-10-05

## 完成内容

- 新增 `src/kintaiyi/game_theory.py`。
- 新增 `project_seven_method_for_game_theory(...)`。
- 新增 `project_seven_methods_for_game_theory(...)`。
- 新增 `taiyi_palace_feature(...)`。
- 新增 `build_game_theory_feature_bundle(...)`。
- 所有博弈投影明确标 `derived_modern_feature=True`。
- 禁止七术结果 stringify 后搜索“成/吉/正/利”。
- 太乙九宫与洛书九宫明确隔离。

## 关键验证

测试覆盖：

1. T7-04 明确 `verdict="不可攻"` 时，即使 notes 中故意含“成、吉、正、利”，仍只得到负向攻击窗口。
2. T7-04 `可攻` 不被说明文字中的“凶、不利”等字反向覆盖。
3. T7-01 仅投影应期，不产生通用吉凶分。
4. `not_computable` 保持不可计算，不因存在 favorable 文本而评分。
5. 真实 `lion(...)` / `tiger(...)` 七术结构可直接投影。
6. 太乙九宫验证为：
   - 1乾
   - 2离
   - 3艮
   - 4震
   - 6兑
   - 7坤
   - 8坎
   - 9巽
7. 中五仅保留土五行，`positional_effect_allowed=False`。
8. feature bundle 固定 `cross_system_palace_mapping=False`。

## CI

加入 C9 测试后：

- 219 passed
- 2 failed

失败仍完全来自旧 `tests/test_eight_divinations_classics.py`：

- 旧预期把 15 当作将吏兵全具；
- 旧预期把 15 当作三才结构全具。

这两项与 C9 无关，且与已经确认的 canonical “15/25/35 只有天算+地算、无人算”冲突，不回滚。

## 结论

C9 第一阶段通过。

当前博弈模块只负责“现代特征投影”，还没有把参考仓库中的支付矩阵/Nash 权重迁入。后续如果迁入，必须继续把所有权重标为现代模型参数，不能声称来自古籍。
