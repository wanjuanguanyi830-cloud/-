# C36 《太乙紫庭经 / 紫庭秘诀》传本见证目录

日期：2026-10-05

## 目的

本层只记录传本、馆藏、目录和在线转录的证据等级。

它不：

- 选择唯一 canonical manuscript；
- 把馆藏存在当成已读正文；
- 假设不同传本附录完全一致；
- 生成任何太乙术法结果。

代码：

`src/kintaiyi/zitingjing_witnesses.py`

## A. 哈佛燕京系清抄《太白兵备统宗宝鉴》

当前在线直接转录可见：

- 《太乙紫庭经表》
- 《太乙紫庭序》
- 释九宫所值九星
- 释天目变化
- 始击变化

识典：

- book id: `HY5849`
- 卷一：https://www.shidianguji.com/book/HY5849/chapter/1l1bukbn18088
- 目录：https://www.shidianguji.com/book/HY5849/chapter/1l1bujx4cdszk

书格等资源说明称该清咸丰十年抄本现存哈佛燕京图书馆；这一馆藏归属当前仍按二级资源说明登记，不把二级说明升级成馆方原始目录记录。

当前在线搜索**未定位**：

`附太乙文昌九星值宫术`

该“未定位”只表示当前在线检索没有找到，不等于证明该抄本绝无此篇。

## B. 上海研易楼藏明抄《太乙紫庭秘诀》

2015 年吴炜维校订、香港星易图书出版的《太乙紫庭秘诀》出版说明称底本藏上海图书馆，并有研易楼藏书钤印。

现代整理本目录明确列：

`附太乙文昌九星值宫术`

出版信息：

- ISBN: 9789881412058
- 初版：2015
- 校订：吴炜维

另有多个二级资源页报告：

- 明钞本
- 181 页
- 约 328MB

用户已明确：**此前已经提供过这份上海研易楼明抄本文件**。

因此原先“项目没有直接收到/读取该文件”的表述撤销。

当前事实应拆成两层：

- file provenance：`user_previously_provided_manuscript_file=True`
- current session retrieval：当前可检索附件/Library 索引未重新挂载该文件

所以现在不是“文件从未提供”，而是：

`pending_reinspection_from_previously_provided_file`

此外，用户确认这份扫描本**此前已经在本地术语库做过初步整理**。当前 GitHub 的 `terminology/` 只保留入口说明，本地 `terminology.json` 尚未迁移，因此旧术语抽取结果不在仓库树中。

这意味着后续应优先恢复“已有术语索引 → 明钞本页级来源”的对应关系，而不是重新从零做全文术语扫描。

在重新取回此前文件并定位附篇页之前，文昌九星仍保持 `catalog_attested_primary_text_pending`，不能只凭目录条目或旧术语词条生成正文规则。

## C. 北京大学馆藏线索

二级文章称另有北京大学馆藏本，但当前项目尚未找到：

- 北京大学图书馆官方目录记录；
- 可公开读取的数字化资源。

因此只登记：

`secondary_article_report_only`

不得升级为 verified holding。

## D. 《千顷堂书目》题名证据

历史书目存在《紫庭秘诀》题名，可证明同名著作曾有著录。

但该证据不能单独证明：

- 与现存研易楼本完全同书；
- 卷次一致；
- 附篇一致；
- 作者题署可靠。

因此只作为：

`title_attested_only`

## E. 文昌九星附篇当前定位

聚合状态：

`catalog_attested_primary_text_pending`

已知：

- 上海研易楼系整理本目录：有该附篇；
- 哈佛清抄汇编：有紫庭正文，但当前在线检索未定位该附篇；
- 北京大学：只有二级馆藏报道，未核官方目录；
- 因此仍不得生成文昌九星紫庭 `primary_result`。

下一动作：

1. 优先重新定位用户此前已经提供的研易楼明抄本文件，并直接校读“附太乙文昌九星值宫术”页；
2. 继续核哈佛抄本是否有异题同术；
3. 查北京大学官方馆藏目录。

## F. 传本隔离原则

固定：

- `canonical_manuscript_selected=None`
- `cross_witness_identity_assumed=False`

不同传本之间只能做：

- title comparison
- section comparison
- textual collation

不得自动互补缺页或附录。
