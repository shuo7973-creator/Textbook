"""第6—10章：独立有理数基准、资源守恒与模型失效边界。"""

from contextlib import redirect_stdout
from decimal import Decimal
from fractions import Fraction as F
import io
import math
from pathlib import Path
import runpy
import unittest

ROOT=Path(__file__).resolve().parents[1]


class MacroTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            cls.lab={n:runpy.run_path(str(ROOT/'labs'/f'ch{n:02d}.py')) for n in range(6,11)}

    def test_price_quantity_independent_rationals(self):
        result=self.lab[6]['price_quantity']([2,5],[10,4],[3,6],[12,5])
        expected={'ql':F(49,40),'qp':F(11,9),'pl':F(27,20),'pp':F(66,49)}
        for key,value in expected.items():
            self.assertAlmostEqual(result[key],float(value))
        self.assertAlmostEqual(result['qf']*result['pf'],float(F(33,20)))

    def test_price_contract_rejects_truncated_zip(self):
        f=self.lab[6]['price_quantity']
        with self.assertRaises(ValueError):
            f([2,5],[10],[3,6],[12,5])
        with self.assertRaises(ValueError):
            f([math.nan],[10],[3],[12])

    def test_growth_contribution_zero_and_negative_base(self):
        f=self.lab[6]['contribution']
        zero=f({'C':60,'rest':40},{'C':64,'rest':36})
        self.assertIsNone(zero['rows']['C']['share'])
        self.assertAlmostEqual(zero['rows']['C']['pull'],.04)
        large=f({'C':60,'NX':-5,'rest':45},{'C':64,'NX':-6,'rest':44})
        self.assertEqual(large['rows']['C']['share'],2)
        self.assertIsNone(large['rows']['NX']['growth'])
        self.assertAlmostEqual(sum(v['pull'] for v in large['rows'].values()),large['growth'])

    def test_diffusion_is_direction_not_magnitude(self):
        f=self.lab[6]['diffusion']
        self.assertAlmostEqual(f(.4,.35,.25),57.5)
        self.assertEqual(f(0,1,0),50)
        with self.assertRaises(ValueError):
            f(.4,.35,.35)

    def test_solow_exact_discrete_denominator(self):
        f=self.lab[7]['steady']; step=self.lab[7]['solow_step']
        result=f(s=.3,delta=.05,n=.01,g=.02)
        D=F(1,20)+F(1,100)+F(1,50)+F(1,5000)
        self.assertEqual(D,F(401,5000))
        self.assertAlmostEqual(result['D'],float(D))
        self.assertAlmostEqual(result['k'],float((F(3,10)/D)**2))
        self.assertAlmostEqual(step(result['k'],s=.3,delta=.05,n=.01,g=.02),result['k'])

    def test_solow_transition_and_zero_boundary(self):
        step=self.lab[7]['solow_step']
        self.assertAlmostEqual(step(4,s=.3),4.2)
        self.assertEqual(step(0),0)
        low,high=1.,9.
        for _ in range(100):
            next_low,next_high=step(low),step(high)
            self.assertLess(low,next_low); self.assertLess(next_low,4)
            self.assertGreater(high,next_high); self.assertGreater(next_high,4)
            low,high=next_low,next_high
        self.assertAlmostEqual(self.lab[7]['steady']()['half_life'],13.513407333964874)

    def test_solow_invalid_positive_steady_state(self):
        for kwargs in ({'delta':0,'n':0,'g':0},{'n':-.2,'delta':.1},{'s':math.nan},{'alpha':1}):
            with self.assertRaises(ValueError):
                self.lab[7]['steady'](**kwargs)

    def test_growth_accounting_log_and_ordinary_rates(self):
        result=self.lab[7]['growth_residual'](.05,.06,.01,.4)
        independent_log=math.log(1.05)-.4*math.log(1.06)-.6*math.log(1.01)
        self.assertAlmostEqual(math.log1p(result['exact']),independent_log)
        self.assertAlmostEqual(result['exact'],.019704013567388712)
        self.assertAlmostEqual(result['linear'],.02)

    def test_is_lm_independent_two_equation_solution(self):
        # Cramer求解 .4Y+200i=68 与 .5Y-400i=40，独立于待测闭式代码。
        a,b,c,d=F(2,5),F(200),F(1,2),F(-400)
        u,v=F(68),F(40); det=a*d-b*c
        Y=(u*d-b*v)/det; rate=(a*v-u*c)/det
        result=self.lab[8]['equilibrium']()
        self.assertEqual(Y,F(1760,13)); self.assertEqual(rate,F(9,130))
        self.assertAlmostEqual(result['Y'],float(Y))
        self.assertAlmostEqual(result['rate'],float(rate))
        self.assertAlmostEqual(result['C']+result['I']+result['G'],float(Y))
        self.assertAlmostEqual(.5*result['Y']-400*result['rate'],40)

    def test_policy_closure_and_credit_spread(self):
        f=self.lab[8]['equilibrium']; base=f()
        fixed=f(G=26.5)
        args=dict(mode='rule',target_rate=base['rate'],anchor_y=base['Y'])
        pegged=f(G=26.5,**args); reactive=f(G=26.5,phi=.001,**args)
        self.assertAlmostEqual(fixed['Y']-base['Y'],10)
        self.assertAlmostEqual(pegged['Y']-base['Y'],16.25)
        self.assertAlmostEqual(reactive['Y']-base['Y'],float(F(65,6)))
        self.assertAlmostEqual(pegged['money']-base['money'],8.125)
        self.assertAlmostEqual(f(spread=.01,**args)['Y']-base['Y'],-5)

    def test_negative_gross_investment_is_not_relabelled(self):
        with self.assertRaises(ValueError):
            self.lab[8]['equilibrium'](c=.8,I0=30,b=1000,h=1000,money=20)
        with self.assertRaises(ValueError):
            self.lab[8]['equilibrium'](mode='rule')

    def test_demand_and_supply_residuals(self):
        f=self.lab[8]['gap_model']
        for demand,supply in ((4,0),(0,2),(1,-1)):
            result=f(demand=demand,supply=supply)
            y,p=result['output_gap_pp'],result['inflation_gap_pp']
            self.assertAlmostEqual(y,demand-2*p)
            self.assertAlmostEqual(p,.5*y+supply)
        self.assertEqual(f(supply=2)['output_gap_pp'],-2)

    def test_consumption_budget_and_euler_conditions(self):
        f=self.lab[9]['consumption']
        result=f(100,80,.1)
        self.assertAlmostEqual(result['c1'],float(F(950,11)))
        self.assertAlmostEqual(result['c2'],95)
        self.assertAlmostEqual(result['budget_residual'],0)
        self.assertAlmostEqual(result['euler_gap'],0)
        bound=f(20,100,borrowing_limit=10)
        self.assertEqual((bound['c1'],bound['c2']),(30,90))
        self.assertGreater(bound['euler_gap'],0)

    def test_income_response_changes_with_constraint(self):
        f=self.lab[9]['consumption']
        self.assertEqual(f(30,100)['c1']-f(20,100)['c1'],5)
        self.assertEqual(f(30,100,borrowing_limit=0)['c1']-f(20,100,borrowing_limit=0)['c1'],10)
        with self.assertRaises(ValueError):
            f(20,100,r=-1)
        with self.assertRaises(ValueError):
            f(20,100,borrowing_limit=-1)

    def test_user_cost_decimal_timing(self):
        f=self.lab[9]['user_cost']; result=f(100,.04,.06,.02)
        expected=Decimal('104')-Decimal('.94')*Decimal('102')
        self.assertEqual(expected,Decimal('8.12'))
        self.assertAlmostEqual(result['exact'],float(expected))
        self.assertAlmostEqual(result['exact']-result['approx'],.12)
        self.assertAlmostEqual(result['exact']+result['resale'],104)
        with self.assertRaises(ValueError):
            f(100,.01,.01,.5)

    def test_orders_inventory_receivables_conservation(self):
        f=self.lab[9]['order_bridge']
        result=f(30,100,10,80,20,90,2,.75,20,10)
        self.assertEqual(result,dict(backlog=40,stock=30,revenue=160,cash=50,ar=130))
        self.assertEqual(20+result['revenue']-result['cash'],result['ar'])
        with self.assertRaises(ValueError):
            f(30,100,10,121,20,90,2,.75,20,10)

    def test_national_saving_and_position_bridge(self):
        accounts=self.lab[10]['national_accounts'](1000,600,150,200,-10,5)
        self.assertEqual((accounts['nx'],accounts['ca'],accounts['savings']),(50,45,245))
        position=self.lab[10]['external_bridge'](45,1,54,8,100,-8,2)
        self.assertEqual(position['nfa1'],140)
        self.assertEqual(position['errors'],0)

    def test_bop_sign_and_omission_convention(self):
        result=self.lab[10]['external_bridge'](28,2,40,8,100)
        self.assertEqual((result['fa_out'],result['fa_credit'],result['errors']),(32,-32,2))
        self.assertEqual(result['bop_residual'],0)

    def test_real_fx_and_net_cash_exposure(self):
        f=self.lab[10]['real_fx_change']
        self.assertAlmostEqual(f(1,1.04,1,1.03,1,1.01),float(F(51,2575)))
        settlement=self.lab[10]['settlement']
        self.assertAlmostEqual(settlement(90,60,7.35)-settlement(100,60,7),-59.5)
        self.assertAlmostEqual(settlement(90,60,7.35,debt=10,forward_amount=10,forward_rate=7.1),144.5)
        with self.assertRaises(ValueError):
            settlement(90,60,7.35,debt=10,forward_amount=21,forward_rate=7.1)


if __name__=='__main__':
    unittest.main()
