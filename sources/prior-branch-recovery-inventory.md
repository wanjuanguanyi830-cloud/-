# 既有旧分支工作恢复清单

日期：2026-10-05

## 目的


在继续新增太乙规则前，先清点已经做过但未进入当前 `main` 的工作，避免重复实现。

本记录只说明“旧工作在哪里、当前如何处理”，不把旧分支内容自动提升为现行 canonical。

## 0. 时间范围硬边界

用户当前要求：

> 仅采用最近两天的工作内容。

以当前项目日期 2026-10-05 计，本恢复清单只允许采用：

- 2026-10-04；
- 2026-10-05。

执行规则：

1. 不能只看“分支现在还在”；具体要恢复的文件必须能追到 2026-10-04 / 2026-10-05 的提交。
2. 更早提交即使被后续分支包含，也不作为恢复依据。
3. 如果同一文件横跨更早历史，只采用最近两天提交实际写入 / 修改的内容；无法分离则不恢复。
4. 当前已核：
   - `four_taiyi.py`：2026-10-04T19:52:53Z；
   - `taiyi_cycles.py`：2026-10-04T19:52:22Z；
   - `taiyi_common.py`：2026-10-04 多次 C1/C2/C3/C7 提交；
   - `kintaiyi.py`：2026-10-04 C6/C7/兼容测试提交；
   - `palace_coordinates.json`：2026-10-04T03:19:43Z；
   - `sixteen_spirits.json`：2026-10-04T03:19:43Z。
5. 因此本轮已恢复的两份 terminology 坐标资产和 C92 所参考的旧 `four_taiyi.py` 均符合时间窗口。

## 1. codex/c1-c7-canonical

分支头：

`cac670c026f98651431c7924ed5f3e10139ffcaf`

### 当前 main 缺失但旧分支存在

- `src/kintaiyi/taiyi_common.py`
- `src/kintaiyi/taiyi_cycles.py`
- `src/kintaiyi/four_taiyi.py`
- `src/kintaiyi/kintaiyi.py`
- `tests/test_taiyi_common.py`
- `tests/test_taiyi_cycles.py`
- `tests/test_four_taiyi.py`
- `tests/test_pan_v2.py`
- `tests/test_legacy_compat.py`
- `tests/test_eight_divinations.py`
- `tests/test_seven_methods.py`
- `docs/pan_v2_schema.md`
- `tests/reports/c1_c7_validation.md`

该分支自己的验证记录曾达到：

`442 passed`

并明确覆盖：

- 十六辰 / 十六神；
- 九宫元数据；
- 大神加位；
- 五行五态；
- 八占；
- 七术；
- 三基；
- 五福；
- 大小游；
- 四太乙十二宫；
- pan v2；
- legacy compatibility。

### 当前处理

#### taiyi_common.py

大部分基础常量 / 五行关系已进入现行：

`src/kintaiyi/taiyi_rules.py`

旧文件不整包恢复，以免形成两个公共真源。

仍可选择性回收：

- 十六辰 -> 九宫反向映射；
- sector detail；
- 九宫 / 十六辰对冲 helper；
- qi_relation 的结构化包装。

#### taiyi_cycles.py

不能直接恢复。

原因是其中部分旧 project canonical 已被后续来源校勘取代：

- 三基 -> C66；
- 五福位置 -> C67；
- 五福吉算 -> C68；
- 三基/五福关系 -> C74；
- 大游/小游已经由现行 cycles + 后续 source-specific 层继续校勘。

特别是旧文件中的“五福 +250 project canonical”不能重新进入现行 canonical。

旧测试只可作为历史行为线索逐项迁移。

#### four_taiyi.py

不能直接恢复，但非常重要。

旧分支已做：

- 12 运行宫；
- 天乙 / 地乙 / 直符 / 四神；
- 每宫3年；
- 三元起宫；
- 6组同宫 pair；
- 五福同域；
- 四神水特殊条；
- 直符部分旺衰表。

现行 main 已有：

- C64：天乙 / 地乙 / 直符位置；
- C65：三神与其他神同宫；
- C90/C91：三基相关关系。

但“旧 four_taiyi.py 中的四神位置 / 三元完整 facade / 部分特殊条”不能视为已全部迁移。

因此该文件标记：

`partial_recovery_candidate_needs_source_reaudit`

#### kintaiyi.py

旧分支存在：

- `TaiyiCanonicalMixin`
- snapshot `Taiyi` facade
- `project_legacy_pan`
- `collect_core_snapshot`

当前 main 没有 `src/kintaiyi/kintaiyi.py`。

不能原样恢复，因为它依赖旧 `taiyi_cycles.py` / `four_taiyi.py`。

应后续重新接：

- C66 / C67 / C68；
- C64 / C65；
- C74 / C90 / C91；
- 当前 pan_v2 contract。

这是“接口恢复”，不是重写算法。

