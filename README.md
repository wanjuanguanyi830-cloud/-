# 太乙术语库与规则库

本仓库用于保存太乙术语、来源限定规则、算法实现、历史局例和验证记录。术语释义、古籍原文、项目采用规则与代码计算彼此分层；具体开发不得仅凭同名词条推导公式。

## 目录

- [`terminology/`](terminology/)：术语库与结构定义。
- [`rules/`](rules/)：按来源与家法隔离的规则和算法。
- [`rules/jinjing/geju/`](rules/jinjing/geju/)：《太乙金镜式经》主格局引擎。
- [`src/kintaiyi/`](src/kintaiyi/)：七术、八占、公共规则、周期算法和卷五军事实战综合层。
- [`docs/pan_v2.md`](docs/pan_v2.md)：当前结构化 pan v2、模块职责与旧 API 迁移说明。
- [`rules/taiyi_v1.json`](rules/taiyi_v1.json)：`schema_version=2.0` 规则记录；文件名保留以兼容现有路径。
- [`sources/`](sources/)：来源证据、异文、采用边界和参考快照。
- [`tests/`](tests/)：规则回归、历史局例输入和差异报告。
- [`CHANGELOG.md`](CHANGELOG.md)：本库实质变更记录。
- [`changelog/`](changelog/)：按批次保存的详细变更记录。

## 规则来源

本次格局主规则唯一采用《太乙金镜式经》卷三，八门值事周期采用卷四。`kentang2017/kintaiyi` 只作为固定版本参考实现、历史局例和旧 `skyeyes_summary` 对照来源；它不属于本仓库的写入目标，也不决定《金镜》主规则。

所有数值算法必须保留输入、精确位置、边界、版本和可回查来源。相异古籍表述进入来源说明与对照测试，不合并进《金镜》运行规则。

七术、八占、公共规则、三基、五福、大游、小游和四太乙采用 `taiyi-t7-d8-v2` 项目规范；canonical、source variant、derived 与 pending 分层记录。卷五 `junshi_zhanlue.py` 组合层继续独立调用 D8-01..08；C9、C10、C11分别提供现代特征投影、严格v2消费和pan builder。所有坐标系显式标注，旧 `config` 函数作为兼容入口。安装 `python -m pip install -e .` 后可直接导入 `kintaiyi` 与 `config`。

## 运行测试

在 Python 3.10+ 环境安装 `pytest` 后，从仓库根目录运行：

```powershell
python -m pytest
python tests/test_skyeyes_summary_audit.py
```

第二条命令重新生成 `tests/reports/skyeyes_summary_audit.md`。差异分类允许旧表摘要与新规则不完全一致；每局结果和差异原因均保留。


