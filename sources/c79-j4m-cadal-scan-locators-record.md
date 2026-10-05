# C79 《太乙金镜式经》卷四十二推法 CADAL 影印定位与 J4M-08 字形校勘

## 目标

在 C63/C76 已完成正文结构、底本见证和异书边界整理后，本轮直接检查四库本扫描 witness：

- witness：CADAL06056494
- 题名：《太乙金鏡式經·卷一~卷四》
- 原书来源：浙江大学图书馆
- 数字扫描：144 页
- source profile：jinjing_siku_volume4

本记录只登记直接图像核验得到的数字扫描页定位与字形纠正，不把数字页码冒充原书叶码。

## 十二法数字扫描 locator

| rule_id | 正文标题 | CADAL 数字扫描页 |
|---|---|---|
| J4M-01 | 推三门具不具 | p.128-129 |
| J4M-02 | 推五将发不发 | p.129-130 |
| J4M-03 | 推主客相关法 | p.130-131 |
| J4M-04 | 推主客 | p.131-132 |
| J4M-05 | 推出师法 | p.132 |
| J4M-06 | 推陈兵向背 | p.132-134 |
| J4M-07 | 推制阵随地法 | p.134-135 |
| J4M-08 | 推随地制变 | p.135-137 |
| J4M-09 | 推太乙在天外地内法 | p.137-138 |
| J4M-10 | 推奇伏法 | p.138-139 |
| J4M-11 | 推太乙风云飞鸟助战法 | p.139-140 |
| J4M-12 | 推阵有风云气定胜负 | p.140-143 |

定位说明：

- J4M-12 标题位于 p.140 左端后序位置；
- 云气方位×颜色主体表从 p.141 展开；
- 聚散、将位及无云气尾句续至 p.143；
- 页码均为数字扫描 sequence，不等同原书叶码。

## J4M-08 字形纠正

直接检查 p.136 可辨：

> 此矛鋋之地也，弓弩三不当一

因此旧电子转录/旧 runtime 中的“矛锤”属于误读，应纠正为：

- favored = 矛鋋
- source_ratio_text = 弓弩三不当一矛鋋

本纠正为 scan-verified textual correction，不是用《汉书》反校后擅改《金镜》。

## 与《汉书》《景祐太乙福应经》的关系

C79 纠字后可确认：

- 《金镜》《汉书》《福应经》此处兵器名均为“矛鋋”；
- 《金镜》仍作“弓弩三不当一”；
- 《汉书》《福应经》对应系统作“长戟二不当一”；
- 《汉书》另有曲道相伏、险厄相薄的剑楯段；
- 训练/将领失误的比例亦存在实质异文。

因此 J4M-08 source profile 仍按《金镜》四库扫描实际文字运行，不能因为《汉书》文本更完整而静默补写。

## 仓库契约

- rules/jinjing_v4_military.json
  - source.scan_locator_version = c79-j4m-cadal-page-locators-v1
  - 每条 J4M rule 均含 scan_locator
  - J4M-08 含 J4M08-C79-01 textual_correction
- src/kintaiyi/jinjing_v4_military.py
  - 萑苇竹萧类 favored = 矛鋋
  - ratio = 弓弩三不当一矛鋋
- tests/test_jinjing_v4_military.py
  - 锁定 runtime 字形
- tests/test_jinjing_v4_military_record.py
  - 锁定十二法 locator 与 textual correction

## 未决

- 原书叶码尚未独立编录；不得把数字扫描页号改称叶码。
- NCL-06604 明钞本仍需逐条图像校字，可作为下一轮异文 witness，但不得覆盖四库 profile。
