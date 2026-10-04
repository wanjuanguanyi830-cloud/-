# C35 有效迁移状态与来源槽位修正

## 目标

C15 是历史迁移候选目录，后续 C16-C34 已改变大量字段的真实状态。

C35 解决两个问题：

1. 历史候选仍把已完成 J4M-11 标成 pending；
2. 旧统宗 flat 六项被错误要求以《太乙紫庭经》 primary_result 才能清除迁移缺口。

## 1. J4M-11 风云飞鸟

《太乙金镜式经》卷四 J4M-11 已有完整 source-specific runtime：

`fengyun_feiniao_zhuzhan(events)`

其关键边界：

- 必须有显式外部风、云、飞鸟观测；
- 不从盘内太乙/飞鸟位置伪造观测；
- 旧参考实现 `flybird_wl` 只根据盘内飞鸟位置生成断语，不是 J4M-11 的等价 runtime。

因此旧：

`推太乙風雲飛鳥助戰法`

改为 quarantined，replacement 固定：

`source_variants.military.weather_bird_support.profiles.jinjing_siku_volume4`

新增：

`build_weather_bird_source_variant(...)`

只有 source_profile/ruleset/rule_id 均匹配 J4M-11 的结果才可进入该槽。

## 2. 紫庭六项 legacy flat 的来源修正

旧 pan 里的：

- 太乙九星
- 文昌九星
- 文昌变化
- 始击变化
- 三旗行宫
- 九宫贵神

来自旧统宗系实现。

因此 legacy migration replacement 不应指向：

`primary_result`

而应指向同源参校槽：

- 前四项 → `collation_results.tongzong_volume6`
- 三旗行宫 / 九宫贵神 → `collation_results.tongzong_volume10`

这样：

- “旧 flat 是否已结构化迁移”
- “《太乙紫庭经》主来源是否研究完成”

成为两个独立状态。

尤其文昌九星仍可保持：

`primary_text_pending`

同时旧统宗 flat 已安全迁到 collation profile。

## 3. C15 历史候选刷新

- 太乙九星：direct primary 已验证，canonical candidate。
- 文昌九星：改为 pending，等待附篇正文；10年/30年参校冲突未解。
- 风云飞鸟：改为 source_variant，J4M-11 已完成，旧 flybird_wl 仅 quarantine。

## 4. migration audit

C13 replacement order 已改用上述 source-specific 路径。

因此 legacy migration readiness 不再被尚未取得的紫庭 primary 文本错误阻塞。

## CI

C35：

```
655 passed in 1.07s
```

当前基线：655 passed / 0 failed。
