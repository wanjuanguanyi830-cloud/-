# C65 卷七三神同宫灾应验证

日期：2026-10-05

验证对象：

- `src/kintaiyi/state_spirit_conjunctions.py`
- `tests/test_c65_state_spirit_conjunctions.py`

## 已验证

1. C65 不读取 C64 位置。
2. `same_palace` 必须显式给 True / False / None。
3. None 保持未检查，不自动制造同宫。
4. False 不命中任何同宫断语。
5. True 只命中卷七直接列出的 pair。
6. 天乙条 5 个直接 pair 均可命中。
7. 地乙条 4 个直接 pair 均可命中。
8. 直符条 3 个直接 pair 均可命中。
9. 共 12 个 direct pair。
10. 正反输入顺序归一到同一 pair，不复制第二条来源。
11. source section 仍保留原正文归属。
12. 未在 C65 三神条直接列出的 pair 不类推。
13. “四神 + 大游”等未列 pair 返回 no direct rule。
14. 大遊 / 太遊 / 太游正规化为大游。
15. 小遊正规化为小游。
16. 四神水宿正规化为四神。
17. “值符”默认拒绝。
18. 只有显式 compatibility mode 才把值符映射直符。
19. C15 三项 action 已更新为 C64+C65 双层。
20. 旧 flat 仍 `migrate_whole=False`。

完整 GitHub Actions CI：

```
1283 passed in 1.59s
```
