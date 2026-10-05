# 太乙七术＋八占＋公共规则层 v1 整合包

本批依据用户给定的完整规范实现。主线是四库本《太乙金镜式经》，《统宗》《景祐》《金钥匙》等补证校勘。已经确认的项目 canonical 不因旧代码或单一转录而变更。本库已有的卷三格局及卷四八门模块保留；它们的动态内外关系不供八占攻击函数调用。

## 规则与来源

[`rules/taiyi_v1.json`](../rules/taiyi_v1.json) 分别保存七术、八占、公共规则、用户提供的原典短句、十条异文和待校事项；它不是古籍全文转录。`source_excerpts` 仅保存本次规范给出的短句。原典页码、影印证据未提供，明确待补。七术古例独立保存在 [`seven_methods_classics.json`](../tests/fixtures/seven_methods_classics.json)，`source_example=true`；补充输入写在 `derived_fields`。八占指定算例与边界算例属于算法回归，标记为推导例，不能反向当作古籍证据。

七术编号 T7-01..07，八占 D8-01..08，公共 R-*，异文 VAR-001..010，古例 EX-T7-*。类别在运行结果中也保持独立。八占原典古例未提供，`EX-D8-*` 预留，当前算例用 `CASE-D8-*`。

## 调用

安装本项目或将仓库根目录及 `src` 加入 Python 搜索路径。传统规则核心仍保持纯Python结构；现代production日期入口依赖 `astronomy-engine` 与 `lunar_python`，安装项目时由 `pyproject.toml` 自动安装。

```python
from kintaiyi.seven_methods import lijin, cloud, leigong, dragon, returnarmy
from kintaiyi.eight_divinations import sancai, calc_preparedness, attack_realm

lijin("甲子")                      # 子→卯→午→酉→子
cloud(7, 3)                        # 主囚，客相
leigong(6, 8, 2, 9, 6)             # 太乙、主大、主参、客大、客参
dragon(9, 6, 3, 2, 8)              # 乘气与严重刑克分层，刑克优先
returnarmy(enemy_arrival_taiyi=2, home_general=6, away_general=9)
sancai(15)                         # 仅天+地；杜塞；不属三才俱足
calc_preparedness(17)              # 将吏兵卒俱备
attack_realm("吕申")               # 固定内，内虚宜攻外
```

`taiyi_rules.py` 包含十六环、十六神固定位置五行、九宫代表点、五态、大神火阶段、十/五/一分解。和德=土，大炅=木，大武=土。吕申加位恒为顺行四格。中五的将宫五行可比较；中五没有十六宫代表点，不能强行求大神。别名太炅、太神只用于输入归一化。

七术 `lijin/lion/cloud/tiger/leigong/dragon/returnarmy` 返回结构化字典。T7-02/03/04 以大神火为主体(A)；T7-05/06/07 以将宫五行为主体、大神落宫五行为环境(B)。四维火阶段为 `None`；墓与废不等同。白云冠带算法采用善战/精锐，两版本原文独立保存。临津一般输出年/月/日/时支，古例的丁卯及五月保存在来源记录，不自行推演其他年干及月序号。

狮子四维分区覆盖丑艮寅、辰巽巳、未坤申、戌乾亥。第18年含起年，偏移17；有完整干支可输出候破干支，只有年支则不伪造年干。普通支应期仅返回候选支及判断，缺第二古籍实例。

`general_conflict()` 自动计算已确认五行克；刑表未确认，调用层可通过 `xing_pairs={(敌宫,我宫),...}` 显式提供已校关系。没有刑表时输出待校，而不宣称已经排除所有刑。白龙保留 `has_qi`，同时由 `conflicts` 决定严重刑克优先断语。

四将不齐时，雷公、白龙仍输出已提供将位的结果及 `missing`。回军的敌初来太乙宫与主客大将都是明确参数；缺失时返回 `status=not_computable`。旧式 `returnarmy(ag_num)` 只能识别客大将，不会把它当敌初来太乙宫。

## 八占与旧接口

`cal_des()` 单算返回三才，亦可分别输入主/客/定算。十/五/一结构共用，但三才与所主语义、正式标签独立。三才经典俱足仅16..19/26..29/36..39。**5仅有地；15/25/35仅有天与地。** 这四个数的 classic 标签只记“杜塞”，不能再因结构缺失追加“无天/无人”等古典标签。10/20/30/40结构无人。

