"""Snapshot facade and reusable legacy engine methods.

This repository has no date-to-board calendar engine. Taiyi accepts an explicit
core snapshot; TaiyiCanonicalMixin can also be used by a calendar engine that
already supplies accnum. No calendar inputs are invented.
"""
import copy

from .four_taiyi import four_taiyi_position
from .taiyi_common import integer
from .taiyi_cycles import minister_base, people_base, ruler_base


class TaiyiCanonicalMixin:
    def kingbase(self, ji_style, taiyi_acumyear):
        return ruler_base(self.accnum(ji_style, taiyi_acumyear))["branch"]

    def officerbase(self, ji_style, taiyi_acumyear):
        return minister_base(self.accnum(ji_style, taiyi_acumyear))["branch"]

    def pplbase(self, ji_style, taiyi_acumyear):
        return people_base(self.accnum(ji_style, taiyi_acumyear))["branch"]

    def _four_position(self, name, ji_style, taiyi_acumyear, yuan=None):
        if yuan is None:
            yuan = getattr(self, "snapshot", {}).get("four_taiyi_yuan", 1)
        return four_taiyi_position(name, self.accnum(ji_style, taiyi_acumyear), yuan=yuan)["palace_id"]

    def skyyi(self, ji_style, taiyi_acumyear, *, yuan=None):
        return self._four_position("天乙", ji_style, taiyi_acumyear, yuan)

    def earthyi(self, ji_style, taiyi_acumyear, *, yuan=None):
        return self._four_position("地乙", ji_style, taiyi_acumyear, yuan)

    def fgd(self, ji_style, taiyi_acumyear, *, yuan=None):
        return self._four_position("四神", ji_style, taiyi_acumyear, yuan)

    def zhifu(self, ji_style, taiyi_acumyear, *, yuan=None):
        return self._four_position("直符", ji_style, taiyi_acumyear, yuan)

    def ming_kingbase(self, ji_style, taiyi_acumyear, *, yuan=None):
        """Confirmed ruler + heaven meeting fact; other narrative rules remain pending."""
        if yuan is None:
            yuan = getattr(self, "snapshot", {}).get("four_taiyi_yuan", 1)
        acc = self.accnum(ji_style, taiyi_acumyear)
        ruler = ruler_base(acc)
        heaven = four_taiyi_position("天乙", acc, yuan=yuan)
        return {"computable": True, "ruler_branch": ruler["branch"], "heaven_palace_id": heaven["palace_id"],
                "heaven_sector": heaven["sector"], "ruler_heaven_same_position": ruler["branch"] == heaven["sector"],
                "pending": ["本接口仅确认君基与天乙同位，不生成未审计的其它断语"]}


class Taiyi(TaiyiCanonicalMixin):
    """Explicit snapshot facade; not a substitute for a date-to-board engine."""

    def __init__(self, snapshot, *, legacy_snapshot=None):
        if not isinstance(snapshot, dict):
            raise TypeError("snapshot须为dict")
        self.snapshot = copy.deepcopy(snapshot)
        self.legacy_snapshot = copy.deepcopy(legacy_snapshot or {})

    def accnum(self, ji_style, taiyi_acumyear):
        self._validate_selection(ji_style, taiyi_acumyear)
        return self.snapshot["accumulated_year"]

    def _validate_selection(self, ji_style, taiyi_acumyear):
        integer(ji_style, 0, 4)
        integer(taiyi_acumyear, 0, 3)
        for name, requested in (("ji_style", ji_style), ("taiyi_acumyear", taiyi_acumyear)):
            if name in self.snapshot and self.snapshot[name] != requested:
                raise ValueError(f"snapshot的{name}与请求不符")

    def pan(self, ji_style, taiyi_acumyear, enable_game_theory=False, *, scenario=None):
        """Retain positional selection arguments and append canonical v2 to flat output."""
        from .pan_v2 import build_pan_v2_from_snapshot

        snapshot = copy.deepcopy(self.snapshot)
        self._validate_selection(ji_style, taiyi_acumyear)
        snapshot.update(ji_style=ji_style, taiyi_acumyear=taiyi_acumyear)
        v2 = build_pan_v2_from_snapshot(snapshot, scenario=scenario)
        result = project_legacy_pan(self.legacy_snapshot, v2)
        result["v2"] = v2
        if enable_game_theory:
            from .game_theory import build_game_theory_feature_bundle
            features = build_game_theory_feature_bundle(
                seven_methods=v2["analysis"]["seven_methods"],
                taiyi_palace=snapshot.get("taiyi_palace"), military=v2["analysis"]["military"],
            )
            result["運籌博弈分析"] = features
            result["v2"]["modern"]["game_theory"] = features
        return result


