# Software Registry

registry/ 是供软件调用的总注册表，不是第四份规则正文。

- catalog.json：指向 terminology / rules / runtime / sources / schemas 的稳定入口。
- operations.json：允许软件直接调用的稳定计算 operation。

总注册表只保存指针和状态，不复制术语定义、算法公式或古籍证据。真实内容仍由各自目录负责。

Python 软件优先调用 kintaiyi.api，不要直接依赖内部模块文件名。


## Source-specific rule API

对已经有唯一 runtime 的 source rule，优先调用：

`kintaiyi.api.calculate_rule(rule_id, ...)`

而不是为每个 source rule 再复制一条 operation alias。

当前《统宗》军事：

- V15-01..14：全部可按 rule_id 调用；
- V17-01..11：全部可按 rule_id 调用；
- V17-D1：可调用，但身份固定为 derived cross-volume helper；
- JF4M-01..11：仍为 source-record-only，不可计算，public API 应拒绝。

底层 source-specific runtime 可能返回 `source_rule_id`。public facade 在其与请求 rule_id 一致时，只做加法归一：

- 保留 `source_rule_id`；
- 增加 `rule_id`；
- 增加 `registry_normalized_rule_id=true`。

这不会改写底层 runtime 或 source profile，只为软件统一消费结果。
