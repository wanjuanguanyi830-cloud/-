# 2026-10-05 C13 legacy migration audit

- 新增 `src/kintaiyi/migration_audit.py`。
- 可审计单个 legacy snapshot 的 v2 迁移状态。
- 可识别 structured replacement gaps。
- 可批量统计迁移率、隔离率、未迁移字段频率。
- 不删除 legacy compat，也不把迁移元数据参与古法判断。
- 新增 `tests/test_migration_audit.py`。
