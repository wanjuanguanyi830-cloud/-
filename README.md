# 太乙术语库与规则库

本仓库用于保存太乙术语、来源限定规则、算法实现、历史局例和验证记录。术语释义、古籍原文、项目采用规则与代码计算彼此分层；具体开发不得仅凭同名词条推导公式。

## 目录

- [`terminology/`](terminology/)：术语库与结构定义。
- [`rules/`](rules/)：按来源与家法隔离的规则和算法。
- [`rules/jinjing/geju/`](rules/jinjing/geju/)：《太乙金镜式经》主格局引擎。
- [`rules/common/`](rules/common/)：十六位、九宫、吕申加位及五行公共规则。
- [`rules/warfare_v1/`](rules/warfare_v1/)：七术与八占 v1 独立算法层。
- [`sources/`](sources/)：来源证据、异文、采用边界和参考快照。
- [`tests/`](tests/)：规则回归、古籍课例输入、来源定位要求和差异报告。
- [`CHANGELOG.md`](CHANGELOG.md)：本库实质变更记录。
- [`changelog/`](changelog/)：按批次保存的详细变更记录。

## 规则来源

《太乙金镜式经》规则继续单独维护。七术 v1 按《四库全书》本卷六整理，八占 v1 记录本轮确认的卷六规则及《统宗宝鉴》补充；二者不合并进《金镜》运行规则。

所有数值算法必须保留输入、精确位置、边界、版本和可回查来源。相异古籍表述进入来源说明与对照测试，不合并进其他规则集。当前新增古例的版次、页码／影像坐标尚不齐，fixture 明确标注为定位不完整。

## 运行测试

在 Python 3.10+ 环境安装 `pytest` 后，从仓库根目录运行：

```powershell
python -m pytest
python tests/test_skyeyes_summary_audit.py
```

第二条命令重新生成 `tests/reports/skyeyes_summary_audit.md`。新规则用例由 `tests/test_warfare_v1_historical_cases.py` 读取 `tests/fixtures/warfare_v1_historical_cases.json`；测试不会将引用位置未核实的夹具视为版本学证据。

