# C61 C15 unported catalog 全局一致性清扫

日期：2026-10-05

## 结果

C15 仍精确覆盖 67 个旧 pan 顶层字段。

清扫后 layer 分布：

- canonical: 31
- derived: 18
- pending: 2
- source_variant: 16

strict pending 只剩：

- 推太乙當時法
- 文昌九星

## 本批升级为来源已证、runtime待拆

天子巡狩：

- 《太乙统宗宝鉴》卷五直接正文已定位；
- 太乙与天目在四维之岁为巡狩期；
- 出方向取天目/文昌所临；
- 行期月另参囚、挟、格、对。

三基 / 五福：

- 君基、臣基、民基；
- 五福太乙、五福吉算/所利；
- CADAL/NGJ见证有卷六/卷七编次差异；
- 仅保存 witness volume variant，不复制公式。

天乙 / 地乙 / 直符：

- 卷七直接正文已定位；
- 分别为金神、土神、火神体系；
- 旧字段题名简写不覆盖直接正文题名。

## 边界

source verified 不等于 runtime implemented。

本批新升级的9项全部保持 migrate_whole=False，旧 flat 结果不得直接搬为 canonical。

十精目录说明同步：C57合会、C58观察、C59数值天气三层已实现，旧 yunqi 综合 wrapper 仍隔离。

## CI

1205 passed / 0 failed。