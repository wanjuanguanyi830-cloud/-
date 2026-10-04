# Modern Liunian Nayin Variant Validation

日期：2026-10-05

## Scope

验证对象：

- `src/kintaiyi/variants/modern_liunian_nayin.py`
- `rules/variants/modern_liunian_nayin.json`
- profile: `modern_liunian_nayin_2026`

该 profile：

- `type=modern_reconstruction`
- `canonical=false`
- 不隶属于 J4M-03

## Runtime boundaries

测试固定：

- 木 + 子 → 角 → 壬 → 壬子 → 桑柘木
- 木 + 丑 → 角 → 癸 → 癸丑 → 桑柘木
- 十二地支到十二律使用古典律历背景映射
- 四维必须显式 `dimension_mode=branch_proxy`
- 日干函数只返回变音顺序
- 变音纳音必须显式给 `transformed_tone`
- 纳音五行比较只返回关系，`verdict=None`

## Namespace isolation

runtime 只能从：

`kintaiyi.variants.modern_liunian_nayin`

导入。

机器 metadata 只能位于：

`rules/variants/modern_liunian_nayin.json`

不再允许：

- `kintaiyi.modern_nayin_variant`
- `rules/j4m03_nayin_variants.json`
- `J4M03-MODERN-LIUNIAN-NAYIN`

作为正式入口。

## Ancient boundary

J4M-03 继续位于：

- `src/kintaiyi/jinjing_v4_military.py`
- `rules/jinjing_v4_military.json`

现代 profile 不允许修改：

- J4M-03 winner
- J4M-03 二目五行表
- J4M → C8 adapter

## Legacy boundary

旧 `kentang2017/kintaiyi::wc_n_sj` 继续只在 J4M-03 metadata 中以 quarantined legacy clue 保存，不与现代 profile 合并。


## pan v2 bundle isolation

新增测试：

`tests/test_modern_variant_pan_v2_bundle.py`

锁定：

- modern section 默认不自动启用任何 profile；
- modern Liunian nayin 必须显式传 payload；
- profile 固定 `canonical=false`；
- `cross_ancient_merge=false`；
- 传入 `build_pan_v2(modern=...)` 后只落在 `modern.profiles`；
- `analysis.patterns/eight_divinations/seven_methods/military` 保持空；
- `source_variants` 保持不变；
- 非 dict payload 必须报错，不进行猜测性包装。
