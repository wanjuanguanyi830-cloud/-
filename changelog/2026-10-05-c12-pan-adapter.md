# 2026-10-05 C12 legacy snapshot adapter

- 新增 `src/kintaiyi/pan_adapter.py`。
- 旧 flat snapshot 可附加严格 `result["v2"]`。
- adapter 只搬已有盘面事实，不运行古法算法。
- 旧军事战略、旧七术断语、旧运筹博弈结果全部隔离。
- structured analysis / modern 必须显式传入。
- scenario 不从客将等旧字段推断。
- 新增 `tests/test_pan_adapter.py`。
