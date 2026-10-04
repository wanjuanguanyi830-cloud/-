# 2026-10-05 C15 unported field catalog

- 盘点参考 `Taiyi.pan()`：108 个顶层字段中 67 个仍 unported。
- 新增 `src/kintaiyi/unported_catalog.py`，覆盖全部 67 个字段。
- 按 canonical / source_variant / derived / pending 分层。
- 新增 P0-P3 迁移优先级。
- 综合卷次包装器固定 `migrate_whole=False`。
- 军事卷四/五/十五/十七明确禁止相互覆盖。
- C14 manifest 为 unported 字段附加候选层与优先级。
- C13 audit 输出 next migration candidates。
- 新增 `tests/test_unported_catalog.py`。
