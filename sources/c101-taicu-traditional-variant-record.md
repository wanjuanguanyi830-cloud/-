# C101 “太蔟 / 太簇”辞书异写关系与项目规范词形

日期：2026-10-05

## 结论

项目规范词形继续固定为：

**太簇**

但“太蔟”不再仅标为普通 source glyph alias，而升级为：

**dictionary_attested_traditional_variant**

即：有辞书依据的传统异写。

## 用户补充辞书证据

用户提供“太蔟”词条：

- 读音：tài cù
- 释义中明确：“亦作太簇”
- 来源：汉语大词典 / 聚典数据开放平台
- 链接：https://app.hanyudacidian.cn/

因此“太蔟”不能描述成 OCR 错字或简单误抄。

## 与四库扫描证据合并

四库《太乙金镜式经》卷四 J4M-03 首例，CADAL06056494 digital scan p.130，直接见来源字形：

**太蔟**

因此现在证据分两层：

1. 辞书层：太蔟、太簇为同一律名的传统异写；
2. 底本层：四库 J4M-03 实际采用“太蔟”字形。

## 项目政策

用户指定项目统一采用：

**太簇**

因此：

- terminology canonical = 太簇
- runtime canonical output = 太簇
- 对外文档规范词 = 太簇
- 太蔟 = accepted source form / traditional variant
- 输入“太蔟”仍可被 runtime 接受
- 原始 source form 必须保留
- 五行仍为金
- 不因为字形不同建立新神名、新元素或新规则

如果以后 NCL-06604 或其他古本也写“太蔟”，只增加 manuscript_form 见证，不改变 canonical。

## 机器字段

rules/jinjing_v4_military.json：

- source.terminology_policy_version = c101-taicu-traditional-variant-v1
- J4M-03.terminology_policy.canonical_form = 太簇
- J4M-03.terminology_policy.variant_classification = dictionary_attested_traditional_variant
- terminology_aliases.太蔟.status = dictionary_attested_traditional_variant
- dictionary_evidence.statement = 亦作太簇

terminology/jinjing-v4-aliases.json：

- canonical 太簇
- accepted source forms: 太簇 / 太蔟
- 太蔟保存辞书与四库双重证据

## 禁止事项

- 不得再把“太蔟”描述成 OCR 误字；
- 不得因为辞书承认异写就把项目 canonical 改回“太蔟”；
- 不得丢弃四库实际字形；
- 不得把两种写法拆成两个十六神条目。
