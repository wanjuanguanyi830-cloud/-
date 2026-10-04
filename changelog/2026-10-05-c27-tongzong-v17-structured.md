# 2026-10-05 C27 Tongzong volume17 structured rules

- 实现 V17-06 见闻虚实。
- 实现 V17-07 讨捕叛亡。
- 实现 V17-08 执囚对吏。
- 实现 V17-09 求索所得。
- 所有规则只消费结构化条件，不解析旧中文断语。
- V17-06 门具将发闻凶异文保留。
- V17-08 主人在内/外异文保留。
- V17-07 藏匿地旺相使用独立 hideout_qi_state。
- V17-09 不调用跨卷 V17-D1 孤虚对照。
- 新增 `tests/test_tongzong_v17_structured.py`。
