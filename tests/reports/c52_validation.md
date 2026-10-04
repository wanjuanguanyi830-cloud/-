# C52 太乙十精来源注册验证

日期：2026-10-05

验证：

1. 十精恰有10项。
2. 次序固定：天皇、帝符、天时、太尊、飞鸟、五行、八风、五风、三风、太乙数。
3. 小周固定20/20/12/4/9/5/9/9/9/72。
4. 卷十八/卷二十作为 witness volume variant。
5. 武经总要与太白兵备作为独立参校。
6. 地符不在 canonical 名单。
7. 地符仅显式 compatibility mode 映射帝符。
8. 太岁不属于十精。
9. 第十项为太乙数。
10. 飞鸟旧周期8与直接小周9冲突。
11. 五风旧周期29与直接小周9冲突。
12. 天皇/帝符/天时/太尊/五行/八风/三风即便周期表面相合也不自动runtime ready。
13. 旧 yunqi._TEN_JING_FN 名单错误被记录。
14. 十精云气断事保持 separate source unit。
15. pan contract 未扩展 ten_essences 槽。
16. cycles root 未使用。
17. 六个旧pan字段由pending升级为来源已确认、公式待审。
18. 不出现“天游太乙”。

clean CI：

```
1006 passed in 1.91s
```

19. C53 已实现飞鸟、五风、太尊、八风、三风、五行六项位置 runtime。
20. C52 `all_position_runtime_ready=False`，因为天皇/帝符/天时仍未全部完成。
21. 天时统宗与太白兵备起点冲突保持 unresolved。
22. 太乙数继续作为独立数值层 pending。


23. C54 太乙数已完成纯数值 runtime，360/72 与云气断事分离。
24. C55 天皇 / 帝符已完成 200/20 十六神重留 runtime。
25. 天皇四维重留固定为4处，不把神名与宫名重复计数。
26. 帝符四正重留固定为4处：地主/子、高丛/卯、大威/午、太簇/酉。
27. 帝符盈差17/70异读只留 witness，均不应用。
28. 当前十精只剩天时位置因来源起点冲突保持 pending。

C55 收口完整 CI：

```
1080 passed in 0.95s
```


29. C56 天时完成 120/12 runtime：阳寅起、阴申起，均顺行十二支。
30. 太白兵备前置总括句“阳申阴寅”保留为同书内部异文；完整推步正文“阳寅阴申”用于参校。
31. 邦盈差二明确拒绝，`apply=False`。
32. C52 `implemented_position_runtimes` 现为9项，`pending_position_runtimes=[]`。
33. C52 `all_position_runtime_ready=True`；太乙数继续由 C54 独立数值层提供。
34. “全部位置 ready”不代表十精云气断事 ready；`cloud_runtime_ready=False` 不变。

C56 收口完整 CI：

```
1095 passed in 1.85s
```
