# 2026-10-05 C17 source-profile isolation

- 新增 `src/kintaiyi/source_profiles.py`。
- 统宗卷四格局与 `jinjing_geju` 分 profile 保存。
- 三门/五将明确 J4M-01/02 与 C8-L2 非公式等价。
- 主客相关 J4M-03 与 C8-L3 明确非直接替代。
- 旧释格局/三门/五将/主客相关由 unported 改为 quarantined。
- C13 replacement gap 改为检查具体 `source_variants.*.profiles`。
- 空 profile 容器不能假装完成迁移。
- 新增 `tests/test_source_profiles.py`。
