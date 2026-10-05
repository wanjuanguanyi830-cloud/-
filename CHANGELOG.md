# 变更记录

## 2026-10-04 — 《太乙金镜式经》格局规则集首版

- 新增《金镜》卷三格局引擎，使用十六神精确坐标与八宫环 `8→3→4→9→2→7→6→1`。
- 规则版本标记为 `jinjing-geju-1.0.0`，结构化事件记录规则版本和来源。
- 重定掩、击、迫、囚、关、格、对、提挟、挟闭、执提、提格及四郭固／四郭杜；主字段统一为“四郭杜”， “四郭社”仅保留异文说明。
- 增加卷四八门 30 年分段、240 年周期实现，覆盖余数为 0 的边界。
- 增加历史局例与 144 局 `skyeyes_summary` 类别差异审计。
- 主规则只来自《太乙金镜式经》；《太乙淘金歌》及参考代码仅用于历史对照。
- 独立结构化详情接口提供 `to_legacy_dict()` 转换及 `TaiyiGejuMixin` 旧方法适配入口。

测试和历史差异见 [`tests/`](tests/) 与 [`tests/reports/skyeyes_summary_audit.md`](tests/reports/skyeyes_summary_audit.md)。

## 2026-10-04：太乙七术＋八占＋公共规则层 v1

新增独立七术、八占、公共规则、五福/大游与旧名兼容入口。项目canonical与异文/短句/古例/推导例分层保存；缺输入或未确认规则明确返回不可计算或待校。完整记录见 `docs/taiyi_v1.md`。已有格局规则及其测试保留。


## 2026-10-05 — 现代太乙纳音 profile 独立化

- 将现代《太乙数纳音体系（修正版）》从 J4M-03 命名空间移出。
- runtime 迁至 `src/kintaiyi/variants/modern_liunian_nayin.py`。
- machine rules 迁至 `rules/variants/modern_liunian_nayin.json`。
- profile 固定为 `modern_liunian_nayin_2026`，variant id 固定为 `MODERN-LIUNIAN-NAYIN`。
- 删除旧 `src/kintaiyi/modern_nayin_variant.py` 与 `rules/j4m03_nayin_variants.json`。
- J4M-03 只保留古籍 canonical / ancient collation；旧 `wc_n_sj` 继续 quarantined。
- 新增命名空间防回归测试，禁止旧 import / 旧 JSON 路径恢复。


## 2026-10-05 — C40 紫庭旧术语库恢复骨架

- 确认研易楼藏明钞《太乙紫庭祕訣》此前已在本地术语库做过初步整理。
- 当前 GitHub 尚未迁入本地 `terminology.json`，因此不重新做全文术语扫描。
- 新增 `terminology/zitingjing-migration-map.json`。
- 固定六项紫庭相关术语到当前 rule/source key 的恢复映射。
- `manuscript_form` 与 `source_page` 在旧术语库或扫描页恢复前必须保持 null。
- 文昌九星外部异文仅用于旧词条命中，不得代填研易楼本 canonical 字形。
- 三旗行宫 / 九宫贵神即使旧术语库存在词条，也不能单凭词条存在升级紫庭来源等级。


## 2026-10-05 — C52–C56 十精基础层收口

- C52 锁定十精名单、小周数、卷十八/卷二十见证边界，并隔离旧“地符/太岁”名称错误。
- C53 重建飞鸟、五风、太尊、八风、三风、五行六项位置 runtime；旧 `%8` 飞鸟与 `%29` 五风不得回流。
- C54 将太乙数独立为 360/72 纯数值层，不混入天气断语。
- C55 建立天皇/帝符 200/20 十六神重留 runtime；帝符四正重留固定为四处，17/70 盈差异读均只留证不应用。
- 删除并行错误的 C53-DIFU，帝符唯一 canonical 为 `C55-DIFU`。
- C56 将天时固定为统宗主 profile：阳寅、阴申起，均顺行十二支；太白兵备同页“阳申阴寅”前置总括句保留为内部异文。
- 十精九项位置 runtime 与太乙数数值 runtime 已全部具备唯一来源实现；十精云气/合会/天气断事仍保持独立未迁。
- C56 收口整库验证：1095 passed / 0 failed。


## 2026-10-05 — C57–C60 十精云气与旧公式隔离

