# C70 《统宗》文昌九星 source-specific runtime 验证

日期：2026-10-05

验证对象：

- `src/kintaiyi/wenchang_nine_stars_tongzong.py`
- `tests/test_c70_wenchang_nine_stars_tongzong.py`
- `src/kintaiyi/zitingjing_collation.py`
- `src/kintaiyi/legacy_formula_quarantine.py`

## 已验证

1. C70 只选择《太乙统宗宝鉴》卷六 NGJ 见证，不冒充跨来源 canonical。
2. NGJ 九星读法固定为文昌、玄凤、明维、阴德、招摇、华明、玄武、玄冥、维明。
3. 每星30年。
4. 小周270。
5. 大周2700。
6. 第1–30年文昌，第31–60年玄凤。
7. 270年末为维明第30年。
8. 2700年末仍保持周期末项，2701重新从文昌第1年开始。
9. 年干甲落艮/青州。
10. 年干乙落震/徐州。
11. 丁落离/荆州，纠正旧丁→巽9。
12. 壬落乾/冀州，纠正旧壬→中5。
13. 结构例可表达“玄凤第11年，甲年落青州；次年乙落徐州”。
14. 干组灾应只按直接正文分组输出。
15. CADAL 的10/30内部冲突继续保留，不覆盖 C70 NGJ profile。
16. 三才世纬只作外部参校，不提升为 C70 主见证。
17. 紫庭附篇仍 `primary_result=None`。
18. 紫庭侧 `canonical_selected=None`。
19. C70 不反填紫庭 primary。
20. 星名异文不静默归一。
21. C70 不根据旧代码推造九星完整动态分布。
22. `full_dynamic_distribution=None`。
23. 旧 `config.wenchang_nine_stars` 已进入 C60 quarantine。
24. 旧实现的星名混用、丁/壬落宫错误、无效 `gong` 循环均有机器审计。
25. C15 `文昌九星` 改为 source_variant，而非 strict pending。
26. C15 当前严格 pending 字段集合为空。
27. “pending=0”仅表示来源治理分类闭合，不表示所有局部正文都已取得。

C70 分层与后续并行修正后的已确认整库基线：

```
1365 passed in 2.41s
```
