# C74 三基 / 五福同宫关系显式层

日期：2026-10-05

## 1. 范围

C74 只处理《太乙统宗宝鉴》卷六 / 卷七见证中：

- 君基
- 臣基
- 民基
- 五福

四者彼此之间的六个同宫 pair。

唯一 runtime：

`src/kintaiyi/three_bases_wufu_conjunctions.py`

rule id：

`C74-THREE-BASES-WUFU-SAME-PALACE`

不在 C74：

- 不读取 C66 三基位置自动判断同宫；
- 不读取 C67 五福位置自动判断同宫；
- 不顺手并入天乙 / 地乙 / 直符 / 四神 / 大游 / 小游；
- 不把“五福与君基相冲”混进同宫规则。

## 2. 六个直接 pair

### 君基 + 臣基

君基条直接见：

- 君臣际会；
- 君治以道；
- 臣辅克忠；
- 国殷民安；
- 万物咸遂。

### 君基 + 民基

君基条直接见稳定核心：

- 务农桑；
- 安百姓；
- 出入有名；
- 使人以时；
- 巡狩省方、观民风。

电子转录末句存在 OCR / 句读不稳，因此 C74 不把不稳定尾句扩写成额外规则。

### 臣基 + 民基

臣基条直接见：

- 下贤者进朝；
- 民安其业；
- 政讼和平；
- 百姓丰厚。

## 3. 三个五福 pair 必须保留“双条来源”

五福与三基的关系在：

- 对应三基条；
- 五福条；

都出现，但细节并不完全相同。

C74 不把两段文字压成一个伪“统一原句”，而是分：

- `base_section`
- `wufu_section`
- `wufu_initial_conjunction`

三层保存。

### 君基 + 五福

君基条：

- 皇室巩固；
- 海宇肃清；
- 君国有嘉祥福瑞之庆。

五福条：

- 人君福寿祚享。

若显式：

`initial_conjunction=True`

再追加：

- 合生后储太子。

五福条另有“君基相冲”句，这是冲关系，不是同宫，因此只留：

`adjacent_non_same_palace_clause`

且：

`applied_in_c74=False`

### 臣基 + 五福

臣基条：

- 利为宰辅；
- 贵极人臣；
- 常亲帝座；
- 任其大事；
- 临大治乱皆致亨通；
- 所临分野人民丰稔；
- 世出英杰。

五福条：

- 福利辅宰。

若显式初交：

- 贤相当生贵人之家。

### 民基 + 五福

民基条：

- 其民富寿；
- 贤福之人生于民家。

五福条：

- 四民乐业；
- 天下熙和。

若显式初交：

- 其分富贵人生于白屋之家。

## 4. 显式关系契约

`same_palace` 必须由调用方显式给：

- True：已确认同宫；
- False：已确认不同宫；
- None：尚未检查。

C74 固定：

- `auto_position_lookup_used=False`
- `auto_same_palace_inference_used=False`

即使 C66 / C67 在同一积年计算出相同位置，也不会自动产生同宫断语。

## 5. “初交之始”不能默认

只对含五福的 pair 接受：

`initial_conjunction`

并且：

- same_palace=True, initial_conjunction=True → 追加初交断语；
- same_palace=True, initial_conjunction=None → 保持 pending；
- same_palace=True, initial_conjunction=False → 明确不追加；
- 非五福 pair 给该参数 → 拒绝；
- 不同宫却声明初交 → 拒绝。

## 6. 卷六 / 卷七见证边界

NGJ 与 CADAL 的相关核心 pair 意义一致，但编卷及个别 OCR / 句读有差异。

C74 固定：

`volume_status="witness_volume_variant"`

不复制两套关系公式。

## 7. C15 状态

三基旧字段现由：

- C66：位置周期；
- C74：三基 / 五福显式关系；

共同替代。

action：

`use_c66_c74_three_bases_layers`

五福旧字段现由：

- C67：来源分 profile 的位置；
- C74：与三基显式关系；
- C68：吉算受益对象（独立字段）；

分层处理。

`明五福太乙所主術` action：

`use_c67_c74_wufu_layers`

所有旧 flat 继续：

`migrate_whole=False`