- C57 将十精合会、旺相、阴阳宫和少数宫位直断独立为显式证据层，禁止从位置自动制造“合”。
- C58 将太乙初移宫云色时变与天气厚薄/色象独立为真实观察层，并纠正旧白7/6→亥子的错误映射为申酉。
- C59 将太乙数天气层与 C54 数值层分开：30/40直接结构化，50句读异文保持 unresolved，旧10/5独立特例不采用。
- C52 十精云气状态现由 C57+C58+C59 三层组成；三层 runtime 已齐备，但所有真实异文继续保留。
- C60 建立集中旧公式 quarantine registry，除单项错误公式外，也隔离 `shijing_luo`、`yunqi_hehui`、`yunqi_zongduan`、`zonghe` 等会重新制造自动同宫和混层的旧综合 wrapper。
- 现代纳音 profile 继续作为独立 modern reconstruction，不因非古籍来源而误归“错误公式”。
- C60 扩展后整库验证：1197 passed / 0 failed。


## 2026-10-05 — C113 旧分支遗留同宫关系恢复

- 重新清点 2026-10-04 / 2026-10-05 旧分支，确认四组已完成但未正式迁入 main 的关系：五福×大游、五福×小游、四神×小游、大游×小游。
- 按《太乙统宗宝鉴》卷七 NGJ / CADAL 见证重新核源，不直接 cherry-pick 旧 project canonical。
- 新增 `src/kintaiyi/wander_conjunctions.py` 与 `tests/test_c113_wander_conjunctions.py`。
- 五福×大游保留“五福条 / 大游条”两个来源层；不自动计算“对冲之分”。
- 五福×小游要求显式 `virtue=True/False` 才选择“有德者昌 / 失德者殃”。
- 四神×小游锁定“人民不安、多生水涝疾疫”；大游×小游据两见证稳定采用“兵丧、水旱、凶暴大作”。
- 更新 `sources/prior-branch-recovery-inventory.md`：C107 已 supersede 旧“大游所在宫未完成”状态；C113 完成上述四组关系核销。


## 2026-10-05 — C114 八占历史例回归恢复

- 从 2026-10-04 warfare 旧 fixture 恢复三条此前未以历史身份迁入 main 的八占古例。
- D8-02：贞观四年主算31，长、利深入。
- D8-04：光化三年主算单3，为单阳。
- D8-08：天宝十年客算17，将吏兵卒皆备。
- 三条均按《太乙统宗宝鉴》卷五 NGJ/CADAL 见证重新核对。
- 新增 `tests/fixtures/eight_divinations_historical_cases.json` 与对应 C114 回归测试。
- 明确保留 D8-08 结构边界：17 的古例标签不得外推成“16以上皆具”；5、15、25、35 继续按十/五/一结构判定。


## 2026-10-05 — C116–C121 卷一玄命 / 考时 / 黄道 / 时计八门 / 直使

- C116：实现“推太乙玄命法”身份→玄命所主直接表，不由玄命表本身生成吉凶。
- C117：实现“推太公考时法”的显式条件链；吉道固定开休生，玄命合要求匹配+旺相+上下相生；“直使前三五、后二四”继续待校。
- C118：实现二十四气黄道日度、二十八宿宿度、十二分野与节气第N日日度推进；“立冬六日日在心宿”回归通过；虚宿度数转录歧义不强补。
- C119：实现卷一时计八门直使，阳遁开生惊休、阴遁杜死伤景，30时一移门；与旧30年岁计八门分层。
- C121：实现阴阳遁太乙直使六纪夜半甲子锚点；保存王希明对张良固定日法的气应修正边界，不把六纪表直接扩成全年连续公式。


## 2026-10-05 — C123 《金镜》卷一岁计八门

- 将旧 `rules/jinjing/eight_door.py` 的240年/30年核心正式归源到卷一“推八门占岁计法”，不再误标为卷四。
- 新 canonical runtime：`src/kintaiyi/jinjing_year_eight_doors.py`，按720→240→30计算直门。
- 开元十二年甲子积1937281算落开门第1年；30年后落休门第1年。
- C123 与 C119 时计八门分层：30年一门 ≠ 30时一门。
- legacy wrapper 继续输出繁体门名并保留0输入兼容，避免破坏现有格局引擎。


## 2026-10-05 — C69B 《金镜》当时法六壬叠盘

