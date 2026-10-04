"""Snapshot facade and reusable legacy engine methods.

This repository has no date-to-board calendar engine. Taiyi accepts an explicit
core snapshot; TaiyiCanonicalMixin can also be used by a calendar engine that
already supplies accnum. No calendar inputs are invented.
"""
import copy

from .four_taiyi import four_taiyi_position
from .taiyi_cycles import minister_base, people_base, ruler_base


class TaiyiCanonicalMixin:
    def kingbase(self, ji_style, taiyi_acumyear):
        return ruler_base(self.accnum(ji_style, taiyi_acumyear))["branch"]

    def officerbase(self, ji_style, taiyi_acumyear):
        return minister_base(self.accnum(ji_style, taiyi_acumyear))["branch"]

    def pplbase(self, ji_style, taiyi_acumyear):
        return people_base(self.accnum(ji_style, taiyi_acumyear))["branch"]

    def _four_position(self, name, ji_style, taiyi_acumyear, yuan=1):
        return four_taiyi_position(name, self.accnum(ji_style, taiyi_acumyear), yuan=yuan)["palace_id"]

    def skyyi(self, ji_style, taiyi_acumyear, *, yuan=1):
        return self._four_position("天乙", ji_style, taiyi_acumyear, yuan)

    def earthyi(self, ji_style, taiyi_acumyear, *, yuan=1):
        return self._four_position("地乙", ji_style, taiyi_acumyear, yuan)

    def fgd(self, ji_style, taiyi_acumyear, *, yuan=1):
        return self._four_position("四神", ji_style, taiyi_acumyear, yuan)

    def zhifu(self, ji_style, taiyi_acumyear, *, yuan=1):
        return self._four_position("直符", ji_style, taiyi_acumyear, yuan)


class Taiyi(TaiyiCanonicalMixin):
    """Explicit snapshot facade; not a substitute for a date-to-board engine."""

    def __init__(self, snapshot, *, legacy_snapshot=None):
        if not isinstance(snapshot, dict):
            raise TypeError("snapshot须为dict")
        self.snapshot = copy.deepcopy(snapshot)
        self.legacy_snapshot = copy.deepcopy(legacy_snapshot or {})

    def accnum(self, ji_style, taiyi_acumyear):
        for name, requested in (("ji_style", ji_style), ("taiyi_acumyear", taiyi_acumyear)):
            if name in self.snapshot and self.snapshot[name] != requested:
                raise ValueError(f"snapshot的{name}与请求不符")
        return self.snapshot["accumulated_year"]
