# Software Registry

registry/ 是供软件调用的总注册表，不是第四份规则正文。

- catalog.json：指向 terminology / rules / runtime / sources / schemas 的稳定入口。
- operations.json：允许软件直接调用的稳定计算 operation。

总注册表只保存指针和状态，不复制术语定义、算法公式或古籍证据。真实内容仍由各自目录负责。

Python 软件优先调用 kintaiyi.api，不要直接依赖内部模块文件名。
