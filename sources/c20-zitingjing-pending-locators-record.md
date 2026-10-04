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

原则：证据等级必须逐项记录；没有《太乙紫庭经》直接正文时，不用统宗文本补成 primary_result。

## 文昌九星

当前证据比三旗/九宫贵神更强。

两处现代整理本《太乙紫庭秘诀》目录均列：

`附太乙文昌九星值宫术`

目录参照：

- https://www.chinyuan.com.tw/all_book/more?id=7195
- https://www.xinyi.hk/goods-7102.html

因此状态：

`catalog_attested_primary_text_pending`

说明：

- 可确认“文昌九星值宫术”附属于现存《太乙紫庭秘诀》传本系统；
- 尚未取得可逐条校读的直接正文；
- `primary_result_allowed=False`；
- 不生成 primary_result。

## 三旗行宫

重新核对《太乙紫庭秘诀》现存十二卷及附录目录后，当前**未见“三旗行宫”题名**。

因此项目原先的：

`primary_source = 太乙紫庭经`

只能保留为“项目拟定主来源目标”，不能当作已证古籍归属。

当前状态：

`project_primary_attribution_unverified`

直接可定位文本来自：

- 《太乙统宗宝鉴》卷十
- 〈明太乙与三旗行宫会合术〉

统宗目录与正文均可直接证明该术存在于卷十。

在取得紫庭传本目录或正文证据前：

- 不得生成紫庭 primary_result；
- 不得把统宗内容改标为紫庭；
- 迁移层级按 source_variant 处理。

## 九宫贵神

重新核对《太乙紫庭秘诀》现存十二卷及附录目录后，当前**未见“九宫贵神”题名**。

项目原先的紫庭主来源指定同样降为：

`project_primary_attribution_unverified`

直接可定位文本来自：

- 《太乙统宗宝鉴》卷十
- 〈明太乙九宫贵神术〉

此外唐代王起〈定祀九宫仪注议〉已经独立记载九宫贵神九神名称及宫、星、卦、五行等体系，可作更早的历史背景证据，但它不是《太乙紫庭经》文本，也不能替代紫庭 primary。

在取得紫庭归属证据前：

- `primary_result_allowed=False`
- 统宗只保留为直接来源 profile / 参校来源；
- 不清除 C18/C13 的紫庭 primary replacement gap。

## 证据等级

当前必须区分：

1. `direct_text_verified`
2. `catalog_attested_text_pending`
3. `project_attribution_unverified`
4. collation/direct-other-source text

只有第 1 级允许直接注入 `primary_result`。

当前三项：

- 文昌九星：第 2 级
- 三旗行宫：第 3 级
- 九宫贵神：第 3 级

这比原先把三项都笼统记作“紫庭正文待定位”更严格。


## 文昌九星外部参校进展

已新增：

`sources/c20-wenchang-nine-stars-collation-record.md`

当前直接外部见证：

- 《三才世纬》卷八十一〈求文昌九宫所主分野〉
- 《太乙统宗宝鉴》卷六两个在线见证

已确认：

- 星名存在明雄/明维、阴玄/阴德、雄明/维明等异文；
- 值宫年率出现 10 / 30 年冲突；
- 一个统宗电子见证自身同时出现“十年一宫”与“宫率三十、小周270、大周2700”。

所以这些材料只进入 collation，不改变 `catalog_attested_primary_text_pending`，也不生成 canonical 推步。
