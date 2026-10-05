# C107 大游太乙所在宫：金镜 / 统宗来源分层

日期：2026-10-05

## 1. 最近两天恢复线索

来源旧工作：

- branch: `codex/taiyi-base-motion-2026-10-04`
- file: `rules/dayou/dayou.json`
- commit: `7f2d1b5dc74ea8dbb0363ee0ebc479de9cb09b08`
- date: 2026-10-04T03:26:49Z

旧工作已经保存：

- 金镜元法4320；
- 小周288；
- 每宫36年；
- 起七宫；
- 顺行八宫；
- 不入中五。

C107 不直接复制旧 JSON 的“单一 canonical”概念，而是重新按来源分 profile。

## 2. 《太乙金镜式经》

“推大游太乙所在”直接见：

- 上元甲寅；
- 元法4320；
- 小周288；
- 36年一宫；
- 命起七宫；
- 顺行八宫；
- 不游中五。

来源：

https://www.shidianguji.com/book/SK1615/chapter/1l9lira3cuf49

因此金镜 profile：

- surplus=0；
- outer=4320；
- small=288；
- rate=36。

同卷另列纪法720，C107保存为 metadata，不把它强塞成位置计算第二次取模。

## 3. 《太乙统宗宝鉴》

卷七“明太游太乙所主术”直接见稳定核心：

- 三十六年考治一宫；
- 二百八十八年一周；
- 加宫盈差34；
- 算法层见大周2880；
- 起七宫；
- 顺行八宫；
- 不入中五。

来源：

https://www.shidianguji.com/zh/book/CADAL02094393/chapter/1lcppwvvwt996

电子转录的算法句另见：

“小周法三百八十八”。

C107 不把 388 写进 runtime，原因：

1. 同条前文已经明确“二百八十八年一周”；
2. 八宫 × 36年 = 288；
3. 《易学象数论》平行条明确：
   - 宫周288；
   - 宫率36；
   - 宫盈差34；
   - 起七宫坤，顺行八宫。

参校：

https://www.shidianguji.com/book/SK0122/chapter/1kfib48aa4ahx

因此 C107 保存：

- electronic_reading=388；
- execution_value=288；
- status=resolved_numeric_transcription_conflict。

这不是把异文删掉，而是把“文本读法”和“执行值”分栏。

## 3.1 统宗两电子见证数字异读

进一步对两份统宗电子见证分栏：

### NGJ892411999009267118912

读作：

- 宫盈差32；
- 大周2880；
- 小周288。

### CADAL02094393

读作：

- 宫盈差34；
- 大周2880；
- 小周388。

这两份读法不得静默拼接成“某一本统宗原文”。

但同条稳定叙述明确：

- 36年一宫；
- 288年一周。

且《易学象数论》平行见证明确：

- 宫盈差34；
- 宫周288；
- 宫率36。

因此 C107 当前执行层采用：

- surplus=34；
- small_cycle=288；

并标：

`collated_selection_not_single_witness_literal`

两份统宗原始数字读法均完整保存在 `witness_variants`，且 `canonical_override=False`。

## 4. 金镜 / 统宗不得乱合

共同：

- small=288；
- rate=36；
- path=[7,8,9,1,2,3,4,6]；
- 不入中五。

金镜：

- epoch=上元甲寅；
- outer=4320；
- surplus=0。

统宗：

- epoch=上元甲子；
- outer=2880；
- surplus=34。

所以旧：

`profile="jinjing_tongzong"`

必须继续作为 mixed legacy compatibility 隔离，不能改名冒充 C107。

## 5. 与 C41 的边界

C41：

- 大游重卦；
- 四象策数；
- 动爻；
- epoch variant 不自动选择。

C107：

- 大游太乙所在九宫。

二者不是同一 runtime。

## 6. 与 C65 / C91 的边界

C65、C91 有大游与其他主体的同宫关系。

C107 只求位置：

- `same_palace_omens_applied=False`
- `auto_conjunction_omens=False`

关系层继续要求显式同宫证据。

## 7. legacy adapter 后续

C107 建立后：

- `bigyo(profile="jinjing")` 应委托 C107 金镜；
- `bigyo(profile="tongzong")` 应委托 C107 统宗；
- `bigyo(profile="jinjing_tongzong")` 保留旧混合数值，但继续 quarantine；
- `config.bigyo()` 默认行为不静默改 source profile。
