# C84 NCL-06604 明钞本第二见证访问与证据边界

## 目标

继续《太乙金镜式经》卷四十二推法的第二见证校勘，对象为：

- witness：NCL-06604
- 版本：明钞本
- 卷数：十卷
- 装订：四册
- 书号：06604
- 索书号：306.6 06604
- 现藏：国家图书馆（台湾）

本轮先解决一个证据等级问题：**确认整卷扫描身份，不等于已经逐页校勘十二推法。**

## 已核实

### 国家图书馆书目

国家图书馆“古籍与特藏文献资源”记录可确认：

- 正题名《太乙金镜式经》
- 唐王希明撰
- 明钞本
- 十卷
- 线装四册
- 9行、行20字、双栏、版心白口、单鱼尾
- 书号/登录号 06604

### Wikimedia Commons 扫描

公开文件：

`NCL-06604 太乙金鏡式經.pdf`

可确认：

- 124 个数字扫描页
- 原文件 2350×1700
- 约 22.57 MB
- 来源标为 National Central Library
- 版本说明与 NCL 书目一致
- 文件为整部十卷明钞本扫描

### 其他公开影印入口

国学汉籍的同书入口亦列：

- 明钞本
- 十卷
- 四册
- 书号 06604
- 台湾国家图书馆藏

可作为“公开扫描身份一致”的辅助见证。

## 本轮没有宣称已核实的内容

当前环境能稳定访问书目、整卷扫描身份及顺序预览，但任意页直接跳转/页级检索并不稳定。因此下列项目仍然是 pending：

- J4M-01..J4M-12 在 NCL 扫描中的逐条数字页 locator；
- 目录“障/陈、置/制、置变/制变、奇兵伏兵/奇伏”的明钞本实际字形；
- J4M-03 “太蔟/太簇”的明钞本实际字形；
- J4M-08 “矛鋋”及比例句在明钞本的实际字形；
- J4M-11、J4M-12 标题与关键断语的明钞本字形。

这些项目只有在目标页图像被直接看到后才能从 pending 升级。

## Canonical 政策

NCL-06604 的角色是：

`independent_manuscript_witness_metadata_verified_page_locators_pending`

证据等级：

`bibliographic_and_whole_scan_identity_verified_not_page_collated`

因此：

1. 不给 NCL-06604 猜 J4M 页码；
2. 不拿目录/电子转录推断其正文标题；
3. 不因其明钞本时代较早而覆盖 `jinjing_siku_volume4`；
4. 若将来直接图像核出异文，以 `source_variant / manuscript_reading` 登记；
5. 四库 profile 的规则仅在明确建立新 profile 时才改变。

## 仓库修改

- `rules/jinjing_v4_military.json`
  - NCL witness 增加 evidence_level
  - public_scan
  - access_audit
  - locator_policy
  - source.witness_audit_version = c84-ncl06604-access-boundary-v1
- `tests/test_jinjing_v4_military_record.py`
  - 锁定“整卷身份已核 ≠ 页级校勘已核”

## 后续

继续寻找能够稳定访问 NCL 任意目标页的公开页图或镜像。

在此之前，NCL-06604 仍是可靠的**第二底本身份见证**，但不是已完成逐字校勘的第二文本。
