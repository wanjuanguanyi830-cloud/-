# C114 八占历史例回归恢复

日期：2026-10-05

## 1. 恢复对象

旧分支：

`integrate-taiyi-war-v1-20261004`

文件：

`tests/fixtures/warfare_v1_historical_cases.json`

其中七术历史例已经由当前 main 的：

- `tests/fixtures/seven_methods_classics.json`
- `tests/test_seven_methods_classics.py`

吸收。

但八占中三条带历史身份的古例只剩规则级测试，旧 fixture 的历史来源身份没有迁入：

- D8-02 长短：唐太宗贞观四年主算31；
- D8-04 孤单：唐昭宗光化三年主算单3；
- D8-08 数有所主：唐玄宗天宝十年客算17。

C114 只恢复这三条，不复制已经有现行覆盖的结构例。

## 2. 直接见证

《太乙统宗宝鉴》卷五。

### NGJ

https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny524fmn96c

直接见：

#### D8-02

“明长短之数，以占缓急术”：

- 十一以上为长；
- 十以下为短；
- 唐太宗贞观四年，主算得三十一；
- 原文以“算长，利以深入”解释李靖深入破突厥之例。

#### D8-04

“明数有孤单，以占成败术”：

- 一三七九为单阳；
- 单阳/孤阳不利主；
- 唐昭宗光化三年，主算得单三，为单阳。

#### D8-08

“明数有所主，以占凶吉术”：

- 十为将军；
- 五为吏士；
- 一为兵卒；
- 唐玄宗天宝十年，客算得十七，原文明写“将吏兵卒皆备”。

### CADAL

https://www.shidianguji.com/book/CADAL02094393/chapter/1lcppwswbwf8a

CADAL 卷五平行见证支持上述 D8-02 与 D8-08 核心读法；另一本 CADAL 转录亦支持光化三年“单三 / 单阳”古例。

## 3. 新增 fixture

`tests/fixtures/eight_divinations_historical_cases.json`

只保存三条直接古例：

- EX-D8-02-ZHENGUAN-4
- EX-D8-04-GUANGHUA-3
- EX-D8-08-TIANBAO-10

新增：

`tests/test_c114_eight_divinations_historical_cases.py`

## 4. 硬边界

### D8-02

历史例只证明：

- 31 = 长；
- 长宜缓、深入。

不把该战役整局结果归因于长短一术。

### D8-04

历史例只锁：

- 3 = 单阳；
- 不利主。

后续废立事件只是原书例证，不新增运行规则。

### D8-08

历史例直接锁：

- 17 = 将军 + 吏士 + 兵卒皆备。

但不得因此恢复旧的：

`16以上皆具`

阈值实现。

当前结构层继续保持：

- 5：只有吏士；
- 15 / 25 / 35：将军 + 吏士；
- 17：三者皆备且有直接古例标签。

## 5. 结论

旧 warfare fixture 的历史例价值已经按现行规则重新吸收。

处理方式仍是：

**旧完成工作定位 → 直接古籍重核 → 只迁仍成立的历史回归意图。**
