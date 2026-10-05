# C80 紫庭旧 terminology.json 恢复可用性审计

日期：2026-10-05

## 目标

C80 不重建术语库。

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

用户此前确认旧术语主库做过初步整理，因此 C80 继续承认：

`prior_local_terminology_status = preliminary_completed_locally`

只是当前没有原文件可安全迁移。

## 为什么不写 parser

旧 schema 未知。

因此不能猜：

- old term id 格式；
- 顶层是 list 还是 dict；
- alias 字段结构；
- definition / note 的嵌套方式；
- 页码字段类型；
- 一个术名是否允许多个来源记录。

C80 固定：

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
- C80：定义“目前能不能恢复”。

两者都不是新的 `terminology.json`。
