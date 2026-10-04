# C61 unported catalog 一致性清扫验证

日期：2026-10-05

验证：

1. C15 catalog 仍完整覆盖 67 个 legacy 字段。
2. `CATALOG` 与 `REFERENCE_PAN_UNPORTED_FIELDS` 集合完全一致。
3. 当前 layer 统计固定为 canonical 31 / source_variant 16 / derived 18 / pending 2。
4. 严格 pending 只剩 `推太乙當時法` 与 `文昌九星`。
5. 巡狩术升级为卷五直接来源已核，但 `migrate_whole=False`。
6. 君基 / 臣基 / 民基 / 五福五项保留卷六/卷七 witness variant。
7. 天乙金神 / 地乙土神 / 直符火神三项升级为卷七直接来源已核。
8. 所有九个新升级字段 action 均为 `source_verified_split_runtime_next`，不会误报 runtime 已实现。
9. 十精旧字段备注同步 C57/C58/C59 已完成云气三层。
10. 旧 flat 与旧综合 wrapper 继续禁止直接迁移。

C61 catalog consistency test：

`tests/test_c61_unported_catalog_consistency.py`

清扫提交后的 CI 已通过；后续 C60 文档增补不改变 C61 分类。
