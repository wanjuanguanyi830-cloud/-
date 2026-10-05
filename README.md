# 太乙术语库与规则库

本仓库用于保存太乙术语、来源限定规则、算法实现、历史局例和验证记录。术语释义、古籍原文、项目采用规则与代码计算彼此分层；具体开发不得仅凭同名词条推导公式。

## 目录

- [`terminology/`](terminology/)：术语库与结构定义。
- [`rules/`](rules/)：按来源与家法隔离的规则和算法。
- [`rules/jinjing/geju/`](rules/jinjing/geju/)：《太乙金镜式经》主格局引擎。
- [`rules/jinjing_v4_military.json`](rules/jinjing_v4_military.json)：四库本《太乙金镜式经》卷四军事十二法 J4M-01..12 来源限定规则表。
- [`src/kintaiyi/`](src/kintaiyi/)：七术、八占、公共规则与五福/大游。
- [`src/kintaiyi/variants/`](src/kintaiyi/variants/)：现代／重构运行时，与古籍 canonical 物理隔离。
- [`rules/variants/`](rules/variants/)：现代／重构 profile 的机器规则；当前含 `modern_liunian_nayin_2026`。
- [`docs/taiyi_v1.md`](docs/taiyi_v1.md)：v1 整合包接口、兼容边界和待校项。
- [`rules/taiyi_v1.json`](rules/taiyi_v1.json)：canonical、原典短句、版本异文分层数据。
- [`sources/`](sources/)：来源证据、异文、采用边界和参考快照。
- [`tests/`](tests/)：规则回归、历史局例输入和差异报告。
- [`CHANGELOG.md`](CHANGELOG.md)：本库实质变更记录。
- [`changelog/`](changelog/)：按批次保存的详细变更记录。

## 规则来源

本次格局主规则唯一采用《太乙金镜式经》卷三，八门值事周期采用卷四。`kentang2017/kintaiyi` 只作为固定版本参考实现、历史局例和旧 `skyeyes_summary` 对照来源；它不属于本仓库的写入目标，也不决定《金镜》主规则。

军事十二法另以四库本《太乙金镜式经》卷四正文为 `jinjing_siku_volume4` 来源层，依次编号 J4M-01..12；与 C8 `volume5_strict` 仅做 crosswalk，不因同名或近名自动合并。《金镜》与《统宗》同名术出现差异时保留独立 source profile。

所有数值算法必须保留输入、精确位置、边界、版本和可回查来源。相异古籍表述进入来源说明与对照测试，不合并进《金镜》运行规则。

现代《太乙数纳音体系（修正版）》独立登记为 `modern_liunian_nayin_2026`，位于 `src/kintaiyi/variants/` 与 `rules/variants/`；它不是 J4M-03 的下属变体，也不得覆盖任何古籍 canonical。

七术、八占与五福/大游采用 `taiyi-t7-d8-v1` 已确认项目规范；四库为底本，《统宗》《景祐》《金钥匙》等补证和异文保留。各模块的来源边界独立；格局规则的来源限定保持原有定义。安装 `python -m pip install -e .` 后可直接导入 `kintaiyi` 与根目录旧名接口 `config`。

## Modern production 日历入口

当前 production canonical 已采用现代天文 / 现代历法事实层：

- `astronomy-engine`：真实两分两至、十二节交节时刻；
- `lunar_python`：现代中国农历、干支与历史历法重建辅助。

太乙岁唯一换年边界：

> **真实天文冬至交节瞬间。**

公历 `Y` 年冬至瞬间起进入太乙 `Y+1` 岁。元旦、春节、立春、春分均不改变太乙岁。

现代四计统一入口：

- `kintaiyi.taiyi_modern_calendar.production_calendar_context(moment)`
- `kintaiyi.taiyi_modern_pan.build_modern_pan_v2(moment, count_type=...)`

`count_type` 必须显式选择：

- 岁计；
- 月计；
- 日计；
- 时计。

现代 pan v2 会同时保存：

- `calendar.taiyi_year`：只由冬至换年决定；
- 农历年：只作并列事实；
- 立春干支年：只作并列事实；
- 月计太阳月：由十二节交节决定；
- 日计：Asia/Shanghai 00:00 民用日；
- 时计：冬/夏至半岁相对积时。

`pan_adapter.py` 只负责旧 flat snapshot 迁移，是 legacy compatibility，不是 modern production 日期计算入口。

安装项目时会自动安装 production 依赖：

```powershell
python -m pip install -e .
```

## 参考与鸣谢

本项目在规则整理、接口核对、历史实现比对与测试设计过程中，参考了开源项目 [kentang2017/kintaiyi](https://github.com/kentang2017/kintaiyi)。

感谢原作者及相关贡献者公开其太乙神数 Python 实现，为本项目提供了有价值的代码结构、历史局例与实现思路参考。

需要特别说明：`kentang2017/kintaiyi` 在本项目中属于**参考／借鉴代码库**，不是本项目的古籍文献来源，也不作为 canonical 规则的最终判定依据。本项目的规则采用、异文处理和来源等级仍以各古籍原文、影印见证及本仓库的独立校勘记录为准。

## 运行测试

在 Python 3.10+ 环境安装 `pytest` 后，从仓库根目录运行：

```powershell
python -m pytest
python tests/test_skyeyes_summary_audit.py
```

第二条命令重新生成 `tests/reports/skyeyes_summary_audit.md`。差异分类允许旧表摘要与新规则不完全一致；每局结果和差异原因均保留。