`calc_length()` 采用统宗11+/10-。五音按尾数两两配宫、徵、羽、商、角；1/3/5/7/9为正音，2/4/6/8/10为比音，尾数0按10；五音本身不直接判吉凶。孤单按明确 canonical 数集判单阳、单阴、孤阳、孤阴、重阳、重阴；13属重阳火厄，28属重阴水厄。5/15/25/35杜塞数以及未列混合数不得再由十位/尾数拆分强塞分类或基本影响。`attack_realm()` 固定内外；`suenwl()` 分 `base` 与 `pattern_corrections`，不自动把未确认修正套入基础胜负。同数返回同数/无明确断语。`tui_danger()` 逐方返回重阳火厄或重阴水厄，其他组合无明确断语。

根目录 [`config.py`](../config.py) 提供请求中的所有旧函数名，并把核心计算委托给独立模块。`_calc_jianbei()` 只作兼容组合，分别返回 `length` 与 `preparedness`；`junshi_zhanlue(...)["數有所主"]` 只调用所主规则。目标仓库原来没有该文件，也没有外部参考项目的 Taiyi 类；因此本次兼容的是旧名称与可确认输入语义，不能宣称已经复现未提供的历史字符串返回或所有外部调用签名。外部实际排盘项目接入时仍须核对其调用层。

## 五福与大游

五福、大游、小游和大游天目现在全部采用**显式 source profile**，旧项目兼容偏移不再作为 canonical 默认值。

五福稳定核心为乾→艮→巽→坤→中、45年一宫、225年一轮：

- `C67-WUFU-TONGZONG`：统宗宫盈差115，大周2250，小周225；
- `C67-WUFU-JINJING`：金镜无盈差，225年直接成周。

旧项目的 `+250` 只保留在 legacy quarantine，不能覆盖上述来源。软件优先使用 `calculate_rule("C67-WUFU-TONGZONG", ...)` 或 `calculate_rule("C67-WUFU-JINJING", ...)`。

大游太乙共同稳定核心为36年一宫、288年完成八宫一轮、起七宫、不入中五，但行宫顺序与历元必须分source profile：

- `C107-DAYOU-JINJING`：上元甲寅、无盈差、元法4320；顺行7→8→9→1→2→3→4→6；
- `C107-DAYOU-TONGZONG`：上元甲子、宫盈差34、外周2880；同样顺行7→8→9→1→2→3→4→6；
- `C107-DAYOU-TAOJIN`：《太乙淘金歌》以唐高宗永徽五年甲寅为七宫第1年，逆行7→6→4→3→2→1→9→8，不借用金镜/统宗盈差。553年古例复算为八宫第13年。

大游天目同样分金镜与统宗 source profile；核心路径与周期由各自已校 runtime 保存。软件层不得把72、180等外层周期替换为核心18步，也不得静默把来源参数混成一个默认 profile。

## 测试与待校

从仓库根目录执行 `python -m pytest -q`。新增测试包括全部七术古例、八占指定组、完整十二支/九宫加位映射、四将五态、刑克优先、回军缺输入、五福/大游各周期与段界、天目全部18步、兼容入口和数据分层。

仍待校项目必须以当前各 catalog/runtime 的 pending/source-boundary 字段为准，不能沿用早期文档快照。当前明确仍包括：狮子普通落支第二独立实例、白龙得云“刑”映射、旧terminology.json与研易楼明钞本页码/逐字原形恢复，以及其他仍标记为 attribution-unverified 的来源项。已确认的三才杜塞、五音正比音、孤单明确数集不再列为待校。


## Modern production 与太乙岁界

现代日期排盘的 production canonical 已从古历复原层分离。

### 太乙岁

唯一换年点：

`真实天文冬至交节瞬间`

规则：

`moment < winter_solstice(Y) -> Taiyi year Y`

`moment >= winter_solstice(Y) -> Taiyi year Y+1`

明确不采用：

- 元旦；
- 春节；
- 立春；
- 春分。

### 四计现代边界

- 岁计：冬至瞬间换太乙岁；
- 月计：十二节精确交节切太阳月；
- 日计：Asia/Shanghai 民用日00:00；
- 时计：冬至/夏至瞬间切半岁，并从该半岁重新起算时计积数。

月计中的 `month_formula_year` 只用于积月公式，不能替代 `taiyi_year`。

农历年和立春干支年都只作并列日历事实。

### Modern pan v2

`build_modern_pan_v2(moment, count_type=...)`

是现代日期到结构化盘面的正式adapter。

pan v2 对 `production_modern` payload 强制验证：

- 必须存在 `calendar.taiyi_year`；
- 必须声明“真实天文冬至交节瞬间”为唯一太乙岁界；
- 必须明确排除元旦/春节/立春/春分换年。

旧 `pan_adapter.py` 只迁移legacy snapshot，不参与现代日期计算。
