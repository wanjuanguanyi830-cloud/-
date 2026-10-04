# C38 太游阳九 / 百六内外卦行限记录

## 直接来源

### 卷十：周期职责

识典《太乙统宗宝鉴》卷十：

https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppwz3ep1yr

“明阳九百六，太游行限观历术”明确：

- 阳九：太游理外卦；
- 10 年一宫；
- 80 年一竟；
- 57 竟 = 4560；
- 百六：太游理内卦；
- 36 年一宫；
- 288 年一竟；
- 15 竟 = 4320。

### 卷九：八宫顺序职责

识典《太乙统宗宝鉴》卷九：

https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppwy0a63aq

“明太游太乙轨运入内卦所在术”明确：

- 起七宫坤卦为首；
- 顺行八宫；
- 不入中五。

“明太游轨运入外卦所在术”又列：

- 坤
- 坎
- 巽
- 乾
- 离
- 艮
- 震
- 兑

故 C38 八宫路径固定：

`7坤 → 8坎 → 9巽 → 1乾 → 2离 → 3艮 → 4震 → 6兑`

## 与旧 guiyun 实现的区别

旧参考：

- 内卦另加 +34；
- 外卦另加 +50；
- 外卦还进入 640 年六十四卦轨运。

C38 本轮只实现“阳九百六太游行限观历术”层：

- 使用 C36 阳九 +130 / 百六 +2050 的限周期作为时间轴；
- 不把旧 +34/+50 偏移混入该层；
- 不把后续重卦、六十四卦轨运一并塞入。

因此 C38 不是旧 `dayou_nei_gua/dayou_wai_gua` 的直接兼容移植。

## 实现

`src/kintaiyi/taiyou_limit_tracks.py`

规则：

- `C38-YJ-OUTER`
- `C38-BL-INNER`

输出：

- round_index
- year_in_round
- palace
- trigram
- year_in_palace
- palace_complete
- round_complete
- big_limit_complete

聚合：

`taiyou_limit_tracks(accumulated_year)`

可嵌入：

`cycles.limits.taiyou_tracks`

## 边界

- 外卦只属于阳九；
- 内卦只属于百六；
- 二者共享八宫序，不共享周期；
- 不自动把整个旧“卷九”wrapper标成 migrated；
- 重卦、策数、动爻属于后续独立规则。

## CI

```
715 passed in 1.16s
```

当前基线：715 passed / 0 failed。
