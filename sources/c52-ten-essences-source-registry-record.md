# C52 太乙十精来源注册表

## 1. 目标

C52 只锁定：

- 十精完整名单与次序；
- 各项小周数；
- 卷十八 / 卷二十见证编次差异；
- 旧 `config.py` / `yunqi.py` 的名称与周期冲突。

C52 本身**不执行十精位置公式**，也不迁十精云气断事；已校公式由后续 C53 runtime 消费。

canonical：

`src/kintaiyi/ten_essences_source_registry.py`

## 2. 直接来源与参校

### 《太乙统宗宝鉴》

不同见证将“十精太乙所主 / 十精太乙云气所主”编在卷十八或卷二十。

因此固定：

- `witness_volumes=[18,20]`
- `volume_status="witness_volume_variant"`

不能因卷次差异复制两套算法。

### 《武经总要》

独立早期参校可核十精完整次序及小周：

1. 天皇 20
2. 帝符 20
3. 天时 12
4. 太尊 4
5. 飞鸟 9
6. 五行 5
7. 八风 9
8. 五风 9
9. 三风 9
10. 太乙数 72

### 《太白兵备统宗宝鉴》

继续作为阴阳起宫、顺逆、宫序的重要参校。

## 3. canonical 十精名单

固定：

- 天皇
- 帝符
- 天时
- 太尊
- 飞鸟
- 五行
- 八风
- 五风
- 三风
- 太乙数

### 旧“地符”

旧 `yunqi._TEN_JING_FN` 把第二项写成“地符”。

直接正文为：

`帝符`

因此：

- 地符不是 canonical 名；
- 仅允许显式 compatibility mode 映射为帝符。

### 旧“太岁”

旧 `_TEN_JING_FN` 把第十项写成太岁。

直接十精第十项为：

`太乙数`

因此太岁不属于 canonical 十精名单。

## 4. 小周数

固定：

```
天皇 20
帝符 20
天时 12
太尊 4
飞鸟 9
五行 5
八风 9
五风 9
三风 9
太乙数 72
```

这些数只用于 C52 来源审计，不等于位置 runtime 已完成。

## 5. 旧位置公式审计

### 飞鸟

旧：

`config.flybird`

核心按：

`accumulated_year % 8`

直接正文 / 武经总要均见：

`小周九`

因此：

- legacy_cycle = 8
- direct_small_cycle = 9
- cycle_matches = False
- runtime_ready = False

不得把旧飞鸟宫位直接迁为 canonical 十精飞鸟。

同时必须继续区分：

- 十精飞鸟：推步神位；
- J4M-11 飞鸟：真实外部飞鸟观测。

两者不可互相替代。

### 五风

旧：

`config.fivewind`

外层使用：

`%29`

直接正文见：

`大周90 / 小周9`

因此：

- legacy_cycle = 29
- direct_small_cycle = 9
- cycle_matches = False
- runtime_ready = False

### 其他周期相合项

天皇、帝符、天时、太尊、五行、八风、三风的旧周期与直接小周表面相合，
但：

`cycle_matches=True`

不等于：

`runtime_ready=True`

仍须逐项核：

- 阴阳起宫；
- 顺逆；
- 重留；
- 九宫 / 十六神路径；
- 余0边界；
- 岁月日时法；
- 被正文明确否定的“宫盈差”。

## 6. 十精云气层

“十精太乙云气所主”包含：

- 与太乙同宫；
- 阴 / 阳宫；
- 旺相休囚；
- 天气厚薄；
- 云气颜色；
- 日月晕昏；
- 风雨雾旱等。

C52 固定：

`cloud_omen_boundary.status="separate_source_unit"`

`runtime_in_c52=False`

不得在名称/周期注册阶段顺便迁天气断语。

## 7. v2 边界

C52 只建议未来目标：

`source_variants.ten_essences`

但本批：

- 不扩展 `SOURCE_VARIANT_KEYS`；
- 不生成 legacy replacement；
- 不把旧顶层升格；
- 不使用 `cycles` root。

## 8. C15 目录更新

旧字段：

- 帝符
- 太尊
- 飛鳥
- 三風
- 五風
- 八風

由：

`pending / cycle_or_ten-essences_source_pending`

改为：

`canonical source registry confirmed / formula pending`

action：

`use_c52_source_registry_formula_pending`

仍固定：

`migrate_whole=False`

## 9. 后续

C53 开始逐项核十精位置公式。

优先：

1. 飞鸟：旧 %8 与直接小周9冲突；
2. 五风：旧 %29 与直接小周9冲突；
3. 帝符：名称/重留结构；
4. 太尊；
5. 八风；
6. 三风。

只有直接公式、边界和测试全部完成后，才可建立位置 runtime。


## 10. 后续 runtime 状态

C52 仍是来源注册表，不自己执行公式。

当前位置 runtime：

- C53：飞鸟、五风、太尊、八风、三风、五行；
- C55：天皇、帝符；
- pending：天时。

数值 runtime：

- C54：太乙数。

固定：

- `implemented_position_runtimes = 8项`
- `pending_position_runtimes = ["天时"]`
- `implemented_number_runtimes = ["太乙数"]`
- `all_position_runtime_ready=False`

天时继续保留来源冲突：

- 统宗：吕申（寅）起，顺行十二辰，阴局取阳局对冲；
- 太白兵备：阳起申、阴起寅。

因此仍为 `source_start_conflict_unresolved`。

帝符唯一 canonical 已转入 C55；并行期间短暂出现的 C53-DIFU 已删除。
