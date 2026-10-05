# C74 三基 / 五福同宫关系验证

日期：2026-10-05

验证对象：

- `src/kintaiyi/three_bases_wufu_conjunctions.py`
- `tests/test_c74_three_bases_wufu_conjunctions.py`

## 已验证

1. C74 只处理君基、臣基、民基、五福四者。
2. 四者恰好形成6个直接 pair。
3. `same_palace` 必须显式给 True / False / None。
4. None 保持未检查，不调用 C66 / C67 自动判断。
5. False 不生成同宫断语。
6. True 才解释对应直接条文。
7. pair 正反输入只做查询正规化，不复制第二条来源。
8. 君基+臣基保留君臣际会、君治臣忠、国殷民安等直接核心。
9. 君基+民基保留务农桑、安百姓、巡狩省方等稳定核心。
10. 臣基+民基保留贤者进朝、民安其业、政讼和平等直接核心。
11. 含五福的三个 pair 分开保存三基条与五福条。
12. 君基+五福不把“皇室巩固”与“五福条人君福寿”压成伪单句。
13. 臣基+五福分别保存臣基条“利为宰辅”等与五福条“福利辅宰”。
14. 民基+五福分别保存民基条“其民富寿”等与五福条“四民乐业、天下熙和”。
15. “同宫在初交之始”必须由 `initial_conjunction=True` 显式触发。
16. 未检查初交时保持 pending。
17. 非五福 pair 不接受 `initial_conjunction`。
18. 不同宫时禁止声明同宫初交。
19. “五福与君基相冲”只留 adjacent relation，不在同宫层应用。
20. C15 三基字段已切换为 C66 + C74。
21. C15 五福位置字段已切换为 C67 + C74。
22. 五福吉算继续由 C68 独立处理。
23. 旧 flat 均继续 `migrate_whole=False`。

完整 GitHub Actions CI：

```
1422 passed / 0 failed
```
