# C102 “太蔟→太簇”进入公共十六神归一层

日期：2026-10-05

## 背景

C101 已确定：

- 项目规范词形：太簇
- 太蔟：辞书可证传统异写
- 四库《太乙金镜式经》J4M-03 首例实际见太蔟

此前只有 J4M-03 私有 runtime alias 接受“太蔟”，公共十六神层 GOD_ALIASES 尚未接受该写法。

## 本轮修改

公共层新增：

太蔟 -> 太簇

位置与五行保持既有 canonical：

- 太簇：酉
- 五行：金

“太蔟”不加入 GODS 主表，因此不会变成第十七个神。

## 术语目录

terminology/sixteen_spirits.json：

- canonical spirit 继续唯一保存“太簇”
- aliases 新增“太蔟 -> 太簇”
- status = dictionary_attested_traditional_variant
- schema_version 升至 1.3.0
- 增加 canonical_glyph_policy.太簇

## 行为边界

允许：

- position("太蔟") == "酉"
- position("太簇") == "酉"

禁止：

- 新建独立“太蔟”神位
- 为太蔟另设五行
- 因别名字形改变任何宫位或推法
- 删除古籍 source form

## 与 J4M-03 的关系

J4M-03 可以继续保留自己的来源级 alias metadata，用来保存：

- 四库 p.130 的实际字形
- manuscript/source form
- canonical 输出名

公共层只负责跨模块统一输入归一。

## 文件

更新：

- src/kintaiyi/taiyi_rules.py
- terminology/sixteen_spirits.json

新增：

- tests/test_c102_taicu_global_alias.py
- sources/c102-taicu-global-alias-record.md
