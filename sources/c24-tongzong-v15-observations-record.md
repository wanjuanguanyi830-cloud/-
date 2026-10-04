# C24 卷十五外部风云观测规则

## 实现

- V15-09 五音风
- V15-12 风从八卦
- V15-13 云气逆顺

新增 `src/kintaiyi/tongzong_v15_observations.py`。

## 总原则

三条都依赖现实观测：

- 风向支
- 风起八卦宫
- 云气来向

缺少观测值时统一：

`status=not_computable`

不得从日期、盘面、太乙宫或其他字段虚构实际风云。

## V15-09 五音风

地支五音：

- 子午 → 宫土
- 丑寅未申 → 徵火
- 卯酉 → 羽水
- 辰戌 → 商金
- 巳亥 → 角木

结构化五行关系：

- wind_parent_of_day
- wind_child_of_day
- day_controls_wind
- wind_controls_day
- same_element

原文明示母来翼子、子来扶母可见成功，因此这两类保留 direct_effect。

控制关系不自动生成主客 winner；避免把某一例局的“客先起大胜”无条件推广。

辰戌商风“鬼风”只在原文明确例型（角木日受商金克）下标 exact example match，不作无限推广。

## V15-12 风从八卦

只有显式 `wind_palace` 才解释：

- 乾/坎/艮 → 利客、客宜先举
- 震/巽/离 → 利主、主宜后应
- 兑 → 客有伏兵，主宜设备
- 坤 → 当前OCR文字有讹，保留 source_text_uncertain

中五不是八卦风向，不参与。

## V15-13 云气逆顺

旧代码用“数字差5”近似冲算，C24 已取消。

改用来源语义：

- 云从所得算方向来 → 顺
- 云从所得算对冲方向来 → 逆
- 其他方向 → 不应

显式输入改为：

`cloud_from_direction`

主算和客算分别判断，不自动压成一个总胜负。
