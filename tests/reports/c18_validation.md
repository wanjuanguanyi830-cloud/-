# C18 《太乙紫庭经》来源层验证报告

日期：2026-10-05

## 来源层级

六项规则统一：

- 主要参考：《太乙紫庭经》
- 参校：《太乙统宗宝鉴》
  - 太乙九星 / 文昌九星 / 文昌变化 / 始击变化：卷六
  - 三旗行宫 / 九宫贵神：卷十

统宗仍可用于参校，不是弃用。

## 结构验证

- primary_source 固定为 `zitingjing`。
- 仅有统宗参校时：
  - `primary_ready=False`
  - `canonical_selected=None`
  - `status=primary_pending`
- 有《太乙紫庭经》结构化结果后：
  - `primary_ready=True`
  - `canonical_selected=zitingjing`
- 主来源与参校结果并列保存，`cross_source_merge=False`。
- 错卷参校来源直接拒绝。
- 旧 flat 六项不会自动进入 primary_result。
- C13 只有在对应 primary_result 存在时才清除 replacement gap。

## CI

并行 J4M 更新完成后最新主分支：

```
332 passed in 0.56s
```

当前基线：332 passed / 0 failed。
