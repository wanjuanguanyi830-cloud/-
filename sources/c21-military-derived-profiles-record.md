# C21 卷十五 / 卷十七军事 derived profile 记录

## 目标

旧 `Taiyi.pan()` 将：

- `軍事應用`
- `軍事占斷`

作为顶层综合 dict 输出。

C21 将它们拆成独立 source_variants profile，不复制旧算法、不与 C8/J4M 合并。

新增：

- `src/kintaiyi/military_derived_profiles.py`
- `build_volume15_military_profile(...)`
- `build_volume17_military_profile(...)`
- `build_military_derived_source_variants(...)`

## 卷十五 profile

profile：

`tongzong_volume15_military_application`

旧综合术目形状锁定为：

- 奇兵伏兵
- 五阵置旗
- 出兵称神
- 陈兵出乡
- 选将之术
- 教兵之术
- 随地制变
- 分合用兵
- 五音风
- 五音观风察将
- 安营置阵
- 风从八卦
- 云气逆顺
- 军势胜负

固定：

- `derived_military_profile=True`
- `cross_volume_merge=False`
- `cross_c8_merge=False`
- `cross_j4m_merge=False`

### 与 J4M 的边界

- 奇兵伏兵 ≠ J4M-10 推奇伏法；
- 随地制变 ≠ 自动覆盖 J4M-08；
- 军势胜负 ≠ J4M-11/12 外部观测规则。

### 与 C8 的边界

分合用兵、安营置阵即使消费三门/五将/格局事实，也不能反写 C8 胜负链。

## 卷十七 profile

profile：

`tongzong_volume17_military_divination`

旧综合术目：

- 出兵用时
- 敌国动静
- 间谍虚实
- 敌使虚实
- 敌兵来方
- 见闻虚实
- 讨捕叛亡
- 执囚对吏
- 求索所得
- 孤虚对照
- 时计诸事
- 占望行人

固定同样的跨层禁止合并标记。

### 与 C8/J4M 的边界

- 敌国动静不是 C8-L3 主客动静；
- 求索所得旧代码虽与卷五孤虚做对照，但属于跨卷对照，不是同一真源；
- 出兵用时不替代 J4M 出师/主客规则。

## legacy quarantine

C14 现在将：

- 军事应用 → `source_variants.military_derived.tongzong_volume15.payload`
- 军事占断 → `source_variants.military_derived.tongzong_volume17.payload`

旧 flat 值不再普通 unported。

只有显式独立 profile payload 存在时，C13 replacement gap 才清除。

## 卷次校勘注意

不同电子本/汇编本可能存在卷次编排差异。

因此 C21 以：

- profile 名
- 术目清单
- source record

共同识别来源，不以“卷号相同”自动认定同一篇。
