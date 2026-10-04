# C30 pan v2 最终聚合契约记录

## 目标

在 C8-C29 已完成的结构化层之上，固定 pan v2 三类结果的根区段职责：

- `analysis`：古法 canonical / 明确组合分析；
- `source_variants`：来源差异、参校、derived 卷次 profile；
- `modern`：现代派生特征。

新增：

`src/kintaiyi/pan_v2_contract.py`

## analysis 固定四槽

- patterns
- eight_divinations
- seven_methods
- military

其中：

`analysis.military`

只接 C8 等明确 canonical/组合层。

禁止放：

- 卷十五 derived military profile；
- 卷十七 derived military profile；
- 旧 flat “军事战略”。

## source_variants 固定四槽

- patterns
- military
- zitingjing
- military_derived

职责：

- patterns：统宗 / 金镜格局 profile；
- military：J4M / 统宗 / C8 upstream 的来源隔离；
- zitingjing：《太乙紫庭经》主来源 + 统宗参校；
- military_derived：卷十五 / 卷十七 derived profiles。

不同槽位不自动深合并。

## modern

当前固定：

`modern.game_theory`

必须带：

`derived_modern_feature=True`

否则拒绝。

现代博弈结果不得进入 analysis。

## legacy 禁令

analysis 内明确拒绝旧 flat 风险键，例如：

- 军事战略
- 运筹博弈分析
- 太乙九星
- 文昌九星
- 文昌变化
- 始击变化
- 三旗行宫
- 九宫贵神

这些旧键必须先经过 C12/C14/C18 的迁移与来源隔离。

## validator

新增 `validate_structured_pan_v2(...)`，在 C11 validator 之上检查：

- derived military 是否误入 analysis.military；
- modern game_theory 是否缺 derived 标记；
- source_variants 是否出现未登记根槽；
- legacy flat 是否重新进入 analysis；
- payload 是否标记当前 C30 aggregation contract。

## 结果

C30 只组装结果，不调用任何太乙公式。
