# C114 八占历史例回归恢复

日期：2026-10-05

从 2026-10-04 `integrate-taiyi-war-v1-20261004` 的旧 historical fixture 中，恢复三条此前完成但未以历史身份迁入 main 的八占古例：

- D8-02：唐太宗贞观四年，主算31，长，利深入；
- D8-04：唐昭宗光化三年，主算单3，为单阳；
- D8-08：唐玄宗天宝十年，客算17，将吏兵卒皆备。

本批按《太乙统宗宝鉴》卷五 NGJ/CADAL 直接见证重新核对，不原样复制旧 fixture。

新增：

- `tests/fixtures/eight_divinations_historical_cases.json`
- `tests/test_c114_eight_divinations_historical_cases.py`
- `sources/c114-eight-divinations-historical-cases-record.md`

边界：

- D8-02 不把整场战役胜负归因于单一长短规则；
- D8-04 不从历史事件扩张新算法；
- D8-08 只锁17这一直接古例，明确禁止恢复“16以上皆具”阈值。
