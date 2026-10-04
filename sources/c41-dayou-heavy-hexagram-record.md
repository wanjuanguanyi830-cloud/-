# C41 卷九太游重卦 / 四象策数 / 动爻记录

## 直接来源

《太乙统宗宝鉴》卷九：

- 明太游内外重卦之策术
- 明历数长短，以观远近之期术

核心结构：

1. 行宫所得之卦画于内；
2. 天数所得之卦画于外；
3. 内外相重，得重卦之象；
4. 四象策数：
   - 乾：老阳，36策
   - 坤：老阴，24策
   - 震、坎、艮：少阳，28策
   - 巽、离、兑：少阴，32策
5. 太游内卦 36 年，六年行一爻：
   - 1–6：初爻
   - 7–12：二爻
   - 13–18：三爻
   - 19–24：四爻
   - 25–30：五爻
   - 31–36：上爻

## 与 C38 的边界

C38 是：

- 阳九外卦 10 年一宫；
- 百六内卦 36 年一宫；
- 复用 C36 限周期。

C41 不调用 C38。

C41 只消费显式：

- inner_trigram
- outer_trigram
- year_in_inner_trigram

并据直接条文生成：

- 上下卦结构
- 内外四象
- 内外策数
- 单爻策数、三爻经卦策数与重卦总策数
- 内卦动爻

## 策数层级修正

卷九给出的：

- 乾 36
- 坤 24
- 震坎艮 28
- 巽离兑 32

在历数算例中实际作为**单爻策数**使用。

每个经卦三爻，因此：

- `trigram_ce = per_line_ce × 3`

重卦六爻的总策：

- `total = inner_trigram_ce + outer_trigram_ce`

例如：

- 乾内 + 震外 → 108 + 84 = 192
- 坤内 + 乾外 → 72 + 108 = 180

这两个数与卷九后续历数算例使用的重卦策数吻合。

因此当前 runtime 固定：

- `inner_per_line`
- `outer_per_line`
- `inner_trigram`
- `outer_trigram`
- `total`
- `total_status="directly_confirmed_by_volume9_examples"`

旧“36/24/28/32直接当整经卦策数再相加”的实现已撤销。


## 外卦动爻

卷九当前直接条文只明确：

“太游入内卦三十六年，均分之，则六年行一爻。”

因此 C41：

`outer_moving_line=None`

`outer_moving_line_status="not_attested_in_direct_c41_rule"`

不照搬旧 `guiyun.py` 的外卦动爻猜法。

## 积年偏移版本

### 统宗 +34 见证

卷七“太游太乙所主”见：

“加宫盈差三十四”。

保留：

`tongzong_offset34_witness`

### 太白兵备校正见证

《太白兵备统宗宝鉴》养玄子明确批评 +34 为牵合纪元，并提出：

“上古积年当加差三万六千六百一十”。

保留：

`taibai_bingbei_epoch_correction = 36610`

### 旧 +50

旧 `guiyun.py` 外卦使用 +50。

当前直接条文未核得等价明文，因此固定：

`status="unsupported_legacy_offset"`

## 策略

C41 runtime 不选择任何 epoch variant：

- `canonical_selected=None`
- `runtime_uses_epoch_variant=False`
- `epoch_formula_applied=False`
- `c38_track_used=False`

先把可直接核证的重卦结构做好，积年换算另案校勘。

## 实现

- `src/kintaiyi/dayou_hexagram.py`
- `tests/test_dayou_hexagram.py`

## CI

```
753 passed in 1.34s
```

当前基线：753 passed / 0 failed。
