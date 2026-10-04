# 太乙术重构 Work 持久规格（C1–C7）

> 目的：Work/新对话可能无法读取原聊天。本文件是仓库内的持久化执行依据。实施前先读本文件；不要依赖聊天上下文。
>
> 最终写入仓库：`wanjuanguanyi830-cloud/-`
>
> 参考仓库：`kentang2017/kintaiyi`，仅用于查旧实现和兼容接口，不作为最终写入目标。

## 0. 总原则

- 不存在“天游太乙”，不要新增。
- canonical / source_variant / derived / pending 分层；OCR/电子转录异常不得覆盖互校后的 canonical。
- 九宫、十六辰/十六神、四太乙十二宫、五福五域、十二支必须分类型。
- 新核心为唯一真源；旧 API 仅做 wrapper/compat facade。
- 缺事件输入时返回 `computable=False` + `missing_inputs/reason`，不得拿当前日期、客大将等别的字段偷换。
- Python >=3.10；保持现有测试/CLI/UI尽量可用。
- 建议提交顺序：C1 common → C2 八占 → C3 七术 → C4 周期 → C5 四太乙 → C6 compat → C7 pan v2。

## 1. C1 公共规则

建议：`src/.../taiyi_common.py` + `tests/test_taiyi_common.py`。按目标仓库现有包结构调整路径。

### 九宫

| 宫 | 卦 | 代表辰 | 五行 | 阴阳 |
|---|---|---|---|---|
|1|乾|乾|金|阴|
|2|离|午|火|阴|
|3|艮|艮|土|阳|
|4|震|卯|木|阳|
|5|中|无十六辰|土|None|
|6|兑|酉|金|阴|
|7|坤|坤|土|阴|
|8|坎|子|水|阳|
|9|巽|巽|木|阳|

显式接口：`sector_to_nine_palace`、`nine_palace_to_trigram`、`nine_palace_representative_sector`、`nine_palace_element`。5宫可有土五行，但不能参与吕申加位。

### 十六宫 / 十六神

环：子→丑→艮→寅→卯→辰→巽→巳→午→未→坤→申→酉→戌→乾→亥→子。

神：子地主、丑阳德、艮和德、寅吕申、卯高丛、辰太阳、巽大炅、巳大神、午大威、未天道、坤大武、申武德、酉太簇、戌阴主、乾阴德、亥大义。

本五行：地主水、阳德土、和德土、吕申木、高丛木、太阳土、大炅木、大神火、大威火、天道土、大武土、武德金、太簇金、阴主土、阴德金、大义水。

必须修正旧表：和德木→土；大炅火→木；大武金→土。关键：辰太阳=土，戌阴主=土。

有损映射：亥子→8；丑艮→3；寅卯→4；辰巽→9；巳午→2；未坤→7；申酉→6；戌乾→1。

### 吕申加位 R-LS-01

吕申寅、大神巳，固定 +4：

子→卯，丑→辰，艮→巽，寅→巳，卯→午，辰→未，巽→坤，巳→申，午→酉，未→戌，坤→乾，申→亥，酉→子，戌→丑，乾→艮，亥→寅。

九宫代表辰输入：1→艮，2→酉，3→巽，4→午，6→子，7→乾，8→卯，9→坤；5不可算。

### 五行关系 R-QI

`GENERATES={木:火,火:土,土:金,金:水,水:木}`
`OVERCOMES={木:土,土:水,水:火,火:金,金:木}`

`qi_relation(subject, environment)`：
- 同类=旺/比和
- environment生subject=相/生我
- environment克subject=死/克我
- subject克environment=囚/我克
- subject生environment=休/我生

25格 state：
- 木：木旺 火休 土囚 金死 水相
- 火：木相 火旺 土休 金囚 水死
- 土：木死 火相 土旺 金休 水囚
- 金：木囚 火死 土相 金旺 水休
- 水：木休 火囚 土死 金相 水旺

不要手抄 `_WX_REL`。

### 固有五行 vs 所在宫五行

太乙木、始击火、文昌土、主大将金、主参将水、客大将水、客参将木。修旧表主将土→金、主参金→水。七术 Mode B 用将所在九宫五行，不用固有五行；对象同时保留 `intrinsic_element` 与 `palace_element`。

### 大神火十二长生（derived）

寅长生、卯沐浴、辰冠带、巳临官、午帝旺、未衰、申病、酉死、戌墓、亥绝、子胎、丑养；艮巽坤乾=None。

## 2. C2 八占

建议独立 `eight_divinations.py`。

### D8-01 三才
`unit=n%10`；天=`n>=10`；地=`unit>=5`；人=`unit%5!=0`。

classic tags：
- 无天 1..9
- 无地 1,2,3,4,11,12,13,14,21,22,23,24,31,32,33,34
- 无人 10,20,30,40
- 三才俱足 16,17,18,19,26,27,28,29,36,37,38,39
- 杜塞 5,15,25,35

structural missing 与 classic tags 分开。

### D8-02 长短
canonical：11以上长，<=10短。长=缓/可深入；短=急/不宜深入。四库“十一以上长，单九以下短”仅作 variant。

### D8-03 五音
1/2宫土人君；3/4徵火宗庙；5/6羽水后妃；7/8商金子孙/太子；9/10角木疾病。奇首为正音，偶数为比音；0按10。五音不直接判吉凶。

### D8-04 孤单
单阳{1,3,7,9}不利主；单阴{2,4,6,8}不利客；孤阳{10,30}不利主；孤阴{20,40}不利客；重阳{11,13,17,19,31,33,37,39}不利主/火厄；重阴{22,24,26,28}不利客/水厄。杜塞数不强塞孤单。

### D8-05 内外
固定八内：阴德、大义、地主、阳德、和德、吕申、高丛、太阳。
固定八外：大炅、大神、大威、天道、大武、武德、太簇、阴主。
天目内→内虚→攻外；天目外→外孤→攻内。不以太乙为中心。

### D8-06 多少
只比主客算。客>主→客胜；客<主→主胜；相等→原典未明言。将居5/杜塞不能覆盖基础结果。

### D8-07 阴阳厄会
阳宫{8,3,4,9}；阴宫{2,7,6,1}；5不参与。
阳+奇→重阳火厄；阴+偶→重阴水厄；其余本术无厄。与 D8-04 独立。

### D8-08 数有所主
复用 components：天→将军，地→吏士，人→兵卒。5仅吏、10仅将、15/25/35将+吏、16/26/36全、40仅将。不要写 n>=16 全具。

总入口返回 D8-01..08。严禁“数有所主→wuyin”。

## 3. C3 七术

Mode A：大神火 subject vs 大神落辰本五行 environment，用于 T7-02/03/04。
Mode B：将所在九宫五行 subject vs 大神落辰本五行，用于 T7-05/06/07。
五态与十二长生分层。

### T7-01 临津问道
输入敌起兵年支。连续4次+4，子→卯→午→酉→子，分别破年/月/日/时。

### T7-02 狮子反掷
输入敌起兵年支；大神→Mode A。旺相不破；休囚死合破。
四维：艮={丑艮寅}、巽={辰巽巳}、坤={未坤申}、乾={戌乾亥}。四维第18年破（offset +17）。
回归：戌→丑/休/艮维/18年；丑→辰太阳土/休；未→戌阴主土/休。

### T7-03 白云卷空
主/客大将九宫分别→大神→Mode A。主7→乾金→囚弱；客3→巽木→相强，客优势。大将5该边不可算。临官/冠带/帝旺/墓独立于五态。四库与景祐冠带文句作 variant。

### T7-04 猛虎相拒
输入敌下营日太乙，不是当前泛太乙。旺相不可攻；死或十二长生衰/墓可攻；囚只作 variant。经典太乙3→巽木/相/不可攻。

### T7-05 雷公入水
输入当日太乙+四将。Mode B。环境克将=>该将死厄。canonical 太乙6→大神子/8水；主8旺，客9相。电子本6→乾作 variant，不覆盖 canonical。

### T7-06 白龙得云
当日太乙+四将，Mode B。旺相宜部署；休囚死（以及有明确来源时墓）不宜。经典太乙9→大神坤土；主6相、客3旺。另做 direct_conflict；“刑”无标准表则 pending。

### T7-07 回军无言
必须输入敌军初来时日太乙。缺失则不可算；禁止拿客大将代替。敌旺相→有伏；敌休囚死→无伏、自破、可攻；己大旺相→本军宜伏。经典初来2→酉金，客9木死→无伏、自破、可攻。

mandatory：T7-LJ-001、LION-001/002/003、CLOUD-001/002、TIGER-001、THUNDER-001、DRAGON-001、RETURN-001/002。

## 4. C4 周期

统一1-based：`r=((value+offset-1)%cycle)+1`，`index=(r-1)//stay`，`year_in=(r-1)%stay+1`。

### 三基 canonical
共同 +250、顺十二支。
- 君基：起午，30年/支，有效360（来源外周期3600）
- 臣基：起午，3年/支，有效36（来源外周期360）
- 民基：起戌，1年/支，有效12（来源外周期360）
四库全起戌仅 variant。
修 kingbase 边界、officerbase 72局依赖、pplbase 起申。

### 五福
乾→艮→巽→坤→中；45年/域，225周期；名黄秘/黄始/黄室/黄庭/玄室。canonical offset +250；+115仅 variant。阶段1-15理天、16-30理地、31-45理人。
吉算用 `year_in_domain` 末位：1君王2王侯臣宰3后妃4太子5民庶6师帅7上将军8中将军9下将军0士卒。
五域：乾{戌乾亥}、艮{丑艮寅}、巽{辰巽巳}、坤{未坤申}、中{子午卯酉}。

### 大游
canonical 7→8→9→1→2→3→4→6；36年/宫，288周期，无5。reverse variant 7→6→4→3→2→1→9→8。阶段1-12天、13-24地、25-36人。+34为 profile，不得多层重复。
大游天目18：未天道、坤大武、坤大武、申武德、酉太簇、戌阴主、乾阴德、乾阴德、亥大义、子地主、丑阳德、艮和德、寅吕申、卯高丛、辰太阳、巽大炅、巳大神、午大威。
凶算用 `year_in_palace` 末位十类。

### 小游
1→2→3→4→6→7→8→9；3年/宫，24周期，无5；y1治天、y2治地、y3治人。古例acc10154821→cycle13→6宫y1治天。

## 5. C5 四太乙

独立12宫：
1乾、2离、3艮、4震、5中、6兑、7坤、8坎、9巽、10绛宫(巳)、11明堂(申)、12玉堂(寅)。
10/11/12不得压成2/6/4。

四太乙：天乙金、地乙土、直符火、四神水。
基础起宫：四神1、天乙6、地乙9、直符5。
三元：四神1→9→5；天乙6→2→10；地乙9→5→1；直符5→1→9。
3年/宫，36周期。只输出 year_in_palace，不虚构天地人 phase。

古例：武德五年壬午天乙玉堂12；应顺元年甲午地乙明堂11；天祐四年丁卯四神6。若不合先查积年/元 adapter。

