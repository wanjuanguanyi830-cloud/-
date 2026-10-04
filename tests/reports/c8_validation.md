# C8 军事综合层验证报告

日期：2026-10-05

## 实施范围

C8 已将 `junshi_zhanlue` 拆为四个明确层级：

1. 八占基础结果（直接复用 D8-01..08）
2. 三门五将（只消费上游事实）
3. 主客动静（只判先后角色/行动姿态）
4. 将帅贤否（只消费经校勘的旺衰事实）

兼容入口 `config.junshi_zhanlue` 已改为调用 C8 canonical 组合层，并保留旧繁体键 `數有所主`；该键仍来自 D8-08，不再误接五音。

## 本轮发现并修正的底层遗漏

C8 边界测试暴露 `taiyi_rules.calc_components` 仍使用旧条件 `unit != 0` 判断人算，导致 5/15/25/35 错带人算/兵卒。

已按持久规格修正为：

```python
unit = n % 10
ten = n >= 10
five = unit >= 5
one = unit % 5 != 0
```

因此 canonical：

- 5：仅地 / 吏士
- 15：天 + 地 / 将军 + 吏士
- 25：天 + 地 / 将军 + 吏士
- 35：天 + 地 / 将军 + 吏士

新增 `tests/test_calc_components_canonical.py` 锁定上述四个边界。

## CI 结果

在修正公式及接入 C8 兼容入口后，GitHub Actions 全量测试结果为：

- 204 passed
- 2 failed

两条失败均来自 `tests/test_eight_divinations_classics.py` 的旧预期：

1. 旧测试要求 15 的 `missing=[]`；canonical 应为 `missing=["兵卒"]`。
2. 旧测试要求 `all(sancai(15)["components"].values()) == True`；canonical 应为 False，因为 15 无人算。

这两条失败不是 C8 新逻辑回归，而是测试夹具仍保留被用户明确纠正前的旧规则。

当前工具的仓库写入安全检查阻止直接修改该既有测试文件，因此保留红灯并记录原因；不得为了 CI 绿灯将 canonical 公式回滚成旧答案。

## C8 验收结论

- C8 分层结构：通过。
- `数有所主` / 五音拆分：通过。
- 主客动静不覆盖 D8-06：通过。
- 三门五将不在综合层偷算：通过。
- 将帅贤否与七术 Mode B / 十二长生隔离：通过。
- `config.py` 兼容入口接 C8：通过。
- 5/15/25/35 canonical 边界：已修正并新增独立测试。
- 全量 CI：除 2 条明确过时测试外无其他失败。
