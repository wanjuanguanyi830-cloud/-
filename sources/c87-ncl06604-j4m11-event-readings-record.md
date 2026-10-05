# C87 NCL-06604 明钞本 J4M-11 风云飞鸟正文异文

## 目标

C86 已完成 NCL-06604 卷四页级 locator，并确认 J4M-11 正文标题为“推太乙风云飞鸟助阵法”、正文起句仍为“经曰助战之法”。

C87 继续只对 J4M-11 正文中视觉无歧义的事件断语做逐句校勘，重点核对此前《景祐太乙福应经》与四库本文字冲突的“主人形/主人刑”一组。

底本定位：

- NCL-06604 明钞本
- J4M-11: digital scan p.62-p.63
- 本轮关键句：p.63

## 直接图像读法

NCL p.63 可直接读出：

- 从客目上去击主，主败；
- 从主人刑上来，主人败；
- 从客刑上来，客败；
- 从太岁太阴月建上来，击主人主人败，击客客败；
- 扶主人阵者主人胜，扶客阵者客胜；
- 回风起伏，飞鸟旋转于阵中旗折，大败之兆；
- 众鸟来噪阵者及有风云冲突主人阵主人败，冲突客阵客败。

最后一句仍按句法保守处理：

- “众鸟来噪阵”单独不拆出一个 winner；
- 明确胜负挂在后续“风云冲突主人阵 / 客阵”两分支。

## 与四库本的实质冲突

当前四库 profile 保存：

- “从主人形上来客败”

NCL 明钞本则保存成完整双分支：

- 主人刑 -> 主人败
- 客刑 -> 客败

这不是可以用“形/刑”一个字就解释完的普通异体，因为：

1. 结果主体也从“四库客败”变成“NCL主人败”；
2. NCL 还明确增加了“客刑 -> 客败”的对称分支。

因此必须作为 substantive manuscript variant 保存，不能拿明钞本文字静默校正四库 runtime。

## 与《景祐太乙福应经》的关系

仓库已记录《福应经》对应读法：

- 从主人刑上来 -> 主人败
- 从客刑上来 -> 客败

NCL p.63 与这一结构同构。

这说明此前 JF4M 中的“主人刑/客刑”不是单纯现代整理误读，而有独立明钞本《金镜》见证支持。

但处理仍是 source-specific：

- jinjing_siku_volume4：保留四库实际文字及现有 runtime；
- NCL-06604：manuscript_reading；
- jingyou_fuying_volume4：独立 source profile；
- 三者不得自动融合为一条“校正版”。

## 仓库契约

rules/jinjing_v4_military.json：

- J4M-11 manuscript_readings.NCL-06604.event_readings
- textual_relation.to_siku
- textual_relation.to_jingyou
- canonical_override=false
- source.ncl_volume4_collation_version = c87-ncl06604-j4m11-event-readings-v1

tests/test_jinjing_v4_military_record.py：

- 锁定主人刑/客刑双分支；
- 锁定其与四库“主人形→客败”的差异；
- 锁定 NCL/Jingyou 不覆盖四库 canonical。

## 未决

p.62 前段“大将宫”句仍继续按高倍率图像单独核字；在其完整主/客限定未确认前，本轮不扩写该句。