六组同宫只比较12宫 palace_id：
- 天乙+地乙：兵戈、土工、农伤
- 天乙+直符：火旱、刀兵、饥疾
- 天乙+四神：水涝、霜雪、兵盗、舟车不通
- 地乙+直符：火旱、兵盗、土工
- 地乙+四神：水旱失调、民灾
- 直符+四神：水旱、饥疫、兵盗

四神水特殊：辰/戌+5或9、丑/未+7或3=克贼；巳/午+2或9=战克；其他 pending。
直符已知：2旺、3长生、4败；其他 pending。

## 6. C6 兼容层

- `config.py` 退化为 facade；新模块不 import config。
- `_SIXTEEN_GOD_WX` 直接来自公共表。
- `_GENERAL_WX` 修主将金/主参水。
- `_WX_REL` 不手写。
- `cal_des` 仅旧显示，基于三才。
- `_calc_jianbei` 不再做长短；若保留，只适配 D8-08。
- `suenwl` 保留四参签名但后两参不影响胜负。
- `neiwai_gongji` 保留旧UI keys：孤虛/宜攻/斷語，底层用固定八内八外。
- `gudan*` 调 D8-04。
- `junshi_zhanlue['数有所主']` 改 D8-08；五音独立。
- `wufu/bigyo/smyo` 只调新周期。
- `kingbase/officerbase/pplbase` 只调新三基。
- `skyyi/earthyi/fgd/zhifu` 改用四太乙12宫模型；旧72局列表不再做算法真源。
- 七术旧函数只做 legacy wrapper；`returnarmy(away_general)` 标 deprecated，新pan不得调用。

## 7. C7 pan v2

新增 `pan_v2.py`，不要 import `Taiyi`。由 `kintaiyi.py` 收集一次 snapshot 后传入 builder。

根结构：

```json
{
  "schema_version": "2.0",
  "meta": {},
  "calendar": {},
  "board": {
    "taiyi": {},
    "eyes": {},
    "calculations": {},
    "generals": {},
    "doors": {}
  },
  "cycles": {
    "three_bases": {},
    "five_blessings": {},
    "big_wander": {},
    "small_wander": {},
    "four_taiyi": {}
  },
  "analysis": {
    "patterns": {},
    "eight_divinations": {},
    "seven_methods": {},
    "military": {}
  },
  "modern": {},
  "source_variants": {},
  "compat": {
    "legacy_top_level": true,
    "legacy_schema": "pan-v1-flat"
  }
}
```

中五 v2 `sector=null`，不要把“中”混进 Sector16。

`board.eyes` 保留 sector本五行 与 nine_palace_element 双层事实。
`board.generals` 同时保留 intrinsic_element / palace_element。

普通 `Taiyi.pan()` 继续保留旧中文顶层字段，并追加 `result["v2"]=v2`。

### scenario 语义
建议 `pan(..., *, scenario=None)`：
- enemy_start_year_branch
- enemy_camp_day_taiyi_palace
- enemy_first_arrival_taiyi_palace

无scenario：T7-01/02/04/07不可算；T7-03可按当前主客将；T7-05/06应显式使用“当日太乙”，不要用任意当前 ji_style 太乙冒充。

先加 `result["v2"]`，再跑现有 game theory 分支。v2必须 JSON-safe。

## 8. 重要附加修正

- `ming_kingbase`：算了 tiany 却检查 `kingb==ty`，应按君基+天乙语义修。
- `ming_pplbase` 天乙断语方向需按来源复核修正。
- 季节八态疑应“旺相胎沒囚死休廢”，但这与七术五态不同，改前先核 source/test。
- 五福+三基“初会”=same_now and not same_previous，不等同五福入域第1年。
- 十六辰对冲：戌↔辰、乾↔巽、亥↔巳、丑↔未、艮↔坤、寅↔申、子↔午、卯↔酉；真中 pending。
- 大游九宫对冲：1↔9、3↔7、2↔8、4↔6。

## 9. C8 卷五军事综合层（已实施第一阶段）

新增 `src/kintaiyi/junshi_zhanlue.py`，总入口 `junshi_zhanlue(...)`。本层只做组合，不复制基础公式。

### C8-L1 八占基础结果

直接复用 D8-01..08。必须保持：

- 五音 = D8-03，独立展示。
- 数有所主 = D8-08，严禁再接到五音。
- 5 仅地算/吏士。
- 15/25/35 仅天算+地算/将军+吏士。
- D8-06 多少胜负不被将居中五、三门五将等后续条件覆盖。

### C8-L2 三门五将

只接收上游 `three_doors` / `five_generals` 事实并归一化；C8 不在组合层重算八门、天目或将宫公式。

未完成独立校勘前，三门/五将底层公式保持 pending，不得把参考仓库旧实现直接升为 canonical。

### C8-L3 主客动静

只处理先后角色与行动姿态：

- 野战：先动者客，后应者主。
- 安居：先举者主，后应者客。
- 三门五将不备可标固守倾向，但本层 `winner=None`，不得另造胜负。

数值多少仍由 D8-06 负责；算长短仍由 D8-02 负责。

### C8-L4 将帅贤否

只消费已经校勘的旺衰事实：

- 旺/相：有气，可任。
- 囚/死：无气，不利。
- 休：pending，不强判。
- 未给状态：not_computable。

禁止借七术 Mode B、十二长生、卷十七格局或未校勘刑表替代。

### C8 默认隔离

默认主链不混入：卷十七孤虚求索、跨卷太乙助主客、辅相贤否、诸将旺衰算法、郡国进贤、出师略地。需要时以后作为独立层组合。

详细来源边界见 `sources/c8-junshi-zhanlue-record.md`。

## 9.1 C9 现代博弈层（已实施第一阶段）

新增 `src/kintaiyi/game_theory.py`。C9 只做结构化现代特征投影，不把现代模型反写为古法。

### C9-01 七术投影

新增 `project_seven_method_for_game_theory(...)`：

- 只读取 `rule_id`、`verdict`、五态、`has_qi`、`enemy_verdict` 等明确字段。
- 禁止把整个七术结果 stringify 后搜索“成/吉/正/利”。
- `notes/aliases/source_variants` 中的文字不得改变博弈信号。
- `not_computable/pending` 不强行量化。
- 所有结果标 `derived_modern_feature=True`。
- T7-01 只投影应期，不自动生成通用吉凶分。

批量入口：`project_seven_methods_for_game_theory(...)`。

### C9-02 九宫体系隔离

新增 `taiyi_palace_feature(...)`，博弈层固定使用太乙九宫：

`1乾 2离 3艮 4震 5中 6兑 7坤 8坎 9巽`。

禁止沿用参考仓库 game_theory 中的洛书宫义：

`1坎 2坤 3震 4巽 6乾 7兑 8艮 9离`。

中五仅保留土五行，不生成虚构的位置策略加成。

### C9-03 现代模型边界

`build_game_theory_feature_bundle(...)` 输出现代模型输入，并固定：

- `derived_modern_feature=True`
- `source_of_truth="structured_taiyi_results"`
- `cross_system_palace_mapping=False`

支付矩阵、权重与 Nash 均衡若后续迁入，必须保持现代派生标记，并把每个权重列为现代模型参数，不得伪称古籍原值。

详细记录见 `sources/c9-game-theory-record.md`。

## 9.2 C10 v2 消费层（已实施第一阶段）

目标仓库当前尚无完整 `Taiyi.pan()` / Streamlit / CLI 主入口，因此先新增 `src/kintaiyi/v2_consumer.py` 作为未来展示层公共入口。

### C10-01 严格 v2 解析

`resolve_v2_payload(...)` 只接受：

- 直接 `schema_version="2.0"` 的 v2；
- legacy pan 容器内明确存在的 `result["v2"]`。

只有旧中文 flat 字段时返回 `not_computable`，不得自动拼装“假 v2”。

### C10-02 子层读取

`read_v2_section/read_v2_analysis/read_v2_board` 缺字段时必须显式给出 `missing_inputs`，不得回退读取旧顶层同名/近义字段。

### C10-03 未来 UI/CLI 视图模型

`build_v2_view_model(...)` 只组织已有 v2 根区段，并固定：

- `consumer_mode="v2_strict"`
- `legacy_fallback_used=False`

当真正 UI/CLI 入口进入目标仓库后，展示层只调用这个消费层。

详细记录见 `sources/c10-v2-consumer-record.md`。

## 9.3 C11 pan v2 producer（已实施第一阶段）

新增 `src/kintaiyi/pan_v2.py`，只负责组装已经算出的事实，不导入 `Taiyi`，不复制任何古法算法。

### C11-01 完整根结构

`build_pan_v2(...)` 固定输出 schema 2.0 的：

- meta
- calendar
- board
- cycles
- analysis
- modern
- source_variants
- compat

并补齐 board/cycles/analysis 的规定子层。

### C11-02 中五与类型边界

- `palace=5` 时 `sector=None`。
- 中五不得伪装为 Sector16。
- 天目 sector_element / nine_palace_element 分层保留。
- generals intrinsic_element / palace_element 分层保留。

### C11-03 scenario

只接受：

- enemy_start_year_branch
- enemy_camp_day_taiyi_palace
- enemy_first_arrival_taiyi_palace

禁止新增“用客将代敌初来太乙”之类替代字段。

### C11-04 JSON-safe 与 validator

- tuple/set 规范为 JSON-safe list。
- 未知对象直接 TypeError，不自动字符串化。
- `validate_pan_v2(...)` 只验证 schema/表示层不变量，不验证古法答案。

builder 输出可直接由 C10 `v2_consumer.py` 消费。

详细记录见 `sources/c11-pan-v2-builder-record.md`。

## 9.4 C12 legacy pan snapshot adapter（已实施第一阶段）

新增 `src/kintaiyi/pan_adapter.py`，用于未来把旧 `Taiyi.pan()` flat snapshot 接到 C11 `build_pan_v2`。

### C12-01 只搬事实

允许从旧 snapshot 搬运明确盘面事实：

- meta/calendar
- 太乙落宫与旧 sector
- 文昌/始击/定目
- 主算/客算/定算旧容器
- 主将/主参/客将/客参
- 八门
- 君基/臣基/民基、五福、大小游

adapter 不调用任何古法算法。

### C12-02 隔离旧混合层

旧 `軍事戰略`、旧七术顶层断语、旧 `運籌博弈分析` 等不得自动提升为 v2。

它们只进入 `compat.quarantined_legacy_keys` 审计记录，并固定：

- `legacy_analysis_promoted=False`
- `legacy_modern_promoted=False`

### C12-03 structured 输入必须显式提供

新的 `analysis.eight_divinations`、`analysis.seven_methods`、`analysis.military` 和 `modern.game_theory` 由调用方显式传入。

不得从旧 prose/string 断语反推。

### C12-04 scenario 不推断

scenario 只接受 C11 三个 canonical 字段；不得从客将、客参等旧盘字段自动生成敌军事件输入。

### C12-05 兼容接线

`attach_v2_to_snapshot(...)` 返回旧 snapshot 副本并新增 `result["v2"]`，不原地修改输入。

