"""Required v2 rule checks using only the Python standard library."""

import unittest

from kintaiyi import cycles, eight_divinations as d8, seven_methods as t7
from kintaiyi.pan_v2 import (
    build_pan_v2, calculation_board, general_board, same_four_taiyi_palace,
    same_nine_palace, same_sixteen_sector, same_wufu_domain, sector_board,
    taiyi_board,
)
from kintaiyi.taiyi_rules import (
    SIXTEEN, dashen_from_nine_palace, dashen_from_sector, qi_relation,
)


class TestCoordinatesAndFiveStates(unittest.TestCase):
    def test_all_sixteen_dashen_mappings(self):
        for index, sector in enumerate(SIXTEEN):
            with self.subTest(sector=sector):
                self.assertEqual(dashen_from_sector(sector), SIXTEEN[(index + 4) % 16])

    def test_all_eight_nine_palace_mappings(self):
        expected = {1: "艮", 2: "酉", 3: "巽", 4: "午",
                    6: "子", 7: "乾", 8: "卯", 9: "坤"}
        for palace, landing in expected.items():
            with self.subTest(palace=palace):
                self.assertEqual(dashen_from_nine_palace(palace), landing)
        with self.assertRaises(ValueError):
            dashen_from_nine_palace(5)

    def test_all_twenty_five_qi_relations(self):
        elements = ("木", "火", "土", "金", "水")
        expected = (
            ("旺", "休", "囚", "死", "相"),
            ("相", "旺", "休", "囚", "死"),
            ("死", "相", "旺", "休", "囚"),
            ("囚", "死", "相", "旺", "休"),
            ("休", "囚", "死", "相", "旺"),
        )
        for row, subject in enumerate(elements):
            for column, environment in enumerate(elements):
                with self.subTest(subject=subject, environment=environment):
                    self.assertEqual(qi_relation(subject, environment), expected[row][column])


class TestSevenMethods(unittest.TestCase):
    def test_lijin_four_step_chain(self):
        self.assertEqual(t7.lijin("甲子")["chain"], ["子", "卯", "午", "酉", "子"])

    def test_lion_corner_and_boundaries(self):
        data = t7.lion("甲戌")
        self.assertEqual(data["dashen"]["sector"], "丑")
        self.assertEqual(data["timing"]["corner_sector"], "艮")
        self.assertEqual(data["timing"]["year_number"], 18)
        self.assertEqual(data["timing"]["year"], "辛卯")
        for start, landing in (("丑", "辰"), ("未", "戌")):
            case = t7.lion(start)
            self.assertEqual(case["dashen"]["sector"], landing)
            self.assertEqual(case["dashen"]["sector_element"], "土")
            self.assertEqual(case["dashen"]["state"], "休")

    def test_cloud_mode_a_winners_and_center(self):
        data = t7.cloud(7, 3)
        self.assertEqual(data["home"]["dashen"]["sector"], "乾")
        self.assertEqual(data["home"]["dashen"]["state"], "囚")
        self.assertEqual(data["home"]["verdict"], "主败")
        self.assertEqual(data["away"]["dashen"]["sector"], "巽")
        self.assertEqual(data["away"]["dashen"]["state"], "相")
        self.assertEqual(data["away"]["verdict"], "客胜")
        blocked = t7.cloud(5, 3)
        self.assertFalse(blocked["computable"])
        self.assertFalse(blocked["home"]["computable"])
        self.assertEqual(blocked["home"]["classic_note"], "杜塞")

    def test_tiger_uses_enemy_camp_taiyi(self):
        data = t7.tiger(3)
        self.assertEqual(data["dashen"]["sector"], "巽")
        self.assertEqual(data["dashen"]["state"], "相")
        self.assertEqual(data["verdict"], "不可攻")
        self.assertFalse(t7.tiger(5)["computable"])

    def test_leigong_mode_b_uses_palace_element(self):
        data = t7.leigong(6, 8, 2, 9, 6)
        self.assertEqual(data["environment"]["sector"], "子")
        self.assertEqual(data["environment"]["sector_element"], "水")
        generals = data["generals"]
        self.assertEqual(generals["home_general"]["palace_element"], "水")
        self.assertEqual(generals["home_general"]["intrinsic_element"], "金")
        self.assertEqual(generals["home_general"]["state"], "旺")
        self.assertEqual(generals["away_general"]["state"], "相")

    def test_dragon_separates_direct_conflict(self):
        data = t7.dragon(9, 6, None, 3, None)
        self.assertEqual(data["environment"]["sector"], "坤")
        self.assertEqual(data["generals"]["home_general"]["state"], "相")
        self.assertEqual(data["generals"]["away_general"]["state"], "旺")
        self.assertIn("home", data["direct_conflict"])
        self.assertEqual(data["generals"]["home_general"]["verdict"], "宜出军/下营")

    def test_returnarmy_requires_enemy_arrival_taiyi(self):
        data = t7.returnarmy(enemy_arrival_taiyi=2, home_general=6, away_general=9)
        self.assertEqual(data["environment"]["sector"], "酉")
        self.assertEqual(data["environment"]["sector_element"], "金")
        self.assertEqual(data["generals"]["away_general"]["state"], "死")
        self.assertEqual(data["enemy_verdict"], "无伏兵、自破、可攻")
        missing = t7.returnarmy(9)
        self.assertFalse(missing["computable"])
        self.assertIn("enemy_arrival_taiyi", missing["missing_inputs"])

    def test_required_inputs_report_structured_missing_values(self):
        for data in (t7.lijin(), t7.lion(), t7.cloud(), t7.tiger(),
                     t7.leigong(), t7.dragon()):
            self.assertFalse(data["computable"])
            self.assertTrue(data["missing_inputs"])
        self.assertFalse(t7.leigong(5)["computable"])
        self.assertFalse(t7.dragon(5)["computable"])


