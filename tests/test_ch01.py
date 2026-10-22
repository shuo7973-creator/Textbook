"""独立手算基准与模型边界；不以测试通过声称真实市场有效。"""

import copy
import unittest

from labs.ch01_scenarios import evaluate, load_case, operating_cashflows, present_value


class CashflowTests(unittest.TestCase):
    def test_manual_first_year(self):
        row = {"year": 1, "revenue": 100, "ebit_margin": .15,
               "depreciation": 4, "capex": 6, "operating_nwc": 20}
        result = operating_cashflows([row], 18, .25)[0]
        self.assertAlmostEqual(result["ebit"], 15)
        self.assertAlmostEqual(result["nopat"], 11.25)
        self.assertAlmostEqual(result["delta_nwc"], 2)
        self.assertAlmostEqual(result["fcff"], 7.25)

    def test_working_capital_release(self):
        row = {"year": 1, "revenue": 100, "ebit_margin": .15,
               "depreciation": 4, "capex": 6, "operating_nwc": 16}
        self.assertAlmostEqual(operating_cashflows([row], 18, .25)[0]["fcff"], 11.25)

    def test_year_order_rejected(self):
        years = load_case()["scenarios"]["base"]["years"]
        with self.assertRaises(ValueError):
            operating_cashflows(list(reversed(years)), 18, .25)

    def test_tax_model_boundary(self):
        years = copy.deepcopy(load_case()["scenarios"]["base"]["years"])
        years[0]["ebit_margin"] = -.1
        with self.assertRaises(ValueError):
            operating_cashflows(years, 18, .25)
        with self.assertRaises(ValueError):
            operating_cashflows(years, 18, 1.2)

    def test_one_year_present_value(self):
        self.assertAlmostEqual(present_value([110], .1), 100)

    def test_recovery_paid_once_at_final_date(self):
        self.assertAlmostEqual(present_value([0, 0], .1, 121), 100)
        self.assertAlmostEqual(present_value([10, 20], 0, 50), 80)

    def test_invalid_discount_inputs(self):
        for rate in (-1, -2, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                present_value([1], rate)
        with self.assertRaises(ValueError):
            present_value([], .1)

    def test_base_hand_calculated_three_year_value(self):
        # 独立逐项手算的现金流，避免从待测函数生成期望值。
        expected = 7.25 / 1.1 + 8.375 / 1.21 + 49.4125 / 1.331
        self.assertAlmostEqual(evaluate(load_case(), "base")["operating_value"], expected)

    def test_hypothesis_and_equity_bridge(self):
        case = load_case()
        base = evaluate(case, "base")
        rate_only = evaluate(case, "base", .09)
        weak = evaluate(case, "weakness")
        self.assertGreater(rate_only["operating_value"], base["operating_value"])
        self.assertLess(weak["operating_value"], base["operating_value"])
        self.assertAlmostEqual(base["equity_value"], base["operating_value"] - 15)
        self.assertAlmostEqual(base["value_per_share"] * 10, base["equity_value"])

    def test_valid_rates_and_input_immutability(self):
        case = load_case()
        original = copy.deepcopy(case)
        values = [evaluate(case, "base", rate)["operating_value"] for rate in (.08, .1, .12)]
        self.assertGreater(values[0], values[1])
        self.assertGreater(values[1], values[2])
        self.assertEqual(case, original)

    def test_zero_shares_rejected(self):
        case = load_case()
        case["common"]["shares"] = 0
        with self.assertRaises(ValueError):
            evaluate(case, "base")


if __name__ == "__main__":
    unittest.main()
