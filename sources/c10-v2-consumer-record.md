# C10 pan v2 消费层记录

## 背景

目标仓库当前尚无完整 `Taiyi.pan()`、Streamlit 或 CLI 主入口，不能假装已经完成 UI 迁移。

因此 C10 第一阶段先建立严格消费接口，供未来 UI/CLI 共用。

## 新增模块

`src/kintaiyi/v2_consumer.py`

入口：

- `resolve_v2_payload(...)`
- `read_v2_section(...)`
- `read_v2_analysis(...)`
- `read_v2_board(...)`
- `build_v2_view_model(...)`

## 核心原则

### 1. v2-first，不混读

允许两种输入：

1. 直接传 `schema_version="2.0"` 的 v2 dict；
2. 传旧 pan 容器，但必须存在 `result["v2"]`。

若只有 `主算/客算/太乙/七式/军事战略` 等旧中文 flat 字段，则返回：

- `status="not_computable"`
- `consumer_mode="v2_strict"`
- `missing_inputs=["v2"]`

不得从 flat 字段自动拼装替代。

### 2. 子层缺失显式报缺

读取：

- `analysis.eight_divinations`
- `analysis.seven_methods`
- `analysis.military`
- `board.taiyi`
- `board.generals`

等子层时，若不存在就返回 missing path，不改读旧字段。

### 3. UI view model 不做算法

`build_v2_view_model(...)` 只组织 v2 已存在内容：

- meta
- calendar
- board
- cycles
- analysis
- modern
- source_variants
- compat

并固定 `legacy_fallback_used=False`。

## 下一阶段

当目标仓库引入真正的 `pan_v2.py` / `Taiyi.pan()` 或 UI/CLI 入口后，只需把展示层改为消费本模块，不再各自解析旧 flat schema。
