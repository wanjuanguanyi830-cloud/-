# C37 五运六气 / 五音之数验证报告

日期：2026-10-05

验证：

1. 十干五运映射。
2. 十二支六气与在泉对宫。
3. 卷三 profile 不计算卷十岁会/天符。
4. 卷十 profile 的岁会关系保持 pending。
5. 五音之数 1..10 映射与 D8-03 一致。
6. 15 仍按尾数5为羽，不受三才缺人影响。
7. 明确 `number_subject_rule_d8_08_used=False`。
8. 旧五运六气仅有卷三 profile 时 replacement gap 仍存在。
9. 卷三+卷十 profile 齐备后五运六气 gap 清除。
10. 五音只需卷三 profile。
11. C30 contract 接受 `wuyun_wuyin` 独立槽。

完整 CI：

```
705 passed in 1.15s
```
