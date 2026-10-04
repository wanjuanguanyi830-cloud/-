# C49 太游 / 小游行宫卦不同术

## 直接来源

《太乙统宗宝鉴》卷十：

- 明太、小游行宫卦不同术

识典：
https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppwz3ep1yr

## 1. 本术不是布尔“不相等”

原文说明：

- 太游：36年行一内卦，取“乾天之策”之义；
- 小游：24年行一内卦，取“坤地之策”之义；
- 二者有尊卑上下之别。

但原文随即反问：

- 太游得乾天之策，何以行坤？
- 小游得坤地之策，何以行乾？

答以：

- 阴得阳而生；
- 阳得阴而成；
- 天地配合；
- 阴阳互用。

因此“乾天之策 / 坤地之策”是轨运率义与尊卑说明，不是限制：

- 太游只能在乾；
- 小游只能在坤。

## 2. canonical 区别

C49 固定：

### 太游

- 内卦周期：36年；
- rate_symbol：乾天之策；
- 依赖：C38-BL-INNER。

### 小游

- 内卦周期：24年；
- rate_symbol：坤地之策；
- 依赖：C47-XY-INNER。

固定：

`systems_distinct=True`

`distinct_by_current_trigram_inequality=False`

## 3. 当前内卦同 / 异

允许对 C38 与 C47 的当前内卦做比较，但结果只标：

`derived_observation_not_source_verdict`

即：

- 当前同卦，不表示两制度相同；
- 当前异卦，也不是本术“成立”的唯一依据。

## 4. 旧实现审计

旧 `guiyun.zonghe()`：

`行宮卦異 = dayou["內卦"] != xiaoyou["內卦"]`

这只是当前状态布尔观察。

它遗漏：

- 36 / 24 周期差异；
- 乾天 / 坤地策义；
- 尊卑上下；
- 阴阳互用；
- “太游亦可行坤、小游亦可行乾”的直接解释。

因此：

`canonical_equivalent=False`

## 实现

- `src/kintaiyi/taiyou_xiaoyou_distinction.py`
- `tests/test_taiyou_xiaoyou_distinction.py`

## CI

```
927 passed in 1.57s
```

当前基线：927 passed / 0 failed。
