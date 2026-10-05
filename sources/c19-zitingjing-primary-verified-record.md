# C19 《太乙紫庭经》直接主来源第一批

## 在线见证

识典古籍书目：

- 《太乙紫庭经》入口：
  https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u3291
- 《太乙紫庭序》：
  https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u3rj9

该在线见证收在《太白兵备统宗宝鉴》卷首/卷一体系中，但页面明确题作《太乙紫庭经》，可作为当前在线原文见证。

## 第一批直接定位

### 1. 太乙九星

主来源章节：

- 〈释九宫所值九星〉
- https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u4tgl

C19 已结构化：

- 九宫 1..9
- 天蓬 / 天芮 / 天冲 / 天辅 / 天禽 / 天心 / 天柱 / 天任 / 天英
- 九州分野
- 当前见证所记吉凶
- “二隐七彰”“四吉五凶”等来源级摘要

本批只做静态来源表；不把后世卷次中的九十年/三百六十年推步法自动归入本篇。

### 2. 文昌变化

主来源章节：

- 〈释天目变化〉
- https://www.shidianguji.com/book/SDZJ0646/chapter/1kg32q85u5vdx

C19 已结构化：

- 文昌 = 天目
- 五行属土
- 辅相象
- 与太乙同宫 = 囚
- 前一宫 = 外迫
- 后一宫 = 内迫
- 相冲 = 对
- 与始击同宫 = 二目相关
- 二目相关按旺相判胜
- 原文所列主/客有利宫组
- 三组明确对宫灾应对象

具体旺相算法仍由独立五行规则提供，不在本篇重复实现。

### 3. 始击变化

主来源章节：

- 〈始击变化〉
- https://www.shidianguji.com/book/SDZJ0646/chapter/1kg32q85u6811

C19 第一阶段只固化核心事实：

- 始击为荧惑之精
- 南方 / 夏 / 火
- 始击为客目
- 利客、应敌
- 临军先举
- 出入、分野、变化不可执一途等基本原则

逐岁干 × 五行灾应表暂记：
`pending_textual_collation`

原因：该段较长，且在线OCR存在异字风险；需完成逐项校读后再固化。

## 天冲吉凶异文

当前《太乙紫庭经》在线见证〈释九宫所值九星〉：

- 三宫：天冲、庚、青州、记“凶”
- 全表正好四吉五凶

同一识典书目后出的《太白兵备统宗宝鉴》卷十〈明太乙九星所主术〉页面则出现：

- 三宫天冲记“吉”

参照页：

https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32qffweib7

因此 C19 固定记录：

- primary_witness = 凶
- collation_witness = 吉
- resolution = preserve_both_no_silent_merge

不得为了与后收录文本一致而无痕改掉主来源读法。

## 尚未直接定位的三项

当前仍保持：

- 文昌九星：`catalog_attested_primary_text_pending`
- 三旗行宫：`project_primary_attribution_unverified`
- 九宫贵神：`project_primary_attribution_unverified`

其中只有文昌九星已有紫庭传本目录证据；三旗行宫与九宫贵神目前仅保留项目拟定的紫庭主来源目标，尚无目录/正文归属证据。当前：

- 不生成 primary_result；
- 不借统宗公式回填；
- C13 replacement gap 继续存在。
- 三旗行宫 / 九宫贵神：已查的紫庭秘诀目录未见同名题目，统宗卷十有直接文本，因此不得提前标为紫庭 canonical。

## 代码

新增：

- `src/kintaiyi/zitingjing_primary.py`
- `tests/test_zitingjing_primary.py`

`build_c19_verified_primary_results()` 当前只返回：

- taiyi_nine_stars
- wenchang_changes
- shiji_changes

送入 C18 source container 后，六项 replacement gap 会从 6 个降为 3 个。


## C29 校核修正

- 九星主来源链接统一为 `1kg32q85u4tgl`。
- 早期记录中的“配干”已撤销：当前 C19 canonical 表只保留已核稳的宫、星、分野、吉凶。
- 剩余三项定位状态与 C20 证据等级统一，不再使用笼统 `pending_direct_locator`。


## C19/C31/C34 术语目录接线

当前新增稳定入口：`terminology/zitingjing.json`。

该目录不改变既有证据等级，只把六项术语、aliases、runtime 与来源门禁集中登记：

- 太乙九星 / 文昌变化 / 始击变化：direct_text_verified；
- 文昌九星：catalog_attested_text_pending；
- 三旗行宫 / 九宫贵神：project_attribution_unverified。

C18 `build_zitingjing_rule_sources()` 仍是 primary_result 的唯一门禁：非 direct_text_verified 项传入 primary_result 必须拒绝。

旧 `terminology/zitingjing-migration-map.json` 继续只负责历史本地术语库恢复，不与稳定消费目录合并。
