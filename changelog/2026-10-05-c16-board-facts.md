# 2026-10-05 C16 board facts

- `pan_v2.BOARD_KEYS` 新增 `sixteen_palaces`。
- C12 adapter 迁移旧 `十六宮分佈` 到 `board.sixteen_palaces`。
- 天乙/地乙/四神/直符/合神/计神迁移到 `board.generals.*.sector`。
- C14 将上述 7 项从 unported 改为 migrated_fact。
- C13 不再将这些字段列为下一批迁移候选。
- 不调用旧算法，只搬 snapshot 事实。
- 新增 `tests/test_c16_board_migration.py`。
