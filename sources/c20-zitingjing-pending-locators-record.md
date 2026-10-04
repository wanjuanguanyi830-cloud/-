# C20 《太乙紫庭经》剩余三项定位证据分层

## 目标

C19 已直接定位并结构化：

- 太乙九星
- 文昌变化
- 始击变化

C20 继续处理：

- 文昌九星
- 三旗行宫
- 九宫贵神

原则：没有《太乙紫庭经》直接正文时，不用统宗参校文本补成 primary_result。

## 文昌九星

当前证据：

- 现代整理本《太乙紫庭秘诀》目录列：
  `附太乙文昌九星值宫术`
- 目录参照：
  https://www.chinyuan.com.tw/all_book/more?id=7195

因此状态：

`catalog_attested_primary_text_pending`

说明：

- 可确认该术与《太乙紫庭秘诀》传本系统有关；
- 但目前未取得可逐条校读的直接正文；
- 不生成 primary_result。

## 三旗行宫

当前《太乙紫庭经》直接条文仍未定位。

项目来源层级继续按校勘原则保留：

`primary_source = 太乙紫庭经`

当前可直接定位的统宗参校文本：

- 《太乙统宗宝鉴》卷十
- 〈明太乙与三旗行宫会合术〉
- https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec

状态：

`project_primary_attribution_direct_text_pending`

统宗文本只进入 collation，不进入 primary_result。

## 九宫贵神

当前《太乙紫庭经》直接条文仍未定位。

可直接定位的统宗参校文本：

- 《太乙统宗宝鉴》卷十
- 〈明太乙九宫贵神术〉
- https://www.shidianguji.com/book/NGJ892411999009267118912/chapter/1lny52hi7lfec

状态：

`project_primary_attribution_direct_text_pending`

## C20 规则

三项均不得因为“已有统宗公式”而自动清除 C18/C13 primary replacement gap。

证据等级必须区分：

1. direct primary text
2. catalog-attested primary affiliation
3. project primary attribution
4. collation text

只有第 1 级可直接生成 primary_result。
