# C81 紫庭旧 terminology.json 恢复可用性审计

日期：2026-10-05

## 目标

C81 不重建术语库。

它只回答一个问题：

> C40 所等待的旧本地 `terminology.json`，现在是否已经取得到足够真实的文件 / schema，可以安全迁移？

结论：

`blocked_missing_original_store`

## 本轮检查

当前 GitHub 树：

- 无根目录 `terminology.json`；
- 无 `terminology/terminology.json`；
- 无 `data/terminology.json`。

上述三个常见路径的 Git 提交历史查询：

- 均无匹配提交。

当前可检索的 ChatGPT Library：

- 以 `terminology`、`太乙紫庭`、`紫庭秘诀` 等标题 / 内容检索未找到可恢复旧文件。

注意：

“当前恢复通道无匹配”**不等于**“历史文件从未存在”。

用户此前确认旧术语主库做过初步整理，因此 C81 继续承认：

`prior_local_terminology_status = preliminary_completed_locally`

只是当前执行环境没有挂载原文件，因此仍不能安全迁移。用户已经确认本地 E 盘仍有副本；这改变“历史文件是否还存在”的证据状态，但不改变当前 parser 禁止状态。

## 当前新增恢复线索

机器状态现在同时记录：

- 用户确认本地 E 盘副本存在；
- 当前 runtime 未挂载该副本；
- `terminology/zitingjing-legacy-scan-recovery.json` 已从此前工作残留恢复文昌九星旧扫描整理词形；
- 原始扫描页尚未重新挂载；
- 旧 terminology.json 的真实 schema / old IDs / old definitions 仍未取得。

这些线索只提高“可恢复性”，不等于旧 store 已恢复。

## 为什么不写 parser

旧 schema 未知。

因此不能猜：

- old term id 格式；
- 顶层是 list 还是 dict；
- alias 字段结构；
- definition / note 的嵌套方式；
- 页码字段类型；
- 一个术名是否允许多个来源记录。

C81 继续固定：

- `original_schema_available=false`
- `parser_allowed=false`
- `synthetic_reconstruction_allowed=false`

以后原文件恢复后，再针对真实 schema 写一次性 adapter。

## 六项核心词条

C40 的恢复顺序保持不变：

1. 文昌九星；
2. 三旗行宫；
3. 九宫贵神；
4. 太乙九星；
5. 文昌变化；
6. 始击变化。

六项当前都不能从旧 store 回填：

- `old_term_record_id`
- `manuscript_form`
- `source_page`
- `source_section`
- `old_definition`
- `old_notes`
- `old_aliases`

## 不能替代旧 store 的材料

以下材料即使已经有较高质量校勘，也不能用来伪造研易楼明钞本字段：

- 《太乙统宗宝鉴》；
- 《三才世纬》；
- 现代整理材料；
- OCR 猜测；
- C70 文昌九星统宗 profile。

尤其 C70 只能说明“统宗卷六怎么写”，不能反填：

- 紫庭实际字形；
- 紫庭页码；
- 旧本地术语 ID；
- 旧定义 / 备注。

## 两种不同的解锁证据

完整旧术语库恢复需要：

- 原 `terminology.json`；
- 或其精确历史快照。

如果只取得研易楼明钞本扫描页，则只能独立恢复：

- `manuscript_form`
- `source_page`
- `source_section`

不能据扫描页重造原来的：

- old ID；
- old notes；
- old aliases；
- old definition 数据结构。

## 新增机器状态

`terminology/zitingjing-recovery-status.json`

它与 C40 migration map 的关系：

- C40：定义“恢复什么”；
- C81：定义“目前能不能恢复”。

两者都不是新的 `terminology.json`。


## Legacy scan residue 边界

文昌九星旧扫描残留现在属于 `legacy scan extraction residue`。它可以证明此前扫描/术语整理确有产物，并提供候选词形用于未来对账；但在 E 盘原扫描页重新挂载前，不得把这些词形写入 `manuscript_form` 或 `source_page`，更不能据此猜旧 `old_term_record_id`。


## 2026-10-05 全分支与公开网络补充审计

### Git 分支

已递归检查当前仓库全部 5 条可见分支：

- `main`
- `codex/c1-c7-canonical`
- `codex/taiyi-base-motion-2026-10-04`
- `codex/taiyi-rules-v2-20261005`
- `integrate-taiyi-war-v1-20261004`

均未发现历史 `terminology.json`。

因此旧主库恢复已明确不是“漏合并某个 Git 分支”，只能等待：

- 用户本地 E 盘原文件；
- 或其他精确旧 store 快照。

### 研易楼明钞公开恢复

公开网络现可确认：

- 书格存在研易楼藏明钞本资源帖；
- 帖内标注 181 单页灰度、328M；
- 现代出版目录明确列 `附太乙文昌九星值宮術`。

但当前公开检索仍未恢复该附篇的直接明钞影印页或逐字正文。

所以：

- `manuscript_form` 继续 null；
- `source_page` 继续 null；
- parser 继续禁止；
- 紫庭文昌九星 primary 继续 blocked；
- 《统宗》C70 只能参校，不能反填。

### 三旗 / 九宫贵神状态变化

这两项现行软件规则来源已经由直接卷十校勘解决：

- `C126-TONGZONG-THREE-BANNERS`
- `C127-TONGZONG-NINE-PALACE-NOBLES`

因此旧 store 恢复这两项的目的只剩：

- 找回旧 term id / definition / notes / aliases；
- 判断研易楼明钞是否另有独立同名/相关 witness。

它们已不再是当前规则来源缺口。