class TestEightDivinations(unittest.TestCase):
    def test_missing_inputs_are_structured(self):
        for data in (d8.sancai(), d8.calc_length(), d8.wuyin_from_calc(),
                     d8.gudan_state(), d8.attack_realm(), d8.suenwl(),
                     d8.tui_danger(), d8.calc_preparedness()):
            self.assertFalse(data["computable"])
            self.assertTrue(data["missing_inputs"])

    def test_sancai_structural_values_and_tags(self):
        expected = {
            5: (False, True, False),
            10: (True, False, False),
            15: (True, True, False),
            16: (True, True, True),
            25: (True, True, False),
            35: (True, True, False),
            40: (True, False, False),
        }
        for value, flags in expected.items():
            with self.subTest(value=value):
                data = d8.sancai(value)
                self.assertEqual(tuple(data["components"][k] for k in ("ten", "five", "one")), flags)
        self.assertIn("杜塞", d8.sancai(5)["classic_tags"])
        self.assertIn("三才俱足", d8.sancai(16)["classic_tags"])
        self.assertNotIn("三才俱足", d8.sancai(15)["classic_tags"])

    def test_length_and_wuyin(self):
        self.assertEqual(d8.calc_length(11)["length"], "长")
        self.assertEqual(d8.calc_length(10)["length"], "短")
        expected = {23: ("徵", "正音"), 15: ("羽", "正音"),
                    16: ("羽", "比音"), 39: ("角", "正音")}
        for value, (tone, tone_kind) in expected.items():
            data = d8.wuyin_from_calc(value)
            self.assertEqual((data["tone"], data["tone_kind"]), (tone, tone_kind))

    def test_gudan_explicit_sets(self):
        expected = {17: "重阳", 37: "重阳", 30: "孤阳", 40: "孤阴", 28: "重阴"}
        for value, state in expected.items():
            with self.subTest(value=value):
                self.assertEqual(d8.gudan_state(value)["state"], state)
        self.assertIsNone(d8.gudan_state(12)["state"])
        self.assertEqual(d8.gudan_state(25)["classic_tags"], ["杜塞"])

    def test_fixed_inner_outer_all_sixteen_gods(self):
        inner = set("阴德 大义 地主 阳德 和德 吕申 高丛 太阳".split())
        outer = set("大炅 大神 大威 天道 大武 武德 太簇 阴主".split())
        self.assertEqual(len(inner), 8)
        self.assertEqual(len(outer), 8)
        for god in inner | outer:
            expected_realm = "内" if god in inner else "外"
            with self.subTest(god=god):
                self.assertEqual(d8.attack_realm(god)["realm"], expected_realm)

    def test_amount_comparison_and_equal(self):
        self.assertEqual(d8.suenwl(20, 30)["winner"], "away")
        self.assertEqual(d8.suenwl(30, 20)["winner"], "home")
        equal = d8.suenwl(20, 20)
        self.assertIsNone(equal["winner"])
        self.assertEqual(equal["status"], "original_unclear")

    def test_yinyang_adversity_is_separate(self):
        self.assertEqual(d8.tui_danger(7, 33)["events"], [])
        self.assertEqual(d8.tui_danger(7, 26)["events"],
                         [{"side": "主", "state": "重阴", "danger": "厄水"}])

    def test_preparedness_roles(self):
        expected = {
            5: ["吏士"], 10: ["将军"], 15: ["将军", "吏士"],
            16: ["将军", "吏士", "兵卒"], 25: ["将军", "吏士"],
            35: ["将军", "吏士"], 40: ["将军"],
        }
        for value, roles in expected.items():
            with self.subTest(value=value):
                self.assertEqual(d8.calc_preparedness(value)["present"], roles)
        self.assertIn("十六以上皆具", d8.calc_preparedness(16)["source_note"])


