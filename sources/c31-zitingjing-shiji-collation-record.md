# C31 《太乙紫庭经》始击岁干×五行校勘与剩余三项证据等级

## 1. 〈始击变化〉直接主来源

识典《太乙紫庭经》〈始击变化〉：

https://www.shidianguji.com/book/SDZJ0646/chapter/1kg32q85u6811

C31 将其中“十干岁 × 始击五行”的灾应整理成 5 组 × 5 行，共 25 个正规化元素槽位：

- 甲乙
- 丙丁
- 戊己
- 庚辛
- 壬癸

## 2. OCR 校字原则

主来源在线 OCR 存在明显字符误识，不能直接按机器字面固化。

### 戊己岁

主在线 OCR 首项作“水为始击”，但同组末尾另有水项，且参校：

- 《太乙秘书》
- 《太乙统宗宝鉴》卷六

均作“木为始击”。

因此 C31：

- 保留 `witness_label="水"`
- 正规化 `element="木"`
- 标记 `status="ocr_corrected_by_collation"`

这是 OCR 校字，不是把参校本提升为主来源。

### 壬癸岁

主在线 OCR 末项作“王为始击，中国有兵”。

《太乙秘书》、统宗卷六及另一识典见证均作“土为始击”。

因此：

- 保留 `witness_label="王"`
- 正规化 `element="土"`
- 同样记录校勘见证链。

### 甲乙岁土项

“土为始击”接在甲乙火项后的下一段，并非丙丁组。

经参校后甲乙组恢复五行齐备。

## 3. 真异文与 OCR 误识必须分开

庚辛岁土为始击的夏季灾应：

- 当前《太乙紫庭经》在线见证：夏大旱
- 《太乙秘书》及统宗参校：夏大水

这不是简单单字 OCR 纠错能够确定的内容差异。

固定：

`resolution="preserve_both_no_silent_merge"`

不得按“多数见证”直接覆盖主来源读法。

## 4. 当前表状态

`shiji_year_element_collation()`：

- normalized_row_count = 25
- normalization_complete = True
- OCR corrections = 2
- textual variants 保留独立列表

`shiji_changes_primary_core()` 当前状态：

`detailed_year_stem_element_table_status="collated_with_preserved_variants"`

## 5. 文昌九星

当前直接证据等级：

`catalog_attested_text_pending`

现有《太乙紫庭秘诀》现代整理本目录可见：

“附太乙文昌九星值宫术”

但尚未取得可逐条校读的该附篇正文。

因此仍不得生成 `primary_result`。

## 6. 三旗行宫 / 九宫贵神

当前证据：

- 已查《太乙紫庭秘诀》十二卷及附录目录，未见同名题目；
- 《太乙统宗宝鉴》卷十有直接可定位文本。

因此两项的《太乙紫庭经》归属状态统一为：

`project_primary_attribution_unverified`

不能再写成已证实“紫庭 canonical”。

统宗卷十继续作为直接参校来源，而不是反填紫庭 primary。
