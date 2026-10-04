# C12 legacy pan snapshot → v2 adapter 记录

## 背景

目标仓库仍没有完整 `Taiyi.pan()` 主程序，因此 C12 不伪造主入口，而是提供未来可直接接在旧 `pan()` 返回前的适配器。

新增：

- `src/kintaiyi/pan_adapter.py`
- `extract_legacy_snapshot_facts(...)`
- `build_v2_from_legacy_snapshot(...)`
- `attach_v2_to_snapshot(...)`

## 原则

### 1. 只搬事实，不运行算法

adapter 只搬运旧 snapshot 已经存在的：

- meta / calendar
- 太乙落宫与旧 sector
- 文昌 / 始击 / 定目
- 主算 / 客算 / 定算的旧容器
- 主将 / 主参 / 客将 / 客参
- 八门值事 / 八门分布
- 君基 / 臣基 / 民基
- 五福 / 大游 / 小游

adapter 不调用八占、七术、周期、军事或博弈算法。

### 2. 旧混合层隔离

以下旧字段不得自动提升到 v2：

- `軍事戰略 / 军事战略`
- `運籌博弈分析 / 运筹博弈分析`
- 旧七术顶层中文断语
- 旧 `推多少以占勝負`
- 旧 `推孤單以占成敗`
- 旧 `推陰陽以占厄會`

这些字段只记入：

`compat.quarantined_legacy_keys`

并固定：

- `legacy_analysis_promoted=False`
- `legacy_modern_promoted=False`

### 3. analysis / modern 必须显式传入

新的：

- `analysis.military`
- `analysis.seven_methods`
- `analysis.eight_divinations`
- `modern.game_theory`

必须由调用方传入已经结构化的结果。

旧 flat 断语不能作为替代品。

### 4. scenario 不自动推断

不得用：

- 客将
- 客参
- 客算
- 其他旧盘字段

推断：

`enemy_first_arrival_taiyi_palace`

scenario 只接受调用方显式给出的 C11 三个 canonical 字段。

### 5. 兼容返回

`attach_v2_to_snapshot(...)` 返回旧 snapshot 的副本并附加：

`result["v2"]`

这样未来旧 UI 可以暂时继续使用 flat 字段，而新 UI/CLI 只读 C10 v2 consumer。

函数不会原地修改原 snapshot。

## 数据流

```
旧 Taiyi.pan() flat snapshot
        │
        ├── 原样保留 → legacy compat
        │
        └── C12 adapter（只搬事实）
                +
            显式 C8/C9 structured results
                ↓
            C11 build_pan_v2
                ↓
            result["v2"]
                ↓
            C10 strict consumer
```
