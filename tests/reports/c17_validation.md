# C17 source profile 验证报告

日期：2026-10-05

完成：

- 新增 patterns source profiles
- 新增 military P0 source profiles
- C14 quarantine replacement 路径细化
- C13 检查具体 profiles 是否非空
- 旧 flat 断语不进入 analysis

关键验证：

1. 统宗格局与金镜格局可同时保存，`canonical_selected=None`。
2. 三门/五将的 C8 角色只标 upstream，不宣称公式等价。
3. 主客相关不允许用 C8-L3 作为直接替代。
4. 空 source profile 容器不能清除 replacement gap。
5. 显式传入各来源结构化结果后，gap 才清零。
6. 与并行新增的 J4M runtime 规则共同测试通过。

完整 CI：

```
306 passed
```

当前基线：306 passed / 0 failed。