未来真正 `Taiyi.pan()` 进入目标仓库时，只需在 return 前调用本适配器；新 UI/CLI 继续只读 C10 strict consumer。

详细记录见 `sources/c12-pan-adapter-record.md`。

## 9.5 C13 legacy flat schema 迁移审计（已实施第一阶段）

新增 `src/kintaiyi/migration_audit.py`，用于量化旧 pan snapshot 的迁移状态。

### C13-01 单盘审计

`audit_legacy_snapshot(...)` 输出：

- migrated fact keys / rate
- quarantined keys / rate
- unported keys / rate
- v2 present / valid
- structured replacement gaps
- 是否可供 v2 core consumer 使用

状态分为：

- `legacy_only`
- `v2_invalid`
- `v2_partial_replacements`
- `v2_core_ready_with_unported_legacy`
- `v2_core_ready`

### C13-02 structured replacement gaps

只要旧 snapshot 仍含以下风险字段，就检查新 v2 是否已有正式替代：

- 旧军事战略 → `analysis.military`
- 旧七术断语 → `analysis.seven_methods`
- 旧八占相关断语 → `analysis.eight_divinations`
- 旧运筹博弈 → `modern.game_theory`

缺替代时不得仅凭“已有 v2”宣称迁移完成。

### C13-03 批量迁移统计

`audit_snapshot_collection(...)` 汇总状态数量、ready 数量、平均迁移/隔离/未迁移比例，以及字段和 replacement gap 频率。

所有输出标 `derived_migration_metadata=True`，不得参与古法判断。

详细记录见 `sources/c13-migration-audit-record.md`。

## 9.6 C14 legacy schema policy 单一真源（已实施）

新增 `src/kintaiyi/legacy_schema.py`，统一定义旧 flat 字段迁移策略。

每个旧字段只能处于：

- `migrated_fact`
- `quarantined`
- `unported`
- `embedded_v2`

### C14-01 migrated fact target

已迁移事实必须有唯一 v2 target path，例如：

- 太乙落宮 → `board.taiyi.palace`
- 主算 → `board.calculations.home`
- 主將 → `board.generals.home_general`
- 八門分佈 → `board.doors.distribution`

### C14-02 quarantined replacement

风险旧字段必须声明新结构 replacement path，例如：

- 軍事戰略 → `analysis.military`
- 旧七术 → `analysis.seven_methods`
- 旧八占相关断语 → `analysis.eight_divinations`
- 運籌博弈分析 → `modern.game_theory`

### C14-03 unknown stays unported

未知旧字段不得猜目标；保持 `target=None`。

### C14-04 C12/C13 去重

C12 adapter 和 C13 migration audit 都读取 C14 registry，不再各自维护字段名单。

详细记录见 `sources/c14-legacy-schema-policy-record.md`。

## 9.7 后续 C15+

- 真正 `Taiyi.pan()` / CLI / UI 文件进入目标仓库后进行实际接线。
- 根据 C13 的 unported 字段频率决定下一批卷次迁移优先级。
- 未迁移卷次继续按 canonical/source_variant/derived/pending 分层，避免全部塞进 analysis。
- 新增字段时先更新 C14 registry，再修改 adapter/audit。

## 9.7 《太乙金镜式经》卷四军事十二法来源层（J4M，12/12 complete）

来源层：

- machine rules: `rules/jinjing_v4_military.json`
- runtime: `src/kintaiyi/jinjing_v4_military.py`
- source record: `sources/jinjing-v4-military-12-record.md`
- source profile: `jinjing_siku_volume4`

### J4M-01..12 固定顺序

以四库本《太乙金镜式经》卷四正文小标题顺序为 canonical：

1. 推三门具不具
2. 推五将发不发
3. 推主客相关法
4. 推主客
5. 推出师法
6. 推陈兵向背
7. 推制阵随地法
8. 推随地制变
9. 推太乙在天外地内法
10. 推奇伏法
11. 推太乙风云飞鸟助战法
12. 推阵有风云气定胜负

当前状态：

- `implemented = J4M-01..12`
- `partial = []`
- `pending = []`

目录短题/异写只作 alias，不另建重复术。

### J4M-03 日计二目纳音

J4M-03 已完成重新校勘，不再把“日计纳音”建模成一个独立当天干支六十甲子纳音变量。

古籍证据链：

- 《金镜》卷四：“皆用日计纳音以决之”“所谓关者，取五行相制之道”；
- 《景祐太乙福应经》对应转录：“日计二目纳音”；
- 《太乙淘金歌》：“二目纳音何以定”“以二目纳音决之，取五行生克为用”；
- 《金镜》卷二：上目始击属客，下目文昌属主。

canonical：

- 客目五行克主目五行 → 客关得主人 → 客胜；
- 主目五行克客目五行 → 主人关得客 → 主胜；
- 无相制关系 → 本条不强设 winner。

《淘金歌》“同音二阵平 / 相生和解”只作 `collation_hint`，不覆盖《金镜》winner。

旧 `day_nayin_element` 仅保留兼容并标 `legacy_input_ignored`。

### J4M 与 C8 的边界

- J4M 是《金镜》卷四 source profile。
- C8 默认仍为 `volume5_strict`。
- 显式 adapter: `src/kintaiyi/jinjing_v4_c8_adapter.py`。
- J4M-01/02 只映射为 C8-L2 上游三门/五将事实。
- J4M-04 完整结果只作为 overlay，不覆盖 C8-L3。
- J4M-03 虽已 complete，但 C8 当前无独立“关法” layer，因此仍不进入 adapter。
- J4M-03 与 J4M-04 永不合并。
- J4M-07 与 J4M-08 永不合并。
- J4M-05 不得用《统宗》卷五兵额表替代。
- J4M-06 不得用旧卷十五“陈兵出乡”替代。

### J4M-09 来源差异

《金镜》卷四：

- 8/3/4：地内助主；
- 9/2/7/6：天外助客；
- 1 宫未列入本段地内组。

《太乙统宗宝鉴》卷五：

- 1/8/3/4：天内助主；
- 9/2/7/6：天外助客。

必须保存为独立 source profile；禁止静默合并。

### J4M-11 / 12 外部观测

- J4M-11 风云飞鸟必须由外部观测事件驱动；
- J4M-12 云气定胜负必须显式输入云气方位/颜色/形态等；
- 无观测不得从盘内字段伪造。

## 9.7A 现代《太乙数纳音体系（修正版）》独立 profile

该现代体系**不属于 J4M-03**。

固定路径：

- runtime: `src/kintaiyi/variants/modern_liunian_nayin.py`
- machine rules: `rules/variants/modern_liunian_nayin.json`
- source record: `sources/modern-liunian-nayin-record.md`
- validation: `tests/reports/modern_liunian_nayin_validation.md`

固定标识：

- profile: `modern_liunian_nayin_2026`
- variant id: `MODERN-LIUNIAN-NAYIN`
- `type=modern_reconstruction`
- `canonical=false`

材料支持：

- 宫徵羽商角；
- 五音纳甲丙戊庚壬并按阴阳配阴干；
- 星神本五行 → 五音；
- 地支 / 四维 → 律吕；
- 合成星神纳音；
- 日干变音顺序；
- 本/变两个纳音可作关系比较；
- 年/月/日/时四计均可扩展使用，但上游历法输入随计改变。

边界：

- 十二地支到十二律采用古典律历标准映射作为背景依赖；
- 四维只有显式 `dimension_mode=branch_proxy` 才取乾亥、艮寅、坤申、巽巳；
- 材料未写成唯一公式的“星神如何由日干序列自动取得变五行”不得补算；
- 本/变纳音五行比较只返回关系，不自动给吉凶/胜负；
- 不得进入 J4M → C8 adapter；
- 不得覆盖任何古籍 canonical。
- 可通过 `src/kintaiyi/variants/profile_bundle.py` 显式包装后传入 `build_pan_v2(modern=...)`；默认 modern section 不自动启用任何 profile，也不得写入 `analysis` / `source_variants`。

已删除旧错误路径：

- `src/kintaiyi/modern_nayin_variant.py`
- `rules/j4m03_nayin_variants.json`
- `tests/test_modern_nayin_variant.py`
- `tests/test_j4m03_nayin_variants.py`

防回归测试：`tests/test_modern_variant_namespace.py`。

## 9.8 C15 unported legacy 字段目录与迁移优先级（已实施）

参考 `Taiyi.pan()` 当前主盘 108 个顶层字段中，C14 尚有 67 个 unported。C15 已全部建立目录，见 `src/kintaiyi/unported_catalog.py`。

### C15-01 四层

每个已知 unported 字段增加候选层：

- `canonical`：来源相对明确，可逐条建 source record 后迁移；
- `source_variant`：必须拆来源 profile，禁止静默选一套；
- `derived`：综合包装或现代派生，不得整体标为古法 canonical；
- `pending`：来源/输入不足，禁止猜。

### C15-02 P0-P3 优先级

- P0：核心盘面或高风险来源边界；
- P1：来源较明确的独立规则 / 高风险军事层；
- P2：辅助体系、跨卷或仍需补来源校勘；
- P3：综合包装器或现代派生。

当前 P0 重点：

- 天乙 / 地乙 / 四神 / 直符 / 合神 / 计神的 board 结构；
- 十六宫分布；
- 推三门具不具；
- 推五将发不发；
- 推主客相关法；
- 释格局。

### C15-03 禁止整体迁移

旧 `卷八/九/十/十一/十二/十三/十四/十八` 综合键，以及卷十五军事应用、卷十七军事占断、跨卷综合项、现代天文桥接，固定 `migrate_whole=False`。

必须先拆成独立规则 / source profile，再进入 v2。

### C15-04 与 C13/C14 连接

C14 的 unported manifest 现在附带：

- candidate_layer
- priority
- source_scope
- migration_action
- migrate_whole

C13 audit 现在附带：

- unported_layer_counts
- unported_priority_counts
- next_migration_candidates

后续迁移顺序应同时参考 C15 priority 与真实 snapshot 的字段频率。

详细记录见 `sources/c15-unported-catalog-record.md`。

## 9.9 C16 P0 第一批 board 结构事实（已实施）

已落实 C15 P0 中不依赖军事断语的一批。

### C16-01 十六宫分布

`board` 新增必需子区段：

`board.sixteen_palaces`

旧 `十六宮分佈` 由 C12 adapter 原样搬运，不重新调用旧 `sixteen_gong(...)` 算法。

C14 当前状态已改为：

`migrated_fact -> board.sixteen_palaces`

### C16-02 六个基础神将

以下旧字段迁入 `board.generals`：

- 天乙 → `tianyi.sector`
- 地乙 → `diyi.sector`
- 四神 → `four_spirits.sector`
- 直符 → `zhifu.sector`
- 合神 → `hegod.sector`
- 计神 → `jigod.sector`

这些旧值是十六神/支位文字，不得套主客大将的 `palace` 字段。

### C16-03 审计状态

上述 7 个字段从 unported 转为 migrated_fact。

C15 目录保留历史候选记录，但 C14/C13 当前迁移状态优先；C13 不再把它们列入 next migration candidates。

