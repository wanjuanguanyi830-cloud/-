"""太乙七术、八占、周期算法与结构化盘面v2。"""

RULESET_VERSION = "taiyi-t7-d8-v2"

from .pan_v2 import build_pan_v2, pan

__all__ = ["RULESET_VERSION", "build_pan_v2", "pan"]

