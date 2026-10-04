# 2026-10-05 C11 pan v2 builder

- 新增 `src/kintaiyi/pan_v2.py`。
- 新增完整 pan v2 2.0 根结构 builder。
- 中五强制 `sector=null`。
- scenario 仅允许三项 canonical 事件输入。
- 保留天目与诸将双层五行事实。
- 非 JSON-safe 未知对象直接拒绝。
- 新增 `validate_pan_v2`。
- 新增 `tests/test_pan_v2_builder.py`。
