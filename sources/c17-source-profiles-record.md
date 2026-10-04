# C17 P0 来源隔离记录：格局、三门、五将、主客相关

## 目标

C15 将以下旧 flat 字段标为高风险 source_variant P0：

- 释格局
- 推三门具不具
- 推五将发不发
- 推主客相关法

C17 不尝试选“唯一正确版本”，而是建立 source-profile 容器，并把旧 flat 值降级为 quarantined。

新增：

- `src/kintaiyi/source_profiles.py`
- `build_pattern_source_variants(...)`
- `build_military_p0_source_variants(...)`
- `build_p0_source_variants(...)`

## 1. 格局 profile

保存：

- `tongzong_volume4`
- `jinjing_geju`

`jinjing_geju` 不是简单“金镜卷四”：

- 目标仓库金镜格局引擎主体来源标《太乙金镜式经》卷三；
- 值事开/生门相关规则另引用卷四。

因此 profile 名使用 `jinjing_geju`，避免错误卷次归并。

容器固定：

- `canonical_selected=None`
- `cross_source_merge=False`

## 2. 三门 / 五将

分别对应：

- J4M-01 推三门具不具
- J4M-02 推五将发不发

C8-L2 只“消费上游事实并归一化”，不是 J4M-01/02 的公式实现。

所以 C17 crosswalk 固定：

`c8_equivalent_formula=False`

允许把 C8 结果登记为 `c8_upstream` profile，只用于说明它的真实角色，不能冒充金镜公式。

## 3. 主客相关法

对应 J4M-03。

C8-L3 是“主客动静/先后”层，只是邻近主题，不是 J4M-03 直接替代。

因此：

- `host_guest_relation` 不允许登记 `c8_upstream` 为替代 profile；
- 强行登记会 ValueError；
- 不得把 J4M-03 与 C8-L3 合并。

## 4. C14 quarantine replacement

旧 flat 字段现在改为：

- 释格局 → `source_variants.patterns.profiles`
- 推三门具不具 → `source_variants.military.three_doors.profiles`
- 推五将发不发 → `source_variants.military.five_generals.profiles`
- 推主客相关法 → `source_variants.military.host_guest_relation.profiles`

只有对应 `profiles` 真正非空时，C13 才认为 replacement gap 已补。

仅创建空容器不能通过审计。

## 5. 与 J4M 当前实现状态解耦

C17 source-profile 架构不依赖某条 J4M 当前是 implemented/partial/pending。

当前仓库 J4M 状态变化时，只需要把真实结构化结果写入对应 profile；
不需要修改来源隔离规则。

## 6. 禁止事项

- 不自动选择 canonical profile；
- 不把不同来源事件去重后当成一个结果；
- 不从旧 prose 断语构造 profile；
- 不把 C8 组合层冒充金镜原法；
- 不把统宗卷四格局覆盖金镜格局。
