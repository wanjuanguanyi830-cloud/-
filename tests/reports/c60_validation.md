# C60 旧错误公式 / 非等价旧实现隔离验证

日期：2026-10-05

## 验证范围

治理层：

`src/kintaiyi/legacy_formula_quarantine.py`

C60 不提供新太乙算法，只登记已经有来源审计依据、不得重新提升为 canonical 的旧实现。

## 已验证

1. 所有登记项固定 `promotion_allowed=False`。
2. 所有登记项固定 `canonical_equivalent=False`。
3. 每项保留明确 reason、source_module 与 replacement rule / layer。
4. 十精旧 %8 飞鸟、%29 五风、漏中五八风、漏九步三风均集中隔离。
5. 天皇 / 帝符 / 天时旧函数即使周期表面相合，也不能替代 C55/C56 来源 runtime。
6. 旧 `_TEN_JING_FN` 的“地符 / 太岁”名单错误被集中隔离。
7. `yunqi.shijing_shu` 只允许 360/72 数值核心作 C54 参校；旧天气 wrapper 同时由 C59 替代。
8. 旧白云 7/6→亥子映射被隔离；C58 固定白7/6→申酉、黑1/8→亥子。
9. 旧 `_YUNQI_COLOR` 整表不能因部分条目可参校而整体提升。
10. 旧 `_shu_duanyu` 的数10/5特例与50混层被隔离。
11. 旧 `_JING_HEHUI` 不能替代 C57 显式合会层。
12. 旧 `shijing_luo` 继承错误十精函数表，不得作为位置真源。
13. 旧 `yunqi_hehui` 仅凭宫号相等自动制造合会，被明确禁止。
14. 旧 `yunqi_zongduan` / `zonghe` 混合位置、数字、自动同宫、云色和天气断语，只保留历史展示意义。
15. 九厄、厄会、国政、岁中灾发、登位云气等已证实非等价旧实现继续在同一 registry 中。
16. `legacy.flybird_wl` 不得替代 J4M-11 真实外部飞鸟观测。
17. 现代 `modern_liunian_nayin_2026` 不被误归为“错误公式”；它保持独立 modern reconstruction profile。
18. 未登记的旧实现不会自动被视为 canonical。

完整 CI：

```
1197 passed in 1.47s
```
