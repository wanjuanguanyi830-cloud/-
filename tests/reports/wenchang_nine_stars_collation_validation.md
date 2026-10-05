# 文昌九星外部参校验证

> **状态更新（2026-10-06）**：本文件保留为历史阶段记录。用户已重新提供研易楼藏《太乙紫庭祕訣》明钞本，目录页（PDF 第5–6页）已直接核验，未见“文昌九星值宫术”题名。文昌九星现行稳定规则归 `C70-TONGZONG-WENCHANG-NINE-STARS`（《太乙统宗宝鉴》卷六 NGJ）；现代整理本“附太乙文昌九星值宫术”只记为编辑层目录证据，来源仍未完全证明。旧文中的“紫庭 primary pending / 扫描未重新挂载 / C70 仅参校”等状态均已被本结论取代。当前依据见 `sources/c70-wenchang-nine-stars-source-separation-record.md`。

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


## C70 后续分层验证

原 C34 跨来源结论保持：

- `primary_result=None`
- `canonical_selected=None`
- 10 / 30 年跨见证冲突仍为 unresolved。

新增的 C70 只把统宗 NGJ 见证单独变成可运行 source profile：

`C70-TONGZONG-WENCHANG-NINE-STARS`

测试明确保证：

- `source_specific_runtime.available=True`
- `cross_source_canonical=False`
- `zitingjing_primary_result=False`

因此“统宗可运行”和“紫庭 primary 未取得”可同时成立，不再用一个 pending 标签混淆。
