# C70 文昌九星来源分离记录

## 结论

当前文昌九星可直接执行的规则归《太乙统宗宝鉴》卷六 NGJ 见证，规则号：

`C70-TONGZONG-WENCHANG-NINE-STARS`

研易楼藏《太乙紫庭祕訣》明钞本当前不再作为文昌九星 primary/pending 来源。

## 研易楼明钞本目录证据

用户重新提供研易楼藏《太乙紫庭祕訣》明钞本扫描件。

扫描目录页（PDF 第5–6页）连续列出卷一至卷十二及“后附”项目；当前目录中未见：

- 文昌九星
- 文昌九星值宫术
- 附太乙文昌九星值宫术

因此，不能把现代整理本目录中的“附太乙文昌九星值宮術”反推为研易楼原钞固有篇目。

本记录只据目录作“题名未见”的来源判断；不由目录缺项外推“所有可能相关正文绝对不存在”。

## 现代整理本边界

现代整理/出版本目录可见“附太乙文昌九星值宮術”。

当前处理：

- 只记为 modern edition appendix；
- provenance unresolved；
- “现代整理时收入《统宗》相关材料”属于合理来源假说，但未取得编辑说明或直接拼合证据前，不写成已证事实；
- 不把现代附篇题名写成研易楼明钞本 manuscript form/source section。

## C70 直接来源

《太乙统宗宝鉴》卷六 NGJ892411999009267118912：
“明文昌九宫所主分野术”。

当前稳定 profile：

- 文昌、玄凤、明维、阴德、招摇、华明、玄武、玄冥、维明；
- 30年一星；
- 270年小周；
- 2700年大周；
- 一宫文昌起，顺行九宫；
- 当前直事星再按所求年干建禄宫落宫/分野。

其他 CADAL / 《三才世纬》见证中的星名与10/30年异读继续作为独立 witness 保存，不覆盖 NGJ profile。

## 旧代码残留

旧 `kentang2017/kintaiyi/src/kintaiyi/config.py` 九星段明确注明来源为：

“太乙統宗寶鑑 卷六：太乙九星 + 文昌九星”。

因此旧代码中的：

文曲、玄鳳、明維、昭搖、立華、華明、玄武、玄冥、雄明

只能作为 prior workflow code residue / legacy audit，不能再称为研易楼明钞本逐字扫描结果。

## 仓库处理

- 稳定术语入口：`terminology/wenchang-nine-stars.json`
- C70 runtime：`kintaiyi.wenchang_nine_stars_tongzong.wenchang_nine_star_tongzong`
- `terminology/zitingjing.json` 只保留跨来源/现代附篇恢复指针
- 若以后发现另一研易楼原钞或异本直接存在该篇，新增独立 ziting witness/profile，不覆盖 C70
