# 术语目录

本目录为太乙术语记录的稳定入口。算法说明保存在 [`rules/`](../rules/)，原典文本与异文证据保存在 [`sources/`](../sources/)；术语词条只说明概念和词形，并通过来源 ID、规则 ID 链接计算行为。

本次先建立规则备份结构；尚未迁移本地术语主库 `terminology.json`，以免把本地全库快照与本次算法变更混成一次未经核对的导入。



## 已知本地术语主库状态

用户确认：此前提供的《太乙紫庭祕訣》研易楼藏明钞本扫描内容，已经在本地术语主库中做过**初步整理**。

因此：

- 该扫描本不是“从未处理”的来源；
- 本地 `terminology.json` 中应存在与紫庭文本相关的初步术语抽取/归类结果；
- 当前 GitHub 仓库尚未迁移该本地术语主库，所以仓库内看不到这些旧术语条目；
- 后续恢复本地术语库时，应先把已有条目与研易楼明钞本页码/术名重新对齐，再决定哪些词条升级为稳定术语记录；
- 已有初步术语整理只能作为**索引与迁移线索**，不能在缺少页级来源定位时自动升级为 canonical 规则证据。

特别关注：

- 文昌九星值宫术；
- 文昌 / 始击变化；
- 三旗相关术语；
- 九宫贵神相关术语；
- 太乙九星及相关异名。

迁移时应保留“旧术语词形 / 来源页 / 规则 ID / 参校异文”四类信息，避免把现代整理词形与明钞本文字静默合并。


## C40 紫庭旧术语库恢复骨架

当前已建立：

`terminology/zitingjing-migration-map.json`

它不是新的术语主库，而是旧 `terminology.json` 的**恢复映射骨架**。

当前只固定：

- 旧词条可能的别名；
- 当前规则键；
- 当前来源证据等级；
- 待从旧术语库恢复的字段；
- 恢复优先级。

当前严禁自动填写：

- `manuscript_form`
- `source_page`

因为这两项必须由旧术语库或研易楼明钞本扫描页直接回填。

恢复顺序：

1. 文昌九星；
2. 三旗行宫；
3. 九宫贵神；
4. 太乙九星；
5. 文昌变化；
6. 始击变化。

前三项优先，因为它们仍直接影响紫庭来源/正文缺口。


## 《太乙金镜式经》卷四来源字形别名

已建立：

`terminology/jinjing-v4-aliases.json`

当前先登记影印证据明确、会影响 runtime 输入的来源字形：

- `太蔟` → 规范词形 `太簇`（J4M-03，四库扫描 p.130）

处理原则：

- 原文字形保留，不删除；
- runtime 可接受来源字形，但另返回规范词形；
- 同一神名的字形归一不得改变五行与规则；
- 近名异书规则不属于术语 alias，不得借此合并。


## NCL-06604《太乙金镜式经》明钞本历史状态

用户确认：NCL-06604《太乙金镜式经》明钞本在此前术语库整理阶段已经提供并做过扫描/初步处理。

当前仓库中的 C84/C86 不是首次取得该来源，而是**旧术语主库未完整迁移后，对既有扫描来源重新建立 GitHub 可追溯证据链**。

因此：

- 不得把“当前仓库此前无 NCL 页级记录”解释成“历史上从未扫描/处理过 NCL-06604”；
- 后续若恢复旧 terminology.json，应优先与 C86 已重建的 NCL p.55-p.64 卷四 locator 对账；
- 若旧术语库中已有 NCL 页码、术名字形或异文记录，应以“历史记录 vs C86 直接图像复核”方式合并，不能重复当成新发现。


## C99 “太簇”规范词形固定

项目规范词形正式固定为：

**太簇**

处理规则：

- 术语主名统一写“太簇”；
- runtime canonical 输出统一写“太簇”；
- 对外文档统一写“太簇”；
- “太蔟”只保留为来源字形 / 历史异文；
- 若 NCL-06604 或其他古本实际写“太蔟”，只登记 manuscript_form，不改变 canonical；
- 两种字形的五行属性均归一为金。

