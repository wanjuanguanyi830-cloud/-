# C18 P1 来源层级记录：紫庭项目主来源目标与统宗参校

## 适用项目

本记录覆盖：

- 太乙九星
- 文昌九星
- 文昌变化
- 始击变化
- 三旗行宫
- 九宫贵神

## 证据分级后的来源策略

不能再把六项一概写成“《太乙紫庭经》主来源已确认”。

当前分为三档：

### 1. 紫庭直接正文已确认

- 太乙九星
- 文昌变化
- 始击变化

这些项目已有可逐条校读的《太乙紫庭经》在线正文，因此：

- `primary_evidence_level=direct_text_verified`
- 允许生成 `primary_result`
- 允许 `canonical_selected=zitingjing`

统宗卷六只作参校。

### 2. 紫庭传本目录已确认、正文待取得

- 文昌九星

两份现代整理本《太乙紫庭秘诀》目录均列：

`附太乙文昌九星值宫术`

因此：

- `primary_evidence_level=catalog_attested_text_pending`
- 可确认其与紫庭传本系统的目录归属
- 尚不能生成 `primary_result`
- 统宗卷六只作参校

### 3. 紫庭归属尚未证实

- 三旗行宫
- 九宫贵神

已查的《太乙紫庭秘诀》十二卷及附录目录中未见这两个同名题目；当前直接可定位文本来自《太乙统宗宝鉴》卷十。

因此：

- `primary_evidence_level=project_attribution_unverified`
- “紫庭主来源”只保留为项目曾采用的校勘目标，不得当成已证古籍归属
- 不允许生成紫庭 `primary_result`
- 迁移时按 source variant / attribution pending 处理
- 统宗卷十的直接文本不得改标成紫庭

## 参校定义

参校来源可以用于：

- 校异文
- 补证缺文
- 比较术名、次序、表格或断语差异
- 记录后世收录变化

参校来源不得：

- 静默覆盖直接主来源
- 用统宗内容冒充紫庭正文
- 因旧代码或旧 `pan()` 注释就提前确定 canonical

## 数据结构要求

`src/kintaiyi/zitingjing_sources.py` 逐条保存：

- `primary_source`
- `primary_evidence_level`
- `primary_result_allowed`
- `primary_result`
- `collation_sources`
- `collation_results`
- `canonical_selected`
- `cross_source_merge=False`

只有：

`primary_evidence_level=direct_text_verified`

才允许注入非空 `primary_result`。

## 在线证据

紫庭直接正文在线见证入口：

- https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u3291

文昌九星目录证据：

- https://www.chinyuan.com.tw/all_book/more?id=7195
- https://www.xinyi.hk/goods-7102.html

三旗行宫 / 九宫贵神当前直接来源：

- 《太乙统宗宝鉴》卷十对应术目

详细 pending 分级见：

`sources/c20-zitingjing-pending-locators-record.md`