详细记录见 `sources/c16-board-facts-record.md`。

## 9.10 C17 P0 来源隔离（已实施）

剩余 P0 不做“公式合并”，而是建立 source-profile 容器。

### C17-01 格局

新增 `build_pattern_source_variants(...)`：

- `tongzong_volume4`
- `jinjing_geju`

`jinjing_geju` 指目标仓库 source-limited 格局引擎；主体来源卷三，值事门相关规则引用卷四。不得把整套金镜格局误标为“卷四”。

固定：

- `canonical_selected=None`
- `cross_source_merge=False`

### C17-02 三门 / 五将

- J4M-01 ↔ 三门
- J4M-02 ↔ 五将
- C8-L2 只消费/归一化上游事实，不是 J4M-01/02 公式实现。

因此 crosswalk 固定：

`c8_equivalent_formula=False`

### C17-03 主客相关

J4M-03“主客相关法”与 C8-L3“主客动静/先后”不得合并。

`host_guest_relation` 不允许把 `c8_upstream` 登记成直接替代 profile。

### C17-04 legacy quarantine

以下旧 flat 字段从 unported 转为 quarantined：

- 释格局
- 推三门具不具
- 推五将发不发
- 推主客相关法

replacement path 分别指向具体 `source_variants.*.profiles`。

仅有空容器不能清除 C13 replacement gap；必须存在真实结构化 profile 结果。

详细记录见 `sources/c17-source-profiles-record.md`。

## 9.11 C18 紫庭项目主来源目标 / 统宗参校层（证据分级）

P1 六项继续放在同一来源容器中，但**不再一概宣称“紫庭主来源已确认”**：

- 太乙九星
- 文昌九星
- 文昌变化
- 始击变化
- 三旗行宫
- 九宫贵神

### C18-01 三档证据

`direct_text_verified`：

- 太乙九星
- 文昌变化
- 始击变化

`catalog_attested_text_pending`：

- 文昌九星

`project_attribution_unverified`：

- 三旗行宫
- 九宫贵神

统宗参校：

- 前四项：卷六
- 三旗 / 九宫贵神：卷十

### C18-02 primary_result 门禁

`src/kintaiyi/zitingjing_sources.py` 固定：

- `primary_evidence_level`
- `primary_result_allowed`
- `primary_result`
- `collation_results`
- `canonical_selected`
- `cross_source_merge=False`

只有：

`primary_evidence_level=direct_text_verified`

才允许注入非空 `primary_result`。

目录证据或项目拟定归属均不能清除 C13 replacement gap。

### C18-03 legacy quarantine

旧 flat 六项继续 quarantined；由于旧 flat 实现本身来自《太乙统宗宝鉴》，replacement path 现在指向同源参校 profile：

- 太乙九星 / 文昌九星 / 文昌变化 / 始击变化 → `collation_results.tongzong_volume6`
- 三旗行宫 / 九宫贵神 → `collation_results.tongzong_volume10`

这只表示“旧实现已被同源结构化参校结果替代”；它**不代表紫庭 primary 已完成**。

紫庭 canonical 完成度仍单独由：

- `primary_evidence_level`
- `primary_ready`
- `primary_result`

判断。

详细记录：

- `sources/c18-zitingjing-primary-record.md`
- `sources/c20-zitingjing-pending-locators-record.md`

## 9.12 C19 紫庭直接主来源第一批（已实施）

已直接定位并结构化：

1. 太乙九星：〈释九宫所值九星〉
2. 文昌变化：〈释天目变化〉
3. 始击变化：〈始击变化〉核心层

对应 runtime：

`src/kintaiyi/zitingjing_primary.py`

### C19-01 太乙九星

保留当前在线见证的九宫、九星、分野、吉凶；天冲“凶”与统宗后出“吉”并列记录，不静默统一。

### C19-02 文昌变化

保存囚、内迫、外迫、对、二目相关等直接规则；旺相计算仍调用独立五行层。

### C19-03 始击变化

核心身份 / 军事角色已固化；C31 已完成逐岁干×五行灾应 5 组×5 行校勘，状态：

`collated_with_preserved_variants`

OCR 校字与真异文分开保存，详见 `sources/c31-zitingjing-shiji-collation-record.md`。

### C19-04 尚未形成 primary_result

- 文昌九星：有目录证据、正文待取得
- 三旗行宫：紫庭归属尚未证实
- 九宫贵神：紫庭归属尚未证实

`build_c19_verified_primary_results()` 只返回前三个 direct-text 项。

## 9.13 C20 剩余三项证据分层（已实施修正）

### C20-01 文昌九星

两份现代整理本《太乙紫庭秘诀》目录均列：

`附太乙文昌九星值宫术`

状态：

`catalog_attested_primary_text_pending`

这足以证明其与紫庭传本系统的目录关联，但不足以结构化正文，因此：

- `primary_result_allowed=False`
- 继续寻找直接正文

### C20-02 三旗行宫

已查的《太乙紫庭秘诀》十二卷及附录目录中**未见“三旗行宫”同名题目**。

状态：

`project_primary_attribution_unverified`

《太乙统宗宝鉴》卷十有直接可定位：

〈明太乙与三旗行宫会合术〉

因此 P1 目录改为 `source_variant`，在证明紫庭归属前不得标为紫庭 canonical。

### C20-03 九宫贵神

已查的紫庭秘诀目录中**未见“九宫贵神”同名题目**。

状态：

`project_primary_attribution_unverified`

《太乙统宗宝鉴》卷十有直接可定位：

〈明太乙九宫贵神术〉

唐王起〈定祀九宫仪注议〉可证明更早的九宫贵神系统背景，但不是紫庭正文。

### C20-04 后续顺序

优先：

1. 继续找“附太乙文昌九星值宫术”直接正文；
2. 文昌九星外部参校已由 `src/kintaiyi/zitingjing_collation.py` 保存《三才世纬》卷八十一与统宗卷六多见证；星名异文及 10/30 年周期冲突保持 unresolved；
3. 三旗 / 九宫贵神只有发现紫庭目录或正文证据后才升级 attribution；
4. 若长期无紫庭证据，可另建统宗卷十 direct source profile，但不得反标为紫庭。

## 9.14 C21 卷十五 / 卷十七军事 derived profiles（已实施）

新增 `src/kintaiyi/military_derived_profiles.py`。

### C21-01 卷十五

独立 profile：

`tongzong_volume15_military_application`

锁定旧综合术目：

- 奇兵伏兵
- 五阵置旗
- 出兵称神
- 陈兵出乡
- 选将之术
- 教兵之术
- 随地制变
- 分合用兵
- 五音风
- 五音观风察将
- 安营置阵
- 风从八卦
- 云气逆顺
- 军势胜负

固定：

- `derived_military_profile=True`
- `cross_volume_merge=False`
- `cross_c8_merge=False`
- `cross_j4m_merge=False`

### C21-02 卷十七

独立 profile：

`tongzong_volume17_military_divination`

锁定旧综合术目：

- 出兵用时
- 敌国动静
- 间谍虚实
- 敌使虚实
- 敌兵来方
- 见闻虚实
- 讨捕叛亡
- 执囚对吏
- 求索所得
- 孤虚对照
- 时计诸事
- 占望行人

### C21-03 旧 flat quarantine

- 军事应用 → `source_variants.military_derived.tongzong_volume15.payload`
- 军事占断 → `source_variants.military_derived.tongzong_volume17.payload`

空 profile 不清除 C13 replacement gap；必须显式有独立 payload。

详细记录见 `sources/c21-military-derived-profiles-record.md`。

## 9.15 C22 军事 rule-unit 目录（已实施）

卷十五 / 卷十七综合 payload 已拆成独立规则号。

### C22-01 卷十五

V15-01..14 共 14 条 source rules。

### C22-02 卷十七

V17-01..11 共 11 条 source rules。

旧“孤虚对照”不是独立卷十七原法，而是卷五内外占攻击 × 卷十七求索所得的跨卷 helper，单列：

`V17-D1`

并固定：

- `source_status=derived_cross_volume_helper`
- 不进入卷十七 canonical source rule 集。

### C22-03 依赖目录

每条规则记录：

- source_rule_id
- source_title
- inputs
- dependency_class
- external_inputs
- J4M/C8 overlap metadata

C21 profile 已增加：

`payload key -> source_rule_id`

详细记录见 `sources/c22-military-rule-units-record.md`。

## 9.16 C23 卷十五低依赖第一批（已实施）

独立实现：

- V15-02 五阵置旗
- V15-03 出兵称神
- V15-04 陈兵出乡
- V15-05 选将
- V15-06 教兵

新增 `src/kintaiyi/tongzong_v15_low_dependency.py`。

### C23-01 五阵校勘

采用：

- 1/8 曲阵黑旗
- 3 直阵青旗
- 4/9 锐阵赤旗
- 2/5 圆阵黄旗
- 6/7 方阵白旗

识典在线 OCR 一处存在“3/6直、6/7方”的重复 6；同篇后文帛色总结与其他兵书见证支持“3直、6/7方”。

参考仓库旧表曾错误写成 3/7直、6方。C23 不回退旧实现，并用 `FORMATION_TEXT_VARIANT` 保存异文与校勘依据。

### C23-02 出兵称神

只结构化来源常规枚举 1/2/3/4/6/7/8/9 的：

- 行列
- 行军缓急
- 祭祀方向
- 帛色
- 面向

不复制长咒文；5与整十不由旧代码补造完整仪式表。

### C23-03 陈兵出乡

只取出乡方向，明确：

`j4m_equivalent=False`

不得替代 J4M-06 推陈兵向背。

### C23-04 选将 / 教兵

保存八征与渐进训练原则，作为静态兵法结构，不进入 C8/J4M 胜负链。

详细记录见 `sources/c23-tongzong-v15-low-record.md`。

## 9.17 C24 卷十五外部风云观测（已实施）

实现：

- V15-09 五音风
- V15-12 风从八卦
- V15-13 云气逆顺

三条均要求显式外部观测；缺观测返回 `not_computable`。

### C24-01 五音风

风向支映射五音五行，但相克关系不自动压成通用主客 winner。

母来翼子 / 子来扶母按原文明示保留 direct_effect。

### C24-02 风从八卦

只解释显式 `wind_palace`；中五不属于八卦风向。

坤宫当前 OCR 疑文保持 `source_text_uncertain`。

### C24-03 云气逆顺

取消旧“数字差5”近似。

改按：

- 云从算向来 = 顺
- 云从对冲方向来 = 逆
- 其他 = 不应

详细记录见 `sources/c24-tongzong-v15-observations-record.md`。

## 9.18 C25 五音观风察将（已实施）

V15-10 改为真实风声输入：

`wind_sound_class`

五类：

- 宫风
- 商风
- 角风
- 徵风
- 羽风

明确：

`v15_09_direction_tone_substitute_allowed=False`

即风向五音与风声五音必须分层，不得互相替代。

本条只描述将帅性情，不直接生成 winner。

详细记录见 `sources/c25-tongzong-v15-wind-sound-record.md`。

## 9.19 C26 卷十七低依赖第一批（已实施）

