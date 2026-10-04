# C37 五运六气 / 五音之数来源拆分记录

## 目标

旧参考实现把：

- 卷三《明太乙统行五运六气术》
- 卷十《明太乙岁会五运六气术》
- 卷三《明五音之数以推休咎术》
- 卷三《明太乙五音之元术》

揉进少数综合函数。

C37 按来源拆开，不再把“卷三/卷十”当成一个公式来源。

## 1. 五运六气：真正跨卷

### 卷三 profile

`tongzong_volume3_wuyun`

范围：

- 五运基础；
- 文昌为主气；
- 始击为客气；
- 统行框架。

明确不计算：

- 岁会；
- 天符；
- 卷十九宫/三旗相关合会。

### 卷十 profile

`tongzong_volume10_wuyun`

范围：

- 年干五运；
- 年支司天 / 在泉；
- 主客气；
- 岁会五运六气框架。

当前：

`suihui_status="pending_direct_table_collation"`

即先固化直接基础映射，旧综合函数中的岁会/天符判断不先照搬。

## 2. 五运基础映射

年干：

- 甲己 → 土
- 乙庚 → 金
- 丙辛 → 水
- 丁壬 → 木
- 戊癸 → 火

年支六气：

- 子午 → 少阴 / 热
- 丑未 → 太阴 / 湿
- 寅申 → 少阳 / 相火
- 卯酉 → 阳明 / 燥
- 辰戌 → 太阳 / 寒
- 巳亥 → 厥阴 / 风

在泉按对宫地支取。

## 3. 五音之数：只属卷三

旧 C15 曾把“五音之数”一起标成卷三/卷十。

C37 修正：

`source_profile="tongzong_volume3_wuyin"`

算数五音核心：

- 1/2 宫、土、人君
- 3/4 徵、火、宗庙
- 5/6 羽、水、后妃
- 7/8 商、金、子孙
- 9/10 角、木、疾病

该核心与 D8-03 一致，因此复用：

`wuyin_from_calc(...)`

但输出明确：

`number_subject_rule_d8_08_used=False`

绝不把 D8-08 将军/吏士/兵卒映射成五音。

## 4. legacy replacement

旧 `五运六气` 是卷三+卷十混合输出。

因此只有同时存在：

- tongzong_volume3
- tongzong_volume10

两个 profile 时，才生成非空：

`wuyun_liuqi.legacy_replacement`

只迁一卷不能清除旧 mixed-flat replacement gap。

旧 `五音之数` 只需要：

`wuyin_number.profiles.tongzong_volume3`

## 5. C30 contract

`source_variants` 新增第五槽：

`wuyun_wuyin`

旧 flat 五运六气 / 五音之数禁止进入 analysis。

## 实现

- `src/kintaiyi/wuyun_wuyin_sources.py`
- `tests/test_wuyun_wuyin_sources.py`

## CI

```
705 passed in 1.15s
```

当前基线：705 passed / 0 failed。
