# 2026-10-05 C33 V17 runtime deduplication

- `tongzong_v17_structured.py` 固定为 V17-06/07/08/09 canonical runtime。
- `tongzong_v17_conditions.py` 改为 compatibility adapter。
- 修正“门不具或将不发”为任一 false 即成立。
- 补回“始击在内”作为讨捕捕得证据。
- 旧 API 字段继续可用，但只翻译 canonical runtime 结果。
- compatibility adapter 增加显式 canonical_runtime 标记。
- 新增架构回归测试，禁止第二套古法公式复生。
