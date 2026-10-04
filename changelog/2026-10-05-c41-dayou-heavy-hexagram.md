# 2026-10-05 C41 Dayou heavy hexagram

- 新增 `dayou_hexagram.py`。
- 实现卷九内外重卦结构。
- 固化四象策数：乾36、坤24、震坎艮28、巽离兑32。
- 实现内卦36年、六年一爻。
- 不生成未见直接条文的外卦动爻。
- 不调用 C38。
- +34 / +36610 / legacy +50 只作为 epoch variants 并列保存。
- runtime 不选择 epoch variant。
- 完整 CI：753 passed / 0 failed。
