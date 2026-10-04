# C54 十精“太乙数”72数值层

日期：2026-10-05

## 1. 范围

C54 只实现十精第十项“太乙数”的纯数值推步。

它不是宫位函数，也不自动输出十精云气、风雨、日晕等断语。

唯一 runtime：

`src/kintaiyi/ten_essences_number.py`

rule id：

`C54-TAIYI-NUMBER`

## 2. 直接来源

### 《太乙统宗宝鉴》

卷十八 / 卷二十见证均保存：

- 周法 360；
- 元法 72；
- 余数命起一数。

因此 C54 固定：

- `big_cycle=360`
- `small_cycle=72`
- 输出范围 `1..72`

余 0 按周期末项处理，不产生 0。

### 《武经总要》

独立参校见“太乙局法七十二除之，不尽者，命起一数”，与 72 数值层一致。

## 3. 旧实现边界

旧 `yunqi.shijing_shu` 的 360→72 数值核心与来源周期相合。

但旧 wrapper 同时把 30 / 40 / 50 等数值直接接天气断语，因此：

- `numeric_core_equivalent=True`
- `wrapper_canonical_equivalent=False`

不得把整个旧函数直接升为 canonical。

## 4. 云气边界

特殊数值的天气解释继续属于十精云气/合会层。

C54 固定：

- `number_only_in_c54=True`
- `weather_omens_applied=False`
- `cloud_omen_applied=False`

## 5. 周期边界

已覆盖：

- 72 → 72；
- 73 → 1；
- 360 → 72；
- 361 → 1；
- 720 → 72。

## 6. 与其他批次的关系

- C52：来源注册表；
- C53：六项九宫/四正型位置 runtime；
- C54：太乙数；
- C55：天皇 / 帝符十六神重留 runtime；
- 天时继续独立 pending。

C54 不扩展 pan v2 contract，也不写入通用 cycles root。
