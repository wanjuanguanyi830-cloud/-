# C40 紫庭术语恢复骨架验证

日期：2026-10-05

## 验证对象

- `terminology/zitingjing-migration-map.json`
- `tests/test_zitingjing_terminology_migration.py`

## 锁定规则

测试固定：

- 本地术语库此前已有初步整理；
- 当前仓库尚未迁入旧 `terminology.json`；
- 六个核心词条均存在迁移目标；
- 所有 `manuscript_form` 当前必须为 null；
- 所有 `source_page` 当前必须为 null；
- 文昌九星参校异文不得升级成明钞本 canonical 读法；
- 三旗 / 九宫贵神继续保持紫庭归属未证；
- 恢复顺序优先当前三项来源缺口。

## 通过条件

在旧术语库未恢复前，任何提交若：

- 填写明钞本页码；
- 选定文昌九星异文；
- 把三旗/九宫贵神升级为紫庭 canonical；

都应被视为越过证据边界。
