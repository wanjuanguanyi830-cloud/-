# 2026-10-06 — C69/C69B stale pending 收口

## 已完成状态

C69B 已在显式输入且 C118 日度可算时完成：

- 以日宿分野支加占时时支并建立天地盘；
- 按日干与显式朝 / 暮取天乙，求贵人落地并确定顺逆；
- 顺逆布十二天将；
- 通过实体地支或九宫 adapter 查询所临天将。

这些步骤不再列入 C69 或 C118 的 pending。

## 当前边界

- 公历日期到节气第几日尚无自动入口；
- 朝 / 暮尚无按时辰自动判定入口；
- C118 虚宿整数未定，跨越该未定边界的日期返回 `not_computable`；
- 九宫到十二支是有损 adapter，严格调用可直接提供实体地支。

因此 `C69.complete_current_time_formula=False` 保留为“完整自动单入口尚未统一”；`C69B.complete_for_explicit_inputs=True` 保持。这个标志不表示显式输入的六壬叠盘核心未实现。

## 变更位置

- C69、C69B、C118 运行时边界与 catalog；
- C69/C69B/C118 来源记录、术语目录、README 与 CHANGELOG；
- C69/C69B/C118 与 legacy catalog 一致性防回归测试。

## 验证

- Targeted pytest：83 passed。
- Full pytest：2456 passed in 3.88s。