## 2. codex/taiyi-base-motion-2026-10-04

分支头：

`7f2d1b5dc74ea8dbb0363ee0ebc479de9cb09b08`

旧分支独有：

- `rules/base_motion/three_bases.json`
- `rules/base_motion/five_blessings.json`
- `rules/base_motion/four_taiyi.json`
- `rules/dayou/dayou.json`
- `rules/dayou/tianmu.json`
- `rules/xiaoyou/xiaoyou.json`
- `rules/xiaoyou/orbit_into_gua.json`
- `terminology/palace_coordinates.json`
- `terminology/sixteen_spirits.json`
- `sources/base-motion-rule-record.md`
- `tests/test_base_motion_rules.py`

### 已恢复到 main

本轮已恢复并与当前 runtime 交叉校验：

- `terminology/palace_coordinates.json`
- `terminology/sixteen_spirits.json`

两者现状态：

`terminology_reference_not_formula_source`

即：

- 保留此前工作成果；
- 不拿旧 JSON 反压当前 source-specific 公式。

### 暂不直接恢复

旧 base-motion JSON 中有后来已被推翻 / 分 profile 的 canonical 选择，例如：

- 三基旧“项目 formula”没有完整反映 C66 的邦盈差层；
- 五福旧文件把无盈差225公式当单一 canonical；
- 旧资料层对 +250 / +115 的历史处理与当前 C67 不同。

因此这些文件先作为旧分支证据，不复制到现行 `rules/` canonical。

## 3. codex/taiyi-rules-v2-20261005

分支头：

`db7e1d7e261a9ba2939b84420bac8553e396f6c8`

旧分支独有：

- `docs/pan_v2.md`
- `sources/source_variants.md`
- `tests/test_taiyi_v2_mandatory.py`

### 处理

`sources/source_variants.md` 很有价值，但它保存的是当时阶段性 canonical，其中仍有：

- 三基 project +250；
- 五福 project +250；
- 大游 / 小游阶段性选择。

后续 C60+ 已继续校勘这些内容，所以不能整页重新当现行真源。

应逐段吸收“来源边界原则”，不恢复旧结果值。

## 4. integrate-taiyi-war-v1-20261004

分支头：

`412da1ef4bdd04512a68df4523d2f7888c4c2806`

旧分支独有：

- `rules/common/taiyi_space.py`
- `rules/warfare_v1/eight_divinations.py`
- `rules/warfare_v1/seven_tactics.py`
- 对应历史例与 source variant 记录。

### 处理

`taiyi_space.py` 的：

- 十六环；
- 位置 -> 九宫；
- 九宫五行；
- 大神加位；
- 火十二长生；

已经大部分被现行 `taiyi_rules.py` / `eight_divinations.py` / `seven_methods.py` 吸收。

因此旧 warfare_v1 不再整包合入。

旧 historical fixtures 仍可用于补回归，但必须对照当前 D8/T7 来源边界逐例迁移。

## 5. 当前仍找不到的旧本地文件

### terminology.json

已检查：

- 当前 main 树；
- 常见路径 Git 历史；
- ChatGPT Library 当前可检索文件。

仍未取得旧本地 `terminology.json` 原文件 / schema。

该项由：

- C40 migration map；
- C81 recovery availability audit；

继续锁定为：

`blocked_missing_original_store`

注意：

旧分支里找到了术语坐标 JSON，不等于找回完整 `terminology.json`。

## 6. 后续执行顺序

以后新增/重写前先查旧分支。

优先恢复：

1. 纯术语 / 坐标资料；
2. 不含旧错误公式的测试意图；
3. pan v2 / legacy facade 的接口结构；
4. 四神 / 四太乙旧实现中仍未迁入 main 的部分。

禁止直接恢复：

1. 已被后续来源校勘推翻的旧 canonical；
2. +250 / +115 等已重新分 source profile 的公式；
3. 旧分支里“看起来可用”但来源状态已变化的组合断语。

原则：

> 旧工作优先复用；旧结论仍须服从后来的来源校勘。


## 7. 2026-10-05 回收进度

本节只记录 2026-10-04 / 2026-10-05 工作的回收状态。

### 已安全恢复

#### terminology 坐标资产

- `terminology/palace_coordinates.json`
  - 来源：2026-10-04 `codex/taiyi-base-motion-2026-10-04`
  - 状态：recovered_prior_work_crosschecked
- `terminology/sixteen_spirits.json`
  - 来源：2026-10-04 同分支
  - 状态：recovered_prior_work_crosschecked
- `terminology/wufu_domains.json`
  - 来源：2026-10-04 `taiyi_cycles.py`
  - 状态：coordinate_reference_not_relation_formula

#### C92

从 2026-10-04 `four_taiyi.py` 回收并按直接来源重核：

- 四神 360 / 36；
- 三年一宫；
- 一宫起；
- 十二运行宫；
- 四神克贼 / 战克明列组合。

