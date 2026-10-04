# C27 卷十七结构条件型规则记录

## 范围

实现《太乙统宗宝鉴》卷十七：

- V17-06 见闻虚实
- V17-07 讨捕叛亡
- V17-08 执囚对吏
- V17-09 求索所得

实现文件：

`src/kintaiyi/tongzong_v17_structured.py`

## 原则

所有规则只消费结构化条件，不扫描旧中文格局断语，不从整段文本猜状态。

### V17-06 见闻虚实

输入包括：

- reported_kind: 吉/凶/忧/喜
- 天目是否掩击太乙
- 三门是否具
- 五将是否发
- 主是否挟客
- 天目内外

不同条件同时成立时并列保存 evidence。

“门具将发且闻凶”存在见证异文：

- 一见证：闻凶则凶
- 另一见证：闻凶不凶

固定保存为 `witness_variant`，禁止择一覆盖。

### V17-07 讨捕叛亡

明确分开：

- capture evidence
- no-capture evidence
- special evidence

天目掩太乙：

`得而复失`

藏匿地掩迫可追，但藏匿地本身旺/相有气时不宜往。

关键边界：

`hideout_qi_state` 是藏匿地气态；不得拿主将/主人旺相替代。

### V17-08 执囚对吏

保存：

- 天目掩击太乙：不利
- 主人旺神：不利
- 太乙初入宫：迟留难解
- 太乙与主同宫、天目临之：易出、遇贵人

“主人在内/外不可入狱”存在相反传本读法，因此固定 source_variant。

### V17-09 求索所得

独立条件：

- 天目内/外
- 主扶客 / 客扶主
- 主人内/外
- 天目格太乙
- 主人旺神
- 春夏六 / 秋冬四的绝气数

本条不得调用 V17-D1 孤虚对照；V17-D1 继续只是跨卷 derived helper。

## 输出策略

各函数返回：

- source_rule_id
- structured evidence
- summary
- source_variants（若有）
- cross_c8_merge=False
- cross_j4m_merge=False

多条正负证据同时成立：

`summary="mixed_evidence"`

不得按代码先后覆盖。
