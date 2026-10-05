# 福应经 / 统宗军事并列 source-profile 术语记录

## 一、《景祐太乙福应经》卷四

稳定目录：

- terminology/military-jingyou-v4.json

规则：

- JF4M-01..11 全部保留为 source_record_only；
- 当前无独立 runtime；
- 不得调用 J4M 平行 runtime 作为替代；
- cross_source_merge = false。

尾部编号必须注意：

- JF4M-10 = 风云飞鸟，平行 J4M-11；
- JF4M-11 = 奇伏，平行 J4M-10；
- J4M-12 对阵云气没有直接 JF4M 对应条。

高风险差异：

- JF4M-06 方向表有 3/7/8，无 5；
- JF4M-09 地内含 1 宫；
- JF4M-10 主人刑 / 客刑败方与金镜存在读法差异；
- JF4M-11 作“奇兵必从大杀之地”，不得改写为金镜句。

## 二、《太乙统宗宝鉴》卷十五 / 卷十七

稳定目录：

- terminology/military-tongzong-v15-v17.json

来源 rule-unit 真源：

- src/kintaiyi/military_rule_units.py

卷十五：

- V15-01..14

卷十七：

- V17-01..11

跨卷 helper：

- V17-D1

当前 source-specific runtime 共20条：

卷十五：
- V15-02 五阵置旗
- V15-03 出兵称神
- V15-04 陈兵出乡
- V15-05 选将
- V15-06 教兵
- V15-09 五音考风
- V15-10 五音观风察将
- V15-12 风从八卦
- V15-13 云气逆顺

卷十七：
- V17-01..11 全部已有 C26/C27/C28 source-specific runtime

仍为 source_rule_catalog_only：
- V15-01 奇兵伏兵
- V15-07 随地制变
- V15-08 分合用兵
- V15-11 安营置阵
- V15-14 军势胜负

另有 derived runtime：
- V17-D1：C32 `cross_volume_helpers.build_guxu_cross_volume_helper`

V17-D1 不是卷十七 canonical source rule。

注意：

reference_function 仅记录旧综合层函数名；是否现行独立 runtime 以 terminology 中的 implementation_status/runtime 与 C23-C28 catalog 为准。

## 三、与《金镜》/C8 的边界

- V15-01 奇兵伏兵 != J4M-10 奇伏；
- V15-04 陈兵出乡 != J4M-06 陈兵向背；
- V15-07 随地制变与 J4M-07/J4M-08 只做近名 crosswalk；
- V15-14 军势胜负不得覆盖 J4M-11/J4M-12 外部观测；
- V17-01 出兵用时不是 J4M-05 出师法；
- V17-02 敌国动静不是 C8-L3；
- V17-D1 是卷五内外占攻击 × V17-09 求索所得的 derived helper，不是卷十七原法。

## 四、卷次说明

当前项目明确可结构化的是：

- 《福应经》卷四；
- 《金镜》卷四；
- 《统宗》卷十五 / 卷十七。

P0 source_profiles 中仍有 tongzong_volume5 作为历史并列来源容器，但当前没有一套可等同于 J4M/JF4M 的“卷五完整十二法 ruleset”。

因此严禁为了对称性人工制造“统宗卷五 J4M 对照表”。
