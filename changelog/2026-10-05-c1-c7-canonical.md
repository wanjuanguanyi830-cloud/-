# C1–C7 canonical implementation

- 基于目标仓库 main 的真实结构，先修复 15 算旧测试与 JSON 八门键基线。
- C1 公共九宫／十六辰坐标、双五行、25格五态及显式有损投影。
- C2 八占显式古典集合、五音正比、D8-03/D8-08 独立。
- C3 七术统一结构、事件输入缺失报告、Mode A/B、特殊阶段及克战分层。
- C4 三基／五福／大小游一基周期；旧零基接口明确转换。
- C5 独立十二宫四太乙、六同宫组合及来源限制特殊层。
- C6 config facade 与三基／四太乙 mixin；既有中文展示 key 保留。
- C7 canonical snapshot builder、同源中文投影、scenario、显式日计／年计与 JSON。
- 目标仓库缺日期排盘引擎；新增 Taiyi 是 snapshot facade，外部日期类需接入 collector。未移植未核定的历法、民基断语或季节八态。
- 每批 pytest 已运行。最终 Python 3.10/3.12 CI 与源码 ruff 检查写入现有工作流；本机实际测试环境为 Python 3.12。
