# 测试与古籍课例规范

## 既有《金镜》测试

本次继续保留以下目录材料与命令：

- `fixtures/historical_cases.json`：既有历史局例位置、来源和预期关系。
- `fixtures/skyeyes_summary_144.json` 与 `reports/skyeyes_summary_audit.md`：144 局审计输入和报告。
- `test_jinjing_geju.py`、`test_historical_cases.py`、`test_skyeyes_summary_audit.py`：既有规则回归。

```powershell
python -m pytest
python tests/test_skyeyes_summary_audit.py
```

每条古籍课例用 JSON fixture 保存原始输入、来源定位、逐步中间值、原书断语和程序预期；pytest 仅断言来源明确支持的字段。规则测试不得以“现有程序算出同样结果”作为来源证据。

## 最低字段

```json
{
  "case_id": "T7-01-LINJIN-001",
  "rule_id": "T7-01",
  "ruleset_version": "1.0.0",
  "case_kind": "historical_case",
  "source": {
    "title": "待补",
    "collection": "四库全书本",
    "juan": 6,
    "chapter": "临津问道",
    "edition": "待补",
    "page_or_image": null,
    "quotation": null,
    "citation_status": "locator-incomplete"
  },
  "inputs": {"start_branch": "子"},
  "expected_steps": [{"step": "大神落点", "value": "卯"}],
  "expected": {"推步": ["子", "卯", "午", "酉", "子"]},
  "source_outcome": null,
  "notes": []
}
```

若卷次、页码、底本或逐字引句尚未核定，必须显式用 `待补`／`null` 并设 `citation_status`，不能捏造精确书目。规则结构演示用例标记 `case_kind: "structural"`，不得冒充古籍课例。

## 验证步骤

1. 核对原文与输入，不替原文缺失的盘面补值。
2. 单独断言位置链、代表点、五行、五态／阶段等每个可观察中间结果。
3. 将原书断语放在 `source_outcome`，只在原书明确断语时映射到程序 `expected`。
4. 文字异文按版本保留；校定词只用作规则字段，不改写引文。
5. 规则未定时预期值必须为空或标为未计算，并增加待校说明。
6. 新版对照测试不删除旧来源 fixture；不同底本分别列案，不用一个多数表决结果覆盖异文。

本批 fixture 的引用位置未齐，状态仍为 `locator-incomplete`；测试覆盖的是已讨论规则的回归，不构成原典版本核验或整套太乙排盘验收。

