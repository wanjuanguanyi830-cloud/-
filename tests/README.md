# 测试与验证材料

- `test_base_motion_rules.py`：从结构化规则 JSON 读取规则并验证起点、换位边界和周期回绕。
- 覆盖君基30／360年、臣基3／36年、民基1／12年，五福45／225年，大游36／288年，小游3／24／240年，四太乙3／36年边界。
- 另验证18步大游天目路径、运行位／九宫字段区分、特殊运行位映射及大旲别名。
- `fixtures/historical_cases.json`：历史局例所需的位置快照、来源定位和预期关系。
- `fixtures/skyeyes_summary_144.json`：固定参考提交的144局审计输入快照。
- `test_jinjing_geju.py`：位置、基础规则、复合关系、旧字典适配及八门边界。
- `test_historical_cases.py`：前24/10、123/12、185/2、198/15、219/36、397/70、418/19局例。
- `test_skyeyes_summary_audit.py`：类别差异分类器和报告生成器。
- `reports/skyeyes_summary_audit.md`：逐局审计报告。

从仓库根目录运行 `python -m pytest`。测试验证的是这些 JSON 所表达的整理规则，不代替原典版本校勘。
