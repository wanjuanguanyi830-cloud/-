# 《太乙金镜式经》卷四军事十二法来源记录

## 定位

本记录对应四库本《太乙金镜式经》卷四连续军事十二法，独立 source profile：

- ruleset: `jinjing-siku-v4-military-12`
- source profile: `jinjing_siku_volume4`
- runtime: `src/kintaiyi/jinjing_v4_military.py`
- machine rules: `rules/jinjing_v4_military.json`
- J4M-03 variant catalog: `rules/j4m03_nayin_variants.json`

本层不得自动并入 C8 `volume5_strict`，也不得以《太乙统宗宝鉴》、现代重构材料或旧代码近名函数静默覆盖。

## 正文 canonical 顺序

1. J4M-01 推三门具不具
2. J4M-02 推五将发不发
3. J4M-03 推主客相关法
4. J4M-04 推主客
5. J4M-05 推出师法
6. J4M-06 推陈兵向背
7. J4M-07 推制阵随地法
8. J4M-08 推随地制变
9. J4M-09 推太乙在天外地内法
10. J4M-10 推奇伏法
11. J4M-11 推太乙风云飞鸟助战法
12. J4M-12 推阵有风云气定胜负

正文小标题为 canonical；目录异题只作 alias。

## 当前完成状态

十二条均已建立完整 source-specific runtime：

- J4M-01 `sanmen_jubu()` / `zhimen_from_cycle_count()`
- J4M-02 `wujiang_fabu()`
- J4M-03 `j4m03_eye_element_from_god()` / `zhuke_xiangguan()`
- J4M-04 `zhuke_fa()`
- J4M-05 `chushi_fa()`
- J4M-06 `chenbing_xiangbei()`
- J4M-07 `zhizhen_suidi()`
- J4M-08 `suidi_zhibian()`
- J4M-09 `taiyi_tianwai_dinei()`
- J4M-10 `qifu_fa()`
- J4M-11 `fengyun_feiniao_zhuzhan()`
- J4M-12 `yunqi_dingshengfu()`

即 **12 complete / 0 partial / 0 pending**。

## J4M-03：日计二目纳音的重新校勘

### 1. 《金镜》卷四正文

《太乙金镜式经》卷四“推主客相关法”写：

- 客关得主人则客胜
- 主人关得客则主胜
- “皆用日计纳音以决之”
- “所谓关者，取五行相制之道”

并给两例，均直接以二目所临十六神的五行相制判胜负。

### 2. 《景祐太乙福应经》异文

对应“释主客相关”现存转录作：

“皆用曰计二目纳音以决之”

其中“曰”高度疑似 OCR 的“日”；关键是比《金镜》多出“二目”二字，因此应理解为：

**日计二目纳音**

而不是“另取一个当天干支纳音五行，再与二目比较”。

### 3. 《太乙淘金歌》直接解释

“定胜负”歌诀写：

- 二目纳音何以定
- 主来克客主军赢
- 客克主兮主不利
- 若也同音二阵平（三阵平为另一转录异文）

注释进一步明言：

**以二目纳音决之，取五行生克为用。**

并直接列十六神五行：

- 金：武德、太簇、阴德
- 木：吕申、高丛、大炅
- 水：大义、地主
- 火：大神、大威
- 土：和德、太阳、天道、大武、阴主、阳德

另举：

- 主目高丛木、客目阳德土 → 木克土 → 主胜客败
- 客目阳德土、主目武德金 → 金土相生 → 战必和解

因此 J4M-03 canonical runtime 现在按“日计主客二目所临神的五行关系”运行。

### 4. 主目/客目与“天目”多义

《金镜》卷二“上下二目”配对义明确：

- 上目 = 始击 = 属客
- 下目 = 文昌 = 属主

因此 J4M-03 正文例中的：

- 地目 → 本条配对义中的主目 / 文昌侧
- 天目 → 本条配对义中的客目 / 始击侧

但“天目”在太乙文献其他位置又可作文昌或二目总名，故 runtime 接口禁止把“天目/地目”直接作为参数名，统一使用：

- `host_eye_*`
- `guest_eye_*`

### 5. canonical 判法

- 客目五行克主目五行 → 客关得主人 → 客胜
- 主目五行克客目五行 → 主人关得客 → 主胜
- 无相制关系 → 《金镜》本条不强宣主客胜负

《淘金歌》的：

- 同音 → 二阵平
- 相生 → 和解

