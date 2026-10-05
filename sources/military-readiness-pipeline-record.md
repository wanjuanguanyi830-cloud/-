# 三门—五将—出师资格链整合记录

## 规则标识

- `CORE-MILITARY-DEPLOYMENT-READINESS`
- runtime: `kintaiyi.military_readiness_pipeline.military_deployment_readiness`

## 目标

把此前孤立的事实串成单向依赖链：

`直使门 -> 八门空间盘 -> 三门具不具 -> J4M-02五将 -> 杜塞折算 -> J4M-05出师`

本层只做 orchestration，不把跨书补文写回任何 source-specific canonical。

## 三门 profile

### jinjing_strict

只使用四库《太乙金镜式经》卷四 J4M-01 明确给出的负面组合。

当动态八门盘出现太乙、天目都避开开休生时，《金镜》本段没有正面“门具”句，保持未知。

### tongzong_v5

使用《太乙统宗宝鉴》卷五明确补出的：

“太乙天目不在开、休、生三门之下，为门具”。

因此可在同一动态八门盘上得到明确 True。

## 五将

先由 J4M-02 只判三类原典阻断：

- 始击有掩击；
- 文昌有囚迫；
- 主客大小将有相关。

任一阻断明确成立即可直接判五将不发。

随后 CORE-WUJIANG-READY 再叠加项目已锁定的：

`5/15/25/35 -> 杜塞 -> 五将不发`

杜塞不伪装成J4M-02原文第四条件。

## 出师

J4M-05继续只消费：

- 当前算为12/22/32；
- 三门具；
- 有效五将发；
- 出军门为开/休/生。

缺任一明确前提则按J4M-05自身状态返回 hold / not_computable。
