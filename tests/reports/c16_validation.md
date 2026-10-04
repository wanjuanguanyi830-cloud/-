# C16 board facts 验证报告

日期：2026-10-05

完成：

- board 新增 `sixteen_palaces`
- 十六宫分布迁入 board
- 天乙/地乙/四神/直符/合神/计神迁入 `board.generals.*.sector`
- 7 个字段在 C14 从 unported 转为 migrated_fact
- C13 不再把它们列为 unported

特别验证：

- 基础神将使用 `sector`，不误写为主客大将式 `palace`
- adapter 只搬 snapshot，不运行旧算法
- C15 审计测试同步更新当前迁移状态

C16 完整 CI：

```
293 passed
```
