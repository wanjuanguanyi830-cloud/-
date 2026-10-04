# 2026-10-05 C9 博弈层解耦

- 新增 `src/kintaiyi/game_theory.py`。
- 七术博弈输入改为结构化字段投影，禁止 stringify 后搜索“成/吉/正/利”。
- 新增 `project_seven_method_for_game_theory` 与批量投影入口。
- 所有现代投影标记 `derived_modern_feature=True`。
- 明确隔离太乙九宫与洛书九宫；博弈层使用 1乾2离3艮4震5中6兑7坤8坎9巽。
- 中五不虚构位置策略加成。
- 新增 `tests/test_game_theory_projection.py`。
