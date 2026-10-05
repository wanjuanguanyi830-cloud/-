# C61 C15 unported catalog 全局一致性清扫

日期：2026-10-05

## 1. 目标

C61 不新增术法 runtime。

本批只清扫 C15 的 67 个 legacy 顶层字段，修正已经与当前来源研究不一致的：

- pending；
- source confidence；
- source scope；
- migration action；
- “已有来源”与“已有 runtime”混淆。

## 2. 清扫结果

67 个字段继续完整覆盖。

当前 layer 统计：

- canonical: 31
- source_variant: 16
- derived: 18
- pending: 2

严格 pending 只剩：

- `推太乙當時法`
- `文昌九星`

这里的 pending 是“直接来源/正文条件仍不足以选择 canonical”，不是“尚未写代码”的同义词。

## 3. 巡狩术

《太乙统宗宝鉴》目录明确列于卷五。

卷五正文直接见：

- 太乙与天目在四维之岁，为巡狩之期；
- 出何方，以天目/文昌所临决之；
- 四维出方见证为：
  - 乾 → 东方；
  - 艮 → 南方；
  - 巽 → 西方；
  - 坤 → 北方；
- 行期另提太乙囚、挟、格、对条件。

因此 `明天子巡狩之期術` 从 source pending 升为：

- layer: canonical
- source_scope: `tongzong_volume5_direct`
- action: `source_verified_split_runtime_next`
- source_confidence: high
- migrate_whole: false

“来源已核”不等于完整 runtime 已实现。

## 4. 君基 / 臣基 / 民基 / 五福

《太乙统宗宝鉴》目录和正文可直接定位：

- 明君基太乙所主术；
- 明臣基太乙所主术；
- 明民基太乙所主术；
- 明五福太乙所主术；
- 明五福吉算所利术。

不同在线见证在卷六 / 卷七编次有差异，因此统一记：

`tongzong_volume6_7_witness_variant_direct`

不复制两套公式。

直接正文已经可见三基、五福的：

- 身份义；
- 周法 / 小周；
- 起点与顺行；
- 与其他神同宫所主；
- 五福五宫 / 45年行一宫等结构。

但这些仍需逐条拆成独立 runtime，旧 flat 字段不得直接搬运。

## 5. 天乙 / 地乙 / 直符

卷七目录直接见：

- 天乙金神；
- 地乙土神；
- 直符火神。

因此旧字段：

- `明天乙太乙所主術`
- `明地乙太乙所主術`
- `明值符太乙所主術`

升级为：

- layer: canonical
- source_scope: `tongzong_volume7_direct`
- action: `source_verified_split_runtime_next`
- source_confidence: high

旧字段题名与正文“金神 / 土神 / 火神”的命名差异只作为题名异文保留。

## 6. 十精状态同步

C57 / C58 / C59 已完成十精云气的：

- 显式合会层；
- 初移宫云色 / 天气观察层；
- 太乙数天气层。

因此 C15 中十精旧字段的备注不再写“云气层未实现”。

但旧 flat 位置与旧 `yunqi` 综合 wrapper 仍不得迁入 canonical。

## 7. 边界

本批没有把任何 `source_verified_split_runtime_next` 改写成“runtime implemented”。

后续选择实现目标时，应优先：

1. 直接正文清楚；
2. 输入边界可显式表达；
3. 不依赖尚未迁入的整盘隐式状态；
4. 可单独测试。

巡狩术最符合这一条件。


## 8. C62–C69 后续状态同步

C61 当批统计随后被各 runtime 分批推进。

截至 C69：

- canonical: 32
- source_variant: 16
- derived: 18
- pending: 1

唯一严格 pending：

- `文昌九星`

原严格 pending `推太乙當時法` 已在 C69 找到《太乙金镜式经》卷一直接同题正文，并建立部分 runtime：

- 十日干朝暮天乙治神；
- 魁罡二辰禁居；
- 天乙及前五后六天将直接主事 / 吉凶。

截至本记录首次整理时，C69 明确：

`complete_current_time_formula=False`

当时的未接通状态已由 C118 与 C69B 后续收口：C69B 现可在显式输入且 C118 日度可算时完成加时、贵人落地、顺逆布将与实体查将。当前 `complete_current_time_formula=False` 仅表示公历日期到节气日序、朝暮自动判定和单一坐标入口未统一；虚宿未定值继续限制跨界日期。

其他 C61 source-verified 项后续已实现：

- 巡狩 → C62；
- 天乙 / 地乙 / 直符位置 → C64；
- 三神同宫 → C65；
- 君基 / 臣基 / 民基位置 → C66；
- 五福位置 → C67（显式统宗 / 金镜 profile）。

五福吉算继续等待 C68 的干净数列见证。


## 9. C70 后续状态同步

截至 C70，C15 的67个 legacy 顶层字段已经全部完成“来源治理层”分类：

- canonical: 32
- source_variant: 17
- derived: 18
- pending: 0

这里的 `pending=0` 只表示：

- 不再有字段处于“连来源类别都无法判定”的严格 pending；
- 每个旧字段都已被分配到 canonical / source_variant / derived 三类之一。

它不表示所有细节公式都已完成。

仍存在明确的局部 pending / unresolved：

- `文昌九星`：紫庭附篇目录已证，但正文未取得；统宗 NGJ 已由 C70 独立实现；
- `明五福吉算所主術`：来源已核，但数列需更干净见证；
- C69 完整“日度加时位”上游仍未接通；
- 三旗 / 九宫贵神的紫庭归属仍未证。

### 文昌九星为何不再是 strict pending

旧 `config.wenchang_nine_stars` 本身直接注明来源：

`《太乙统宗宝鉴》卷六`

C70 又取得卷六 NGJ 直接见证：

- 每星30年；
- 大周2700；
- 小周270；
- 宫率30；
- 年干落宫表。

因此 legacy 字段的来源已经明确，可以归：

`source_variant`

而不是继续写：

`pending`

但《太乙紫庭秘诀》附篇：

`附太乙文昌九星值宫术`

仍：

`catalog_attested_primary_text_pending`

两条状态必须并存，不能互相覆盖。