实现：

- V17-03 间谍虚实
- V17-04 敌使虚实
- V17-05 敌兵来方
- V17-11 占望行人

### C26-01 间谍

内外、深浅、客将位置由上游显式结构化；不复刻旧宫界近似。

### C26-02 敌使

收集太乙与客目/客大将五行制化证据。

实证与虚证同时出现时：

`mixed_evidence`

不得按 if 顺序覆盖。

### C26-03 敌兵

固定：

- 5/15/25/35 → 杜塞不来；
- <=15 → 兵寡无将；
- >=16 **且阴阳和** → 兵众有将有卒；
- 时计阴 → 无贼，不按兵数扩断。

客目左右前后/四维由上游显式提供。

### C26-04 行人

南方来数存在版本异文：

- 1/6 来
- 3/8 来

固定 `variant_conflict`，不择本静默覆盖。

详细记录见 `sources/c26-tongzong-v17-low-record.md`。

## 9.20 C27 卷十七结构条件型规则（已实施）

已实现：

- V17-06 见闻虚实；
- V17-07 讨捕叛亡；
- V17-08 执囚对吏；
- V17-09 求索所得。

### C27-01 结构输入

只消费结构化的：

- 内外；
- 旺相；
- 掩击；
- 扶挟；
- 门具将发；
- 季节与数位。

禁止解析旧中文断语。

### C27-02 冲突证据

同一盘同时出现正负条件时固定：

`summary="mixed_evidence"`

不得按 if/elif 顺序覆盖。

### C27-03 source variants

保留：

- V17-06 门具将发且闻凶的异读；
- V17-08 主人在内/外不可入狱的异读。

### C27-04 跨卷边界

V17-D1 孤虚对照继续只作为跨卷 derived helper。

V17-09 求索所得不调用 V17-D1。

详细记录见 `sources/c27-tongzong-v17-structured-record.md`。

## 9.21 C28 卷十七高依赖综合规则（已实施）

已实现：

- V17-01 出兵用时；
- V17-02 敌国动静；
- V17-10 时计诸事。

### C28-01 出兵用时

结构条件独立保存：

- 冬至后阳局 / 夏至后阴局背景；
- 文昌无囚迫；
- 始击无掩击；
- 算和；
- 大小将发；
- 太乙不在开、休、生门下。

开休生门下是独立阻项，不得用“三门具”代替。

### C28-02 敌国动静

5/15/25/35 杜塞固定“敌不来”。

来降 / 为寇改为 favorable / hostile evidence 聚合；好坏征兆并存时保留 `mixed_evidence`。

“客目南行来、北行不来”只按原文北敌示例使用，不泛化成四方通则。

### C28-03 时计诸事

分栏保存：

- 掩击百事；
- 门具将发算和；
- 吏/民事项；
- 旺相胎没死囚休废；
- 吕申太阳阴主避向。

吕申避向只接受上游 `forbidden_directions`，本层不从太乙宫自行重算。

### C28-04 witness volume variant

识典 NGJ 见证题作卷十七；CADAL 等同组内容见作卷十九。

项目 rule_id 继续保持 V17，不因版本卷号差异复制算法。

详细记录见 `sources/c28-tongzong-v17-high-record.md`。

## 9.22 C29 C19 来源记录清理（已实施）

已完成：

- 《太乙紫庭经》〈释九宫所值九星〉链接统一为 `1kg32q85u4tgl`；
- 撤销未完成逐字校勘的“配干”字段；
- 九星主来源表当前只固化宫、星、分野、吉凶；
- 文昌九星改为 `catalog_attested_primary_text_pending`；
- 三旗行宫 / 九宫贵神改为 `project_primary_attribution_direct_text_pending`。

来源层级不变：

- 《太乙紫庭经》主来源；
- 《太乙统宗宝鉴》参校。

## 9.23 C30 pan v2 最终聚合契约（已实施）

新增 `src/kintaiyi/pan_v2_contract.py`。

### C30-01 analysis

固定四槽：

- patterns
- eight_divinations
- seven_methods
- military

`analysis.military` 只放 C8 等明确 canonical/组合层。

卷十五/卷十七 derived military profile 禁止放入 analysis.military。

### C30-02 source_variants

固定四槽：

- patterns
- military
- zitingjing
- military_derived

不同来源槽不自动深合并。

### C30-03 modern

现代博弈固定进入：

`modern.game_theory`

并强制：

`derived_modern_feature=True`

### C30-04 legacy 防回流

旧 flat 风险键不得重新进入 analysis。

C30 validator 在 C11 schema validator 上继续检查：

- derived profile 层级；
- modern marker；
- source_variants 根槽；
- legacy flat 回流；
- aggregation contract 标记。

详细记录见 `sources/c30-pan-v2-contract-record.md`。

## 9.24 C31 《太乙紫庭经》始击校勘与证据等级（已实施）

### C31-01 始击十干岁 × 五行

〈始击变化〉逐岁干 × 五行灾应已整理为：

- 甲乙；
- 丙丁；
- 戊己；
- 庚辛；
- 壬癸；

共 5 × 5 = 25 个正规化元素槽位。

### C31-02 OCR 校字

经《太乙秘书》、统宗卷六等参校：

- 戊己首项在线 OCR “水”校为木，同时保留 witness_label；
- 壬癸末项在线 OCR “王”校为土，同时保留 witness_label；
- 甲乙土项确认接续于本组，不归入丙丁。

OCR 校字不等于提升参校本为主来源。

### C31-03 真异文

庚辛岁土为始击：

- 当前紫庭在线见证：夏大旱；
- 《太乙秘书》/统宗参校：夏大水。

固定 `preserve_both_no_silent_merge`。

### C31-04 剩余三项证据等级

- 文昌九星：`catalog_attested_text_pending`
- 三旗行宫：`project_primary_attribution_unverified`
- 九宫贵神：`project_primary_attribution_unverified`

三旗/九宫贵神当前只有统宗卷十直接文本，不能标成已证实紫庭 canonical。

详细记录见 `sources/c31-zitingjing-shiji-collation-record.md`。

## 9.25 C32 V17-D1 跨卷 derived helper（已实施）

V17-D1 只对照：

- D8-05 内外占攻击；
- V17-09 求索所得。

新增 `src/kintaiyi/cross_volume_helpers.py`。

### C32-01 输入锁定

仅接受：

- `attack_result.rule_id == "D8-05"`
- `request_result.source_rule_id == "V17-09"`

### C32-02 不重算

helper 不：

- 重新算内外；
- 重跑求索；
- 解析格局/断语；
- 修改来源结果。

### C32-03 derived 身份

固定：

- `source_rule_id="V17-D1"`
- `source_status="derived_cross_volume_helper"`
- `canonical_source_rule=False`
- `canonical_source_rule_count=0`

永不进入 V17-01..11 canonical source rule 集。

详细记录见 `sources/c32-cross-volume-guxu-record.md`。

## 9.26 C33 卷十七条件 runtime 去重（已实施）

V17-06/07/08/09 的唯一 canonical runtime 固定为：

`src/kintaiyi/tongzong_v17_structured.py`

旧：

`src/kintaiyi/tongzong_v17_conditions.py`

已改为 compatibility adapter，只保留旧函数名与旧字段形状。

固定返回：

- `compat_adapter=True`
- `canonical_runtime="tongzong_v17_structured"`

并同步修正 canonical 两处来源逻辑：

- “门不具或将不发”任一为 false 即成立；
- 始击/下目在内属于 V17-07 捕得证据。

禁止在 compatibility adapter 重新维护第二套古法公式。

详细记录见 `sources/c33-v17-runtime-dedup-record.md`。

## 9.27 C34 文昌九星外部参校层（已实施）

文昌九星继续保持：

`primary_evidence_level="catalog_attested_text_pending"`

《太乙紫庭秘诀》目录可证“附太乙文昌九星值宫术”这一术目，但尚未取得可逐条校读正文，因此：

- `primary_result=None`
- `canonical_selected=None`
- 不实现 canonical 推步。

新增外部参校：

- 《三才世纬》卷八十一；
- 《太乙统宗宝鉴》卷六 CADAL；
- 《太乙统宗宝鉴》卷六 NGJ。

已记录星名异文：

- 明雄 / 明维；
- 阴玄 / 阴德；
- 招摇 / 招煥；
- 雄明 / 维明。

值宫周期存在 10 年 / 30 年冲突，且 CADAL 同一见证内部即有：

- 叙述句 10 年一宫；
- 推法宫率 30；
- 小周 270；
- 大周 2700。

因此周期固定：

`unresolved`

不得据任一参校见证生成紫庭 canonical runtime。

详细记录见 `sources/c34-wenchang-nine-stars-collation-record.md`。

## 9.28 C35 有效迁移状态修正（已实施）

### C35-01 J4M-11

“推太乙风云飞鸟助战法”已不再是 pending。

J4M-11 已有完整 source-specific runtime，并要求真实外部观测。

旧 `flybird_wl` 只根据盘内飞鸟位置生成断语，因此降为 legacy quarantine。

replacement 固定：

`source_variants.military.weather_bird_support.profiles.jinjing_siku_volume4`

只有经 J4M-11 profile/ruleset/rule_id 校验的结果才可清除迁移缺口。

### C35-02 legacy flat 与主来源研究分离

旧 pan 六项紫庭相关 flat 来自统宗实现，因此迁移 replacement 改为：

- 太乙九星 / 文昌九星 / 文昌变化 / 始击变化 → `tongzong_volume6` collation；
- 三旗行宫 / 九宫贵神 → `tongzong_volume10` collation。

旧 flat 是否已结构化迁移，不再要求尚未取得的紫庭 `primary_result`。

### C35-03 文昌九星

文昌九星历史候选改为：

`pending / primary_text_pending`

继续允许外部参校，但不得实现 canonical 推步。

完整验证：655 passed / 0 failed。

详细记录见 `sources/c35-effective-migration-state-record.md`。

## 9.29 C36 阳九 / 百六大小限（已实施）

新增：

`src/kintaiyi/limit_cycles.py`

### C36-01 阳九

直接来源数值：

- 大限 4560；
- 小限 456；
- 十小限成一大限；
- 阳盈差 130。

### C36-02 百六

直接来源数值：

- 大限 4320；
- 小限 288；
- 十五小限成一大限；
- 阴盈差 2050。

### C36-03 witness volume variant

识典在线见证题作《太乙统宗宝鉴》卷十；
项目旧资料曾标作卷九。

固定记录 `witness_volume_variant`，不复制算法。

### C36-04 legacy quarantine

旧 pan 的“陽九 / 百六”只是地支位置，不是大小限。

因此 replacement：

- `cycles.limits.yangjiu`
- `cycles.limits.bailiu`

不得自动搬旧值。

### C36-05 pan v2

`cycles` 新增：

`limits`

C12 adapter 支持显式 `cycles` overlay，但仍不从 legacy flat 自动重建。

完整验证：666 passed / 0 failed。

详细记录见 `sources/c36-yangjiu-bailiu-limits-record.md`。

## 9.30 C37 五运六气 / 五音之数来源拆分（已实施）

