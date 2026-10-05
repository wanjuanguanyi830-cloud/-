# C116 《金镜》卷一“推太乙玄命法”

日期：2026-10-05

## 来源

《太乙金镜式经》卷一：

- 天子玄命在天乙；
- 皇后玄命在天后；
- 公侯玄命在太常；
- 将军玄命在勾陈；
- 九牧玄命在螣蛇；
- 常侍玄命在天空；
- 二千石玄命在青龙；
- 大夫、吏士玄命在朱雀；
- 庶人玄命在行年。

直接见证：

- https://zh.wikisource.org/zh-hans/太乙金鏡式經_(四庫全書本)/卷01
- https://www.shidianguji.com/book/SK1615/chapter/1l9lir739il1m

## 实现

新增：

- `src/kintaiyi/jinjing_xuanming.py`
- `tests/test_c116_jinjing_xuanming.py`

C116 只做身份 -> 玄命所主映射。

不做：

- 旺相判断；
- 上下相生判断；
- 吉凶；
- 庶人行年推算。

这些条件属于后续“推太公考时法”或独立行年层。

OCR/转录“二干石”只作 `二千石` alias，不作为第二 canonical 身份。
