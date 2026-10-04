# C49 太游 / 小游行宫卦不同术验证

日期：2026-10-05

验证：

1. 太游36年一内卦。
2. 小游24年一内卦。
3. 太游rate_symbol=乾天之策。
4. 小游rate_symbol=坤地之策。
5. 乾/坤策义不限制实际行卦。
6. canonical区别不依赖当前内卦!=。
7. 找到当前同卦年份时，systems_still_distinct仍为True。
8. 找到当前异卦年份时，也只标derived observation。
9. C38输入须为C38-BL-INNER。
10. C47输入须为C47-XY-INNER。
11. 36/24周期被篡改时拒绝。
12. 旧zonghe布尔比较canonical_equivalent=False。
13. 不把整个卷九综合wrapper标为已迁移。

完整 CI：

```
927 passed in 1.57s
```
