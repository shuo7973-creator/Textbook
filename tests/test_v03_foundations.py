"""独立算术基准与真实错误边界；不替代参考教材正文审校。"""

from contextlib import redirect_stdout
from decimal import Decimal
from fractions import Fraction
import copy
import io
import math
from pathlib import Path
import runpy
import unittest

from labs.ch01_scenarios import load_case, symmetric_attribution

ROOT = Path(__file__).resolve().parents[1]


class FoundationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            cls.lab = {n: runpy.run_path(str(ROOT / 'labs' / f'ch{n:02d}.py'))
                       for n in range(2, 6)}

    def test_value_corners_independent_decimal(self):
        result = symmetric_attribution(load_case())
        cash = [Decimal('7.25'), Decimal('8.375'), Decimal('49.4125')]
        expected = sum(c / Decimal('1.1')**t for t, c in enumerate(cash, 1))
        self.assertAlmostEqual(result['corners'][0], float(expected))
        self.assertAlmostEqual(result['interaction'], -.1133755212461196)
        self.assertAlmostEqual(result['rate'], 1.1625352445266337)
        self.assertAlmostEqual(result['operations'], -5.471037873320274)
        self.assertAlmostEqual(result['rate'] + result['operations'], result['total'])

    def test_attribution_zero_changes(self):
        case = load_case()
        self.assertAlmostEqual(symmetric_attribution(case, new_rate=.10)['rate'], 0)
        self.assertAlmostEqual(symmetric_attribution(case, new_scenario='base')['operations'], 0)

    def test_pit_cutoff_and_future_invariance(self):
        lab = self.lab[2]; rows = copy.deepcopy(lab['rows']); original = copy.deepcopy(rows)
        f = lab['asof']
        self.assertIsNone(f(rows, 'CY001', '2025H1', '2025-08-20T18:09:59+08:00'))
        selected = f(rows, 'CY001', '2025H1', '2025-08-20T18:10:00+08:00')
        self.assertEqual(selected['value'], 72)
        old = f(rows, 'CY001', '2024FY', lab['cutoff'])
        self.assertEqual(f(rows + [lab['future']], 'CY001', '2024FY', lab['cutoff']), old)
        self.assertEqual(rows, original)

    def test_pit_rejects_conflicting_keys_and_time(self):
        lab = self.lab[2]; rows = copy.deepcopy(lab['rows']); f = lab['asof']
        with self.assertRaises(ValueError):
            f(rows + [rows[0]], 'CY001', '2024FY', lab['cutoff'])
        conflict = dict(rows[2], version='v-conflict', value=999)
        with self.assertRaises(ValueError):
            f(rows + [conflict], 'CY001', '2024FY', lab['cutoff'])
        with self.assertRaises(ValueError):
            f(rows, 'CY001', '2024FY', '2025-09-01T09:00:00')

    def test_ttm_comparability_and_roles(self):
        lab = self.lab[2]; f = lab['ttm_from_selected']; selected = lab['selected']
        self.assertEqual(f(*selected), 142)
        self.assertIsNone(f(selected[0], None, selected[2]))
        with self.assertRaises(ValueError):
            f(lab['rows'][0], selected[1], selected[2])
        with self.assertRaises(ValueError):
            f(selected[0], selected[2], selected[1])

    def test_group_order_and_immutability(self):
        f = self.lab[3]['group_returns']
        records = [('B', '2025-01-02', 45), ('A', '2025-01-01', 100),
                   ('B', '2025-01-01', 50), ('A', '2025-01-02', 110)]
        original = copy.deepcopy(records)
        result = f(records)
        self.assertEqual(result, f(list(reversed(records))))
        self.assertEqual(records, original)
        self.assertAlmostEqual(result[0]['return'], .1)
        self.assertAlmostEqual(result[1]['return'], -.1)

    def test_missing_prices_break_chain_and_bad_values_fail(self):
        f = self.lab[3]['group_returns']
        records = [('A', '2025-01-01', 100), ('A', '2025-01-02', None),
                   ('A', '2025-01-03', 110)]
        self.assertEqual(f(records), [])
        for invalid in (0, -1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                f([('A', '2025-01-01', invalid)])
        with self.assertRaises(ValueError):
            f([records[0], records[0]])

    def test_window_excludes_unavailable_observation(self):
        f = self.lab[3]['past_mean']
        self.assertEqual(f([2, 4, 6, 99999], 3, 3), 4)
        self.assertIsNone(f([2, None, 6, 8], 3, 3))
        self.assertIsNone(f([2, 4, 6, 8], 3, 2))

    def test_training_scale_independent_benchmark(self):
        f = self.lab[3]['fit_scale']; center, scale = f([1, 2, 3])
        self.assertEqual(center, 2)
        self.assertAlmostEqual(scale**2, float(Fraction(2, 3)))
        self.assertAlmostEqual((10-center)/scale, 9.797958971132712)
        with self.assertRaises(ValueError):
            f([3, 3, 3])

    def test_ar1_variance_double_covariance_sum(self):
        # 与实现的单重滞后求和不同，直接逐对累加精确有理数协方差。
        n = 3; rho = Fraction(1, 2); variance = Fraction(4)
        expected = sum(variance*rho**abs(i-j) for i in range(n) for j in range(n))/n**2
        self.assertEqual(expected, Fraction(22, 9))
        self.assertAlmostEqual(self.lab[4]['mean_variance_ar1'](3, 2, .5), float(expected))

    def test_mean_and_prediction_interval_benchmarks(self):
        lab = self.lab[4]
        for actual, expected in zip(lab['mean_ci'], (-.014369528171525736, .05436952817152574)):
            self.assertAlmostEqual(actual, expected)
        for actual, expected in zip(lab['prediction'], (-.05685260134351498, .09685260134351498)):
            self.assertAlmostEqual(actual, expected)
        self.assertAlmostEqual(math.sqrt(lab['mean_variance_ar1'](40, .2, .6)), .06174544518)

    def test_ar1_invalid_inputs_and_block_boundaries(self):
        f = self.lab[4]['mean_variance_ar1']
        for args in [(0, .2, .5), (3, math.nan, .5), (3, math.inf, .5), (3, .2, 1)]:
            with self.assertRaises(ValueError):
                f(*args)
        bootstrap = self.lab[4]['circular_block_means']
        self.assertEqual(bootstrap([2, 2, 2], 2, 5, 7), [2]*5)
        self.assertEqual(bootstrap([1, 2, 9], 3, 5, 7), [4]*5)
        with self.assertRaises(ValueError):
            bootstrap([1, math.nan], 1, 5, 7)

    def test_ols_exact_small_sample(self):
        result = self.lab[5]['ols_one']([1, 2, 3], [2, 3, 5])
        for field, expected in [('alpha', Fraction(1, 3)), ('beta', Fraction(3, 2)),
                                ('sse', Fraction(1, 6)), ('s2', Fraction(1, 6))]:
            self.assertAlmostEqual(result[field], float(expected))
        self.assertAlmostEqual(result['se_beta']**2, float(Fraction(1, 12)))
        self.assertAlmostEqual(result['beta'] - 12.706*result['se_beta'], -2.1679062601616925)

    def test_omitted_variable_textbook_example(self):
        x, z, y = [1, 2, 3, 4], [1, 1, 2, 2], [4, 5, 8, 9]
        self.assertAlmostEqual(self.lab[5]['ols_one'](x, y)['beta'], 1.8)
        for actual, expected in zip(self.lab[5]['ols_two'](x, z, y), (1, 1, 2)):
            self.assertAlmostEqual(actual, expected)

    def test_unidentified_regressions_rejected(self):
        with self.assertRaises(ValueError):
            self.lab[5]['ols_one']([1, 1, 1], [2, 3, 5])
        with self.assertRaises(ValueError):
            self.lab[5]['ols_two']([1, 2, 3], [2, 4, 6], [2, 3, 5])


if __name__ == '__main__':
    unittest.main()