因此“太蔟/太簇”不再是待决 canonical 问题，只剩来源字形校勘问题。


## C101-C102 太簇 / 太蔟统一政策

规范词形固定为：

**太簇**

辞书与底本证据同时确认：

- “太蔟”读 tài cù；
- 辞书释为“亦作太簇”；
- 四库《太乙金镜式经》卷四 J4M-03 首例实际见“太蔟”。

因此：

- 太蔟不是 OCR 误字；
- 太蔟是辞书可证的传统异写；
- 太簇是项目唯一 canonical 名；
- 公共 GOD_ALIASES 接受 太蔟 -> 太簇；
- 十六神主表仍只有“太簇”，不建立第二条神名；
- 宫位仍为酉，五行仍为金；
- 古籍原字形继续保留在 source/manuscript 字段。


## C105 NCL-06604 旧术语记录对账

已建立 `terminology/ncl06604-legacy-reconciliation-map.json`。

该明钞本此前已经扫描并用于术语整理；当前映射用于旧 `terminology.json` 恢复后的去重与合并，不代表首次处理 NCL-06604。

原则：旧记录与 C86-C88 当前影像复核按 witness / rule / concept 对账；一致则合并来源链，冲突则并列保存，不重复建立同一来源。


## D8 八占 canonical 术语目录

已建立：

`terminology/d8-eight-divinations.json`

该文件不是旧本地 `terminology.json` 的替代品，而是当前仓库已经校勘规则的稳定术语入口，覆盖：

- D8-01 三才；
- D8-02 长短；
- D8-03 五音；
- D8-04 孤单；
- D8-05 内外；
- D8-06 多少；
- D8-07 阴阳厄会；
- D8-08 数有所主。

其中重点固定：

- 三才结构缺失与 classic 标签分层；
- 5 仅地，15/25/35 仅天+地；
- 五音正音/比音明确，尾数0按10；
- 杜塞数不强塞孤单；
- D8-04 孤单与 D8-07 阴阳厄会独立；
- D8-08 数有所主不得再接到 D8-03 五音。

后续恢复旧主术语库时，应以旧 term id / 原字形 / 页码与本目录的 rule_id 对账，而不是覆盖本目录的规则边界。


## T7 七术 canonical 术语目录

已建立：

`terminology/t7-seven-methods.json`

覆盖 T7-01..07：

- 临津问道；
- 狮子反掷；
- 白云卷空；
- 猛虎相拒；
- 雷公入水；
- 白龙得云；
- 回军无言（兼收“回车无言”异名）。

本目录重点保存七术的事件输入边界与 Mode A / Mode B 分层。需要敌起兵、敌下营日、敌初来时等事件输入的术，术语条目本身就声明 required_inputs，防止后续展示层或旧 API 用当前盘字段偷换。


## 公共 canonical 术语层

已建立：

`terminology/common-core.json`

该目录作为 D8 八占与 T7 七术共同依赖的公共术语真源，当前覆盖：

- 太乙九宫；
- 十六辰；
- 十六神及本五行；
- 吕申加位；
- 大神；
- 五态 / 五行生克关系；
- 大神火十二长生；
- 固有五行与所在宫五行的分层。

固定边界：

- 九宫与十六辰是不同坐标体系，十六辰投影九宫是有损映射；
- 中五有土五行，但无十六辰代表点；
- 和德=土、大炅=木、大武=土，辰太阳=土、戌阴主=土；
- 太簇是项目 canonical 词形，太蔟只作来源异写；
- 吕申加位统一为十六环顺行四格；
- 五态由统一五行生克函数生成，不维护第二套手抄表；
- 大神火十二长生与五态分层，墓不等于废；
- 主大将固有五行金、主参将水；七术 Mode B 仍必须取将实际所在九宫五行。

