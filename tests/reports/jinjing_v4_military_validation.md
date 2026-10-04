# J4M 《太乙金镜式经》卷四军事十二法验证报告

日期：2026-10-05

## 总结

J4M 来源层：

- ruleset: `jinjing-siku-v4-military-12`
- source profile: `jinjing_siku_volume4`
- rule ids: `J4M-01..J4M-12`

当前状态：

- **11 条完整 source-specific runtime**
- **1 条 partial：J4M-03**
- **0 条 pending**

J4M-04 已从原先“C8 只覆盖角色子层”的 partial 状态升级为独立完整 runtime；C8 本身仍不自动采用该完整逻辑。

## J4M-04 完成验证

runtime：

`kintaiyi.jinjing_v4_military.zhuke_fa`

### 角色层

固定：

- 陈兵原野 → 先动客、后应主
- 安居之势 → 先动主、后应客

### 行动条件层

当：

- 三门具
- 五将发
- 阴阳和

三项同时成立时：

- `action_status=raise_forces_favorable`
- `action_advice=称兵`
- `source_campaign_verdict=所向必克`
- `source_temporal_outcome=先胜后负`

但：

- `winner=None`

因为“先胜后负”原文没有在本句指定应强拆成哪一方最终胜负。

当：

- 三门不具
- 五将不发
- 阴阳不和

三项同时成立时：

- `action_status=hold_and_defend`
- `action_advice=不利举兵，宜固守吉`

混合组合不扩写为完整胜负公式；若三门或五将本身失败，只保存 J4M-01/02 已明确的硬约束。

### 始发神层

固定：

- 东 → 阴德
- 南 → 和德
- 西 → 大炅
- 北 → 大武

“以定主客所起归之神”之后的细推步，本段未展开，因此 runtime 只返回始发神和原文方法说明。

### 互视其算层

固定 cross-side reference：

- 客欲知主 → 主算
- 主人欲知客 → 客算

只做引用，不把 D8-06 多少胜负反写入 J4M-04。

### 可计算状态拆分

J4M-04 现区分：

- `role_computable`
- `source_combination_computable`
- `hard_constraints_computable`

避免“角色已经可判，但门将阴阳条件缺失”时把所有语义压成一个布尔值。

## J4M-03 校勘结论

runtime：

`kintaiyi.jinjing_v4_military.zhuke_xiangguan`

已确认正文明确部分：

- 客目克主目 → 客关得主人 → 客胜
- 主目克客目 → 主人关得客 → 主胜

仍未闭合：

“皆用日计纳音以决之”。

核对多种《太乙金镜式经》转录后，没有找到：

- 日计纳音如何参与关法的进一步公式
- 纳音与主目/客目同五行时的明文规则
- 比和、生我、我生的明文胜负规则
- 主将与太乙同宫参与本条的明文

因此保持：

- `implementation_status=implemented_partial_source_specific`
- `collation_status=formula_not_expanded_in_checked_jinjing_transcriptions`
- `fully_computable=False`

## legacy `wc_n_sj` 隔离验证

旧参考函数 `kentang2017/kintaiyi::wc_n_sj` 额外包含：

- 纳音等于主目五行 → “主关”
- 纳音等于客目五行 → “客关”
- 主将是否与太乙同宫 → 改写胜负
- 比和 / 生我 / 我生 → 判和

这些没有在卷四本段得到明文支持。

机器规则已写入 `legacy_reference_quarantined`，测试锁定“不能升级为 canonical”。

## 当前十二法状态

完整：

- J4M-01 推三门具不具
- J4M-02 推五将发不发
- J4M-04 推主客
- J4M-05 推出师法
- J4M-06 推陈兵向背
- J4M-07 推制阵随地法
- J4M-08 推随地制变
- J4M-09 推太乙在天外地内法
- J4M-10 推奇伏法
- J4M-11 推太乙风云飞鸟助战法
- J4M-12 推阵有风云气定胜负

partial：

- J4M-03 推主客相关法

## 防混法测试

当前测试锁定：

- J4M-01 不退化成旧 `threedoors`
- J4M-02 不退化成旧 `fivegenerals`
- J4M-03 与 J4M-04 永不合并
- J4M-03 不引入旧 `wc_n_sj` 的纳音同类 / 太乙同宫推断
- J4M-04 “先胜后负”不强设 winner
- J4M-04 混合三门/五将/阴阳组合不冒充正文完整断法
- J4M-05 不替换为《统宗》卷五兵额表
- J4M-06 不替换为旧卷十五陈兵出乡
- J4M-07 ≠ J4M-08
- J4M-08 原文比例不转现代战力分数
- J4M-09 《金镜》与《统宗》profile 分离
- J4M-10 不调用旧卷十五奇伏近名算法
- J4M-11 无外部观测不得计算
- J4M-12 原文未列颜色不得用五行补表

## C8 crosswalk

J4M-04 machine metadata：

- target layer: `C8-L3`
- status: `source_runtime_complete_c8_roles_only`

含义：

- J4M-04 source-specific 已完整
- 现有 C8-L3 仍只保存先后动静角色
- 暂不直接改写 C8 `volume5_strict`

下一步应新增显式 adapter/source profile，而不是把 J4M-04 逻辑直接塞进 C8 默认路径。

## CI

J4M-04 runtime 与测试提交后：

GitHub Actions run `37230461892`：

- conclusion: `success`
- result: **345 passed in 0.59s**

机器 metadata 与 J4M-03 legacy quarantine 锁定后：

GitHub Actions run `37230473016`：

- conclusion: `success`
- result: **347 passed in 0.60s**

较早 run 145 / 147 的单项失败，是 runtime/catalog 先变更、旧测试尚期待 J4M-04 为 partial 的提交顺序问题；更新测试后恢复全绿，不是规则语义失败。

## 下一步

J4M 卷四十二法来源层已经达到可收口状态。

建议下一阶段：

1. 新增 **J4M → C8 显式 adapter**
2. adapter 必须要求 `source_profile=jinjing_siku_volume4`
3. 默认 C8 `volume5_strict` 保持不变
4. J4M-03 继续保持 partial，直到发现可信的“日计纳音”展开公式
