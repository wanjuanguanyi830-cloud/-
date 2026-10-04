# C62 天子巡狩之期术验证

日期：2026-10-05

验证对象：

- `src/kintaiyi/imperial_inspection.py`
- `tests/test_c62_imperial_inspection.py`

## 已验证

1. 太乙与天目必须同时在四维，才判为巡狩年。
2. 四维固定为乾 / 艮 / 巽 / 坤。
3. 只有太乙在四维或只有天目在四维，均不成立巡狩年。
4. 天目乾 / 阴德 → 东方。
5. 天目艮 / 和德 → 南方。
6. 天目巽 / 大炅 → 西方。
7. 天目坤 / 大武 → 北方。
8. 十六神名可通过公共 canonical 正规化为位置，不另造神位表。
9. 巽位西方的方向事实与神名 OCR 异读分离。
10. 囚 / 挟 / 格 / 对必须显式输入。
11. 繁体挾 / 對只做字形正规化。
12. 未检查行月格局时保持 pending。
13. 显式检查但未见四格时，不自行给出行月。
14. 即使命中囚 / 挟 / 格 / 对，也只标记来源条件成立。
15. `month_number=None` 固定。
16. `month_number_computation_supported=False` 固定。
17. 不从日期自动推太乙。
18. 不自动推天目。
19. 不从其他格局 runtime 自动制造囚 / 挟 / 格 / 对。
20. 非巡狩年保留“遣使按行风俗”等来源 fallback。
21. C15 旧字段仍 `migrate_whole=False`，但 action 已更新为 C62 runtime。

完整 GitHub Actions CI：

```
1238 passed in 1.29s
```
