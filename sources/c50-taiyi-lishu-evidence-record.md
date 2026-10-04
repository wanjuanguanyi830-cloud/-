# C50 太乙历数之期证据聚合层

## 直接来源

《太乙统宗宝鉴》卷十：

- 明太乙历数之期术

识典：
https://www.shidianguji.com/book/CADAL02055529/chapter/1l5eriw9odw6f

重要参校：

《太白兵备统宗宝鉴》“释大游太乙观历数”
https://www.shidianguji.com/book/SDZJ0646/chapter/1kghfsbbgiwc2

## 1. 本术不是单一寿数公式

正文以“帝王应天顺人始终之期”为总纲。

基础厄会：

- 即位年支加大义；
- 视太阳、阴主所临；
- 并取太阳/阴主各自合神，共成“四神”。

随后要求继续参详：

- 太乙入运气爻卦象；
- 太游轨运卦爻；
- 小游轨运卦爻；
- 内外极限；
- 囚、迫、击、格、掩、挟等。

因此 C50 是证据聚合层，不存在一个可以替代全部证据层的已证单公式。

固定：

- `final_lifespan_formula=None`
- `final_lifespan_years=None`
- `c42_formula_reused_as_c50=False`
- `c43_formula_reused_as_c50=False`

## 2. 与 C42 / C43 的边界

### C42

卷九“历数长短 / 安居”：

- 重卦策数；
- 动爻；
- 纳甲；
- 历数长短。

不得把 C42 的数值算法直接当作 C50 帝王始终总纲。

### C43

C43 已结构化：

- 即位干支；
- 太阳 / 阴主；
- 行限显式证据。

C50 可消费 C43，但 C50 还要求额外的“四神合神期”和其他轨运/格局证据。

因此 C43 也不等于 C50。

## 3. C50 必需证据

canonical runtime：

`src/kintaiyi/taiyi_lishu_evidence.py`

完整 evidence bundle 要求：

- 即位年合法六十甲子；
- C43 厄会结果；
- 太阳 / 阴主及其合神四神期显式证据；
- C41 太游重卦 / 卦爻证据；
- C47 小游重卦 / 卦爻证据；
- 太乙入运气爻卦象显式证据；
- 囚迫击格掩挟显式检查。

无格局也须传空 list。

## 4. 登位云气

正文又附登位日月旁云气。

统宗在线见证多写单值：

- 黄土 5；
- 白金 9；
- 青木 3，并注 8 可用成数；
- 黑水 6；
- 赤火 7。

《太白兵备统宗宝鉴》明确给出生数/成数：

- 木 3 / 8；
- 火 2 / 7；
- 土 5 / 10；
- 金 4 / 9；
- 水 1 / 6。

C50 因此只保存双值，不擅选一个：

- `sheng_number`
- `cheng_number`
- `selected_number=None`

固定：

`number_selection_status="source_pair_preserved_unselected"`

云气本身不参与“最终寿数”自动计算。

## 5. 去重

曾并行出现：

`imperial_lishu_scope.py`

现已删除。

唯一 C50 truth source：

`taiyi_lishu_evidence.py`

## CI

```
955 passed in 1.62s
```

当前基线：955 passed / 0 failed。
