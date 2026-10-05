# C79 — 卷四十二推法影印页定位与“矛鋋”纠字

日期：2026-10-05

本轮直接核对 CADAL06056494 四库扫描：

- 将 J4M-01..J4M-12 全部绑定到数字扫描 p.128-p.143；
- 明确这些 locator 是数字扫描页，不是原书叶码；
- 纠正 J4M-08 旧 OCR/转录“矛锤”为扫描可见的“矛鋋”；
- 相应更新 runtime、machine rules、测试契约和历史来源记录；
- 保留《金镜》《汉书》《福应经》的比例/段落异文，不做跨书静默校正。

关键更正：J4M-08 四库本 p.136 为“此矛鋋之地也，弓弩三不当一”。

新增：
- sources/c79-j4m-cadal-scan-locators-record.md

更新：
- rules/jinjing_v4_military.json
- src/kintaiyi/jinjing_v4_military.py
- tests/test_jinjing_v4_military.py
- tests/test_jinjing_v4_military_record.py
- sources/jinjing-v4-military-12-record.md
- sources/c76-jinjing-v4-witness-collation-record.md
