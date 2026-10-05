# C86 NCL-06604 明钞本卷四十二推法页级校勘

## 目标

C84 只确认了 NCL-06604 的书目与整卷扫描身份，当时因为页级访问不稳定，卷四十二推法仍保持 pending。

C86 通过 Wikimedia Commons 对该 PDF 的 page-specific 高分辨率预览逐页核图，已经直接定位到卷四，并完成十二推法的页级 locator 与第一批关键异文校勘。

底本：

- witness: NCL-06604
- edition: 明钞本
- 全书: 十卷四册
- 数字扫描: 124 页
- 来源: National Central Library
- 本轮直接核图范围: p.42-p.64

## 一、卷次边界

直接图像确认：

- p.42：明确见“太乙金镜卷第二”终结字样，卷二结束；
- p.43：明确见“太乙金镜卷第三”，卷三开始；
- p.54：明确见“太乙金镜卷第三终”；
- p.55：明确见“太乙金镜卷第四”，并列卷四目录，同页开始 J4M-01 正文；
- p.64：明确见“太乙金镜卷第四终”。

因此 NCL 明钞本卷四数字扫描范围可确定为：

**p.55-p.64**

## 二、十二推法 NCL locator

| rule_id | 四库 canonical 标题 | NCL 数字扫描页 |
|---|---|---|
| J4M-01 | 推三门具不具 | p.55-56 |
| J4M-02 | 推五将发不发 | p.56 |
| J4M-03 | 推主客相关法 | p.56-57 |
| J4M-04 | 推主客 | p.57-58 |
| J4M-05 | 推出师法 | p.58 |
| J4M-06 | 推陈兵向背 | p.59-60 |
| J4M-07 | 推制阵随地法 | p.60 |
| J4M-08 | 推随地制变 | p.60-61 |
| J4M-09 | 推太乙在天外地内法 | p.61-62 |
| J4M-10 | 推奇伏法 | p.62 |
| J4M-11 | 推太乙风云飞鸟助战法 | p.62-63 |
| J4M-12 | 推阵有风云气定胜负 | p.63-64 |

这些均为 NCL PDF 数字扫描页码，不是原书叶码。

## 三、标题校勘

### J4M-06

NCL 正文 p.59 明写：

**推陈兵向背**

与四库正文 canonical 一致，不是四库目录“推障向背法”。

结论：

- “障向背法”继续只作四库目录 alias；
- 明钞本为“陈兵向背”提供了独立正文见证。

### J4M-07

NCL p.60 正文写：

**推制阵随地法**

与四库正文一致，不是目录“推置阵随地法”。

### J4M-08

NCL p.60 正文写：

**推随地制变**

与四库正文一致，不是目录“推随地置变”。

因此 J4M-06/07/08 的正文标题在明钞本与四库正文相合，进一步说明“障/置/置变”属于目录层异题，不能反过来改 canonical body title。

### J4M-10

NCL p.62 正文写：

**推奇兵伏兵法**

这与四库目录 alias 相同，但与四库正文“推奇伏法”不同。

这是明确的 manuscript body-heading variant：

- NCL 明钞正文: 推奇兵伏兵法
- 四库正文: 推奇伏法
- 四库目录: 推奇兵伏兵法

处理：只登记 NCL manuscript reading，canonical_override=false。

### J4M-12

NCL p.63 正文写：

**推对阵有云气定胜负**

与四库目录 alias 相同，而不同于四库正文 canonical“推阵有风云气定胜负”。

同样作为 manuscript body-heading variant 保存，不改 J4M-12 canonical id/title。

## 四、J4M-08 “矛鋋”得到第二影印见证

NCL p.61 “萑苇竹萧”段直接可见：

- 兵器名：**矛鋋**
- 对应句：**弓弩三不当一**

因此 C79 对四库 CADAL p.136 的“矛锤 -> 矛鋋”纠正得到明钞本独立支持。

这意味着：

- “矛锤”更应视为后来的电子转录/OCR误读；
- NCL 与四库扫描在“矛鋋”这一字形上一致；
- 但《金镜》本段与《汉书》《福应经》的兵种/比例结构差异仍然存在，不因字形一致而消失。

## 五、J4M-09 的实质异文：1宫

NCL p.61-p.62 明写：

- “太乙在 **一八三四宫** 者为地内宫助主人”
- “太乙在 **九二七六宫** 者为天外宫助客”

因此明钞本 NCL-06604 的宫组是：

- inner = [1, 8, 3, 4]
- outer = [9, 2, 7, 6]

这与《景祐太乙福应经》《太乙统宗宝鉴》已有 variant 一致，但与当前四库卷四正文 profile 不同：

- 四库 canonical inner = [8, 3, 4]
- NCL manuscript inner = [1, 8, 3, 4]

处理原则：

**NCL 的 1宫只证明另一传本系统确有 [1,8,3,4]，不能静默反填 jinjing_siku_volume4。**

机器规则中明确 canonical_override=false。

## 六、仍待精核

本轮暂不强判：

- J4M-03 首例“太蔟 / 太簇”在 NCL p.57 的精确字形；
- J4M-11 标题“助战”字形与个别句读；
- 十二法全段逐字异文。

原因不是页码未知，而是当前第一轮只登记视觉上无歧义的关键项；疑难字必须在更高倍率下再判。

## 七、仓库状态

rules/jinjing_v4_military.json：

- NCL witness 升级为 volume4_scan_range_and_j4m_page_locators_verified_readings_in_progress
- evidence level: page_collated_for_volume4_j4m_locators_with_selected_readings
- 新增 volume_boundaries
- 十二条均新增 ncl_scan_locator
- J4M-06/07/08/09/10/12 新增 manuscript_readings["NCL-06604"]
- source.ncl_volume4_collation_version = c86-ncl06604-v4-j4m-locators-v1

测试锁定：

- 卷三终 p.54；
- 卷四起 p.55；
- 卷四终 p.64；
- 十二条 locator；
- J4M-08 矛鋋；
- J4M-09 NCL 含1宫但四库 canonical 不变；
- J4M-10/J4M-12 标题 variant 不覆盖 canonical。

## 结论

C84 的“页级 pending”已被 C86 对卷四范围 supersede。

现在 NCL-06604 不再只是书目级第二 witness，而是：

**已完成卷四页级定位、已完成关键异文第一轮校勘的独立明钞本 witness。**
