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

## 9.7 《太乙金镜式经》卷四军事十二法来源层（J4M，已建档第一阶段）

新增 `rules/jinjing_v4_military.json` 与 `sources/jinjing-v4-military-12-record.md`。

### J4M-01..12 固定顺序

以四库本《太乙金镜式经》卷四**正文小标题顺序**为 canonical：

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

卷首目录的短题/异写只记 `toc_aliases`，不得另建重复术。

### J4M 与 C8 的边界

- J4M 是《金镜》卷四 source profile。
- C8 当前 `volume5_strict` 是旧 `junshi_zhanlue` 拆分后的组合边界。
- crosswalk 只说明语义落点，不能把 partial 误标为 implemented。
- J4M-03“主客相关法”与 J4M-04“推主客”必须分层。
- J4M-07“制阵随地”与 J4M-08“随地制变”必须分层。
- J4M-05 不得用《统宗》卷五的兵额表替代。
- J4M-06 不得用旧卷十五“陈兵出乡”替代。

### J4M-09 来源差异

四库本《金镜》卷四正文列：

- 8/3/4：地内助主；
- 9/2/7/6：天外助客；
- 1 宫未列入该段地内组。

《太乙统宗宝鉴》卷五同名术列：

- 1/8/3/4：天内助主；
- 9/2/7/6：天外助客。

必须保存为两个 source profile；禁止用旧代码 `[1,8,3,4]` 静默覆盖《金镜》卷四记录。

### 后续实现顺序

先做纯表与低依赖规则 J4M-06、07、09，再接 J4M-05、10；J4M-03 需统一日计纳音与主客目五行输入；J4M-11、12 需要显式外部观测模型，无观测时返回 `not_computable`。


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

## 9.11 C18 《紫庭经》主来源 / 统宗参校层（已实施第一阶段）

P1 前六项已经建立来源容器：

- 太乙九星 / 文昌九星；
- 文昌变化 / 始击变化；
- 三旗行宫 / 九宫贵神。

### C18-01 来源层级

固定：

- **主要参考：《紫庭经》**
- **参校来源：《太乙统宗宝鉴》卷六 / 卷十**
  - 太乙九星、文昌九星、文昌变化、始击变化：统宗卷六参校；
  - 三旗行宫、九宫贵神：统宗卷十参校。

“参校”可用于校异、补证、版本对读；不得静默覆盖《紫庭经》主来源。

### C18-02 来源容器

新增 `src/kintaiyi/zitingjing_sources.py`。

每条规则分别保存：

- `primary_source="zitingjing"`
- `primary_result`
- `collation_sources`
- `collation_results`
- `canonical_selected`
- `cross_source_merge=False`

仅有统宗参校结果时：

- `primary_ready=False`
- `canonical_selected=None`
- `status="primary_pending"`

只有存在《紫庭经》结构化主来源结果时，才允许：

`canonical_selected="zitingjing"`

### C18-03 legacy quarantine

旧 `pan()` 中这六项当前实现来自统宗系代码，不能直接升为新 canonical。

因此 C14 将它们改为 quarantined，并要求 replacement path 指向对应：

`source_variants.zitingjing.rules.<rule>.primary_result`

只有参校结果、没有主来源结果时，C13 replacement gap 仍然存在。

### C18-04 参校不是弃用

统宗卷六/卷十继续保留在 `collation_results` 中，用于：

- 校异；
- 补证；
- 对读；
- 记录后世收录差异。

禁止把“参校”理解为“不使用统宗”。

详细记录见 `sources/c18-zitingjing-primary-record.md`。

## 9.12 后续 C19+

- 逐条整理《紫庭经》六项正文和表格，形成真正 `primary_result`；
- 同步保存统宗卷六/卷十参校差异；
- 若主来源与参校本不一致，进入 source_variant/variant_note，不做无痕合并；
- 卷十五、卷十七军事层继续按独立 derived profile 拆分。


## 10. 验收

每批至少运行现有 pytest/ruff（若配置存在）。不得为了兼容把已确认错误公式改回去。兼容的是 API/keys/类型，不是错误答案。
