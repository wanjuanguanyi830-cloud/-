# 2026-10-05 C18 《太乙紫庭经》主来源 / 统宗参校

- 太乙九星、文昌九星、文昌变化、始击变化改为《太乙紫庭经》主要参考。
- 三旗行宫、九宫贵神改为《太乙紫庭经》主要参考。
- 《太乙统宗宝鉴》卷六/卷十保留为重要参校来源，不弃用。
- 参校用于校异、补证、版本对读，不得静默覆盖主来源。
- 新增 `src/kintaiyi/zitingjing_sources.py`。
- 六项旧 flat 字段改为 quarantined，replacement 必须指向对应《太乙紫庭经》 `primary_result`。
- 只有统宗参校结果时，C13 replacement gap 仍然存在。
- 主来源与参校结果可并列保存，`cross_source_merge=False`。
- 新增 `tests/test_zitingjing_sources.py`。
