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
