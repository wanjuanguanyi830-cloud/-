# 太乙仓库分层架构

本仓库采用“数据分层 + 稳定公共接口”的结构，目标是让后续桌面软件、Web API、移动端或其他语言实现能够通过稳定 ID 和公共 API 使用太乙数据，而不依赖内部文件名。

## 分层

| 层 | 目录 | 职责 |
| --- | --- | --- |
| 术语层 | terminology/ | 标准名、别名、定义、分类、边界、rule/source 引用 |
| 规则层 | rules/ | canonical 规则、source profiles、机器配置 |
| 运行层 | src/kintaiyi/ | 可执行算法；按来源和规则边界实现 |
| 证据层 | sources/ | 古籍原文、见证、页码、异文、OCR 修正与校勘 |
| 总注册表 | registry/ | 只保存跨层指针和软件级入口，不复制正文或算法 |
| 数据契约 | schemas/ | registry / operation / result 的 JSON 数据契约 |
| 稳定 API | kintaiyi.api | 软件唯一推荐调用面 |
| 回归测试 | tests/ | 算法、来源边界、registry、API 完整性 |

## 单一事实来源

仓库不建立第二份“全量复制总库”。每一类事实只允许一个 owner：

- 术语解释只在 terminology/ 维护；
- 规则与 source profile 只在 rules/ 维护；
- 算法只在 src/kintaiyi/ 维护；
- 文献证据只在 sources/ 维护；
- registry/ 只登记这些 owner 的稳定指针。

## 软件调用

新软件优先从 kintaiyi.api 调用 get_term / get_rule / calculate / build_pan。

需要明确来源 profile 的算法仍要求调用方显式传入，不设置跨来源默认值。

## registry

registry/catalog.json 描述各层 owner 和入口。
registry/operations.json 只登记对软件稳定开放的 calculation operation；待校、只有 source record、没有独立 runtime 的规则不得伪装为 stable operation。

## 兼容策略

当前采取 additive migration：

1. 保留现有 src/kintaiyi/* runtime；
2. 保留根目录 config.py 旧接口；
3. 新增 kintaiyi.api facade；
4. 新软件只依赖 facade 和 registry；
5. 等公开 API 稳定后，再考虑内部文件物理搬迁。

## 已锁定的跨层边界

- 5 只有地算；15/25/35 只有天+地；10/20/30/40 只有天。
- 太乙岁唯一在真实天文冬至瞬间换年。
- 古籍积年、积月、章岁、章月等属于 source profile，不替代 modern production calendar。
- 紫庭太乙九星静态 primary 与统宗 C124 动态太乙九星分层。
- C70 文昌九星不得反填紫庭 canonical。
- 同名术跨金镜、统宗、景祐、紫庭等来源时保持 source profile 隔离。

## 后续迁移原则

旧本地 terminology.json 恢复后，只向当前 stable terminology catalogs 回填旧 term id、manuscript form、页码与 notes；不得覆盖已确认 rule/source 边界。未知旧词条保持 unmapped。
