# C19 《太乙紫庭经》主来源篇目索引与第一批 source facts

## 在线主来源入口

识典古籍：

- 《太乙紫庭經》书目入口：
  https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u3291
- 汇编目录：
  https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q452g7jm

目录在卷一连续列出：

- 太乙紫庭经表
- 太乙紫庭序
- 释九宫所值九星
- 释八门所直事
- 释九宫变化加临干支
- 太乙所临宫分
- 释天目变化
- 始击变化
- 释主客大小将所临
- 大小游等

因此 C19 把这部分与后续统宗卷十“明太乙九星所星术”等条目明确拆开。

## 六项定位状态

### 1. 太乙九星

主来源直接篇目已定位：

- 《太乙紫庭经》〈释九宫所值九星〉
- 识典：
  https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u4tgl

已可结构化的主来源事实：

- 天蓬：一宫，冀州，凶
- 天芮：二宫，荆州，凶
- 天冲：三宫，青州，凶
- 天辅：四宫，徐州，吉
- 天禽：五宫，豫州，吉
- 天心：六宫，雍州，吉
- 天柱：七宫，梁益州，凶
- 天任：八宫，兖州，吉
- 天英：九宫，扬州，凶

正文另明确九星配九宫、十年一易。

注意：本批只录静态 source facts，不直接采用旧统宗代码的大周900 / 小周90等算法。那套计算必须另做参校来源比对。

### 2. 文昌变化

主来源直接篇目已定位：

- 《太乙紫庭经》〈释天目变化〉
- 识典：
  https://www.shidianguji.com/zh/book/SDZJ0646/chapter/1kg32q85u5vdx

正文明确：

- 天目在地号文昌；
- 文昌与太乙同宫为囚；
- 前一宫为外迫；
- 后一宫为内迫；
- 与太乙相冲为对；
- 与始击同宫为二目相关，需结合旺相。

### 3. 文昌变化的重要异文

《太乙紫庭经》当前识典主来源文本：

- 主方组：1/8/3/7
- 客方组：4/9/6/2

统宗卷六参校摘录常见：

- 主方组：8/3/7
- 客方组：4/9/2/6

C19 固定记为：

`variant_requires_collation`

不得用统宗参校本静默删去主来源的一宫。

### 4. 始击变化

《太乙紫庭经》卷一目录已直接列：

- 始击变化

因此当前状态：

`toc_confirmed_primary_chapter`

但 C19 暂不把其他版本/统宗正文冒充成识典主来源直接页面，待直接页面定位后再结构化。

### 5. 文昌九星

已见《太乙紫庭秘诀》现代书目著录：

- “附太乙文昌九星值宫术”

但目前识典《太乙紫庭经》在线正文未直接定位该篇全文。

状态：

`bibliographic_anchor_only`

不得直接把旧统宗卷六函数升成主来源公式。

### 6. 三旗行宫 / 九宫贵神

项目来源策略仍以《太乙紫庭经》传统为主要参考，统宗卷十为重要参校。

但当前在线检索尚未找到二者在《太乙紫庭经》中的直接同名篇目，因此状态固定：

`pending_direct_primary_location`

在找到主来源正文前：

- 统宗卷十结果可放 collation_results；
- 不得形成 primary_result；
- 不得清除 C13 replacement gap。

## 代码

新增：

- `src/kintaiyi/zitingjing_primary_catalog.py`
- `src/kintaiyi/zitingjing_source_facts.py`
- `tests/test_zitingjing_primary_catalog.py`

## 原则

C19 是来源事实层，不是旧统宗算法翻版。

只有直接定位主来源正文后，才允许把规则推进到 primary_result。
