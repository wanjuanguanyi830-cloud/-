import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def branch_at(rule, n):
    start_index = rule["order"].index(rule["start_position"])
    step = (n - 1) // rule["years_per_position"]
    return rule["order"][(start_index + step) % len(rule["order"])]


def palace_at(rule, n):
    step = ((n - 1) // rule["years_per_position"]) % len(rule["order"])
    order = rule["order"]
    return order[step]["nine_palace"] if isinstance(order[step], dict) else order[step]


class BaseMotionRuleTests(unittest.TestCase):
    def test_three_bases_starts_and_boundaries(self):
        rules = {item["id"]: item for item in load("rules/base_motion/three_bases.json")["rules"]}
        self.assertEqual([branch_at(rules[key], 1) for key in ("jun-ji", "chen-ji", "min-ji")], ["午", "午", "戌"])
        self.assertEqual(branch_at(rules["jun-ji"], 30), "午")
        self.assertEqual(branch_at(rules["jun-ji"], 31), "未")
        self.assertEqual(branch_at(rules["jun-ji"], 360), "巳")
        self.assertEqual(branch_at(rules["jun-ji"], 361), "午")
        self.assertEqual(branch_at(rules["chen-ji"], 3), "午")
        self.assertEqual(branch_at(rules["chen-ji"], 4), "未")
        self.assertEqual(branch_at(rules["chen-ji"], 36), "巳")
        self.assertEqual(branch_at(rules["chen-ji"], 37), "午")
        self.assertEqual(branch_at(rules["min-ji"], 1), "戌")
        self.assertEqual(branch_at(rules["min-ji"], 2), "亥")
        self.assertEqual(branch_at(rules["min-ji"], 12), "酉")
        self.assertEqual(branch_at(rules["min-ji"], 13), "戌")

    def test_five_blessings_45_and_225_year_boundaries(self):
        rule = load("rules/base_motion/five_blessings.json")
        self.assertEqual(palace_at(rule, 1), 1)
        self.assertEqual(palace_at(rule, 45), 1)
        self.assertEqual(palace_at(rule, 46), 3)
        self.assertEqual(palace_at(rule, 225), 5)
        self.assertEqual(palace_at(rule, 226), 1)

    def test_dayou_36_and_288_year_boundaries(self):
        rule = load("rules/dayou/dayou.json")
        self.assertEqual(palace_at(rule, 1), 7)
        self.assertEqual(palace_at(rule, 36), 7)
        self.assertEqual(palace_at(rule, 37), 8)
        self.assertEqual(palace_at(rule, 288), 6)
        self.assertEqual(palace_at(rule, 289), 7)
        self.assertNotIn(5, rule["order"])

    def test_xiaoyou_3_24_and_240_year_boundaries(self):
        rule = load("rules/xiaoyou/xiaoyou.json")
        self.assertEqual(palace_at(rule, 1), 1)
        self.assertEqual(palace_at(rule, 3), 1)
        self.assertEqual(palace_at(rule, 4), 2)
        self.assertEqual(palace_at(rule, 24), 9)
        self.assertEqual(palace_at(rule, 25), 1)
        self.assertEqual(palace_at(rule, 240), 9)
        self.assertEqual(palace_at(rule, 241), 1)
        self.assertNotIn(5, rule["order"])
        orbit = load("rules/xiaoyou/orbit_into_gua.json")
        self.assertEqual((orbit["hexagram_years"], orbit["line_years"]), (24, 4))
        self.assertIsNone(orbit["order"])

    def test_four_taiyi_three_year_boundaries(self):
        rule_set = load("rules/base_motion/four_taiyi.json")
        self.assertEqual([r["start_running_palace"] for r in rule_set["rules"]], [1, 6, 9, 5])
        for rule in rule_set["rules"]:
            start = rule["start_running_palace"]
            self.assertEqual(((start - 1 + (3 - 1) // 3) % 12) + 1, start)
            self.assertEqual(((start - 1 + (4 - 1) // 3) % 12) + 1, start % 12 + 1)
            self.assertEqual(((start - 1 + (36 - 1) // 3) % 12) + 1, ((start + 10) % 12) + 1)
            self.assertEqual(((start - 1 + (37 - 1) // 3) % 12) + 1, start)

    def test_running_palaces_and_nine_palaces_are_separate_and_complete(self):
        coordinates = load("terminology/palace_coordinates.json")
        self.assertEqual(len(coordinates["running_palaces"]), 12)
        self.assertEqual([p["running_palace"] for p in coordinates["running_palaces"]], list(range(1, 13)))
        specials = {p["running_palace"]: p["nine_palace"] for p in coordinates["running_palaces"] if p["running_palace"] >= 10}
        self.assertEqual(specials, {10: 2, 11: 6, 12: 4})
        spirits = load("terminology/sixteen_spirits.json")
        self.assertEqual(len(spirits["spirits"]), 16)
        self.assertEqual(next(a for a in spirits["aliases"] if a["alias"] == "大旲")["canonical_name"], "大炅")

    def test_dayou_tianmu_keeps_18_steps_and_open_216_variant(self):
        record = load("rules/dayou/tianmu.json")
        self.assertEqual(len(record["order"]), 18)
        marker = lambda entry: (entry["branch"], entry["spirit"], entry["nine_palace"])
        self.assertEqual(marker(record["order"][1]), marker(record["order"][2]))
        self.assertEqual(marker(record["order"][6]), marker(record["order"][7]))
        self.assertEqual(record["current_path_summary"]["金镜推法总数"], 72)
        self.assertTrue(any("216" in item["claim"] for item in record["variants"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
