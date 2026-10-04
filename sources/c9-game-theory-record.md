# C9 `game_theory.py` 解耦记录

## 目标

旧参考实现把七术结果整体转为字符串，再搜索“成 / 吉 / 正 / 利”决定现代博弈支付方向；同时把太乙落宫按洛书宫义解释。

C9 将这两类隐式混法拆除。

## 1. 七术只做结构化投影

新增：

- `project_seven_method_for_game_theory(...)`
- `project_seven_methods_for_game_theory(...)`
- `build_game_theory_feature_bundle(...)`

原则：

- 只读取七术结果中的明确字段，如 `rule_id`、`verdict`、`state`、`has_qi`、`enemy_verdict`。
- `notes`、`aliases`、说明文字中出现“成/吉/正/利”不影响投影。
- `not_computable` / `pending` 保持不可计算，不强行量化。
- 每个投影都标 `derived_modern_feature=True`，不得伪装为古法 canonical。
- 投影只读源结果，不反写七术。

### 各术边界

- T7-01 临津问道：只给应期，不直接生成通用吉凶分。
- T7-02 狮子反掷：只按明确 `verdict=合破/不破` 投影攻击窗口。
- T7-03 白云卷空：只比较明确五态，不从文字断语猜强弱。
- T7-04 猛虎相拒：只按 `可攻/不可攻/无明确断语` 投影。
- T7-05 雷公入水：按四将结构化五态做现代相对态势；字段不全则保持 partial。
- T7-06 白龙得云：只读 `has_qi` 和结构化 `conflicts.*.severe`。
- T7-07 回军无言：只读明确 `enemy_verdict` / `home_verdict`。

## 2. 太乙九宫与洛书隔离

博弈层使用本项目太乙九宫：

- 1 乾
- 2 离
- 3 艮
- 4 震
- 5 中
- 6 兑
- 7 坤
- 8 坎
- 9 巽

旧参考实现中的注释/策略加成按洛书：

- 1 坎
- 2 坤
- 3 震
- 4 巽
- 6 乾
- 7 兑
- 8 艮
- 9 离

两套宫义不同，禁止互换。

新增 `taiyi_palace_feature(...)`，输出：

- `mapping_system="taiyi_nine_palace"`
- 太乙九宫卦名
- canonical 宫五行
- 中五标 `positional_effect_allowed=False`

## 3. 现代模型边界

C9 第一阶段只做“可审计特征投影”。

支付矩阵、策略权重、Nash 均衡属于现代派生模型，后续若迁入，必须：

- 继续标 `derived_modern_feature=True`
- 明确每个权重是现代模型参数，不得说成古籍原值
- 不得重新读取中文 prose 猜吉凶
- 不得用洛书宫义替代太乙九宫