保存在 `collation_hint`，不覆盖《金镜》本条 winner。

### 6. 旧 day_nayin_element 模型作废

旧 runtime 曾把“日计纳音”误建模成一个独立 `day_nayin_element`。

现保留该参数只为 API 兼容：

- `legacy_input_ignored`
- 不参与判定
- 不得再据它生成“主关/客关”

## 通用六十甲子纳音：只作背景，不替代 J4M-03

《梦溪笔谈》等古籍所述一般纳音法包括：

- 六十律旋相为宫
- 一律含五音
- 十二律纳六十音
- 同类娶妻
- 隔八生子
- 五行先仲而后孟，孟而后季

这是六十甲子纳音的通用生成理论。

但 J4M-03 的古代太乙参校文本已经直接把“二目纳音”落实为二目所临十六神的五行生克，因此 **不能再因为通用纳音法存在，就额外给 J4M-03 塞入一个当天干支六十甲子纳音变量**。

## 现代《太乙数纳音体系（修正版）》单独建 variant

用户提供的现代材料明确说明其第四章太乙纳音应用体系属于作者自行构建 / 无师自通的现代重构。

现登记：

`J4M03-MODERN-LIUNIAN-NAYIN`

profile：

`modern_liunian_nayin_2026`

只保存该材料明确支持的结构：

- 太乙五音顺序：宫徵羽商角
- 五音纳天干：宫徵羽商角 → 甲丙戊庚壬，并配阴干
- 星神本五行 → 五音
- 星神所落地支/四维 → 律吕
- 五音与律吕合成星神纳音
- 引入变五行与按日干改变的五音顺序
- 每个星神可得本/变两个纳音
- 本五行与变五行所得纳音可以比较
- 四计均可使用，但历法输入随计改变
- 可用于取象、能量比较、取数、方位、应期等

该 variant 当前是：

`implemented_modern_variant`

runtime：

- `kintaiyi.modern_nayin_variant.modern_star_base_nayin()`
- `kintaiyi.modern_nayin_variant.modern_day_tone_sequence()`
- `kintaiyi.modern_nayin_variant.modern_star_transformed_nayin()`
- `kintaiyi.modern_nayin_variant.compare_modern_nayin_elements()`

实现边界：

- 十二地支到十二律采用古典律历标准映射，作为材料所称“十二地支与十二律配合”的背景依赖；
- 四维不会自动换算，只有显式 `dimension_mode=branch_proxy` 时才使用材料列出的乾→亥、艮→寅、坤→申、巽→巳；
- 日干只返回材料明确给出的变音顺序，不自动替作者决定“某星神由该序列取得哪一个变五行”；
- 本/变纳音比较只返回五行关系，不自动生成吉凶或胜负。

材料中的示例“太乙木→角音→纳壬；落子→壬子→桑柘木”已作为 runtime 单元测试固定。

即使已经可运行，也仍然：

- `canonical=False`
- `source_class=modern_reconstruction`

不得据此声称《金镜》“日计二目纳音”原义就是现代“双纳音”体系。

## legacy wc_n_sj 单独隔离

旧 `kentang2017/kintaiyi::wc_n_sj` 另作：

`J4M03-LEGACY-WCNSJ`

其额外行为：

- 独立日计纳音五行等于主/客目五行 → 标主关/客关
- 主将是否与太乙同宫 → 改写主客断语
- 比和 / 生我 / 我生 → 判和

这些均不得自动进入 J4M-03 canonical。

## 其他关键边界

- J4M-03 ≠ J4M-04
- J4M-07 ≠ J4M-08
- 《金镜》J4M-09 ≠ 《统宗》同名术
- J4M-11 / 12 外部观测不得由盘内事实伪造
- modern reconstruction、legacy runtime、ancient canonical 三层必须分离

## J4M → C8 显式 adapter

`src/kintaiyi/jinjing_v4_c8_adapter.py`

只接受显式：

`source_profile=jinjing_siku_volume4`

当前映射：

- J4M-01 `three_doors_ready` → C8-L2
- J4M-02 `five_generals_released` → C8-L2
- J4M-04 → `j4m_overlay.host_guest_full`

J4M-03 虽已 canonical complete，但 C8 当前没有独立“关法” layer，因此仍不进入 adapter，不得硬塞进 C8-L3 或 D8-06。

默认 `junshi_zhanlue(...)` 仍保持：

`source_profile=volume5_strict`
