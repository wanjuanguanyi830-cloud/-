# C105 NCL-06604 旧术语记录对账

日期：2026-10-05

用户确认 NCL-06604 明钞本此前已经用于术语库扫描与初步整理。

本轮新增：
- terminology/ncl06604-legacy-reconciliation-map.json
- tests/test_c105_ncl_legacy_reconciliation.py

用途：以后恢复旧 terminology.json 时，将历史 NCL 条目与 C86-C88 当前直接影像复核结果逐项合并，避免重复建立同一来源。

当前映射覆盖：
- J4M-03 太簇/太蔟
- J4M-05 出师数值
- J4M-06 陈兵向背
- J4M-08 矛鋋
- J4M-09 天外地内
- J4M-10 奇兵伏兵标题
- J4M-11 风云飞鸟
- J4M-12 云气定胜负

旧术语库的原 ID、定义、备注与 alias 尚未取得，因此保持空值，等待真实旧记录恢复后填写。

合并原则：
- 一致则合并来源链；
- 不一致则并列记录差异；
- NCL manuscript 与四库 canonical 继续分开；
- 不把历史 NCL 来源再次导入成新的独立来源。
