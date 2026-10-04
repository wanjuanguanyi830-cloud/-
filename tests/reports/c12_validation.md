# C12 legacy pan adapter 验证报告

日期：2026-10-05

## 完成内容

- 新增 `src/kintaiyi/pan_adapter.py`。
- 可从旧 flat snapshot 搬运明确盘面事实并构建 v2。
- 旧军事战略、旧七术中文断语、旧运筹博弈分析不自动提升。
- structured analysis / modern 必须显式传入。
- scenario 不从客将等旧字段推断。
- `attach_v2_to_snapshot(...)` 不原地修改旧 snapshot。
- 旧整数宫位 dict key 在 C12 适配层规范为 JSON 字符串 key；C11 builder 仍保持严格。

## CI 中发现并修复的问题

初版 adapter 直接搬运旧：

```python
{"八門分佈": {1: "開"}}
```

C11 正确拒绝非字符串 JSON object key。

修复策略：

- 不放宽 C11。
- C12 只对 legacy 容器做表示规范：
  `{1: "開"} -> {"1": "開"}`
- 不改变术义和值。

## 关键验证

1. 旧盘 meta/calendar/board/cycles 事实可提取。
2. 主算 `[数, 描述]` 只拆容器，不重算描述。
3. 旧军事战略被隔离。
4. 旧运筹博弈分析被隔离。
5. 旧七术断语即使含“成吉正利”也不会进入新 analysis。
6. 新 C8/C9 structured 结果可显式写入。
7. scenario 必须显式提供。
8. 中五仍由 C11 强制 `sector=null`。
9. unported 卷次只进入 compat 审计记录。
10. 附加 v2 后 C10 consumer 会优先读取 embedded v2。

## CI

修复 legacy numeric map key 后：

- 247 passed
- 2 failed

两条失败仍仅为旧 `tests/test_eight_divinations_classics.py` 对 15 的过时预期，无 C12 新失败。

## 结论

C12 第一阶段通过。

现在已具备未来旧 `Taiyi.pan()` 的实际接线方式，而不需要让新模块重新依赖旧 flat schema。
