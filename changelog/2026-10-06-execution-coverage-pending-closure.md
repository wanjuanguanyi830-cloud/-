# 执行覆盖 stale pending 收口

本轮以 main `b4c8d08934950d4ef01ac33257ff7955e75ee342` 为起点。

- C23 的 `pending_low_dependency` 清空，V15-09/12/13 改列 `implemented_by_c24`。
- C24 的 `next_dependency` 清空，V15-10 改列 `implemented_by_c25`。
- 各模块 `implemented` 仍只列本模块负责规则，避免重复计算覆盖。
- 卷十五/十七术语中20处旧“当前只登记”说明与现有独立 runtime 同步。
- C123 来源记录改为已实现开门加四锚点及合门判断，并链接仓库已有直接和平行来源记录。

来源依据均为仓库现有记录：
`sources/c23-tongzong-v15-low-record.md`、
`sources/c24-tongzong-v15-observations-record.md`、
`sources/c25-tongzong-v15-wind-sound-record.md`、
`sources/jinjing-eight-door-overlay-record.md`、
`sources/jinjing-year-door-meeting-record.md`。

真实边界保留：实际风向/风起宫/云来向/风声缺输入仍不可算；
坤宫讹文、未定义算向、不合成总胜负不变；
C119时计移动叠加尚未重建，王希明直使加锚点仍为 `parallel_reconstruction`。
本轮未新增古籍公式、未提升未核验来源等级。

新增防回归覆盖目录交接与真实可调用 runtime、四条规则缺观测不可算、
术语不再声称只登记、C123来源记录与现行叠加状态一致。

实际本地验证：定向 **120 passed / 0 failed**（0.46s）；
full pytest **2459 passed / 0 failed**（3.65s）。
