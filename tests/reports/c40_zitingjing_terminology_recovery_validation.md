# C40 紫庭术语恢复骨架验证

> **状态更新（2026-10-06）**：本文件保留为历史阶段记录。用户已重新提供研易楼藏《太乙紫庭祕訣》明钞本，目录页（PDF 第5–6页）已直接核验，未见“文昌九星值宫术”题名。文昌九星现行稳定规则归 `C70-TONGZONG-WENCHANG-NINE-STARS`（《太乙统宗宝鉴》卷六 NGJ）；现代整理本“附太乙文昌九星值宫术”只记为编辑层目录证据，来源仍未完全证明。旧文中的“紫庭 primary pending / 扫描未重新挂载 / C70 仅参校”等状态均已被本结论取代。当前依据见 `sources/c70-wenchang-nine-stars-source-separation-record.md`。

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
