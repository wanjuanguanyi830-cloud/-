# C13 legacy migration audit 验证报告

日期：2026-10-05

## 完成内容

- 新增 `src/kintaiyi/migration_audit.py`。
- 单盘审计 legacy/v2 迁移状态。
- 批量统计迁移率、隔离率、unported 字段频率。
- 识别 structured replacement gaps。
- 审计元数据不参与古法判断。

## C13 加入后的测试

在修正旧 15 测试预期前：

- 254 passed
- 2 failed

两条失败仍是历史过时测试，与 C13 无关。

随后已把旧测试与确认 canonical 对齐：

- 15 缺兵卒；
- 15 无人算；
- 不修改实现公式。

修正后全套：

- 256 passed
- 0 failed

## 结论

C13 第一阶段通过，且此前长期保留的两条 stale CI failure 已清零。