`terminology/d8-eight-divinations.json` 与 `terminology/t7-seven-methods.json` 已显式声明 `shared_catalog=terminology/common-core.json`，后续不得在各自目录复制一套公共表。


## 格局 source-profile 术语目录

已建立：

`terminology/patterns.json`

该目录不是把所有古籍格局合并成一套，而是明确区分：

- `jinjing_geju`：目标仓库《太乙金镜式经》source-limited 格局引擎；
- `tongzong_volume4`：《太乙统宗宝鉴》卷四并列 profile。

固定：

- `canonical_selected=null`
- `cross_source_merge=false`

`jinjing_geju` 术语覆盖：

- 掩、击、迫、囚、关、格、对；
- 提挟、挟闭；
- 四郭固、四郭杜；
- 执提、提格。

卷次边界：

- 前十一项主体来自《金镜》卷三；
- 执提、提格使用值事门，引用卷四。

机器主字段固定“**四郭杜**”；“四郭社”只作来源异文，不建立第二个 canonical 格局词条。

该目录继续复用 `terminology/common-core.json` 的九宫与十六辰坐标，不在格局目录另抄一套坐标表。


## 军事 P0 source-profile 术语目录

已建立：

`terminology/military-p0.json`

覆盖三项高风险近名术：

- 三门 / 推三门具不具；
- 五将 / 推五将发不发；
- 主客相关法。

来源并列：

- 四库《太乙金镜式经》卷四：J4M-01/02/03；
- 《景祐太乙福应经》卷四：JF4M-01/02/03；
- 《太乙统宗宝鉴》卷五：并列 source profile；
- C8：只记录组合/归一化角色，不是古籍公式来源。

固定：

- `canonical_selected=null`；
- `cross_source_merge=false`；
- `c8_formula_equivalent=false`。

特别边界：

- C8-L2 可以消费三门/五将上游事实，但不能冒充 J4M/JF4M 公式；
- C8-L3 主客动静与 J4M-03 主客相关法不是同一术，禁止互相替代；
- `CORE-WUJIANG-READY`“有效五将发不发”是项目跨层整合规则，杜塞取五将不发，但不能回写成《金镜》J4M-02 原文条件。


## 周期类术语目录

已建立：

`terminology/cycles.json`

覆盖：

- 三基：君基、臣基、民基（C66）；
- 五福太乙（金镜/统宗 C67 source profiles）；
- 大游太乙所在（金镜/统宗 C107）；
- 大游天目（金镜/统宗 C106）；
- 小游太乙所在（金镜/统宗 C103）；
- 四太乙：天乙、地乙、直符、四神（C64/C92）；
- 阳九 / 百六大小限（C36）；
- 太游阳九外卦 / 百六内卦行限（C38）。

周期层固定原则：

- 古法周期不改写 production 历法：太乙岁仍只在真实天文冬至交节瞬间换年；
- 金镜/统宗同名周期必须显式 source profile；
- 位置与同宫/灾应解释分层；
- 五福含中五，大游/小游八宫路径不入中五；
- 四太乙 canonical 名固定“天乙、地乙、直符、四神”，“值符”只作旧名/题名异写；
- 大游太乙、大游天目、阳九百六太游行限、重卦策数等属于不同术层，不得因为名称相近而合并。

早期 `rules/taiyi_v1.json` 中的五福 `project +250` 与大游 `jinjing_tongzong` 混源摘要已改为兼容隔离说明，正式真源改指 C67/C103/C106/C107 等 source-specific runtime。


## 仓库术语总索引

已建立：

`terminology/catalog-index.json`

当前 stable catalogs 共六组：

1. `common-core.json`：公共坐标/神名/五态；
2. `t7-seven-methods.json`：七术；
3. `d8-eight-divinations.json`：八占；
4. `patterns.json`：格局 source profiles；
5. `military-p0.json`：三门/五将/主客相关；
6. `cycles.json`：三基、五福、大小游、四太乙、阳九百六等周期。

另外单列：

