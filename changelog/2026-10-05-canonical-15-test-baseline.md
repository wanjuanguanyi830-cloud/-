# 2026-10-05 canonical 15 测试基线修正

此前实现已经按确认规则修正：

- 5：仅地算（吏士）
- 15 / 25 / 35：仅天算 + 地算（将军 + 吏士）
- 15 / 25 / 35：无人算（缺兵卒）

但旧 `tests/test_eight_divinations_classics.py` 仍保留两条过时预期：

1. 15 的 preparedness `missing=[]`
2. 15 的三才 components 全为 True

本次只修测试预期：

- 15 preparedness → `missing=["兵卒"]`
- 15 components → `ten=True, five=True, one=False`
- 明确断言三才缺“人”

未修改 canonical 实现，也未为了 CI 回退公式。
