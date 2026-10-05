# C97 五福旧 compatibility 回流隔离与 C67/C68 委托

日期：2026-10-05

## 1. 问题

在回收 2026-10-04 旧工作时发现，当前 `main` 仍有：

`src/kintaiyi/cycles.py`

并由：

`config.py`

直接导出：

`wufu`

旧默认：

`profile="project"`

固定：

`offset=250`

且旧返回曾带：

`canonical="taiyi-t7-d8-v1"`

这与后续 C67 已核来源冲突。

C67 当前明确分开：

- 统宗：宫盈差115，大周2250，小周225；
- 金镜：无该115盈差，225年一周。

后期 +250 只能作为未选择 source variant / 历史项目兼容，不能继续标 canonical。

## 2. C97 处理

不删除旧 API。

原因：

- `config.py` 仍作为 legacy compatibility 入口；
- 外部旧调用可能依赖 `wufu(0)` 等0基输入。

因此 C97 采取：

> API兼容保留，错误 canonical 身份撤销。

## 3. project +250

调用：

`wufu(year)`

或：

`wufu(year, profile="project")`

仍返回旧数值行为，但必须带：

- `canonical=None`
- `canonical_equivalent=False`
- `quarantined=True`
- `promotion_allowed=False`
- replacement:
  - C67-WUFU-TONGZONG
  - C67-WUFU-JINJING

rule id：

`LEGACY-WUFU-PROJECT-250`

因此旧结果可以用于兼容显示 / 回归，但不能进入新 canonical 调用链。

## 4. source_115 改为真正委托 C67

旧 API 是 0 基 accumulated_year。

C67 是 1 基 accumulated_count。

适配固定：

`count = accumulated_year + 1`

然后调用：

`wufu_position(count, source_profile="tongzong")`

返回的：

- 宫位；
- 入宫年；
- 盈差；

均来自 C67。

旧 `realm=理天/理地/理人` 只保留为：

`legacy_compatibility_derived`

不反写为 C67 来源事实。

## 5. 新增 jinjing compatibility profile

旧 compatibility API 现在允许显式：

`wufu(year, profile="jinjing")`

同样：

`count = year + 1`

再委托：

`C67-WUFU-JINJING`

不再用 project +250 假装统一五福公式。

## 6. 五福吉算改委托 C68

旧：

`wufu_gb(year_in_palace)`

原先只按个位索引旧 `NUMBER_SUBJECTS`。

C97 改为：

`C68-WUFU-AUSPICIOUS-NUMBER`

所以：

- 2 → 公侯；
- 5 → 民；

采用 C68 当前直接见证正规化标签。

大游凶算 `dayou_xiong` 保持独立旧兼容标签，不受这次修改。

## 7. C60 quarantine

新增：

- `kintaiyi.cycles.wufu.project`
- `config.wufu_default`

两者都：

- `promotion_allowed=False`
- `canonical_equivalent=False`

replacement 指向 C67 两个显式来源 profile。

## 8. 时间窗口

C97 是 2026-10-05 当前治理工作。

它处理的是当前 main 中仍存的旧回流口，不借用两天以前的旧工作内容。

此次发现路径来自对 2026-10-04 `taiyi_cycles.py` 与当前 main 的对比，符合用户“仅采用最近两天工作内容”的限制。
