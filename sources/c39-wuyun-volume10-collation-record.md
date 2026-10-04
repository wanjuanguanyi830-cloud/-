# C39 卷十五运六气细表校勘记录

## 1. 直接来源

识典《太乙统宗宝鉴》卷十：

https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec

核心段落：

- 明太乙岁会五运六气术
- 五运行气配属之目
- 六气配属之目
- 五运配五音
- 六气配五行
- 运气太过之变
- 运气不及之变
- 运行平气之序
- 明运气与太乙天符合会之目术

## 2. 五运配五音

已直接固定：

- 土运 → 宫 → 黄天
- 金运 → 商 → 素天
- 水运 → 羽 → 玄天
- 木运 → 角 → 苍天
- 火运 → 徵 → 丹天

## 3. 六气配五行

五行层已固定：

- 厥阴 → 木
- 少阴 → 火
- 太阴 → 土
- 少阳 → 火
- 阳明 → 金
- 太阳 → 水

化气文字存在 OCR / 传本差异，C39 保留 witness + collation 双列，不静默改字。

例如：

- 少阴：统宗见“君火势化”，参校候选“热化”
- 太阴：统宗见“温土雨化”，参校候选“湿土雨化”
- 少阳：统宗见“相火水化”，参校候选“暑化”

## 4. 太过 / 不及 / 平气纪名

统宗在线 OCR 与医家通行本存在若干差异。

C39 不强行归一，而是逐项保存：

- `tongzong`
- `collation`
- `status`

典型：

- 太过土：崇阜 / 敦阜
- 不及土：卑坚 / 卑监
- 平气火：外明 / 升明
- 平气金：主君 / 审平

这些差异不得通过“看起来像 OCR 错字”而无痕覆盖。

## 5. 合会枚举异文

《太乙统宗宝鉴》当前见证：

- 天会
- 岁会
- 逆会
- “三合辐辏，则为太乙天符”

《太白兵备统宗宝鉴》见证：

- 天会
- 岁会
- 逆会
- 辐辏

即存在“三项 + 辐辏汇合”与“四项并列”差异。

固定：

`meeting_enum_status="source_variant_unresolved"`

`canonical_selected=None`

## 6. 太乙天符

卷十说明：

- 九宫三旗与运相合为岁会框架；
- 司天气运与太乙天符同并，涉及太乙天符判法；
- 仍需要九宫天符、三旗等结构化输入。

因此 C39：

`taiyi_tianfu_formula_status="requires_structured_nine_palace_and_meeting_inputs"`

当前不生成伪公式。

## 7. 太过 / 不及边界

旧参考实现曾直接用年干阴阳：

- 阳干 → 太过
- 阴干 → 不及

卷十正文还同时要求观察：

- 阳宫 / 阴宫神
- 阳干 / 阴干年
- 阳阳相加有余
- 阴阴相加不足

故 C39 固定：

`year_stem_only_finalizes_taiguo_buji=False`

不得只凭年干直接给某年最终太过/不及结论。

## 8. C37 状态升级

C37 卷十 profile 从：

`pending_direct_table_collation`

升级为：

`core_tables_collated_meeting_variant_pending`

表示：

- 基础细表已校；
- 合会枚举仍有 source variant；
- 太乙天符仍待结构化输入。

## 实现

- `src/kintaiyi/wuyun_volume10_collation.py`
- `tests/test_wuyun_volume10_collation.py`

## CI

```
735 passed in 1.20s
```

当前基线：735 passed / 0 failed。
