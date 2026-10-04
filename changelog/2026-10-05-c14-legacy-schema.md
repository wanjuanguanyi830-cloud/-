# 2026-10-05 C14 legacy schema registry

- 新增 `src/kintaiyi/legacy_schema.py`。
- legacy field policy 改为单一真源。
- C12 adapter 改读 registry。
- C13 migration audit 改读 registry。
- 明确 migrated_fact / quarantined / unported / embedded_v2 四态。
- 明确每个 quarantined 字段的新 replacement path。
- 新增 `tests/test_legacy_schema.py`。
