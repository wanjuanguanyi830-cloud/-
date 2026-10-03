"""Mixin for hosts that need the historical ``Taiyi.shi_geju`` shape."""

from __future__ import annotations

from .engine import GejuContext, analyze_geju, to_legacy_dict


class TaiyiGejuMixin:
    """Expose ``shi_geju`` and ``shi_geju_detail`` on a host board class.

    A host class must implement ``_jinjing_geju_context`` to adapt its own
    board fields to the source-limited rule module. This mixin deliberately
    does not import or depend on the reference ``kintaiyi`` package.
    """

    def _jinjing_geju_context(self, ji_style: int, taiyi_acumyear: int) -> GejuContext:
        raise NotImplementedError("host must map its chart fields to GejuContext")

    def shi_geju_detail(self, ji_style: int, taiyi_acumyear: int) -> dict:
        context = self._jinjing_geju_context(ji_style, taiyi_acumyear)
        return analyze_geju(context)

    def shi_geju(self, ji_style: int, taiyi_acumyear: int) -> dict[str, str]:
        return to_legacy_dict(self.shi_geju_detail(ji_style, taiyi_acumyear))
