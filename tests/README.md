# 测试与验证材料

- `fixtures/historical_cases.json`：历史局例所需的位置快照、来源定位和预期关系。
- `fixtures/skyeyes_summary_144.json`：固定参考提交的 144 局审计输入快照。
- `test_jinjing_geju.py`：位置、基础规则、复合关系、旧字典适配及八门边界。
- `test_historical_cases.py`：前24/10、123/12、185/2、198/15、219/36、397/70、418/19局例。
- `test_skyeyes_summary_audit.py`：类别差异分类器和报告生成器。
- `reports/skyeyes_summary_audit.md`：逐局审计报告。

运行：

```powershell
python -m pytest
python tests/test_skyeyes_summary_audit.py
```

测试证明代码符合这些固定规则输入；它不等于对所有历史文本完成版本校勘或占验验证。

