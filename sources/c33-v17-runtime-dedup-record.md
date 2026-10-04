# C33 卷十七条件层去重记录

## 目标

目标仓库曾同时存在两套 V17-06/07/08/09 runtime：

- `tongzong_v17_structured.py`
- `tongzong_v17_conditions.py`

C33 固定：

- canonical runtime：`tongzong_v17_structured.py`
- compatibility adapter：`tongzong_v17_conditions.py`

## canonical 修正

在去重过程中同步修正两处来源逻辑：

1. “三门不具或五将不发”：
   - 任一为 false 即成立；
   - 不要求两者同时 false。

2. 讨捕叛亡：
   - 始击/下目在内也是捕得证据；
   - 太乙与主人同宫而天目临之保留为独立捕得证据。

## compatibility adapter

旧函数名继续保留：

- `hearsay_reality`
- `capture_fugitive`
- `prison_interrogation`
- `request_gain`

但这些函数只调用 canonical runtime，再翻译为旧字段形状。

适配层固定返回：

- `compat_adapter=True`
- `canonical_runtime="tongzong_v17_structured"`

禁止在适配层再次维护第二套古法判断。

## 旧 API 特殊兼容

V17-08 旧接口曾暴露一组传本冲突：

- 掩击 / 主人在外 / 旺神

C33 仅作为旧 API 的 source_variant 表达保留；
canonical runtime 的古法证据仍以 `tongzong_v17_structured.py` 为准。

## 验证

完整测试：

```
643 passed in 0.61s
```
