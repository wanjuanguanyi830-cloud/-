# 2026-10-05 C42 Dayou lishu / settled-reign rules

- 新增唯一 canonical runtime：`dayou_lishu.py`。
- 回修 C41 策数：36/24/28/32 为单爻策数，经卦乘3。
- 锁定乾内108 + 震外84 = 192 等卷九算例。
- 纳甲数末组按参校正规化为巳亥=4，同时保留“己亥四”OCR witness。
- 初/四只加本爻纳甲。
- 二/五六爻纳甲总和倍加。
- 三/六不倍不加。
- 历数除策中间量因历史算例冲突，不自动生成取余公式。
- 安居一二四五长、三六短与附加政治证据分层。
- 删除并行重复 `dayou_lifespan.py` runtime，保持单一真源。
- 当前 CI：782 passed / 0 failed。
