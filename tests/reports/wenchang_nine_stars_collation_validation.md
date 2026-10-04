# 文昌九星外部参校验证

日期：2026-10-05

## 验证对象

- `src/kintaiyi/zitingjing_collation.py`
- `tests/test_zitingjing_collation.py`

## 锁定边界

测试保证：

- 紫庭侧仍是 `catalog_attested_text_pending`；
- `primary_result=None`；
- `canonical_selected=None`；
- 《三才世纬》只作为 `sancai_shiwei_volume81` 外部参校；
- 该来源不能用于其他紫庭规则；
- 统宗两个在线见证并列保存；
- 星名异文不静默归一；
- 10 / 30 年值宫冲突固定为 `unresolved`；
- 不生成文昌九星 canonical 推步算法。

## 已机器化的周期冲突

CADAL witness：

- prose rate = 10
- algorithm rate = 30
- small cycle = 270
- large cycle = 2700
- `internal_conflict=True`

NGJ witness：

- prose rate = 30
- algorithm rate = 30
- small cycle = 270
- large cycle = 2700
- `internal_conflict=False`

这使得“直接按统宗实现文昌九星”在当前阶段被明确禁止。
