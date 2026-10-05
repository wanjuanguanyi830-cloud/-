# C112 遗留同宫关系恢复

日期：2026-10-05

恢复并重新核源四组 2026-10-04 已完成但此前未正式迁入 main 的关系：

- 五福 × 大游
- 五福 × 小游
- 四神 × 小游
- 大游 × 小游

新增：

- `src/kintaiyi/wander_conjunctions.py`
- `tests/test_c112_wander_conjunctions.py`
- `sources/c112-recovered-wander-conjunctions-record.md`

规则边界：

- 不自动从 C67/C92/C103/C107 推同宫；
- 五福×大游保留五福条 / 大游条两层来源；
- 五福×小游显式区分有德 / 失德；
- 大游×小游按 NGJ/CADAL 两见证稳定读法采用“凶暴大作”；
- 不重复 C65/C91/C94 已有 pair。
