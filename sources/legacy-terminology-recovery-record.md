# 旧 terminology.json 恢复边界记录

## 当前状态

旧本地 terminology.json 曾完成过初步整理，但当前仓库仍未取得原始文件或真实 schema。

因此状态保持：

blocked_missing_original_store

不得把当前 stable catalogs 反向拼成“旧 terminology.json”。

## 当前恢复资产

- terminology/zitingjing-migration-map.json
- terminology/ncl06604-legacy-reconciliation-map.json
- terminology/legacy-recovery-manifest.json

其中 legacy-recovery-manifest 是可逆映射层，不是 master store。

## Manifest 当前覆盖

- stable catalogs: 13
- stable entries: 111
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