- migration assets：紫庭旧术语恢复、NCL-06604旧记录对账；
- supporting assets：金镜来源字形 aliases、五福五域坐标等。

该索引**不是**旧本地 `terminology.json` 的替代主库。旧库重新取得后，按总索引中的 preferred term / aliases / rule_id / source profile 对账，再恢复旧 term id、原字形、页码和 notes；未知旧词条保持 unmapped，不猜归属。


## 紫庭 source-sensitive 正式术语目录

已建立：

`terminology/zitingjing.json`

六项固定分级：

- 太乙九星：`direct_text_verified`；
- 文昌九星：`catalog_attested_text_pending`；
- 文昌变化：`direct_text_verified`；
- 始击变化：`direct_text_verified`；
- 三旗行宫：`project_attribution_unverified`；
- 九宫贵神：`project_attribution_unverified`。

只有前三个 `direct_text_verified` 项中的太乙九星、文昌变化、始击变化允许注入 `primary_result`；文昌九星虽有《太乙紫庭秘诀》目录证据，但直接正文未取得；三旗行宫与九宫贵神目前只有统宗卷十直接文本，不能反标为紫庭 canonical。

`terminology/zitingjing-migration-map.json` 继续作为旧本地术语库恢复资产，负责未来回填 old term id / manuscript form / source page 等；它不再承担当前稳定术语消费入口。


## 五运六气 / 五音之数术语目录

已建立：

`terminology/wuyun-wuyin.json`

固定分层：

- 卷三 `C37-V3-WYUN`：明太乙统行五运六气术；
- 卷十 `C37-V10-WYUN`：明太乙岁会五运六气术；
- 卷十 `C39`：五运六气细表校勘；
- 卷三 `C37-V3-WYIN`：五音之数 / 五音之元。

五音之数只复用 `D8-03` 的“算数 -> 五音”共同核心；明确不使用 `D8-08` 数有所主。卷十五运配五音与卷三五音之数是相邻概念，但不是同一个输入层或source rule。

卷十C39目前：基础五运/六气/纪名表已校；天会/岁会/逆会/辐辏枚举仍有source variant；太乙天符需要九宫天符、三旗等结构化输入，不允许只凭年干生成伪公式。

## 卷九 / 卷十 source-rule 术语目录

已建立：

`terminology/volume9-10.json`

覆盖：

- C41 太游内外重卦 / 四象策数 / 内卦动爻；
- C42 历数长短 / 安居之代历数；
- C43 厄会行限；
- C44 国政革易 / 法令变更；
- C45 岁中灾发月日之期；
- C46 阴阳九厄水旱灾期。

卷次边界：

- C41/C42 按卷九直接术文登记；
- C43-C46 当前在线见证编在卷十，但项目旧参考长期标卷九，固定为 `witness_volume_variant`，不复制两套算法。

严格输入边界继续保留：C43完整六十甲子与神数证据、C44六神显式落点与长短和否、C45文昌/天目双目标两阶段、C46九段长度累计而非旧阈值算法。


## 显式关系层术语目录

已建立：

`terminology/relations.json`

覆盖：

- C65 天乙 / 地乙 / 直符条下直接同宫关系；
- C74 三基 × 五福同宫；
- C90 三基 × 天乙 / 地乙 / 直符；
- C91 三基 × 四神 / 大游 / 小游；
- C94 五福 × 四太乙同五福域解释；
- C113 五福 × 大游、五福 × 小游、四神 × 小游、大游 × 小游。

该目录固定一个重要系统边界：**位置层不自动生成关系层。**

也就是说：

- C64/C66/C67/C92/C103/C107 等位置结果即使数值上同宫；
- 关系 runtime 仍要求调用方显式传 `same_palace` / `same_wufu_domain`；
- 未列 pair 不按对称、类推或五行常识补断。

C74 的五福初交、C90/C91 的条件治理分支、C94 的 interpretation profile、C113 五福×小游的 virtue 分支都保留各自显式输入，不能被展示层自动省略。
