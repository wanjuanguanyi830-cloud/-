# C43 卷九厄会行限严格来源契约

## 直接来源

《太乙统宗宝鉴》“明阳九百六，太游行限观历术”。

原文要求：

1. 帝王即位年**干支**参与加大义；
2. 取太阳（天罡）、阴主（天魁）所临；
3. 以大武、和德为界，视阴阳顺逆而行；
4. 年限不是十六宫简单步数，而有原文神数累计；
5. 还须参详阳九百六、太乙入卦、旺相休囚、太乙格等证据。

## 旧参考实现审计

旧：

`guiyun.ehui_xingxian(year_zhi, enzhi=None)`

存在：

- 核心只用 year_zhi；
- 把大义固定为亥；
- 以十六点简单 offset 推太阳/阴主；
- 以位置步数当年数；
- 未表达大武/和德顺逆界；
- 未表达神数累计；
- 未并列后续太乙格 / 阳九百六 / 旺相休囚修正。

因此：

`canonical_equivalent=False`

不得直接迁入新 truth source。

## 严格输入契约

新增：

`src/kintaiyi/volume9_ehui.py`

C43 不自己猜盘式“加大义”，只消费显式来源证据：

- `enthronement_ganzhi`
- `taiyang_landing`
- `yinzhu_landing`
- `direction`
- `count_evidence`

只给地支时直接拒绝；两字虽成“干+支”但不属于六十甲子（如甲丑、乙寅）也拒绝。

缺太阳/阴主落点、顺逆或神数证据时：

`status="not_computable"`

## 汉高祖原例

卷九见：

- 即位：乙未；
- 太阳临申；
- 阴主临寅；
- 逆行；
- 起数1 + 大威2 + 大炅9 + 高丛4 = 16。

C43 原样结构化：

`base_limit_years=16`

原文又说第12年：

“太乙入六十七局，丙午与太岁格，主崩亡”。

该证据作为：

`correction_evidence`

保留，固定：

`corrections_applied=False`

不以实际第12年事件反写基础16年行限计数。

## source_variants

C30 新增：

`source_variants.volume9`

旧 `厄會行限` replacement：

`source_variants.volume9.ehui_limit.legacy_replacement`

只有完整、可计算的 C43 结果才生成非空 legacy_replacement。

旧 flat 断语不会自动清除 migration gap。

## CI

```
799 passed in 1.31s
```

当前基线：799 passed / 0 failed。
