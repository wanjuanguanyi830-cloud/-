# C1–C7 validation — 2026-10-05

## Repository and source boundary

- 唯一目标：`https://github.com/wanjuanguanyi830-cloud/-`，默认分支 main。
- 直接按本次自包含规格执行，未调用聊天读取工具。
- 初始同步 main：`7677f8316052b65cb659eb8d616a23e77e0e8f0d`。
- 为保存并行更新，随后合入 main `54e2a26fd73b0e515332c68920423b7d4d2593f1` 的 C12–C17／J4M 内容。
- 参考仓库仅核接口与年积年 adapter，未写入参考仓库；没有增加生产依赖。

## Checks actually run

| 批次 | 全套 pytest |
|---|---:|
| 基线修复 | 249 passed |
| C1 | 307 passed |
| C2 | 324 passed |
| C3 | 329 passed |
| C4 | 353 passed |
| C5 | 361 passed |
| C6 | 365 passed |
| C7 | 376 passed |
| 合入并行更新后 | 440 passed |
| JSON key 冲突及选择参数回归 | 442 passed |

本机测试运行于 Python 3.12；最后一次全套测试 442 passed，两个 warning 是旧 returnarmy 单参数调用的预期 DeprecationWarning。没有将15算正确规则改回旧错误。

`python -m ruff check src config.py` 通过。所有20个 src／config Python 文件用 `ast.parse(feature_version=(3,10))` 检查语法通过。构建零生产依赖 wheel，并在仓库外安装后导入公共核心、四太乙、config、Taiyi，检查资源记录、结构化缺输入和 JSON 序列化通过。

CI 已配置 Python 3.10／3.12 矩阵、pytest 与源码 ruff。该配置不等于已完成这两个版本的远程运行；实际远程状态以 GitHub Actions 为准。

## Mandatory coverage

- 十六辰／十六神、九宫元数据、全16项大神映射／8项九宫映射、中五拒绝、25格五态、火十二长生、双五行及双坐标对冲。
- 八占全1..40古典集合、5/15/25/35结构缺人、五音正比、显式孤单集合、固定八内八外、基本多少与阴阳厄独立。
- 七术古例、四将Mode B、死亡风险不误用休囚、白龙direct_conflict分层、中五单边不可算、缺事件不借当前盘。
- 三基边界及3个古例、五福边界／阶段／末位所主／五域、大小游完整周期与天目18、大游profile盈差只加一次、小游天祐元年例。
- 四太乙十二宫／三元起宫／3个古例、无伪造phase、六同宫pair不投影九宫、五福同域、来源未覆盖返回pending。
- legacy keys／类型适配、config动态25格、D8-03与D8-08分离、旧中文盘与v2同源、scenario／日计太乙／年计积年、JSON与无输入报告。

## Material limitations

目标仓库没有原版日期排盘类或 Streamlit／CLI 应用。本次新增的是 **snapshot Taiyi facade**、canonical builder、collector 与可供原日期引擎复用的 mixin；没有声称移植参考项目日期构造器。完整日期排盘接入、jieqi季节八态、ming_pplbase来源审计与未确认古籍卷页仍待后续输入／审计。已有C8+实现保留，本批不扩张其来源范围。
