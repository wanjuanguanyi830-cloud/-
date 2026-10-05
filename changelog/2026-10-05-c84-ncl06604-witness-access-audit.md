# C84 — NCL-06604 明钞本见证访问边界

日期：2026-10-05

本轮确认 NCL-06604 的书目与整卷公开扫描身份：

- 明钞本
- 十卷
- 四册
- 书号 06604
- Wikimedia Commons 124 页整卷扫描
- 来源为 National Central Library

同时明确：整卷身份已核不等于十二推法逐页已核。

因此 NCL witness 继续保持：

`independent_manuscript_witness_metadata_verified_page_locators_pending`

新增 evidence_level、public_scan、access_audit、locator_policy，并用测试禁止后续把“书目已确认”误写成“明钞本文字已逐条核定”。

新增：
- sources/c84-ncl06604-witness-access-audit-record.md

更新：
- rules/jinjing_v4_military.json
- tests/test_jinjing_v4_military_record.py
