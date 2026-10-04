# C47 小游轨运 / 重卦 / 动爻记录

## 直接来源

《太乙统宗宝鉴》卷九：

- 明小游轨运内卦所在术
- 明小游轨运外卦所在术
- 明小游内外相重之策术

识典：
https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppwy0a63aq

参校《太白兵备统宗宝鉴》：
https://www.shidianguji.com/book/SDZJ0646/chapter/1kghfsbbgiwc2

## 1. 内卦

直接结构：

- 大周：1920
- 小周：192
- 每24年一经卦
- 卦序：乾、离、艮、震、兑、坤、坎、巽
- 24年均分六爻，因此4年一爻

一份统宗在线 OCR 大周字样残损/误作1900类读法；
《太白兵备统宗宝鉴》明确见1920、192、24，并有万历己未余80、入震8年的算例。

runtime 取1920，同时保留 OCR note。

## 2. 外卦

直接结构：

- 纪元周：360
- 八卦周：24
- 每3年一经卦
- 卦序同内卦
- 第一年理天
- 第二年理地
- 第三年理人

360与24分层保存，不压成单一模数。

## 3. 重卦

- 内卦画下；
- 外卦画上；
- 内卦动爻使用4年一爻；
- 外卦本层不另造动爻。

C47 不强制命名六十四卦：

- `hexagram_name=None`
- `hexagram_name_status=not_resolved_in_c47`

## 4. 策数

四象策数复用 C41 已校共享表：

- 乾每爻36
- 坤每爻24
- 震坎艮每爻28
- 巽离兑每爻32

每经卦三爻后再合计。

只复用策数表，不复用 C41 大游积年/epoch。

## 5. 与大游分离

固定：

- `c38_track_used=False`
- `dayou_epoch_offset_used=False`
- 不使用 +34 / +50
- 不与阳九百六太游轨迹混并

## 实现

- `src/kintaiyi/xiaoyou_hexagram.py`
- `tests/test_c47_xiaoyou_hexagram.py`

## 验证基线

与 C46 同批功能测试全套：

`882 passed / 0 failed`
