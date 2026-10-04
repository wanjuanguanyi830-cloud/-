# C44 国政革易 / 法令变更严格来源模型

## 来源与卷次

当前识典《太乙统宗宝鉴》在线见证编在卷十；
项目旧参考长期注作卷九。

固定：

- online_witness_volume = 10
- project_legacy_volume_label = 9
- volume_status = witness_volume_variant

## 原文结构

“国政革易，法令变更术”要求：

1. 以吕申加即位 / 创立新事之年；
2. 视太簇所临，主国政革易、法令变更、风俗服色；
3. 并视太阳、阴主、地主、武德、大义所临；
4. 以当年干支数结合算长短、和不和判断远近；
5. 再看六神所临宫有无关囚迫掩击格挟杜固。

## 六神所主

- 太簇：国政革易、法令变更、风俗改常、服色更易
- 太阳：纪律隳废、厄会兵刃
- 阴主：奸臣匿谋、凶丧祸乱
- 地主：礼仪废失、口舌谣言
- 武德：迁移易地、创营宫室
- 大义：毁折废弃

《太白兵备统宗宝鉴》另并列“大神、大义”毁折废弃类事，作为 source variant 保存，不反写统宗六神核心。

## 远近传本数字

两见证共同：

- 算长且和 → 事应在远
- 算短不和 → 事应在近
- 远例：90 / 180

近期数字有差异：

- 当前统宗见证：9 / 28
- 《太白兵备统宗宝鉴》：9 / 18

因此 C44 只稳定输出：

- distance_class = 远 / 近

具体年数只放：

- witness_candidates
- canonical_year_selected = None

## 旧参考实现审计

旧 `guiyun.guozheng_bianyi(year_zhi)`：

- 只接年支，不接完整创立年干支；
- 用静态吕申与六神位置作简单十六位旋转；
- 不接算长短 / 和不和；
- 不接六神落宫格局证据；
- 要诀写成 90 / 190，与直接见证 90 / 180 不符；
- 不保留 18 / 28 传本差异。

固定：

`canonical_equivalent=False`

## 严格输入

新增：

`src/kintaiyi/volume9_governance.py`

要求：

- foundation_ganzhi
- god_landings
- calc_length
- calc_harmonious
- pattern_evidence

即便明确“没有格局”，也要显式传：

`pattern_evidence={}`

否则不算完整。

## v2 / migration

旧 `國政章易` replacement：

`source_variants.volume9.governance_change.legacy_replacement`

只有完整 C44 profile 才清除 migration gap。

## CI

```
818 passed in 1.36s
```

当前基线：818 passed / 0 failed。
