# C15 unported legacy 字段分层目录记录

## 背景

参考 `Taiyi.pan()` 当前主盘有 108 个顶层字段。

与 C14 `legacy_schema.py` 对照后：

- 已迁移 / 已隔离：41 个
- 仍为 unported：67 个

C15 对这 67 个字段全部建立迁移元数据，不只列示例。

新增：

- `src/kintaiyi/unported_catalog.py`
- `catalog_unported_field(...)`
- `prioritize_unported_fields(...)`
- `unported_catalog_report(...)`

并让 C14 manifest 与 C13 audit 消费该目录。

## 四层定义

### canonical

来源相对明确，可作为古法结构化候选，但仍须保留 source record。

典型：

- 十六宫分布：统宗卷二
- 太乙九星 / 文昌九星：**《紫庭经》主来源，统宗卷六参校**
- 文昌变化 / 始击变化：**《紫庭经》主来源，统宗卷六参校**
- 三旗行宫 / 九宫贵神：**《紫庭经》主来源，统宗卷十参校**
- 厄会行限 / 国政章易 / 岁中灾发：统宗卷九

这里的“参校”是版本校异、补证、对读用途；不能把统宗参校来源反过来标为主要出处。

### source_variant

不能选一个来源静默覆盖其他来源。

典型：

- 推三门具不具 / 推五将发不发 / 推主客相关法：
  J4M《金镜》卷四与统宗/C8需拆 profile
- 释格局：
  统宗卷四与当前金镜格局层拆 profile
- 五运六气 / 五音之数：
  参考pan自身即标卷三/卷十
- 金函玉镜、二十八宿辅助层：
  独立 source profile，不并入太乙核心 canonical

### derived

旧实现的综合包装或现代派生，不得把整个返回 dict 标作古籍 canonical。

典型：

- 卷八 / 九 / 十 / 十一 / 十二 / 十三 / 十四 / 十八
- 军事应用（卷十五）
- 军事占断（卷十七）
- 神将所主（卷二/七综合）
- 卷一朓胸流水线中的 Meeus 现代天文桥接
- 八宫旺衰节气环境投影

### pending

来源或输入模型尚不足，禁止猜。

典型：

- 帝符 / 太尊 / 飞鸟 / 三风 / 五风 / 八风
- 推太乙当时法
- 天子巡狩、君臣民基所主等旧顶层断语
- 推太乙风云飞鸟助战法：J4M-11 需要显式外部风云飞鸟观测

## 优先级

- P0：核心盘面或高风险来源边界
- P1：来源较明确的独立规则 / 高风险军事层
- P2：辅助体系、跨卷或仍需补来源校勘
- P3：综合包装器或现代派生，不应整体迁移

当前重点 P0 包括：

- 天乙 / 地乙 / 四神 / 直符 / 合神 / 计神结构事实
- 十六宫分布
- 推三门具不具
- 推五将发不发
- 推主客相关法
- 释格局

## 整体迁移禁令

以下类型固定 `migrate_whole=False`：

- 旧“卷X”综合包装器
- 卷十五军事应用
- 卷十七军事占断
- 跨卷综合项
- 现代天文桥接
- 已知 source_variant 冲突项

这些内容只能拆成独立规则或独立 source profile 后再进入 v2。

## 与 C13/C14 的连接

C14 的 `status="unported"` 不变，但现在额外返回：

- candidate_layer
- priority
- source_scope
- migration_action
- migrate_whole

C13 现在额外输出：

- unported_layer_counts
- unported_priority_counts
- next_migration_candidates

因此后续可直接根据真实盘样本频率和 C15 priority 决定迁移顺序。
