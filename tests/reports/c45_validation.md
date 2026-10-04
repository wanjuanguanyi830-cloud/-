# C45 岁中灾发月日之期验证

日期：2026-10-05

验证对象：

- `src/kintaiyi/volume9_disaster_timing.py`
- `tests/test_volume9_disaster_timing.py`

## 锁定边界

1. 在线见证卷十 / 项目旧卷九标签并存，不复制算法。
2. 第一阶段为“太岁合神加岁支 → 文昌、天目 → 灾发月及冲月”。
3. 第二阶段为“当月合神加月支 → 文昌、天目 → 日层期及冲处”。
4. 文昌临辰可映三月，冲戌映九月。
5. 文昌与天目均须显式提供；缺任一目标时该阶段不完整。
6. 四维位不擅自折成月份。
7. 日层四维落点保存为 point，不能冒充 branch。
8. 不伪造具体现代历法日期。
9. 文昌宫阴阳由上游显式提供，不使用 legacy `_YANG_GONG` 猜测。
10. 文昌同太乙 / 格掩迫击挟提只作年度不协/不稔证据，不改月期。
11. 无格局也须显式传空 list。
12. 月层完整而日层缺失时仅为 `partial_month_only`。
13. 只有月、日两阶段都完整才生成 legacy replacement。
14. 旧 `suizhong_zaifa` 不视为 canonical equivalent。

当前通过基线：

```
841 passed / 0 failed
```
