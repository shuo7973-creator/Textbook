"""第11—15章独立现金流、账本守恒和错误边界检查。"""

from contextlib import redirect_stdout
from fractions import Fraction as F
import io
import math
from pathlib import Path
import runpy
import unittest

ROOT=Path(__file__).resolve().parents[1]


class MoneyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            cls.lab={n:runpy.run_path(str(ROOT/'labs'/f'ch{n:02d}.py')) for n in range(11,16)}

    def test_loan_payment_system_conservation(self):
        change=self.lab[11]['bank_change']
        a=dict(loan=80,reserve=70,deposit=120,equity=30)
        b=dict(loan=70,reserve=40,deposit=90,equity=20)
        a=change(a,loan=60,deposit=60)
        a=change(a,reserve=-60,deposit=-60)
        b=change(b,reserve=60,deposit=60)
        self.assertEqual(a['reserve']+b['reserve'],110)
        self.assertEqual(a['deposit']+b['deposit'],270)
        self.assertEqual(a['equity']+b['equity'],50)

    def test_repayment_and_loss_are_not_same_transaction(self):
        change=self.lab[11]['bank_change']
        a=dict(loan=100,reserve=50,deposit=120,equity=30)
        repay=change(a,loan=-20,deposit=-20)
        loss=change(a,loan=-20,equity=-20)
        self.assertEqual(repay['deposit'],100)
        self.assertEqual(loss['deposit'],120)
        self.assertEqual(loss['equity'],10)
        self.assertEqual(repay['equity'],30)

    def test_bank_cannot_pay_from_negative_reserves(self):
        f=self.lab[11]['bank_change']
        a=dict(loan=100,reserve=10,deposit=80,equity=30)
        with self.assertRaises(ValueError): f(a,reserve=-20,deposit=-20)
        with self.assertRaises(ValueError): f(a,loan=5)
        with self.assertRaises(ValueError): f(a,loan=math.nan)

    def test_statistical_bridge_exact_denominator(self):
        x=self.lab[11]['comparable_growth'](100,110,30,40)
        self.assertAlmostEqual(x['new'],float(F(2,13)))
        self.assertAlmostEqual(x['old'],.1)
        self.assertAlmostEqual(x['mismatched'],.5)

    def test_multiplier_sign_boundary(self):
        f=self.lab[11]['multiplier']
        self.assertLess(f(.3,.1),f(.2,.1))
        self.assertGreater(f(.3,1.2),f(.2,1.2))
        self.assertEqual(f(.2,1),1)
        with self.assertRaises(ValueError): f(0,0)
        with self.assertRaises(ValueError): f(-.1,.2)

    def test_margin_denominator_and_repricing(self):
        x=self.lab[12]['interest_margin'](100,90,.05,.02)
        self.assertAlmostEqual(x['nii'],3.2)
        self.assertAlmostEqual(x['nim']-x['spread'],.002)
        # 独立直接求新收入、新支出，不调用实验中的delta表达式。
        new_income=60*.045+40*.05
        new_cost=54*.02+36*(.02+.017)/2
        self.assertAlmostEqual(new_income-new_cost,2.954)
        self.assertAlmostEqual(x['nii']+self.lab[12]['delta'],new_income-new_cost)

    def test_capital_sale_reconciles_full_balance_sheet(self):
        x=self.lab[12]['repair_sale'](5,80,.1,.02,available=60)
        self.assertAlmostEqual(x['sale'],float(F(75,2)))
        # 损失后资产97、负债92、权益5；出售款用于还负债。
        assets=97-x['sale']; liabilities=92-x['sale']*.98
        self.assertAlmostEqual(assets-liabilities,x['equity'])
        self.assertAlmostEqual(x['rwa']*.1,x['equity'])
        self.assertAlmostEqual(x['ratio'],.1)

    def test_capital_sale_infeasible_and_already_sufficient(self):
        f=self.lab[12]['repair_sale']
        for h in (.1,.2):
            with self.assertRaises(ValueError): f(5,80,.1,h)
        with self.assertRaises(ValueError): f(5,80,.1,.02,available=30)
        with self.assertRaises(ValueError): f(0,80,.1,0)
        self.assertEqual(f(10,80,.1,.2)['sale'],0)

    def test_liquidity_assets_liabilities_and_gap(self):
        f=self.lab[12]['liquidity_sale']
        x=f(10,25,40,.1)
        self.assertAlmostEqual(x['sold'],float(F(50,3)))
        self.assertAlmostEqual(x['loss'],float(F(5,3)))
        self.assertAlmostEqual(50+40-x['sold'],67+8-x['loss'])
        self.assertEqual(f(10,25,10,.1)['gap'],6)
        self.assertEqual(f(30,25,40,.1)['cash'],5)

    def test_bootstrap_independent_exact_cashflows(self):
        ds=[F(100,103),F(100,104)**2,F(200,209)**3]
        cfs=[[103],[4,104],[5,5,105]]
        prices=[sum(F(c)*d for c,d in zip(cf,ds)) for cf in cfs]
        result=self.lab[13]['bootstrap']([(cf,float(p)) for cf,p in zip(cfs,prices)])
        for a,b in zip(result,ds): self.assertAlmostEqual(a,float(b))
        # 负利率正折现因子应允许。
        self.assertEqual(self.lab[13]['bootstrap']([([100],101)]),[1.01])

    def test_bootstrap_and_ytm_reject_wrong_domain(self):
        b=self.lab[13]['bootstrap']; y=self.lab[13]['ytm']
        with self.assertRaises(ValueError): b([([100],100),([200,100],100)])
        with self.assertRaises(ValueError): b([([5,105],100)])
        with self.assertRaises(ValueError): y([5,-105],100)
        with self.assertRaises(ValueError): y([100],10)
        self.assertAlmostEqual(y([100],10,high=10),9)

    def test_zero_duration_and_finite_difference(self):
        f=self.lab[13]['risk']; p=self.lab[13]['bond_price']
        z=f([0,0,100],.05)
        self.assertAlmostEqual(z['macaulay'],3)
        self.assertAlmostEqual(z['modified'],float(F(20,7)))
        cf=[3,3,3,103]; h=1e-4; r=f(cf,.04)
        first=(p(cf,.04+h)-p(cf,.04-h))/(2*h)
        second=(p(cf,.04+h)-2*p(cf,.04)+p(cf,.04-h))/h**2
        self.assertAlmostEqual(-first/r['price'],r['modified'],places=6)
        self.assertAlmostEqual(second/r['price'],r['convexity'],places=5)

    def test_horizon_return_needs_reinvestment(self):
        p=self.lab[13]['bond_price']([5,105],.04)
        self.assertAlmostEqual(math.sqrt((105+5*1.04)/p)-1,.04)
        self.assertLess(math.sqrt(110/p)-1,.04)

    def test_twist_exposure_not_eliminated_by_equal_duration(self):
        f=self.lab[13]['zero_reprice']
        terminal1=50*F(26,25)
        terminal3=50*F(26,25)**3
        expected=terminal1/F(21,20)+terminal3/F(103,100)**3
        bar=f(50,1,.04,.05)+f(50,3,.04,.03)
        self.assertAlmostEqual(bar,float(expected))
        self.assertEqual(f(100,2,.04,.04),100)
        self.assertGreater(bar,100.99)

    def test_risk_neutral_state_price_sum(self):
        # 两个状态价格分别q/(1+rf)，无需把YTM当期望回报。
        value=F(98,100)/F(103,100)*105+F(2,100)/F(103,100)*40
        self.assertAlmostEqual(self.lab[13]['credit_price'],float(value))
        spread=F(105)/value-1-F(3,100)
        self.assertAlmostEqual(self.lab[13]['credit_spread'],float(spread))

    def test_debt_bridge_nominal_amounts_and_stability(self):
        f=self.lab[14]['debt_bridge']
        x=f(.6,.04,.06,.02,.01)
        balance=F(600)+F(24)+F(106,5)+F(53,5)
        self.assertAlmostEqual(x['next'],float(balance/F(1060)))
        self.assertAlmostEqual(f(.6,.04,.06,x['stable_pd'],.01)['next'],.6)
        stress=f(.6,.08,.02,.02,.01)
        self.assertAlmostEqual(stress['stable_pd'],float(-F(77,1700)))
        with self.assertRaises(ValueError): f(.6,.04,-1,.02)

    def test_repricing_calendar_tax_and_negative_saving(self):
        f=self.lab[14]['repricing_saving']
        x=f([(60,1),(40,.5)],.005,.002,.25)
        # 直接按上半年/下半年各自有效本金计算。
        cash=(60*.003*.5+100*.003*.5)*.75
        self.assertAlmostEqual(x['aftertax'],cash)
        self.assertAlmostEqual(f([(60,1),(40,.5)],.005,.002)['aftertax'],.24)
        self.assertLess(f([(100,1)],.002,.005)['pretax'],0)
        with self.assertRaises(ValueError): f([(100,1.1)],.005,.002)

    def test_surprise_uses_probability_and_preserves_sign(self):
        f=self.lab[14]['policy_surprise']
        self.assertEqual(f([(.75,-25),(.25,0)],-25)['surprise_bp'],-6.25)
        self.assertEqual(f([(1,-50)],-25)['surprise_bp'],25)
        with self.assertRaises(ValueError): f([(.75,-25),(.5,0)],-25)

    def test_currency_discount_paths_multiple_maturities(self):
        f=self.lab[15]['forward_from_discount']
        domestic=foreign=0
        for cf,dd,df in [(100,.98,.95),(80,.95,.90),(60,.92,.86)]:
            domestic+=cf*f(7,dd,df)*dd
            foreign+=7*cf*df
        self.assertAlmostEqual(domestic,foreign)
        self.assertAlmostEqual(f(7,1/1.01,1/1.025),float(F(1414,205)))

    def test_fx_execution_uses_correct_sides(self):
        f=self.lab[15]['executable_paths']
        x=f(6.99,7.01,6.79,6.81,.02,.03,.05,.06)
        expected1=F(679,100)*F(105,100)/F(701,100)-F(103,100)
        expected2=F(699,100)*F(102,100)-F(681,100)*F(106,100)
        self.assertAlmostEqual(x['borrow_domestic'],float(expected1))
        self.assertAlmostEqual(x['borrow_foreign'],float(expected2))
        self.assertLess(max(x.values()),0)
        self.assertGreater(f(6.99,7.01,7,7.02,.02,.03,.05,.06)['borrow_domestic'],0)
        with self.assertRaises(ValueError): f(7.01,6.99,6.79,6.81,.02,.03,.05,.06)

    def test_hedge_delivery_replication_and_overhedge(self):
        f=self.lab[15]['hedge_cash']
        for spot in (5,6.4,7.4,9):
            self.assertAlmostEqual(f(100,100,6.8,spot)['cash'],680)
            # 实物交割：收到60，再买40补足交割100。
            self.assertAlmostEqual(f(60,100,6.8,spot)['cash'],680-40*spot)
            self.assertEqual(f(60,100,6.8,spot)['residual'],-40)

    def test_forward_mark_value_vs_final_hedged_cash(self):
        f=self.lab[15]['forward_value']
        self.assertEqual(f(100,6.8,6.8,.99),0)
        self.assertAlmostEqual(f(100,6.8,7,.99),-19.8)
        self.assertAlmostEqual(f(100,7,6.8,.99),19.8)
        with self.assertRaises(ValueError): f(100,6.8,7,0)


if __name__=='__main__':
    unittest.main()
