# C95 10月4日 snapshot collector 安全回收

日期：2026-10-05

## 1. 用户时间边界

仅采用：

- 2026-10-04；
- 2026-10-05；

已经完成的工作。

C95 来源于 10月4日：

`codex/c1-c7-canonical/src/kintaiyi/kintaiyi.py`

相关提交：

- e3ca5af6d434 — 2026-10-04T19:53:06Z；
- 18635deed7b9 — 2026-10-04T19:53:43Z；
- 266d69628c05 — 2026-10-04T19:55:13Z。

## 2. 为什么不原样恢复 Taiyi facade

10月4日旧 facade 依赖：

- `taiyi_cycles.py`
- `four_taiyi.py`
- 当时的 `build_pan_v2_from_snapshot()`

其中周期层后来已经被：

- C64；
- C66；
- C67；
- C68；
- C92；

等重新校勘。

当前 main 又已有：

- C11 pan_v2；
- C12 pan_adapter；
- C30 pan_v2_contract。

所以把旧 `Taiyi(snapshot).pan()` 整段复制回来，会重新绑定旧公式和旧聚合方式。

C95 明确不这么做。

## 3. 回收的核心

回收：

`collect_core_snapshot(engine, ji_style, taiyi_acumyear)`

职责只剩：

- 取当前 style 的积年；
- 取当前 style 的太乙；
- 若当前不是年计，另外显式取 style=0 的年积年；
- 若当前不是日计，另外显式取 style=2 的日太乙；
- 文昌、始击、定目、主客定算、主客大小将各调用一次；
- 输出 raw snapshot。

不运行任何：

- 三基；
- 五福；
- 四太乙；
- 七术；
- 八占；
- 军事；
- 现代博弈。

## 4. 保留的旧设计意图

### primitive 只调用一次

同一 selected style 下：

- `skyeyes`
- `sf`
- `se`
- `home_cal`
- `away_cal`
- `set_cal`
- `home_general`
- `home_vgen`
- `away_general`
- `away_vgen`

各调用一次。

### 年 / 日事实不能借当前 style

非年盘：

`year_accumulated_year = engine.accnum(0, profile)`

非日盘：

`day_taiyi_palace = engine.ty(2, profile)`

这保留了 10月4日测试里最重要的边界：

> 月 / 日 / 时盘不能借自己的积年冒充年计积年；
> 非日盘不能拿当前太乙冒充日计太乙。

## 5. 不恢复

C95 暂不恢复：

- `TaiyiCanonicalMixin`
- `Taiyi(snapshot).pan()`
- `project_legacy_pan()`

因为它们必须先重接当前：

- C30 structured pan contract；
- C12 legacy quarantine；
- 新 source-specific 周期层。

后续若恢复 facade，应只在这些现行接口之上重接。
