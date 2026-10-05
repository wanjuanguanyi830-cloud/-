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

C68 后新增独立古籍 profile：

- `jingyou_fuying_volume4`
- 规则集：`jingyou-fuying-v4-military-11`
- 编号：`JF4M-01..JF4M-11`

P0 三项现在可并列保存：

- 三门：J4M-01 / JF4M-01 / 统宗 / C8 upstream
- 五将：J4M-02 / JF4M-02 / 统宗 / C8 upstream
- 主客相关：J4M-03 / JF4M-03 / 统宗

但 `canonical_selected=None`、`cross_source_merge=False` 仍不变。

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
- 不把统宗卷四格局覆盖金镜格局；
- 不把《景祐太乙福应经》JF4M 的古本异文自动补入 J4M；
- 不因两个古籍 profile 主题同名就把字段拼成“最佳版本”。


## 7. C68 后的《福应经》独立 profile

《景祐太乙福应经》卷四现已从 J4M 内嵌异文提升为独立规则集：

- `rules/jingyou_fuying_v4_military.json`
- source profile：`jingyou_fuying_volume4`
- rule ids：`JF4M-01..JF4M-11`

`src/kintaiyi/source_profiles.py` 的 `MILITARY_PROFILE_KEYS` 已允许该 profile。

重要：允许“并列保存”不等于允许“合并计算”。C17 的原始设计原则继续有效：

- 不自动选 canonical；
- 不跨来源补字段；
- C8 不成为古籍公式替代；
- JF4M 当前是 source_record_only，不能借 J4M runtime 伪装成已实现。


## 8. 格局术语目录接线

现已新增：

`terminology/patterns.json`

它只做 source-profile 术语登记，不改变 C17 的来源隔离原则。

已固定：

- `jinjing_geju` 的 13 个格局术语与 `rules/jinjing/geju/ruleset.json` 对齐；
- 主体卷三：掩、击、迫、囚、关、格、对、提挟、挟闭、四郭固、四郭杜；
- 卷四值事门：执提、提格；
- `四郭社` 仅为 `四郭杜` 的来源异文；
- `tongzong_volume4` 继续只作为并列 profile；
- `canonical_selected=None`；
- `cross_source_merge=False`；
- 格局坐标继续引用 `terminology/common-core.json`，不复制第二套九宫/十六辰定义。

因此“术语统一”只统一名称、字段和来源归属，不等于合并金镜与统宗的格局判断。


## 9. 军事 P0 术语目录接线

新增 `terminology/military-p0.json`，将 C17 三项 source-sensitive 术语与 crosswalk 固定关联：

- three_doors: J4M-01 / JF4M-01；
- five_generals: J4M-02 / JF4M-02；
- host_guest_relation: J4M-03 / JF4M-03。

术语层同步 C17 的强制边界：

- 三门、五将允许登记 `c8_upstream`，但仅表示 C8-L2 的消费/归一化角色；
- 主客相关法禁止登记 `c8_upstream` 为替代 profile；
- C8-L3 主客动静不是 J4M-03/JF4M-03；
- `CORE-WUJIANG-READY` 仅为跨层整合规则，不属于古籍 source rule；
- 所有 profile 继续 `canonical_selected=None`、`cross_source_merge=False`。
