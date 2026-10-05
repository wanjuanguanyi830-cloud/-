# C98 大游 / 大游天目旧 compatibility 回流隔离

日期：2026-10-05

## 1. 时间范围

本轮旧工作依据只使用 2026-10-04 / 2026-10-05。

主要旧工作来源：

- `codex/taiyi-base-motion-2026-10-04/rules/dayou/dayou.json`
- `codex/taiyi-base-motion-2026-10-04/rules/dayou/tianmu.json`
- `codex/taiyi-base-motion-2026-10-04/sources/base-motion-rule-record.md`

这些文件的实际提交均在 2026-10-04。

## 2. 发现的回流问题

当前 `src/kintaiyi/cycles.py` 仍有旧兼容函数：

- `bigyo()`
- `bigyo_tianmu()`

其中：

`bigyo(profile="jinjing_tongzong")`

把：

- 金镜宫序；
- 统宗 +34 宫盈差；

压进单一 profile。

这违反“来源异文不乱合”。

而 2026-10-04 的基础运行记录已经明确：

> 旧 config.bigyo() 只作实现参照，不以其逻辑覆盖本规则。

## 3. 大游天目问题更明确

2026-10-04 `tianmu.json` 已经记录：

- 金镜当前采用推法摘要：72 → 18；
- 起未·天道；
- 顺行十六神；
- 大武、阴德各重留一算；
- 18步路径。

同一记录又明确把旧：

- `%180`
- `+214`

逻辑列为：

`deprecated_reference`

因此当前 legacy wrapper 的默认：

`bigyo_tianmu(profile="tongzong")`

不能继续带 canonical 身份。

## 4. C98 处理原则

C98 不尝试凭旧兼容代码重建新的大游真公式。

只做治理：

> 数值兼容可保留；canonical 身份必须撤销。

### bigyo

旧数值算法继续跑，但输出：

- `canonical=None`
- `canonical_equivalent=False`
- `promotion_allowed=False`

默认混合 profile：

`jinjing_tongzong`

额外：

`quarantined=True`

淘金歌 profile：

- 历元缺失时继续不可算；
- 显式给 epoch_offset 只算兼容试值；
- 仍不升格 canonical。

### bigyo_tianmu

默认旧 +214 profile：

- `quarantined=True`
- `canonical=None`

金镜 profile：

- 无 epoch_offset 时继续不可算；
- 显式 epoch_offset 后可沿旧18步路径做兼容试算；
- 仍不等于“完整来源历元接口已恢复”。

## 5. C60 新增隔离

新增：

- `kintaiyi.cycles.bigyo.jinjing_tongzong`
- `config.bigyo_default`
- `kintaiyi.cycles.bigyo_tianmu.tongzong`
- `config.bigyo_tianmu_default`

它们统一：

- `promotion_allowed=False`
- `canonical_equivalent=False`

当前 replacement 不指向猜测的新 runtime。

原因：

大游 / 大游天目的 source-specific 位置 runtime 尚需独立重接。

## 6. 与 C41 / C47 的边界

C41 处理的是：

- 大游内外重卦；
- 策数；
- 动爻；
- 并明确不自动选择 epoch variant。

C47 处理的是：

- 小游轨运 / 重卦。

C98 不把 `cycles.bigyo()` 偷换成 C41，因为：

- “大游太乙行宫位置”
- “大游重卦结构”

不是同一层。

## 7. 结果

C98 的目的不是增加公式数量，而是减少“看起来能算所以像真源”的旧入口。

统一真源原则保持：

- 金镜与统宗不乱合；
- deprecated reference 不升级；
- 缺 source-specific runtime 时明确 pending，而不是借 legacy compatibility 顶上。


## 8. C106 直接来源复核后的修正

C98 对“大游天目”的隔离结论属于**阶段性治理结论**，现已被 C106 的直接来源复核部分推翻。

后续直接核得：

- 《太乙金镜式经》：天目元法72、周法18、起天道、顺十六神、大武/阴德重留；
- 《太乙统宗宝鉴》：神盈差214、大周180、小周18、顺十六宫、大武/阴德重留；
- 《易学象数论》平行条又明确“余起天道”，支持统宗电子转录中起点 OCR 的正规化。

因此：

- `bigyo_tianmu(profile="tongzong")` 不再是错误公式隔离项；
- `bigyo_tianmu(profile="jinjing")` 也不再是“缺完整来源接口”的旧试算；
- 两者都由 C106 source-specific runtime 承担；
- legacy 0基 API 只作为 C106 的输入/输出适配层。

C60 已撤销：

- `kintaiyi.cycles.bigyo_tianmu.tongzong`
- `config.bigyo_tianmu_default`

两项 quarantine。

C98 仍然有效的隔离只剩：

- `bigyo(profile="jinjing_tongzong")`
- `config.bigyo_default`

因为大游太乙行宫本身仍把金镜宫序与统宗 +34 混为一个旧 profile，尚未完成 source-specific 重接。