- C118 日度上游与 C69 天乙朝暮表已通过 C69B 接通。
- 实现“日在何宿→计属何辰→以时加位→立贵前后”的六壬叠盘。
- 庚申日、立冬六日、寅时原例复算出青龙/太常/六合/天空，与《金镜》主要落将逐项吻合。
- 公开转录“客参将在天定下”保留原字，同时将六壬复算结果记录为“天空”，不以算法静默改写底本文字。
- 完整自动当时法仍保留历法日期入口、朝暮自动判定、九宫/十二支无损坐标三项边界。


## 2026-10-05 — C124 《统宗》卷六太乙九星动态层

- 新增 `src/kintaiyi/taiyi_nine_stars_tongzong.py`，独立实现《太乙统宗宝鉴》卷六太乙九星动态 source profile。
- 周期固定为 900 年大周、90 年小周、10 年一星，命起天蓬，顺行九星。
- 采用 NGJ892411999009267118912 与 CADAL02055529 两个直接见证互校；CADAL“星率十”与原例“1121 年得天禽直符、初入一年”相互吻合，用以排除 OCR“星率九”的误读。
- 给定年干时，按六干星宫锚点安当前直符并顺九宫布全九星；丙年天蓬直符例回归为 8→9→1→2→3→4→5→6→7。
- 《紫庭经》〈释九宫所值九星〉继续作为静态九宫 primary；C124 仅属《统宗》动态 profile，不反填紫庭周期。
- C124 与 C70 文昌九星明确分层：C124 为太乙九星 900/90/10 且可布全九星；C70 为文昌九星 2700/270/30，当前只稳定支持直事星及年干落宫/分野。
- 新增九星 crosswalk 与 C124 专项测试，禁止太乙九星、文昌九星及跨来源周期静默合并。


## 2026-10-05 — 研易楼明钞本旧扫描成果恢复

- 用户确认研易楼藏《太乙紫庭祕訣》明钞本此前整理术语库时已经扫描，本地 E 盘仍有原文件；废止“扫描资源未取得”的旧表述。
- 从旧 `kentang2017/kintaiyi` 派生实现残留恢复文昌九星旧整理序列：文曲、玄鳳、明維、昭搖、立華、華明、玄武、玄冥、雄明。
- 新增 `terminology/zitingjing-legacy-scan-recovery.json`，明确其身份为 legacy scan extraction witness，而非重新生成的 manuscript transcription。
- 文昌九星 primary evidence 更新为 `legacy_scan_extraction_recovered_page_pending`：旧扫描成果已确认存在并恢复部分残留，但 E 盘原扫描/旧 `terminology.json` 未重新挂载前仍禁止生成紫庭 primary runtime。
- 与 C70《统宗》NGJ 见证的文昌/文曲、阴德/昭搖、招摇/立華、维明/雄明及年干落宫差异全部并列保存，不静默合并。
- 恢复词形单列为 `recovered_scan_aliases`；`old_term_record_id`、`source_page`、`old_aliases` 等旧 store 原字段继续保持 null，防止把派生残留误当旧库原字段。


## 2026-10-05 — 软件调用分层 / registry / public API

- 保留现有 `terminology/`、`rules/`、`sources/` 和 `src/kintaiyi/` owner，不进行破坏性物理搬迁。
- 新增 `registry/catalog.json`：统一登记术语、规则、runtime、来源、schemas 与测试层的稳定指针，不复制算法和正文。
- 新增 `registry/operations.json`：登记软件可直接调用的 stable operations；待校或 source-record-only 项不得伪装成可运行接口。
- 新增 `kintaiyi.api`：提供 `get_term`、`search_terms`、`get_rule`、`calculate`、`calendar_context`、`build_pan`、`explain_result`。
- 将 `terminology`、`rules`、`registry`、`schemas` 作为 package data 随 Python 包安装，避免软件依赖仓库相对路径。
- 新增 registry/API 回归测试，锁定三才 5 与 15/25/35 边界、C124 太乙九星 source profile、runtime 可解析性和 packaged JSON 资源。
- 新增 `docs/ARCHITECTURE.md`，明确单一事实来源、兼容策略和后续旧术语库迁移原则。


## 2026-10-05 — C125 《紫庭经》太乙九星直符周期 + 旧扫描来源纠正

