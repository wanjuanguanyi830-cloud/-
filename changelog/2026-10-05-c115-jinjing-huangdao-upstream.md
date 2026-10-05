# C115 《金镜》卷一黄道日度 / 宿度 / 十二分野上游

日期：2026-10-05

新增：

- `src/kintaiyi/jinjing_huangdao_tables.py`
- `tests/test_c115_jinjing_huangdao_tables.py`
- `sources/c115-jinjing-huangdao-upstream-record.md`

实现：

- 二十四气黄道日度所在24项锚点；
- 二十八宿黄道度数表；
- 十二分野 / 地支映射；
- `term_day_position(term, day_number)` 日度推进 helper。

直接回归《金镜》“推太乙当时法”实例：

- 立冬第1日 = 房1；
- 立冬第5日 = 房5；
- 立冬第6日 = 心1。

边界：

- 四库公开转录“虚”宿度数存在缺字/分数歧义，C115 不据总周天或后世宿度表反推；
- 日度推进若必须跨越未定虚宿边界，返回 not_computable；
- 不在 C115 自动执行时支加位或六壬安天乙诸将。

C69 已同步：

- 日度上游改由 C115 提供；
- `complete_current_time_formula=False` 保持；
- 剩余核心缺口为时支加位与完整六壬式安将。