### C37-01 五运六气

分为两个独立 profile：

- 卷三 `tongzong_volume3_wuyun`：统行五运六气、主客气框架；
- 卷十 `tongzong_volume10_wuyun`：岁会五运六气框架。

禁止把两卷静默揉成一个 canonical 公式。

卷十岁会/天符细表当前继续：

`pending_direct_table_collation`

### C37-02 五音之数

“五音之数 / 五音之元”修正为卷三独立来源。

算数五音复用 D8-03 已校核心：

- 1/2 宫；
- 3/4 徵；
- 5/6 羽；
- 7/8 商；
- 9/10 角。

明确：

`number_subject_rule_d8_08_used=False`

不得把 D8-08 将军/吏士/兵卒映射成五音。

### C37-03 legacy replacement

旧 `五运六气` 是卷三+卷十 mixed flat，因此两 profile 都存在后才清除 replacement gap。

旧 `五音之数` 只需卷三 profile。

### C37-04 C30 contract

`source_variants` 新增：

`wuyun_wuyin`

完整验证：705 passed / 0 failed。

详细记录见 `sources/c37-wuyun-wuyin-source-split-record.md`。

## 9.31 C38 太游阳九 / 百六内外卦行限（已实施）

新增：

`src/kintaiyi/taiyou_limit_tracks.py`

### C38-01 周期

阳九外卦：

- 10 年一宫；
- 80 年一竟；
- 57 竟 = 4560。

百六内卦：

- 36 年一宫；
- 288 年一竟；
- 15 竟 = 4320。

### C38-02 八宫序

卷九直接条文固定：

`7坤 → 8坎 → 9巽 → 1乾 → 2离 → 3艮 → 4震 → 6兑`

顺行八宫，不入中五。

### C38-03 与旧 guiyun 分离

C38 复用 C36 大小限时间轴与盈差；

不采用旧 `dayou_nei_gua/dayou_wai_gua` 的 +34/+50 偏移，
也不把六十四卦轨运、重卦、策数、动爻混入本层。

### C38-04 v2

结果可放：

`cycles.limits.taiyou_tracks`

但旧“卷九” composite wrapper 仍保持 derived / unported。

完整验证：715 passed / 0 failed。

详细记录见 `sources/c38-taiyou-limit-tracks-record.md`。

## 9.32 C39 卷十“五运六气”细表校勘（已实施）

新增：

`src/kintaiyi/wuyun_volume10_collation.py`

C39 在 C37 的卷十 profile 上继续校勘：

- 五运配五音；
- 六气配五行 / 化气；
- 太过、不及、平气纪名；
- 天会 / 岁会 / 逆会 / 辐辏枚举异文。

### C39-01 已校基础表

五运：

- 土 → 宫 / 黄天
- 金 → 商 / 素天
- 水 → 羽 / 玄天
- 木 → 角 / 苍天
- 火 → 徵 / 丹天

六气：

- 厥阴 → 木 / 风
- 少阴 → 火 / 君火
- 太阴 → 土 / 湿
- 少阳 → 火 / 相火
- 阳明 → 金 / 燥
- 太阳 → 水 / 寒

OCR / 传本异文原样保留，不静默统一。

### C39-02 纪名表

太过、不及、平气五行纪名已经结构化，但统宗在线见证与参校读法存在：

- 崇阜 / 敦阜；
- 卑坚 / 卑监；
- 外明 / 升明；
- 主君 / 审平；

等差异，均保持 `canonical_selected=None`。

### C39-03 会类边界

统宗见：

- 天会
- 岁会
- 逆会
- 三合辐辏则为太乙天符

《太白兵备统宗宝鉴》另有“四类并列”见证。

固定：

- `meeting_enum_status=source_variant_unresolved`
- 不以年干捷径直接定太过/不及；
- 缺九宫天符 / 合会结构输入时不得生成太乙天符。

## 9.33 C40 紫庭旧术语库恢复骨架（已实施）

用户确认此前提供的《太乙紫庭祕訣》研易楼藏明钞本已经在本地术语主库做过初步整理；当前 GitHub 只缺旧 `terminology.json` 的迁移。

新增：

- `terminology/zitingjing-migration-map.json`
- `sources/c40-zitingjing-terminology-recovery-record.md`
- `tests/test_zitingjing_terminology_migration.py`
- `tests/reports/c40_zitingjing_terminology_recovery_validation.md`

### C40-01 不重扫

后续恢复旧术语库时，不从零重新做全文术语抽取。

先恢复：

- old term id
- manuscript form
- source page
- source section
- old definition / notes / aliases

再与当前 rule/source key 对齐。

### C40-02 六项映射骨架

- 太乙九星 → `taiyi_nine_stars`
- 文昌九星 → `wenchang_nine_stars`
- 文昌变化 → `wenchang_changes`
- 始击变化 → `shiji_changes`
- 三旗行宫 → `three_banners`
- 九宫贵神 → `nine_palace_nobles`

### C40-03 强制空值

旧术语库或扫描页未恢复前：

- `manuscript_form=null`
- `source_page=null`

不得用统宗、《三才世纬》、现代材料或 OCR 猜测代填研易楼本实际字形 / 页码。

### C40-04 恢复优先级

1. 文昌九星；
2. 三旗行宫；
3. 九宫贵神；
4. 太乙九星；
5. 文昌变化；
6. 始击变化。

前三项优先解决现有紫庭来源缺口；后三项用于补页码、原字形与旧术语 ID。

### C40-05 parser 暂缓

未知旧 `terminology.json` 的真实 schema 前，不写猜测性 migration parser。

待旧文件重新提供后，按真实 schema 写一次性 adapter。

## 9.34 C41 卷九太游重卦 / 四象策数 / 动爻（已实施）

新增：

`src/kintaiyi/dayou_hexagram.py`

### C41-01 重卦结构

直接按卷九：

- 行宫所得卦为内卦；
- 天数所得卦为外卦；
- 外在上、内在下。

### C41-02 四象策数

固定的 36 / 24 / 28 / 32 是**单爻策数**：

- 乾：老阳 36；
- 坤：老阴 24；
- 震 / 坎 / 艮：少阳 28；
- 巽 / 离 / 兑：少阴 32。

每个经卦三爻，因此：

`trigram_ce = per_line_ce × 3`

卷九算例锁定：

- 乾内 108 + 震外 84 = 192；
- 坤内 72 + 乾外 108 = 180。

### C41-03 内卦动爻

36 年一内卦，六年一爻：

- 1–6 初爻；
- 7–12 二爻；
- 13–18 三爻；
- 19–24 四爻；
- 25–30 五爻；
- 31–36 上爻。

当前直接条文未见外卦等价动爻法，因此：

`outer_moving_line=None`

### C41-04 epoch variant

- 统宗见证：+34；
- 《太白兵备统宗宝鉴》养玄子批评 +34，并提出 +36610；
- 旧 `guiyun.py` 外卦 +50 暂无直接明文。

因此 runtime 不选任何 epoch：

- `canonical_selected=None`
- `epoch_formula_applied=False`
- `c38_track_used=False`

完整验证：753 passed / 0 failed。

详细记录见 `sources/c41-dayou-heavy-hexagram-record.md`。

## 9.35 C42 卷九历数长短 / 安居之代（已实施）

新增唯一 canonical runtime：

`src/kintaiyi/dayou_lishu.py`

### C42-01 纳甲干支数

固定：

- 甲己子午 = 9；
- 乙庚丑未 = 8；
- 丙辛寅申 = 7；
- 丁壬卯酉 = 6；
- 戊癸辰戌 = 5；
- 巳亥 = 4。

在线 OCR 的“己亥四”保留为 witness，经参校正规化为“巳亥四”。

### C42-02 爻位加数

- 初 / 四：只加本爻纳甲干支数；
- 二 / 五：六爻全部纳甲干支数求和后倍加；
- 三 / 六：亢极，不倍不加。

### C42-03 策数除减中间量

历史算例存在：

- 洪武例：535 % 180 = 175，算术一致；
- 万历己未例：146、192、48 三数字无法按同一普通取余公式成立。

因此：

- `automatic_remainder_formula=None`
- `status=source_example_conflict_requires_explicit_base`

只有调用方显式提供 `base_remainder_after_ce` 才继续给最终历数。

### C42-04 安居之代

基础爻位：

- 一、二、四、五：历数长；
- 三、六：历数短；
- 二：正旺；
- 五：时已过；
- 三：内极灾较轻；
- 六：外极灾较重。

阴阳得失位、阳爻有无应、君臣合格及掩迫囚击等只作为独立证据，不覆盖基础长短。

### C42-05 单一真源

并行产生的重复 `dayou_lifespan.py` 已清除，不保留第二套公式。

当前验证基线：782 passed / 0 failed。

详细记录见 `sources/c42-dayou-lishu-record.md`。

## 9.36 C43 卷九厄会行限严格来源契约（已实施）

新增：

`src/kintaiyi/volume9_ehui.py`

### C43-01 旧实现不得直接迁移

原文要求完整即位年干支、加大义后的太阳/阴主落点、大武/和德界顺逆与神数累计。

旧 `guiyun.ehui_xingxian` 只用年支并做十六位简单步数，因此：

`canonical_equivalent=False`

### C43-02 严格输入

C43 只消费：

- `enthronement_ganzhi`
- `taiyang_landing`
- `yinzhu_landing`
- `direction`
- `count_evidence`

缺一则 `not_computable`，不猜盘式。

### C43-03 汉高祖例

乙未即位：

- 太阳临申；
- 阴主临寅；
- 逆行；
- 起数1 + 大威2 + 大炅9 + 高丛4 = 16。

第12年太乙格另作 correction evidence，不覆盖基础16年。

### C43-04 v2 / legacy

C30 新增：

`source_variants.volume9`

旧 `厄會行限` replacement：

`source_variants.volume9.ehui_limit.legacy_replacement`

只有完整 C43 结果才清除 migration gap。

完整验证：799 passed / 0 failed。

详细记录见 `sources/c43-volume9-ehui-record.md`。

## 9.37 C44 国政革易 / 法令变更严格来源模型（已实施）

新增：

`src/kintaiyi/volume9_governance.py`

### C44-01 旧实现边界

旧 `guozheng_bianyi(year_zhi)` 只接年支并静态旋转六神，不能表达原文“吕申加创立新事之年”。

固定：

`canonical_equivalent=False`

### C44-02 严格输入

要求：

- 完整创立年干支；
- 太簇、太阳、阴主、地主、武德、大义六神落点；
- 算长 / 短；
- 算和 / 不和；
- 六神落宫格局检查。

无格局也必须显式传空 dict。

### C44-03 远近期

- 长且和 → 远；
- 短不和 → 近。

两见证远例均为 90 / 180。

近期见证不同：

- 统宗：9 / 28；
- 太白兵备：9 / 18。

因此只判远 / 近，不选择具体年数。

### C44-04 source variant

太白兵备另并列“大神”毁折废弃类事；
统宗核心仍以六神为主，不静默合并。

### C44-05 v2 / legacy

旧 `國政章易` replacement：

