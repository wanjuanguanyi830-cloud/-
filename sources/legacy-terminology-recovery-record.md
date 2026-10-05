# 旧 terminology.json 恢复边界记录

## 当前状态

旧本地 terminology.json 曾完成过初步整理，但当前仓库仍未取得原始文件或真实 schema。

因此状态保持：

blocked_missing_original_store

不得把当前 stable catalogs 反向拼成“旧 terminology.json”。

## 当前恢复资产

- terminology/zitingjing-migration-map.json
- terminology/ncl06604-legacy-reconciliation-map.json
- terminology/zitingjing-legacy-scan-recovery.json
- terminology/zitingjing-recovery-status.json
- terminology/legacy-recovery-manifest.json

其中 legacy-recovery-manifest 是可逆映射层，不是 master store；zitingjing-legacy-scan-recovery 是旧扫描整理残留 witness，不回填 old_term_record_id / manuscript_form / source_page 等旧 store 字段。

## Manifest 当前覆盖

- stable catalogs: 15
- stable entries: 148
- migration-linked stable entries: 14
- NCL migration-only candidates: 0

NCL 的 8 个旧对账项现均可指向 stable terminology：

- J4M-03 太簇 / 太蔟相关
- J4M-05 出师
- J4M-06 陈兵向背
- J4M-08 随地制变 / 矛鋋
- J4M-09 太乙在天外地内
- J4M-10 奇伏
- J4M-11 风云飞鸟助战
- J4M-12 阵有风云气定胜负

## 严禁推断的旧字段

原件未恢复前，以下字段必须保持 null：

- old_term_record_id
- manuscript_form
- source_page
- source_section
- old_definition
- old_notes
- old_aliases

当前直接影像已核的 NCL 页码是 current_verified_evidence，不等于旧 terminology.json 当时记录的 source_page 字段。

## 未来取得旧 store 后的合并顺序

1. 保留原 old_term_record_id，不重新编号。
2. 用 preferred term / aliases 产生候选 stable refs。
3. 用 manuscript_form / source_page / source_section / rule id / source profile 排除误合并。
4. 一致则合并来源链。
5. 冲突则 legacy/current 并列。
6. 无法唯一匹配则保持 unmapped。
7. 不为达到100%匹配率猜归属。

## 不变量

- stable rule_id / source profile 不由旧库覆盖。
- OCR 或旧录入错误不能覆盖当前直接来源复核。
- 同名跨来源规则继续分 profile。
- 旧库恢复只增加历史身份、字形、页码、定义与 notes，不逆转已经完成的 source-specific 校勘。


## 研易楼明钞本旧扫描恢复

用户已确认：研易楼藏《太乙紫庭祕訣》明钞本此前在整理术语库阶段已经扫描，且本地 E 盘仍保存原文件。因此“未取得扫描资源”的旧表述废止。

当前执行环境仍未重新挂载 E 盘原扫描，也未恢复旧 `terminology.json` 原始字节。需要严格区分两条证据链：

1. **明钞本扫描事实**：用户确认此前已扫描；这一事实成立，但当前还没有重新取得当时的页码、逐字抄录、old term id 与 notes。
2. **旧代码残留**：`kentang2017/kintaiyi/src/kintaiyi/config.py` 仍保存九星旧实现，但其第1020–1024行明确写明来源为《太乙统宗宝鉴》卷六。因此其中“文曲、玄鳳、明維、昭搖、立華、華明、玄武、玄冥、雄明”等词形只能视为 prior workflow code residue，**不能直接认定为研易楼明钞本逐字扫描结果**。

恢复资产：`terminology/zitingjing-legacy-scan-recovery.json`。该资产同时记录“明钞本此前已扫描”与“旧统宗九星实现残留”，并明确禁止把两者混成同一来源。

当前处理原则：

- 研易楼本 `manuscript_form/source_page/old_term_record_id/old_notes` 继续保持待原件恢复；
- 旧代码词形与 C70《统宗》NGJ 见证的差异继续并列；
- 文曲/文昌、昭搖/阴德、立華/招摇、雄明/维明及旧年干落宫表不得静默归一；
- 只有 E 盘原扫描或旧 `terminology.json` 重新挂载后，才能判断这些旧词形是否也见于研易楼本。
