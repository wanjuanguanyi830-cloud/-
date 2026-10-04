# C59 十精太乙数天气 / 合会断语

日期：2026-10-05

## 直接来源

- 《太乙统宗宝鉴》卷十八 / 卷二十“十曰太乙数”；
- 《太乙金镜式经》卷七“推太乙数法”；
- 《武经总要》后集卷十八十精太乙数条。

C59 与 C54 分层：

- C54 只计算 1..72 太乙数；
- C59 解释显式提供的太乙数与天气 / 合会证据；
- C59 不自动从积年重算 C54，也不从盘面位置制造合、冲、挟。

## 1. 稳定数值断语

跨见证稳定：

- 数30 → 日晕、大风；
- 数40 → 阴雨、黄雾。

旧 `yunqi.shijing_shu` 的数10 / 数5独立断语没有当前直接条文支持，固定不采用。

## 2. 数50句读异文

《武经总要》近似分为：

- 数得50 → 日晕、大风；
- 数与天目旺相合 → 日晕。

《太乙金镜式经》与统宗当前转写更接近：

- 数得50 + 与天目旺相合 → 日晕。

因此：

- 数50单独 `effects=None`
- `canonical_selected=None`
- `source_segmentation_variant_unresolved`

不得把武经句读静默覆盖统宗 / 金镜。

当调用方显式给：

- number=50
- 合天目
- 天目旺相

可保留“日晕”为各见证共同支持结果，但数50自身异文仍继续存在。

## 3. 显式关系

C59 支持：

- 合太乙 → 日晕、大风；
- 冲太乙 → 日晕、风起；
- 合天目且旺相 → 日晕；
- 太乙挟天目 → 阴雨、日晕、大风；
- 合飞鸟，且飞鸟在6/8/9宫 → 日晕；
- 与天地并 → 日晕；
- 与天地相当 → 大风；
- 合太乙飞鸟 → 疾风；
- 合主计 → 日晕，但保留天10、地9、武经“主计8”的细节异文。

所有关系必须显式输入。

固定：

- `auto_number_lookup_used=False`
- `auto_relation_inference_used=False`

无关系也须显式传空 list。

## 4. 主计细节

金镜：

- 天10、地9、数与主计合。

武经：

- 天10、地9、数与主计8合。

因此 C59 要求：

- heaven_calculation
- earth_calculation
- main_calculation

均显式给出后再保留对应见证边界。

## 5. 唯一 canonical runtime

曾并行出现：

- `ten_essences_number_weather.py`
- `ten_essences_number_omens.py`

现保留信息更完整的：

`src/kintaiyi/ten_essences_number_omens.py`

前者及其测试已删除。

rule id：

`C59-TAIYI-NUMBER-OMEN`

## 6. 十精云气三层完成

当前：

- C57：显式合会 / 旺相 / 阴阳宫；
- C58：初移宫云色时变 / 天气形态观察；
- C59：太乙数天气 / 数值合会。

因此 C52 registry 可标：

- `cloud_conjunction_runtime_ready=True`
- `cloud_observation_runtime_ready=True`
- `cloud_number_omen_runtime_ready=True`
- `cloud_runtime_ready=True`

这里的“ready”表示三层均有可审计 runtime；未决异文仍保持 unresolved，不表示强行统一来源。

## 7. CI

C59 去重与 C52/C54 同步后：

```
1182 passed / 0 failed
```