class TestCyclesAndPanV2(unittest.TestCase):
    def test_five_blessings_boundaries(self):
        for boundary in (1, 45, 46, 90, 91, 135, 136, 180, 181, 225, 226):
            accumulated = (boundary - 250) % 225
            data = cycles.wufu(accumulated)
            expected_relative = 1 if boundary == 226 else boundary
            self.assertEqual(data["relative_year"], expected_relative)
        self.assertEqual(cycles.wufu(0, profile="source_115")["offset"], 115)

    def test_three_base_profiles_and_1_based_formula(self):
        data = cycles.three_bases(111)["bases"]
        self.assertEqual(data["jun_ji"]["sector"], "午")
        self.assertEqual(cycles.three_bases(4)["bases"]["chen_ji"]["sector"], "午")
        self.assertEqual(cycles.three_bases(12)["bases"]["min_ji"]["sector"], "未")
        self.assertEqual(data["jun_ji"]["stay_years"], 30)
        self.assertEqual(cycles.three_bases(4)["bases"]["chen_ji"]["stay_years"], 3)

    def test_big_and_small_wander_boundaries(self):
        for missing in (cycles.wufu(), cycles.bigyo(), cycles.bigyo_tianmu(),
                        cycles.three_bases(), cycles.smyo(), cycles.four_taiyi()):
            self.assertFalse(missing["computable"])
            self.assertTrue(missing["missing_inputs"])
        self.assertNotEqual(cycles.bigyo(0)["palace_id"], 5)
        example = cycles.smyo(10154821)
        self.assertEqual((example["relative_year"], example["palace_id"],
                          example["year_in_palace"], example["realm"]),
                         (13, 6, 1, "治天"))
        for boundary in (1, 36, 37, 72, 73, 108, 109, 144, 145, 180, 181, 216, 217, 252, 253, 288, 289):
            accumulated = (boundary - 34) % 288
            data = cycles.bigyo(accumulated)
            self.assertEqual(data["relative_year"], 1 if boundary == 289 else boundary)

    def test_dayou_tianmu_all_eighteen_steps(self):
        for step, god in enumerate(cycles.DAYOU_TM_PATH, 1):
            accumulated = (step - 214) % 18
            data = cycles.bigyo_tianmu(accumulated)
            self.assertEqual((data["step_number"], data["god"]), (step, god))
        self.assertEqual(cycles.bigyo_tianmu(0, profile="jinjing")["status"], "not_computable")

    def test_four_taiyi_twelve_palaces_and_sanyuan_shift(self):
        first = cycles.four_taiyi(1)["taiyi"]
        self.assertEqual({name: item["palace_id"] for name, item in first.items()},
                         {"四神": 1, "天乙": 6, "地乙": 9, "直符": 5})
        second_yuan = cycles.four_taiyi(61)["taiyi"]
        self.assertEqual({name: item["palace_id"] for name, item in second_yuan.items()},
                         {"四神": 9, "天乙": 2, "地乙": 5, "直符": 1})
        third_yuan = cycles.four_taiyi(121)["taiyi"]
        self.assertEqual({name: item["palace_id"] for name, item in third_yuan.items()},
                         {"四神": 5, "天乙": 10, "地乙": 1, "直符": 9})
        found = set()
        for year in range(1, 181):
            for record in cycles.four_taiyi(year)["taiyi"].values():
                self.assertIn(record["palace_id"], range(1, 13))
                if record["palace_id"] >= 10:
                    found.add((record["palace_id"], record["palace_name"], record["sector"]))
        self.assertIn((10, "绛宫", "巳"), found)
        self.assertIn((11, "明堂", "申"), found)
        self.assertIn((12, "玉堂", "寅"), found)

    def test_four_taiyi_pending_matrix_and_known_water_conflicts(self):
        matrix = cycles.four_taiyi_central_matrix(cycles.four_taiyi(1))
        self.assertEqual(len(matrix["pairs"]), 6)
        self.assertTrue(all(row["interpretation_status"] == "pending" for row in matrix["pairs"]))
        for sector, palace, state in (("辰", 5, "克贼"), ("戌", 9, "克贼"),
                                      ("丑", 7, "克贼"), ("未", 3, "克贼"),
                                      ("巳", 2, "战克"), ("午", 9, "战克")):
            self.assertEqual(cycles.four_god_water_conflict(sector, palace)["state"], state)
        self.assertEqual(cycles.four_god_water_conflict("辰", 4)["status"], "pending")

    def test_small_wander_interaction_requires_named_co_location(self):
        data = cycles.xiaoyou_suozhu(cycles.smyo(1), co_located=("君基", "民基"))
        self.assertEqual([item["effect"] for item in data["effects"]],
                         ["双君之象、争夺兵革", "兴兵役"])
        unresolved = cycles.xiaoyou_suozhu(cycles.smyo(1), co_located=("五福",))
        self.assertEqual(unresolved["effects"][0]["status"], "pending_virtue")
        self.assertEqual(cycles.wufu_interaction()["effects"][0]["status"], "pending_co_location")

    def test_pan_v2_and_coordinate_safe_comparisons(self):
        general = general_board("home_general", 8)
        self.assertEqual((general["intrinsic_element"], general["palace_element"]), ("金", "水"))
        self.assertEqual(calculation_board(16)["last_digit"], 6)
        self.assertTrue(calculation_board(16)["components"]["one"])
        taiyi = taiyi_board(1)
        sector = sector_board("乾")
        four = cycles.four_taiyi(1)["taiyi"]["天乙"]
        self.assertTrue(same_nine_palace(taiyi, taiyi_board(1)))
        self.assertTrue(same_sixteen_sector(sector, sector_board("乾")))
        self.assertIsNone(same_nine_palace(taiyi, four))
        self.assertTrue(same_four_taiyi_palace(four, four))
        self.assertTrue(same_wufu_domain(cycles.wufu(0), cycles.wufu(225)))

        pan = build_pan_v2(
            meta={"method": "project_canonical", "accumulated_year": 1},
            calendar={"gregorian": {"year": 2026}},
            board={"taiyi": taiyi},
            cycles={"five_blessings": cycles.wufu(1)},
            analysis={"eight_divinations": {"D8-01": d8.sancai(16)}},
            source_variants={"VAR-015": "six-to-eight canonical"},
            derived=[{"id": "DER-test"}], pending=["pending source note"],
            compat={"太乙": 3},
        )
        self.assertEqual(pan["schema_version"], "2.0")
        self.assertEqual(pan["compat"], {"太乙": 3})
        self.assertIn("source_variants", pan)
        self.assertEqual(pan["derived"], [{"id": "DER-test"}])
        self.assertEqual(pan["pending"], ["pending source note"])
        self.assertIn("seven_methods", pan["analysis"])
        self.assertIn("four_taiyi", pan["cycles"])
        self.assertIsNone(pan["calendar"]["branches"]["day"])
        self.assertIn("home_assistant", pan["board"]["generals"])
        self.assertIsNone(same_nine_palace({"palace_id": 1}, {"palace_id": 1}))


if __name__ == "__main__":
    unittest.main()