`source_variants.volume9.governance_change.legacy_replacement`

完整验证：818 passed / 0 failed。

详细记录见 `sources/c44-volume9-governance-record.md`。

## 9.38 C45 岁中灾发月日之期（已实施）

新增：

`src/kintaiyi/volume9_disaster_timing.py`

### C45-01 两阶段

第一阶段：

`太岁合神加岁支 → 文昌 / 天目所临及冲处 → 灾发月`

第二阶段：

`当月合神加月支 → 文昌 / 天目所临及冲处 → 日层之期`

月层与日层各自保留输入，不用单层结果冒充完整“月日之期”。

### C45-02 文昌 / 天目双目标

原文并举文昌、天目，因此两个阶段都要求两者的显式落点。

缺天目时：

`not_computable`

旧只看单一 skyeyes / 文昌的实现不能清除 migration gap。

### C45-03 四维边界

月份只在落十二支时换算：

- 寅1 … 丑12。

若落艮 / 巽 / 坤 / 乾：

- 保存十六宫 point；
- 月份不擅自折算；
- 月层保持不完整。

日层同样先保存 point；只有落十二支时才填 `day_branch`。

固定：

`specific_calendar_day=None`

不得把四维位冒充地支日，也不得伪造具体现代日期。

### C45-04 水旱 / 年度证据

文昌宫阴阳由上游显式提供：

- 阳宫 → 旱；
- 阴宫 → 水。

禁止旧 `_YANG_GONG` 猜测。

文昌同太乙与格 / 掩 / 迫 / 击 / 挟 / 提只作为“君臣不协、岁不丰稔”证据，不改灾发月候选。

### C45-05 legacy replacement

旧 `歲中災發` 保持 quarantine。

只有：

- month_stage computable；
- day_stage computable；

同时成立，才生成：

`source_variants.volume9.disaster_timing.legacy_replacement`

当前验证：841 passed / 0 failed。

详细记录：

- `sources/c45-volume9-disaster-timing-record.md`
- `tests/reports/c45_validation.md`

## 9.39 C46 阴阳九厄水旱灾期（已实施）

新增：

`src/kintaiyi/yinyang_nine_calamities.py`

### C46-01 九段按“段长”累计

直接来源的九段长度：

- 106
- 374
- 480
- 720
- 720
- 600
- 600
- 480
- 480

合计 4560。

旧 `guiyun.yinyang_jiu_e` 把这些数直接当累计阈值比较，第二段以后会错位。

C46 改为先累计成：

- 1–106
- 107–480
- 481–960
- 961–1680
- 1681–2400
- 2401–3000
- 3001–3600
- 3601–4080
- 4081–4560

固定：

`legacy_reference_audit.canonical_equivalent=False`

### C46-02 灾年

九厄灾年：

`9 / 9 / 9 / 7 / 7 / 5 / 5 / 3 / 3`

总计 57 年。

五阳主旱，四阴主水。

### C46-03 文本异文

保留并校：

- 第四段 702 / 720；
- “四阳七灾水” / “四阴七灾水”；
- “九阳三灾旱五年”中的 3 / 5 冲突。

runtime 只在平行见证与篇内总数 / 算术一致时正规化：

- 第四段取 720；
- 第四段取阴；
- 第九灾年取 3。

### C46-04 周期

使用：

`(accumulated_year + 130) mod 4560`

余 0 视为第4560年。

灾期取各段末尾对应的 9 / 7 / 5 / 3 年。

详细记录：

- `sources/c46-yinyang-nine-calamities-record.md`
- `tests/reports/c46_validation.md`

## 9.40 C47 小游轨运 / 重卦 / 动爻（已实施）

新增：

`src/kintaiyi/xiaoyou_hexagram.py`

### C47-01 内卦

- 大周 1920；
- 小周 192；
- 24 年一经卦；
- 4 年一爻；
- 卦序：乾、离、艮、震、兑、坤、坎、巽。

统宗在线一见证的大周数字 OCR 残损；
《太白兵备统宗宝鉴》参校明确 1920 / 192 / 24，并有万历己未余80、入震8年的算例。

### C47-02 外卦

- 纪元周 360；
- 八卦周 24；
- 3 年一经卦；
- 第一年理天；
- 第二年理地；
- 第三年理人。

### C47-03 重卦

- 外卦在上；
- 内卦在下；
- 动爻只取内卦4年一爻；
- 不另造外卦动爻；
- 不强制命名六十四卦。

固定：

`hexagram_name=None`

`hexagram_name_status="not_resolved_in_c47"`

### C47-04 与大游分离

只复用 C41 已校四象策数表。

固定：

- `c38_track_used=False`
- `dayou_epoch_offset_used=False`

不使用大游 +34 / +50，也不与阳九百六太游轨迹混并。

详细记录：

- `sources/c47-xiaoyou-hexagram-record.md`
- `tests/reports/c47_validation.md`

C46/C47 功能测试加入后的已确认基线：

`882 passed / 0 failed`

## 9.41 C48 小游统卦行爻所主灾祥（已实施）

新增：

`src/kintaiyi/xiaoyou_line_omens.py`

### C48-01 四层分离

C48 只消费 C47：

- 爻位；
- 外卦三才；
- 格局；
- 显式纳甲。

不重算小游轨运，不强制命名六十四卦。

### C48-02 爻位

- 二、五：安平；
- 初、四：算和且有应为吉；
- 初、四：不和且无应，君臣失助、世不宁；
- 三：内极，基础为“事多凶变”；
- 六：外极，基础为“事多凶变”。

只有又逢凶格时才追加“内极尚轻 / 外极为重”。

初四的算和/应必须显式输入。

### C48-03 三才

- 理天：天有变异、日月失辉、五星失度类；
- 理地：风雨不调、禾谷不成；
- 理人：人民疾疫、时多荒俭。

### C48-04 格局

关、囚、掩、迫、击、挟、格、对只作灾象加重证据：

`patterns_aggravate_only=True`

不覆盖基础爻位判断。

### C48-05 纳甲

必须显式提供：

`moving_line_najia=[天干, 地支]`

缺纳甲时返回 partial。

固定：

`legacy_sixtyfour_hexagram_lookup_used=False`

### C48-06 分野与 OCR

天干 / 地支分野按本条直接正文重建，不使用旧 `_YAO_GAN_FENYE` 的扩展。

“风宣”“夭慧变现”等 OCR 不稳文字保留 witness，不静默改义。

丁 / 辛分野参校另保留《太白兵备统宗宝鉴》“南海 / 西戎梁益”等读法；统宗主见证仍保持“蛮 / 西域”。纳甲干支配对只校验天干与地支字符，不套六十甲子日辰奇偶规则。

完整验证：914 passed / 0 failed。

详细记录见 `sources/c48-xiaoyou-line-omens-record.md`。

## 9.42 C49 太游 / 小游行宫卦不同术（已实施）

新增：

`src/kintaiyi/taiyou_xiaoyou_distinction.py`

### C49-01 本术不是“当前两卦不等”

原文固定：

- 太游：36年行一内卦，得乾天之策；
- 小游：24年行一内卦，得坤地之策；
- 二者有尊卑上下之别。

但原文同时明确：

- 太游得乾天之策仍可行坤；
- 小游得坤地之策仍可行乾。

因此乾 / 坤之策是率义，不是卦位限制。

### C49-02 canonical 差异

- 太游内卦依赖 C38-BL-INNER；
- 小游内卦依赖 C47-XY-INNER；
- 36 / 24 周期职责固定不同。

固定：

`systems_distinct=True`

`distinct_by_current_trigram_inequality=False`

### C49-03 当前同 / 异卦

允许比较当前内卦，但只标：

`semantic_status="derived_observation_not_source_verdict"`

当前同卦不取消制度差异；
当前异卦也不是本术唯一判据。

### C49-04 旧实现

旧 `guiyun.zonghe()['行宮卦異']` 只有：

`dayou["內卦"] != xiaoyou["內卦"]`

因此：

`canonical_equivalent=False`

完整验证：927 passed / 0 failed。

详细记录：

- `sources/c49-taiyou-xiaoyou-distinction-record.md`
- `tests/reports/c49_validation.md`

## 9.43 C50 太乙历数之期证据聚合层（已实施）

唯一 canonical runtime：

`src/kintaiyi/taiyi_lishu_evidence.py`

### C50-01 本术不是单一寿数公式

正文以“帝王应天顺人始终之期”为总纲。

基础厄会：

- 即位年支加大义；
- 视太阳 / 阴主；
- 并取各自合神，共成“四神”。

随后还须参详：

- 太乙入运气爻卦象；
- 太游轨运卦爻；
- 小游轨运卦爻；
- 内外极限；
- 囚迫击格掩挟。

因此固定：

- `final_lifespan_formula=None`
- `final_lifespan_years=None`

### C50-02 与 C42 / C43 分层

- C42：卷九策数 / 纳甲 / 历数长短；
- C43：基础厄会显式证据；
- C50：帝王始终历数的多层证据聚合。

禁止把任一旧单函数直接当 C50 总公式。

### C50-03 完整证据包

要求：

- 合法六十甲子即位年；
- C43 厄会；
- 太阳 / 阴主及其合神四神期；
- C41 太游重卦；
- C47 小游重卦；
- 太乙入运气卦象；
- 囚迫击格掩挟检查。

证据齐备后仍只返回 evidence bundle，不自动生成终年。

### C50-04 登位云气数

统宗与太白兵备参校后保留五行生数 / 成数双值：

- 木 3 / 8；
- 火 2 / 7；
- 土 5 / 10；
- 金 4 / 9；
- 水 1 / 6。

固定：

`selected_number=None`

不擅自选生数或成数。

### C50-05 去重

重复 `imperial_lishu_scope.py` 已删除。

完整验证：955 passed / 0 failed。

详细记录：

- `sources/c50-taiyi-lishu-evidence-record.md`
- `tests/reports/c50_validation.md`

## 9.44 C51 登位旁云气生克 / 干支数（已实施）

新增：

`src/kintaiyi/coronation_cloud_omens.py`

### C51-01 日 / 辰分离

正文明确：

- 以干为日；
- 以支为辰。

因此日干五行与日支五行分别参与判断。

干支五行映射明确以《五行大义·第五论配支干》作背景依赖，不把该参校提升成《统宗》正文。

旧 `yunqi_zhanbo` 只取日干五行，不能作为 canonical 等价实现。

### C51-02 五种生克

独立保存：

- 云生日；
- 云生辰；
- 云克日；
- 日生云；
- 比和。

多个关系可以同时成立，不用 if / elif 压成单一断语。

### C51-03 云形

- 阴云 → 位祚不久；
- 五色彩云 → 国代绵远寿昌、子孙兴旺。

阴云 / 五色彩云允许不提供单一云色；此时只解释形态，不计算云与日/辰五行生克。

### C51-04 云气双数

继续沿用 C50 生数 / 成数双值：

- 木3/8；
- 火2/7；
- 土5/10；
- 金4/9；
- 水1/6。

不自动选择单一云数。

### C51-05 干支和数

复用 C42 已校干支数。

只输出：

