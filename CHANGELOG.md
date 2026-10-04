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
