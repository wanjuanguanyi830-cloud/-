# C32 V17-D1 孤虚跨卷 helper 审计记录

## 定位

V17-D1 不是卷十七 canonical source rule。

它只是：

- D8-05 / 卷五“内外占攻击”
- V17-09 / 卷十七“求索所得”

之间的跨卷对照。

新增：

`src/kintaiyi/cross_volume_helpers.py`

## 输入约束

`build_guxu_cross_volume_helper(...)` 只接受：

- `attack_result.rule_id == "D8-05"`
- `request_result.source_rule_id == "V17-09"`

不接受其他规则冒充。

## 禁止重算

C32 不：

- 重算天目内外；
- 重跑 V17-09；
- 解析旧中文断语；
- 从格局字符串提取孤虚；
- 改写 D8-05；
- 改写 V17-09。

V17-09 为此回显自己的结构化 `inputs.skyeyes_realm`，让 helper 能检查两边输入是否一致。

## 输出

固定：

- `source_rule_id="V17-D1"`
- `source_status="derived_cross_volume_helper"`
- `canonical_source_rule=False`
- `cross_volume=True`

对照状态：

- `base_aligned`
- `request_modified_by_other_conditions`
- `request_direction_changed_by_other_conditions`
- `input_conflict`
- `undetermined`

## canonical 边界

`c32_catalog()` 固定：

`canonical_source_rule_count = 0`

V17-D1 永不进入 V17-01..11 canonical source rule 集。