`stem + branch = sum`

当前直接正文未给无歧义的年 / 月 / 日时尺度选择式，因此：

- `time_scale=None`
- `specific_period=None`

完整验证：970 passed / 0 failed。

详细记录：

- `sources/c51-coronation-cloud-omens-record.md`
- `tests/reports/c51_validation.md`

## 9.45 C52 太乙十精来源注册表（已实施）

新增唯一 canonical registry：

`src/kintaiyi/ten_essences_source_registry.py`

### C52-01 十精名单

固定次序：

1. 天皇
2. 帝符
3. 天时
4. 太尊
5. 飞鸟
6. 五行
7. 八风
8. 五风
9. 三风
10. 太乙数

旧 `yunqi._TEN_JING_FN` 的“地符 / 太岁”不能作为 canonical 十精名称。

### C52-02 小周数

固定：

`20 / 20 / 12 / 4 / 9 / 5 / 9 / 9 / 9 / 72`

C52 只确认来源与小周，不迁位置公式。

### C52-03 卷次边界

《太乙统宗宝鉴》不同见证将十精篇编为卷十八或卷二十。

固定：

`volume_status="witness_volume_variant"`

《武经总要》与《太白兵备统宗宝鉴》作独立参校。

### C52-04 旧公式审计

明确冲突：

- 旧 `config.flybird`：%8；直接小周9；
- 旧 `config.fivewind`：%29；直接小周9。

其他旧函数即使周期表面相合，也仍：

`runtime_ready=False`

须逐项核起宫、顺逆、重留、宫序、余0及盈差。

### C52-05 十精云气分层

“十精太乙云气所主”保持独立 source unit。

C52 不迁：

- 合太乙；
- 阴阳宫；
- 旺相休囚；
- 天气厚薄；
- 风雨云雾断语。

### C52-06 v2 / migration

C15 中：

- 帝符
- 太尊
- 飛鳥
- 三風
- 五風
- 八風

升级为：

`source verified / formula pending`

但：

- 不扩展 pan v2 contract；
- 不生成 legacy replacement；
- 不写入 cycles root。

clean CI：1006 passed / 0 failed。

详细记录：

- `sources/c52-ten-essences-source-registry-record.md`
- `tests/reports/c52_validation.md`

## 9.46 C53 九宫 / 四正型十精位置 runtime（已实施六项）

唯一 runtime：

`src/kintaiyi/ten_essences_positions.py`

实现：

- 飞鸟：90 / 9；
- 五风：90 / 9；
- 太尊：40 / 4；
- 八风：90 / 9；
- 三风：90 / 9；
- 五行：50 / 5。

所有函数要求显式阳/阴遁，不从日期自动推遁。

固定边界：

- 飞鸟十精神位 ≠ J4M-11 外部飞鸟观测；
- 十精云气断事不随位置自动计算；
- 被正文否定的附加盈差不应用。

C53 catalog 只声明本模块六项；其他层委托：

- 天皇 → C55-TIANHUANG；
- 帝符 → C55-DIFU；
- 太乙数 → C54-TAIYI-NUMBER；
- 天时 → C56-TIANSHI。

## 9.47 C54 十精太乙数（已实施）

新增：

`src/kintaiyi/ten_essences_number.py`

固定：

- 周法 360；
- 元法 72；
- 输出 1..72；
- 余0按周期末项处理。

旧 `yunqi.shijing_shu` 只认可数值核心相合；
30/40/50等天气断语不属于 C54。

详细记录：

- `sources/c54-ten-essences-number-record.md`
- `tests/reports/c54_validation.md`

## 9.48 C55 天皇 / 帝符十六神重留（已实施）

新增：

`src/kintaiyi/ten_essences_sixteen_gods.py`

两项均：

- 大周200；
- 小周20；
- 十六神顺行；
- 四处各重留一算；
- 阴局按统宗主 profile 逐步取阳局对冲。

天皇四维重留：

- 阴德 / 乾；
- 和德 / 艮；
- 大炅 / 巽；
- 大武 / 坤。

帝符四正重留：

- 地主 / 子；
- 高丛 / 卯；
- 大威 / 午；
- 太簇 / 酉。

并行产生的错误重复 `C53-DIFU` 已删除，帝符唯一 canonical 固定为 `C55-DIFU`。

盈差异文全部只留证、不应用。

详细记录：

- `sources/c55-ten-essences-sixteen-gods-record.md`
- `tests/reports/c55_validation.md`

当前 clean baseline：

`1080 passed / 0 failed`

## 9.49 C56 天时 120 / 12 runtime（已实施）

新增：

`src/kintaiyi/ten_essences_tianshi.py`

### C56-01 统宗主公式

固定：

- 大周 120；
- 小周 12；
- 阳局吕申（寅）起；
- 顺行十二辰；
- 阴局取阳局对冲，因此申起；
- 阴局同样顺行十二辰。

阳：

`寅 → 卯 → 辰 → 巳 → 午 → 未 → 申 → 酉 → 戌 → 亥 → 子 → 丑`

阴：

`申 → 酉 → 戌 → 亥 → 子 → 丑 → 寅 → 卯 → 辰 → 巳 → 午 → 未`

### C56-02 太白兵备内部异文

《太白兵备统宗宝鉴》同页出现两层文字：

- 前置总括句：阳申、阴寅；
- 完整推步正文：阳寅、阴申，均顺行十二宫。

后者又在算法总结处重复“阳寅阴申起”，并与统宗主公式一致。

因此：

- 完整推步正文用于参校 canonical；
- 前置总括句保留为 `intro_summary_variant`；
- 不删异文，不取折衷，不静默倒换起点。

《武经总要》主条“吕申起、顺行十二辰”继续作独立参校；一见证另有“阴起武德（申）”补句。

### C56-03 邦盈差

邦盈差二由统宗正文明确否定。

固定：

- `witness_value=2`
- `apply=False`

### C56-04 十精基础层完成

当前位置九项全部有唯一 runtime：

- C53：飞鸟、五风、太尊、八风、三风、五行；
- C55：天皇、帝符；
- C56：天时。

数值层：

- C54：太乙数。

C52 registry 当前：

- `pending_position_runtimes=[]`
- `all_position_runtime_ready=True`
- `implemented_number_runtimes=["太乙数"]`

这里的“完成”只指位置 / 数值基础层；十精云气、旺相休囚、合会断事仍是独立后续层。

完整验证：

`1095 passed / 0 failed`

详细记录：

- `sources/c56-ten-essences-tianshi-record.md`
- `tests/reports/c56_validation.md`

## 9.50 C57 十精太乙云气显式合会层（已实施）

新增：

`src/kintaiyi/ten_essences_cloud_omens.py`

### C57-01 显式合会，不自动同宫

C57 只解释调用方显式给出的：

- 合太乙；
- 合天目；
- 十精之间合会；
- 旺相 / 非旺相；
- 太乙所在阴 / 阳宫；
- 太尊、飞鸟少数直接宫位断语。

固定：

- `auto_position_lookup_used=False`
- 不读取 C53/C55/C56 落宫自动制造“合”
- 无合会时也须显式传空 list

### C57-02 飞鸟层级分离

十精飞鸟是推步神位。

J4M-11 飞鸟是真实外部观测。

两者不得互相替代。

### C57-03 见证异文

保留：

- 天皇合飞鸟：“有阴雨 / 小阴雨”；
- 天皇合天时：“阴昏 / 小昏”；
- 三风合天时：“小阴雨 / 小阴风”；
- 五行、八风条“地符 / 帝符”名称异文。

只有稳定核心可正规化；真异文固定 unresolved。

### C57-04 张良总括句

统宗在线与《三才世纬》对“阳宫暗 / 晴旱”及“五行是否列入”有差异。

固定：

- `canonical_selected=None`
- `runtime_applied=False`

总括句不覆盖各十精逐条直接断语。

### C57-05 十精云气尚未全完成

C57 只完成合会层。

仍 pending：

- 太乙初移宫云色时变；
- 天气纯厚 / 薄、黄雾、黑赤、青白等形态；
- 天旱取阳 / 天雨取阴总括；
- 旺相使变速修饰；
- 太乙数30 / 40 / 50等天气断语。

因此 C52 registry 固定：

- `cloud_conjunction_runtime_ready=True`
- `cloud_runtime_ready=False`

完整验证：

`1115 passed / 0 failed`

详细记录：

- `sources/c57-ten-essences-cloud-conjunctions-record.md`
- `tests/reports/c57_validation.md`

## 9.51 C58 十精初移宫云色时变 / 天气观察层（已实施）

新增：

`src/kintaiyi/ten_essences_cloud_observations.py`

### C58-01 观察事件分层

C58 专属：

`太乙初移宫候云气`

不等于 C51：

`天子初登位日月旁云气`

也不等于 C57 十精合会层。

### C58-02 云色时变

统宗当前直接见：

- 青3/4 → 寅卯；
- 白7/6 → 申酉；
- 黑1/8 → 亥子。

赤9/2 → 巳午由《太乙金镜式经》《武经总要》一致参校支持；
统宗当前在线 OCR / 图像转写缺该句，因此标：

`collation_supported_primary_online_gap`

### C58-03 旧白云错误

旧表白7/6 → 亥子错误。

canonical：

`白7/6 → 申酉`

`黑1/8 → 亥子`

### C58-04 观察窗口

日计：

- 初移宫本日；
- 日出 / 日午 / 日晡；
- 后二日不候。

时计：

- 初移宫本时；
- 后二时不占。

### C58-05 天气形态

显式观察：

- 纯厚 → 雨；
- 华薄 → 风；
- 黄雾 → 晕；
- 黑赤 → 风；
- 青白 → 寒；
- 凝润 → 雾雨；
- 如扫 → 晴；
- 文彩轮囷萧索 → 大晴。

三才世纬“黑赤风热 / 青白风寒”只作参校扩展。

### C58-06 总括修饰

- 旱 → 阳占；
- 雨 → 阴占；
- 旺相 → 变疾速。

飞鸟合太乙风向存在：

- 上来；
- 下来；

异文，固定 `canonical_selected=None`。

当前 C52：

- `cloud_conjunction_runtime_ready=True`
- `cloud_observation_runtime_ready=True`
- `cloud_number_omen_runtime_ready=False`
- `cloud_runtime_ready=False`

完整验证：

`1161 passed / 0 failed`

详细记录：

- `sources/c58-ten-essences-cloud-observations-record.md`
- `tests/reports/c58_validation.md`

## 9.52 后续 C59+

下一优先级：

1. C59：太乙数30/40/50及与太乙/天目/飞鸟等合会天气数值层；
2. 完成后再判断十精云气整体能否标 `cloud_runtime_ready=True`；
3. C60 继续维护全局旧错误公式 / 非等价实现隔离；
4. 清扫 C15 remaining pending / source_variant；
5. 恢复旧 terminology.json，并继续文昌九星 / 三旗 / 九宫贵神归属核证。

## 10. 验收

每批至少运行现有 pytest/ruff（若配置存在）。不得为了兼容把已确认错误公式改回去。兼容的是 API/keys/类型，不是错误答案。
