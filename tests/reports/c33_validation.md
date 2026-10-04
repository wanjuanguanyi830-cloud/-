# C33 V17 runtime 去重验证

日期：2026-10-05

验证：

- structured 模块是唯一 canonical runtime。
- conditions 模块返回 compat_adapter=True。
- conditions 模块标记 canonical_runtime=tongzong_v17_structured。
- 旧 V17-06/07/08/09 API 测试继续通过。
- source variants 继续保留。
- canonical 修正后的“门不具或将不发”与“始击在内”测试通过。

完整 CI：

```
643 passed in 0.61s
```

当前基线：643 passed / 0 failed。
