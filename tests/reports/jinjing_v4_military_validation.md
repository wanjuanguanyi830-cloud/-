# J4M 《太乙金镜式经》卷四军事十二法验证报告

日期：2026-10-05

## 总体状态

- ruleset: `jinjing-siku-v4-military-12`
- source profile: `jinjing_siku_volume4`
- rule ids: `J4M-01..J4M-12`

当前：

- **12 条 complete source-specific runtime**
- **0 条 partial**
- **0 条 pending**

## J4M-03 重新校勘结论

此前状态：

`implemented_partial_source_specific`

原因是把《金镜》“皆用日计纳音以决之”理解成“还缺一个独立当天干支纳音输入”。

重新检索古籍后，该理解已修正。

### 证据链

1. 《太乙金镜式经》卷四：
   - 客关得主人 → 客胜
   - 主人关得客 → 主胜
   - “皆用日计纳音以决之”
   - “所谓关者，取五行相制之道”

2. 《景祐太乙福应经》卷四“释主客相关”：
   - 现存转录作“皆用曰计二目纳音以决之”
   - “曰”视为 OCR 可疑字
   - 关键补字是“二目”

3. 《太乙淘金歌》“定胜负”：
   - “二目纳音何以定”
   - “以二目纳音决之，取五行生克为用”
   - 明列十六神五行
   - 主目克客 → 主胜
   - 客目克主 → 客胜
   - 同音 → 二阵平（另有“三阵平”转录）
   - 相生例 → 战必和解

4. 《太乙金镜式经》卷二：
   - 上目 = 始击 = 属客
   - 下目 = 文昌 = 属主

由此把 J4M-03 解释为：

**日计主客二目所临十六神，以其五行关系决“关”。**

不再额外引入一个独立的六十甲子“当天纳音五行”。

## J4M-03 runtime

入口：

- `j4m03_eye_element_from_god()`
- `zhuke_xiangguan()`

### 十六神五行参校表

金：

- 武德
- 太簇
- 阴德

木：

- 吕申
- 高丛
- 大炅

水：

- 大义
- 地主

火：

- 大神
- 大威

土：

- 和德
- 太阳
- 天道
- 大武
- 阴主
- 阳德

### canonical 判法

- 客目克主目 → `relation=客关得主人` → `winner=客`
- 主目克客目 → `relation=主人关得客` → `winner=主`
- 无相制 → `winner=None`

现：

- `fully_computable=True`
- `status=ok`

### 非 canonical 参校提示

《淘金歌》：

- 同音 → 二阵平
- 相生 → 和解

只写入：

`collation_hint`

且：

`canonical_override=False`

因此不会把后出参校文本的“和/平”强行改成《金镜》本条 winner。

## “天目”多义防错

测试锁定：

- 本条主目：文昌 / 下目 / 地目（配对义）
- 本条客目：始击 / 上目 / 天目（配对义）

不允许仅凭“天目”二字自动判其为文昌或始击。

runtime 参数统一使用：

- `host_eye_*`
- `guest_eye_*`

## 旧 day_nayin_element 已降为兼容字段

旧接口：

`day_nayin_element`

现状态：

`legacy_input_ignored`

它不再参与 J4M-03 胜负。

测试保证即使传入该字段，也不会改变由二目五行相制得到的结果。

## 通用纳音与 J4M-03 分离

一般六十甲子纳音古法如《梦溪笔谈》所述：

- 六十律旋相为宫
- 一律含五音
- 十二律纳六十音
- 同类娶妻
- 隔八生子
- 仲 / 孟 / 季递传

该背景不等于 J4M-03 要额外计算一个当天六十甲子纳音。

J4M-03 已由太乙内部“二目纳音”参校直接解释。

## 现代《太乙数纳音体系（修正版）》variant

新增机器表：

`rules/j4m03_nayin_variants.json`

modern profile：

`modern_liunian_nayin_2026`

状态：

`reference_only_not_canonical`

材料明确支持并记录：

- 宫徵羽商角
- 五音纳甲丙戊庚壬
- 星神本五行转五音
- 星神所落地支/四维转律吕
- 合成星神纳音
- 变五行
- 日干五音顺序
- 每个星神两个纳音
- 本/变纳音比较
- 四计可用但历法输入随计改变

同时机器规则锁定：

- 不能据此声称《金镜》原义就是现代双纳音体系
- 不能把现代日干变音顺序写入 J4M-03 canonical
- 不能用 modern variant 改写 canonical winner

## legacy wc_n_sj variant

另存：

`J4M03-LEGACY-WCNSJ`

状态：

`quarantined`

禁止进入 canonical。

## catalog 状态

`j4m_low_dependency_catalog()`：

- implemented: `J4M-01..J4M-12`
- partial: `[]`
- pending: `[]`

## C8 边界

J4M-03 现在虽已 complete，但仍不进入 J4M → C8 adapter。

原因已从旧的“partial”改为：

**C8 当前没有独立关法 layer。**

禁止：

- 硬并入 C8-L3 主客动静
- 用它覆盖 D8-06 多少占胜负
- 自动加入默认 `volume5_strict` 总胜负链

## CI

J4M-03 runtime / metadata / variant catalog 修正后：

GitHub Actions run `37231852841`：

- conclusion: `success`
- result: **464 passed in 0.77s**

较早 run 199 / 203 / 204 的 J4M 红灯主要来自提交顺序中旧测试仍期待 J4M-03 为 partial；更新锁定测试后恢复全绿。

## 阶段结论

J4M 卷四军事十二法 source layer 现可正式视为：

**12 / 12 complete**

同时保留三层隔离：

1. ancient canonical / ancient collation
2. modern reconstruction
3. legacy implementation

后续不应再以 modern 或 legacy 反写 canonical。
