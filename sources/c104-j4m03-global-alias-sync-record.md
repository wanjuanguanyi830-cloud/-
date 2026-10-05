# C104 J4M-03 与公共十六神 alias 单一真源

日期：2026-10-05

## 目标

C102 已把“太蔟 -> 太簇”加入公共 GOD_ALIASES。

此前 J4M-03 runtime 仍保留一份本地映射：

太蔟 -> 太簇

虽然值相同，但长期存在两处独立写死 canonical 值的漂移风险。

## 本轮处理

J4M-03 仍保留 source-specific alias 表，只暴露本条实际需要保存的来源异写“太蔟”。

但 canonical 值不再独立写死，而改为读取：

GOD_ALIASES["太蔟"]

因此：

- 公共 canonical 真源：src/kintaiyi/taiyi_rules.py::GOD_ALIASES
- J4M-03：保存来源作用域与输出 metadata
- terminology/jinjing-v4-aliases.json：保存来源、辞书和底本证据
- terminology/sixteen_spirits.json：保存全局十六神 canonical/alias 目录

## 为什么不直接把所有 GOD_ALIASES 引入 J4M-03

本轮不扩大 J4M-03 的 source-specific 输入语义。

也就是说：

- 太蔟是 J4M-03 已有直接底本证据的异写；
- 其他公共繁体/异写是否作为 J4M-03 来源字形，需要各自来源证据；
- 不因为公共层能归一，就自动宣称每一种 alias 都出现在本条古籍。

因此采用“canonical 单一真源 + source alias 窄作用域”的结构。

## 测试

tests/test_c104_j4m03_global_alias_sync.py 锁定：

- GOD_ALIASES["太蔟"] == 太簇
- j4m03_eye_element_from_god("太蔟") == 金
- J4M-03 输出保留 guest_eye_god=太蔟
- guest_eye_god_canonical 与公共 GOD_ALIASES 完全一致

## 规则不变

本轮不改变：

- J4M-03 五行关系；
- winner 判法；
- 主客目定义；
- 四库来源 profile；
- 太簇的酉位和金五行。
