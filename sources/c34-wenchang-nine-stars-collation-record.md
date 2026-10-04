# C34 文昌九星外部参校层

## 状态

文昌九星当前仍为：

`catalog_attested_text_pending`

已有《太乙紫庭秘诀》现代整理本目录证据：

`附太乙文昌九星值宫术`

但尚未取得该附篇可逐条校读正文。

因此：

- `primary_result=None`
- `canonical_selected=None`
- 不实现 canonical 推步。

## 外部参校

新增：

`src/kintaiyi/zitingjing_collation.py`

当前并列保存：

1. 《三才世纬》卷八十一
2. 《太乙统宗宝鉴》卷六 CADAL 见证
3. 《太乙统宗宝鉴》卷六 NGJ 见证

## 已发现异文

### 星名

至少包括：

- 明雄 / 明维
- 阴玄 / 阴德
- 招摇 / 招煥
- 雄明 / 维明

不得无痕归一。

### 值宫周期

已见：

- 10 年一宫
- 30 年一宫

更关键的是 CADAL 同一电子见证内部同时出现：

- 叙述句：10 年一宫
- 推法：宫率 30
- 小周 270
- 大周 2700

因此周期状态固定：

`unresolved`

## C18 接口

`wenchang_nine_stars.collation_sources` 当前允许：

- `tongzong_volume6`
- `sancai_shiwei_volume81`

但两者都只是参校来源。

## 禁止

- 不得用《三才世纬》替代紫庭附篇正文；
- 不得用统宗某一见证直接生成 primary_result；
- 不得在 10 / 30 年冲突未解时固化 canonical runtime。
