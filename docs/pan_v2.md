# 太乙规则库 v2 与 pan 数据模型

本页说明当前实现。规则正文及来源边界见 [`rules/taiyi_v1.json`](../rules/taiyi_v1.json) 与 [`source_variants.md`](../sources/source_variants.md)；历史 v1 说明已由本页取代。

## 顶层结构

`kintaiyi.pan_v2.pan()` / `build_pan_v2()` 产出固定键的结构化对象：

```text
schema_version, meta, calendar, board, cycles, analysis, modern,
source_variants, derived, pending, compat
```

`compat` 只承载旧平铺字段，是输出兼容区。v2 规则不读取它。`source_variants` 只保存来源异文，`derived` 保存推导结果及依据，`pending` 保存缺证/未确认问题；不得把它们写回 canonical 规则。

- `meta` 固定保存 `ji_style`、`method`、`accumulated_year`、`source_profile`。
- `calendar` 分开保存公历、干支、年/月/日/时支、农历和节气。
- `board` 保存盘面事实，不在对象构造时添加断语。太乙、天目、四将、算数均保留坐标、九宫/十六辰五行等必要的原始字段。
- `cycles` 保存三基、五福、大游、小游、四太乙周期。
- `analysis` 分开放格局、八占、七术和军事分析。
- `modern` 保存 C9 博弈特征投影等派生现代特征，并显式标记来源和派生性质。

构造时省略字段仍会补齐固定骨架；不完整输入由调用方以 `computable=false`、`missing_inputs`、`reason` 明示，不伪造默认盘面。

## 坐标约束

九宫、十六辰、十二支、四太乙十二宫、五福五域使用不同坐标标签。使用 `same_nine_palace`、`same_sixteen_sector`、`same_four_taiyi_palace`、`same_wufu_domain` 进行同坐标比较；未显式标注坐标或坐标类型不符时返回 `None`。中五没有十六辰代表点。

显式转换 API：`sector_to_nine_palace()`、`nine_palace_to_trigram()`、`nine_palace_representative_sector()`、`dashen_from_sector()`、`dashen_from_nine_palace()`。旧 `num2gong` 只作为代表 sector 的兼容别名。

## 规则模块

- `taiyi_rules.py`：十六环、五行、九宫转换、大神固定加四、五态关系与共享数字分解。
- `seven_methods.py`：T7-01..07。Mode A 的主体为火，Mode B 的主体为将所在九宫五行。白龙乘气与 direct conflict 独立；回军必须提供敌军初来太乙宫。
- `eight_divinations.py`：D8-01..08。D8-01结构与经典标签分开，D8-05固定内外，D8-06只比较主客算，D8-07与D8-04分别计算。
- `cycles.py`：统一 1-based 年数公式，含三基、五福、大游、小游及保留10–12号的四太乙宫环。出处未明的关系保持 `pending`。
- `junshi_zhanlue.py`：卷五军事实战综合层，只组合独立八占与上游三门、五将、将帅状态；D8-03五音与D8-08数有所主分栏，不跨卷反推基础规则。
- `game_theory.py`：C9只读七术明确字段并投影为现代派生特征；不搜索断语关键词，九宫映射复用本项目共享表。
- `v2_consumer.py`：C10严格读取v2区段，缺失即报不可计算，不从旧平铺字段回填。
- `pan_v2.py`：C11纯 builder 组装上游事实，校验JSON安全和中五无十六辰代表点。
- `config.py`：旧名称兼容包装。新增逻辑应直接调用规则模块，不依赖兼容字段。

## 快速示例

```python
from kintaiyi.pan_v2 import build_pan_v2, taiyi_board
from kintaiyi.seven_methods import lijin, returnarmy

result = build_pan_v2(
    meta={"method": "project_canonical", "accumulated_year": 1},
    calendar={"branches": {"year": "子"}},
    board={"taiyi": taiyi_board(3)},
    cycles={},
    analysis={"seven_methods": {"T7-01": lijin("甲子")}},
    source_variants={},
    derived=[],
    pending=[],
    compat={},
)
missing = returnarmy(away_general=9)
assert missing["computable"] is False
```

旧界面可以继续使用 `config.py` 中原有名称。测试以仓库根目录执行 `python -m pytest -q`；无 pytest 时，`tests/test_taiyi_v2_mandatory.py` 可由标准库 `unittest` 运行。
