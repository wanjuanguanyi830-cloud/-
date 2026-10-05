# T7-06 白龙得云：“刑克”校勘收口

状态：**canonical 可执行层收口为九宫五行“克”；不建立独立“将宫刑”算子。**

## 结论

三组直接/平行来源都保存“刑克”措辞，但没有任何一组给出可执行的“将宫相刑表”、宫数映射或一条以独立“刑”关系演算的古例。

本轮重新比较句内结构后，四库本《太乙金镜式经》卷六提供了更强的内部证据：

- 对我方大将，正文使用“刑克”；
- 紧接的我方小将平行句只写“克小将亦然”；
- 同条古例只实际演示五行生、比、旺相，不演示第二套“刑”算法。

因此当前最保守、可复核的运行解释是：T7-06 的严重敌我关系按敌大将所在九宫五行是否克我方大将/参将所在九宫五行计算；“刑克”不再拆出一套来源未见的独立将宫刑映射。

这是一项本条运行解释，不是宣称太乙文献中所有“刑克”二字都只有一个固定词义。

## 《太乙金镜式经》卷六

“推白龙得云术六”可直接确认：

- 大神所临与主客大小将按五行旺相休囚死判有气/无气；
- 敌方大将对我方大将出现“刑克”时，断为严重不利；
- 紧接的小将平行条件简写为“克小将亦然”；
- 原例没有另列将宫相刑表，也没有演示独立“刑”步骤。

公开核对：

- Chinese Text Project，《太乙金镜式经》卷六：https://ctext.org/wiki.pl?chapter=80794&if=gb
- Wikisource，四库本《太乙金镜式经》卷六：https://zh.wikisource.org/zh-hans/太乙金鏡式經_(四庫全書本)/卷06

四库本“小将”平行句只保留“克”，是本轮关闭“必须另找刑表” pending 的关键内部证据。

## 《太乙统宗宝鉴》卷十二

“明白龙得云第六术”同样保存“刑克”措辞，但：

- 算例仍只演示五行生比与旺相；
- 未给白龙得云专用九宫刑表；
- 未定义如何从两个将宫自动推出独立“刑”。

公开核对：

- CADAL02055529 卷十二：https://www.shidianguji.com/book/CADAL02055529/chapter/1l5erkkzm1quh
- CADAL02094393 卷十二：https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppx1tk60ii

因此统宗只证明该措辞流传，不足以建立第二套计算器。

## 《太乙金钥匙》

“白龙得云”亦保存敌大将“刑克”我方将宫的表述，但没有定义将宫刑映射。

同书其他位置还可见“击/掩”之后以“刑克”概括不利后果的用法，而未随附统一刑表。这进一步说明：不能仅见“刑克”二字，就假定仓库必须存在一个全局技术型“刑” operator。

公开核对：

- 识典古籍《太乙金钥匙》：https://www.shidianguji.com/book/NGJ89241199902106666022/chapter/1lq8dkvlnkx7u

## 与其他“刑”体系的边界

太乙其他层确实另有技术型“刑”，例如城名/刑杀层的地支刑法，以及某些九宫变化、神名关系中的“刑”。这些对象、输入和用途都不同于 T7-06 主客大小将关系。

当前仍固定：

- 不把地支三刑投影成九宫大将刑；
- 不把神名相刑表移植给主客大小将；
- 不凭宫数、方位或五行常识制造额外“刑”关系。

## Runtime 处理

kintaiyi.seven_methods.general_conflict() 现在分两层。

canonical 只计算：敌大将九宫五行 → 克 → 我方大将 / 参将九宫五行。

若成立，events 记录 relation=克，severe=True，canonical verdict=出战必死。若不成立，不再因为缺“刑表”返回 pending。

旧接口参数 xing_pairs 暂不删除，以免破坏已有调用，但其身份明确降为 explicit_external_extension_not_canonical。调用方显式传入的 pair 只进入 external_xing_events，并且不进入 canonical events、不改变 canonical severe、不改变 canonical verdict，也不在 dragon() 中覆盖将帅乘气结果。

如果未来找到能直接证明某一将宫刑法就是 T7-06 所指的来源桥梁，应新增独立 source profile / rule，而不是静默把外部 pair 升级进当前 canonical。

## 状态

原状态：three_source_phrase_verified_xing_mapping_unresolved

现状态：three_source_phrase_verified_control_only_canonical_no_independent_xing_operator

因此 T7-06 的算法 pending 关闭。仍可继续研究“刑克”在不同太乙文本中的词义史，但这属于校勘/语义研究，不再阻塞白龙得云运行时。