不恢复旧 yuan 三元默认表。

#### C93

从 2026-10-04 `zhifu_known_state()` 回收：

- 二宫火旺；
- 三宫火长生；
- 四宫火败。

其他宫继续 source_pending。

#### C94

从 2026-10-04：

- `FIVE_MEETING_EFFECTS`
- `FIVE_DOMAINS`
- `PALACE_DOMAINS`

回收五福 × 四太乙金土火水灾应解释。

现行收紧：

- 必须显式 `interpretation_profile`；
- 必须显式 `same_wufu_domain`；
- 不再自动读取坐标或位置生成关系。

#### C95

从 2026-10-04 `kintaiyi.py` 回收：

- `collect_core_snapshot()` 的 collector 设计；
- 当前 style / 年 style / 日 style 明确分取；
- primitive 单次调用；
- selection validation 意图。

未恢复：

- 旧 `TaiyiCanonicalMixin`；
- 旧 `Taiyi(snapshot).pan()`；
- 旧 `project_legacy_pan()`。

### 已由现行模块覆盖，不再重复恢复

10月4日 `test_pan_v2.py` 中以下意图已有现行覆盖：

- pan v2 根结构 / JSON-safe → C11；
- 中五 sector=null → C11 / C30；
- scenario 必须显式 → C11；
- modern game theory 必须 derived → C30；
- legacy 军事 / 七术 / modern 不自动提升 → C12；
- 年积年不得借月日时积年 → C95；
- 日太乙必须明确取 day style → C95；
- primitive 单次采集 → C95。

因此旧 `tests/test_pan_v2.py` 不整文件恢复。

10月4日 `tests/test_legacy_compat.py` 中：

- legacy flat quarantine → C12 / C60；
- JSON key collision → C12；
- 七术 / 八占 canonical delegate → 现行 T7 / D8 tests；
- 旧周期 facade 等价测试因公式后来 source-specific 化，不再原样恢复。

### 已明确淘汰 / 不直接恢复

- 旧 `taiyi_cycles.py` 中五福 `project_canonical=+250`；
- 旧 `four_taiyi.py` yuan 默认旋转公式；
- 旧 `TaiyiCanonicalMixin` 对上述旧周期的直接委托；
- 旧 `project_legacy_pan` 覆盖 canonical flat 值的做法；
- 旧 `docs/pan_v2_schema.md` 中已经被后续 C30/C67/C68 等改写的周期说明。

这些内容保留在 2026-10-04 分支历史中作为过程证据，不重新写入现行 canonical。


## 8. C96 / C97 后续回收治理

### C96

从 2026-10-04 `taiyi_common.py` 仅回收当前仍缺失的纯 helper，并直接并入唯一公共真源：

`src/kintaiyi/taiyi_rules.py`

包括：

- 十六辰→九宫；
- 十六环通用旋转 / 对冲；
- 九宫代表点 / 对冲；
- sector detail；
- qi_relation 包装；
- general_palace_qi。

旧 `GENERAL_ELEMENTS / ROLE_ELEMENTS` 未恢复：

- 当前没有独立来源层复核；
- 不是本轮必须的纯坐标事实；
- 不因旧代码存在就自动升格。

### C97

通过对 2026-10-04 `taiyi_cycles.py` 与当前 main 比较，发现当前主线 `cycles.py` 仍保留旧五福：

`project +250`

且旧返回曾标为 canonical。

C97 处理：

- 旧 project +250 数值兼容仍保留；
- `canonical=None`
- `quarantined=True`
- `promotion_allowed=False`
- 正确来源改由 C67 显式 profile；
- 吉算改委托 C68。

C60 新增隔离：

- `kintaiyi.cycles.wufu.project`
- `config.wufu_default`

因此“最近两天旧工作回收”不仅是找回遗漏，也用于发现当前 main 仍残留的阶段性旧公式并阻止回流。


### C98

对 2026-10-04 `rules/dayou/dayou.json` / `rules/dayou/tianmu.json` 与当前 `cycles.py` 对比后，确认当前 legacy compatibility 仍有两处容易回流成“真源”的入口。

处理：

- `bigyo(profile="jinjing_tongzong")`
  - 金镜 / 统宗混源；
  - 保留数值兼容；
  - 撤销 canonical；
  - 默认路径 quarantine。
- `bigyo_tianmu(profile="tongzong")`
  - 旧 %180/+214 已被 2026-10-04 记录标为 deprecated_reference；
  - 保留旧 API；
  - 撤销 canonical；
  - 默认路径 quarantine。

新增 C60 登记：

- `kintaiyi.cycles.bigyo.jinjing_tongzong`
- `config.bigyo_default`
- `kintaiyi.cycles.bigyo_tianmu.tongzong`
- `config.bigyo_tianmu_default`

这一步属于“旧工作回收时发现主线旧公式回流口并隔离”，不是把旧大游公式重新升格。