- 直接复核《太乙紫庭经》〈释九宫所值九星〉，确认本篇自身明确“九星十年一易”；九星合为90年直符循环。
- 开元十二年原例积算 1937281，按90年循环余31，前三星各十年后余1，得到天辅直符第1年；新增 `C125-ZITING-TAIYI-NINE-STARS-CYCLE` runtime。
- C125只实现紫庭主来源可直接证明的直符周期；正文虽见甲/乙年加六甲/六乙句，但OCR残文不足以单独重建完整十干动态布星，因此不借C124《统宗》反填。
- C124《统宗》与C125《紫庭》继续分 profile：两者都支持十年一星，但C124另有900年大周和完整年干九星布置，C125当前不继承这些额外层。
- 来源纠正：用户确认研易楼藏《太乙紫庭祕訣》明钞本此前在术语库整理阶段已经扫描，E盘仍存原件；但旧 `kentang2017/kintaiyi/config.py` 九星段明确标注来源为《太乙统宗宝鉴》卷六。因此“文曲、玄鳳、明維、昭搖、立華、華明、玄武、玄冥、雄明”等旧代码词形只作 prior workflow code residue，不能直接称为研易楼本逐字扫描 witness。
- `terminology/zitingjing-legacy-scan-recovery.json` 已改为同时记录“明钞本此前已扫描”与“旧统宗九星代码残留”两条独立证据链；`manuscript_form/source_page/old_term_record_id/old_notes` 继续待E盘原页或旧 `terminology.json` 恢复。


## 2026-10-05 — 软件总库 / Public API v1 收口

- 仓库固定为术语 `terminology/`、规则 `rules/`、运行时 `src/kintaiyi/`、来源证据 `sources/`、总注册表 `registry/`、数据契约 `schemas/` 六层；总注册表只存指针，不复制正文或公式。
- `kintaiyi.api` 新增稳定查询/调用面：`get_term`、`search_terms`、`get_rule`、`calculate`、`calculate_rule`、`describe_rule`、`capabilities`、`repository_status` 等。
- `calculate_rule(rule_id, ...)` 可从 rules/terminology exact runtime 指针解析算法；唯一 source profile 可自动选择 profile key；source-record-only 项保持不可执行。
- 七术7项、八占8项，以及五福/大小游、阳九百六、岁计/时计八门、太乙九星 C124/C125、文昌九星 C70 等已登记 public operation alias。
- 《统宗》卷十五 V15-01..14 与卷十七 V17-01..11 均可按 source rule id 调用；景祐 JF4M-01..11 仍保持 source-record-only。
- 修正三才杜塞边界：5/15/25/35 classic 标签只为“杜塞”；结构层仍分别记录5仅地、15/25/35仅天+地。
- 清理 rules registry 中五福/大游旧混合 profile，恢复金镜/统宗 source profile 明确隔离。
- public API 固定为 `1.0`；新增 registry/operation/result/capabilities/repository-status schemas 和软件接入文档 `docs/SOFTWARE_API.md`。
- 本轮收口期间 CI 从历史不一致状态恢复为全绿，并持续由 GitHub Actions 对 main 执行全库 pytest。


## 2026-10-05 — 景祐卷四军事 runtime 收口

- JF4M-01..11 从仅有 source records 推进为《景祐太乙福应经》卷四自身的 source-specific runtime，11/11 均可按 rule_id 解析。
- JF4M 与《太乙金镜式经》J4M 继续保持平行 crosswalk，不允许调用 J4M runtime 替代景祐规则。
- JF4M-10 对应 J4M-11 风云飞鸟；JF4M-11 对应 J4M-10 奇伏；J4M-12 没有直接 JF4M 对应项。
- JF4M-02“大小将不相开”、JF4M-07完整地形字表、JF4M-10部分观测句仍保留文本/扫描 pending；runtime 可用不等于来源文字已经完全无疑点。
- catalog-index 与 crosswalk audit 已同步：景祐军事 runtime coverage 固定为 11/11，并单列 02/07/10 pending。

## 2026-10-05 — 旧术语库恢复状态分层

- 新增 `legacy_recovery_status()`，把“算法/规则待校”与“历史原件当前不可访问”分开。
- 当前旧 `terminology.json` 的真实 schema 与原文件仍未重新挂载；parser 与 synthetic reconstruction 均保持禁止。
- 用户已确认研易楼藏《太乙紫庭祕訣》明钞本及相关旧资料在本地 E 盘仍存，但当前运行环境未挂载。
- 未取得原件前，old_term_record_id、旧定义、旧 notes、manuscript_form、source_page 等字段继续保持 null；外部参校来源不得代填研易楼明钞本逐字字段。
- 新增 `schemas/legacy-recovery-status.schema.json` 与公开 API 回归测试。
