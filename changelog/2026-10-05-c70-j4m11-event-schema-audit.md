# C70 — 收紧 J4M-11 风云飞鸟观测事件语法

日期：2026-10-05

修复两处 source overreach：

1. 每条外部事件现在必须显式声明 phenomenon=风/云/飞鸟类，缺失 phenomenon 不得仅凭“扶阵/冲阵/迫击”等动作触发断语。
2. “迫击大将宫”只接受原文动作“迫击”，删除旧 runtime 对近义“冲击”的自动兼容。

《福应经》的更展开/冲突读法继续保存在独立 JF4M profile，不进入 J4M canonical。
