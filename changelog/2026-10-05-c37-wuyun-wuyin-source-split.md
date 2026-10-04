# 2026-10-05 C37 Wuyun Wuyin source split

- 新增 `wuyun_wuyin_sources.py`。
- 卷三“统行五运六气”与卷十“岁会五运六气”分 profile。
- 五音之数修正为卷三独立来源。
- 五音算数核心复用 D8-03，禁止使用 D8-08。
- 旧五运六气只有卷三+卷十两 profile 均存在时才算 replacement 完成。
- C30 source_variants 新增 `wuyun_wuyin` 槽。
- 旧五运六气 / 五音之数改为 quarantine。
- 完整 CI：705 passed / 0 failed。
