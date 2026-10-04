# C51 登位旁云气生克 / 干支数观察层

## 直接来源

《太乙统宗宝鉴》卷十“明太乙历数之期术”末段：

- 天子初登位日月旁云气生克

识典：
https://www.shidianguji.com/book/CADAL02055529/chapter/1l5eriw9odw6f

重要参校：

《太白兵备统宗宝鉴》
https://www.shidianguji.com/book/SDZJ0646/chapter/1kghfsbbgiwc2

## 1. 日 / 辰必须分开

正文明确：

- 以干为日；
- 以支为辰。

因此：

- 日五行 = 日干五行；
- 辰五行 = 日支五行。

干支五行映射以《五行大义·第五论配支干》作背景依赖：甲乙寅卯木，丙丁巳午火，戊己辰戌丑未土，庚辛申酉金，壬癸亥子水。该背景依赖只用于解释本条“生 / 克”，不改变《统宗》主见证层级。

旧 `guiyun.yunqi_zhanbo` 只取日干五行，所谓“云生辰”实际没有检查日支，是结构错误。

## 2. 五种关系

C51 分别保存：

- 云生日 → 国祚昌、多子；
- 云生辰 → 内宫享福、多女；
- 云克日 → 绝嗣；
- 日生云 → 吉；
- 比和 → 吉。

多个关系可以同时成立。

固定：

`overall_single_verdict=None`

不再用 if / elif 压成单一断语。

## 3. 云形

- 阴云 → 位祚不久；
- 五色彩云 → 国代绵远寿昌、子孙兴旺。

云形与五行生克是并列证据。

阴云 / 五色彩云可以只凭形态成立，**无需单一云色**；此时保留 form_effects，但 `relation_checked=False`，不伪造某一五行云色来计算生克。

## 4. 云气生数 / 成数

直接复用 C50 已校双值：

- 木 3 / 8；
- 火 2 / 7；
- 土 5 / 10；
- 金 4 / 9；
- 水 1 / 6。

固定：

- `cloud_number_selection=None`
- `cloud_number_selection_status=sheng_cheng_pair_unselected`

不擅自选生数或成数。

## 5. 干支数

复用 C42 已校干支数：

- 甲己子午 9；
- 乙庚丑未 8；
- 丙辛寅申 7；
- 丁壬卯酉 6；
- 戊癸辰戌 5；
- 巳亥 4。

例如：

己亥 = 9 + 4 = 13。

旧 `_GAN_NUM` 把己列为4，已明确废止。

## 6. 时间尺度

正文说当日干支数“通而并之”，又提：

- 大而计年；
- 小而计月；
- 近而计日时。

但当前直接文本没有给一个无歧义的“何时选年 / 月 / 日时”的统一判别式。

因此：

- `time_scale=None`
- `specific_period=None`

只保存干支和数，不自动生成具体期限。

## 实现

- `src/kintaiyi/coronation_cloud_omens.py`
- `tests/test_coronation_cloud_omens.py`

## CI

```
970 passed in 1.21s
```

当前基线：970 passed / 0 failed。
