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

## 9.30 后续 C37+

下一优先级：

1. 五运六气 / 五音之数继续保持跨卷 source_variant，先做卷三 / 卷十来源拆分；
2. 明阳九百六太游行限观历术的“外卦十年一宫 / 内卦三十六年一宫”另建规则，不塞入 C36 大小限；
3. 继续寻找文昌九星附篇正文；
4. 三旗行宫 / 九宫贵神继续归属核证；
5. 剩余 P2/P3 字段按 C30 固定槽位迁移。


## 10. 验收

每批至少运行现有 pytest/ruff（若配置存在）。不得为了兼容把已确认错误公式改回去。兼容的是 API/keys/类型，不是错误答案。
