# 现代《太乙数纳音体系（修正版）》来源记录

## 定位

本记录对应用户提供的现代材料《太乙数纳音体系（修正版）》第四章“关于太乙数中律吕和纳音体系的系统性总结”。

该体系独立于古籍 canonical：

- profile: `modern_liunian_nayin_2026`
- variant id: `MODERN-LIUNIAN-NAYIN`
- runtime: `src/kintaiyi/variants/modern_liunian_nayin.py`
- machine rules: `rules/variants/modern_liunian_nayin.json`

材料作者明确说明该套太乙纳音应用属于自己构建 / 无师自通的现代体系，因此 source class 固定为：

`modern_reconstruction`

不得改写《太乙金镜式经》J4M-03 或其他古籍规则。

## 材料明确支持的结构

### 太乙五音

材料采用：

- 宫 → 土
- 徵 → 火
- 羽 → 水
- 商 → 金
- 角 → 木

顺序为：

`宫徵羽商角`

### 五音纳天干

材料写：

`宫徵羽商角纳甲丙戊庚壬`

并以太乙木为例：

- 太乙为木
- 木为角音
- 角纳壬
- 落子取阳干壬
- 得壬子
- 壬子为桑柘木

runtime 将这一示例作为固定验收。

### 地支 / 律吕

材料明确使用“十二地支与十二律配合”。

runtime 采用古典律历标准映射作为背景依赖：

- 子 黄钟
- 丑 大吕
- 寅 太簇
- 卯 夹钟
- 辰 姑洗
- 巳 仲吕
- 午 蕤宾
- 未 林钟
- 申 夷则
- 酉 南吕
- 戌 无射
- 亥 应钟

该背景只用于构造现代 profile，不进入 J4M-03 canonical。

### 四维

材料同时提到四维存在不同取法，并给出“按照历法”一组：

- 乾 → 亥
- 艮 → 寅
- 坤 → 申
- 巽 → 巳

因此 runtime 默认不自动处理四维；只有显式：

`dimension_mode=branch_proxy`

才使用这组映射。

### 日干变音顺序

材料明确列出：

- 甲己：宫徵羽商角
- 乙庚：徵羽商角宫
- 丙辛：羽商角宫徵
- 壬丁：商角宫徵羽
- 癸戊：角宫徵羽商

runtime 只返回该顺序。

材料没有写成唯一算法说明“某一星神本五行在当天如何由该顺序自动取得唯一变音”，所以该步不自动补算。

### 本 / 变两个纳音

材料说明：

- 星神原本五行为“本五行”
- 可有“变五行”
- 本五行与变五行所得出的纳音可以比较、衬托
- 每个星神可以有两个纳音

runtime 因此提供显式 `transformed_tone` 的变纳音构造，但不自行推导 transformed tone。

### 使用范围

材料明确说：

“他四计都可以用，但相对应的历法是要改变的”。

因此 profile scope 为：

- 年计
- 月计
- 日计
- 时计

但当前 runtime 只实现纳音构造本身，不替各计补完整历法上游。

## 当前 runtime

- `modern_star_base_nayin()`
- `modern_day_tone_sequence()`
- `modern_star_transformed_nayin()`
- `compare_modern_nayin_elements()`

关系比较只返回：

- 比和
- 一生二 / 二生一
- 一克二 / 二克一

材料未给出统一的“这些关系如何自动转为吉凶/胜负”公式，因此 `verdict=None`。

## 与 J4M-03 的关系

二者只在“纳音”主题上相关。

J4M-03 canonical：

- 古籍来源
- 日计主客二目所临神五行
- 以五行相制判关胜负

本 profile：

- 现代重构
- 面向星神本/变纳音
- 四计均可扩展使用

所以本 profile 不是 J4M-03 variant，也不进入 J4M → C8 adapter。
