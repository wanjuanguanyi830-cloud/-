# 2026-10-05 C45 disaster month/day timing

- 新增 `volume9_disaster_timing.py`。
- 将“岁中灾发月日之期”拆成岁→月、月→日两个独立阶段。
- 两个阶段均要求显式文昌与天目落点；不再只看文昌。
- 文昌/天目落支可映月份或日支；落四维只保存十六宫 point，不擅自折月或冒充地支。
- 文昌宫阴阳由上游显式提供，不使用旧 `_YANG_GONG` 猜测。
- 文昌同太乙及格掩迫击挟提保留为年度不协/不稔证据，不改写灾期。
- 旧 `suizhong_zaifa` 降为非 canonical 等价参考。
- 只有月、日两阶段都完整才清除旧 `歲中災發` migration gap。
- 当前 CI：841 passed / 0 failed。
