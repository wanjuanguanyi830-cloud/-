# 太乙软件调用接口

本文件面向桌面软件、Web API、移动端和其他上层应用。

原则：**应用只依赖公开 API、rule_id、operation name 和 schema；不要依赖内部 Python 文件路径。**

## 1. 版本检查

```python
from kintaiyi import registry_versions

versions = registry_versions()
# {
#   "public_api_version": "1.0",
#   "registry_schema_version": "1.0",
#   "operations_schema_version": "1.0",
#   "operations_api_version": "1.0",
#   ...
# }
```

公开 API 出现破坏性修改时必须提升主版本。内部源码重排、文献校勘、增加新规则等，只要公开契约不破坏，可保持 API 主版本不变。

## 2. 查询软件当前能力

```python
from kintaiyi import capabilities

menu = capabilities()
```

返回值按 domain 分组，可直接用于构建软件功能菜单。当前包括 modern、seven_methods、eight_divinations、cycles、doors、nine_stars 等。

## 3. 查术语

```python
from kintaiyi import get_term, search_terms

get_term("三才")
search_terms("九星")
```

术语数据唯一来源仍是 `terminology/`。API 不复制术语正文。

## 4. 查规则

```python
from kintaiyi import get_rule, describe_rule

get_rule("D8-01")
describe_rule("C67-WUFU-TONGZONG")
```

`describe_rule()` 同时返回：

- rule registry 元数据；
- exact runtime candidates；
- 对应公开 operation alias。

没有 exact runtime 的 source-record-only / attribution-pending 项也可以查询，但 runtime candidates 为空。JF4M-01..11 已不属于这一类：它们目前均有《景祐太乙福应经》独立 source-specific runtime。

## 5. 首选：按 rule_id 计算

```python
from kintaiyi import calculate_rule

sancai = calculate_rule("D8-01", 15)
wufu = calculate_rule("C67-WUFU-TONGZONG", 1)
taiyi_star = calculate_rule("C124-TONGZONG-TAIYI-NINE-STARS", 1121)
ziting_cycle = calculate_rule("C125-ZITING-TAIYI-NINE-STARS-CYCLE", 1937281)
```

当 exact rule_id 唯一对应某个 source profile，facade 可自动提供该 runtime 所需的 profile key。

例如 C67：

- `C67-WUFU-TONGZONG` → `source_profile="tongzong"`
- `C67-WUFU-JINJING` → `source_profile="jinjing"`

这只是调用适配，不合并两个来源。

## 6. Operation alias

对于面向 UI 的稳定功能名，可调用：

```python
from kintaiyi import calculate

calculate("eight.sancai", 15)
calculate("seven.lijin", 2026)
calculate("stars.taiyi.tongzong_dynamic", 1121)
```

operation name 是人类可读的软件别名；canonical 身份仍以 rule_id / source profile 为准。

## 7. Modern production

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from kintaiyi import calendar_context, build_pan

moment = datetime(2026, 12, 22, 12, 0, tzinfo=ZoneInfo("Asia/Shanghai"))

facts = calendar_context(moment)
pan = build_pan(moment, count_type="岁计")
```

现代 production 边界保持：

- 太乙岁唯一在真实天文冬至瞬间换年；
- 元旦、春节、立春、春分不换太乙岁；
- 月计使用十二节精确交节；
- 日计使用 Asia/Shanghai 民用日；
- 时计使用真实冬至/夏至半岁。

## 8. Source-specific result normalization

部分古籍 runtime 原生字段为 `source_rule_id`。通过 `calculate_rule()` 调用时，如果它与请求 rule_id 一致，facade 只做加法归一：

- 保留 `source_rule_id`；
- 增加 `rule_id`；
- 增加 `registry_normalized_rule_id=true`。

不会删除或改写来源字段。

## 9. 不可执行规则

只有 source record、来源归属待证、正文待取得的规则不得因为进入总库就变成算法。

《景祐太乙福应经》JF4M-01..11 当前已全部有独立 runtime，可按 rule_id 调用；但 JF4M-02/07/10 仍保留疑字或扫描待核字段，因此“可执行”不等于“来源文本已完全无 pending”。

对于仍无 exact runtime 的 source-record-only / attribution-pending 条目，`describe_rule()` 仍可用于显示规则和来源说明，而 `calculate_rule()` 会拒绝执行。

## 10. 错误语义

- 未登记 runtime：`KeyError`
- 一个 rule_id 出现多个不等价 runtime：`RuntimeError`
- 参数格式错误：保留具体 runtime 自身的 `TypeError` / `ValueError`
- 缺古籍证据：具体 runtime 应返回 pending / not_computable，或根本不注册 runtime；公共 facade 不替规则补造事实。

## 11. 数据契约

机器可读契约：

- `schemas/registry.schema.json`
- `schemas/operation.schema.json`
- `schemas/result.schema.json`
- `schemas/capabilities.schema.json`

应用可以把这些 schema 作为后续 TypeScript / Kotlin / Swift / Dart DTO 的生成依据。

## 12. 禁止的依赖方式

新软件不要：

- 直接硬编码 `src/kintaiyi/*.py` 文件位置；
- 从中文术名猜 runtime；
- 把同名古法自动合并；
- 从 source-record-only 记录生成计算结果；
- 用《统宗》结果补成《紫庭》canonical；
- 用旧项目兼容公式覆盖已校来源 profile。

内部目录未来可以继续整理，而上层软件只要 API v1 契约不变，就无需同步重构。


## 13. 仓库/数据状态页

应用如果需要显示“当前数据整理到什么程度”，不要把数量写死在前端。使用：

```python
from kintaiyi import repository_status

status = repository_status()
```

该结果实时由已打包索引计算，包含：

- stable catalog 数量；
- stable terminology entry 数量；
- public operation 数量和 domain；
- crosswalk audit snapshot；
- 旧 `terminology.json` 是否完成迁移；
- public API 版本。

因此后续继续增加术法或术语时，软件状态页可以自动更新。


## 14. 旧术语库恢复状态

```python
from kintaiyi import legacy_recovery_status

recovery = legacy_recovery_status()
```

该接口专门显示旧 `terminology.json`、研易楼明钞本原页和旧字段恢复是否具备条件。它不会从当前 canonical 反推旧 term id、旧定义、旧 notes、manuscript_form 或 source_page。