def project_legacy_pan(legacy_snapshot, v2):
    """Display projection only; old keys and complete containers come from canonical facts."""
    result = copy.deepcopy(legacy_snapshot)
    board, cycles = v2["board"], v2["cycles"]
    if board["taiyi"]["computable"]:
        result["太乙落宮"] = board["taiyi"]["palace_id"]
        result["太乙"] = board["taiyi"]["sector"] or "中"
    for name, role in (("主算", "home"), ("客算", "away"), ("定算", "fixed")):
        fact = board["calculations"][role]
        if fact["computable"]:
            result[name] = [fact["value"], list(fact["classic_tags"])]
    for name, role in (("文昌", "skyeyes"), ("始擊", "shiji"), ("定目", "dingmu")):
        fact = board["eyes"][role]
        if fact["computable"]:
            result[name] = [fact["sector"], fact["god"]] if name == "文昌" else fact["sector"]
    for name, role in (("主將", "home_general"), ("主參", "home_assistant"), ("客將", "away_general"), ("客參", "away_assistant")):
        fact = board["generals"][role]
        if fact["computable"]:
            result[name] = fact["palace_id"]
    for name, role in (("君基", "ruler"), ("臣基", "minister"), ("民基", "people")):
        fact = cycles["three_bases"][role]
        if fact["computable"]:
            result[name] = fact["branch"]
    for name, role in (("五福", "five_blessings"), ("大游", "big_wander"), ("小游", "small_wander")):
        fact = cycles[role]
        if fact["computable"]:
            if isinstance(result.get(name), dict):
                value = copy.deepcopy(result[name])
                value.update(fact)
                for alias in ("宫", "宮"):
                    if alias in value:
                        value[alias] = fact["palace_id"]
                result[name] = value
            else:
                result[name] = fact["palace_id"]
    for name, fact in cycles["four_taiyi"].items():
        if isinstance(fact, dict) and fact.get("computable"):
            result[name] = fact["palace_id"]
    return result


def collect_core_snapshot(engine, ji_style, taiyi_acumyear):
    """Calendar-engine adapter; each primitive board method is called once per style."""
    acc = engine.accnum(ji_style, taiyi_acumyear)
    taiyi = engine.ty(ji_style, taiyi_acumyear)
    data = {"accumulated_year": acc, "taiyi_palace": taiyi,
            "year_accumulated_year": acc if ji_style == 0 else engine.accnum(0, taiyi_acumyear),
            "day_taiyi_palace": taiyi if ji_style == 2 else engine.ty(2, taiyi_acumyear),
            "ji_style": ji_style, "taiyi_acumyear": taiyi_acumyear}
    methods = {"wenchang_sector": "skyeyes", "shiji_sector": "sf", "dingmu_sector": "se",
               "home_cal": "home_cal", "away_cal": "away_cal", "fixed_cal": "set_cal",
               "home_general": "home_general", "home_assistant": "home_vgen",
               "away_general": "away_general", "away_assistant": "away_vgen"}
    for field, method in methods.items():
        data[field] = getattr(engine, method)(ji_style, taiyi_acumyear)
    return data
