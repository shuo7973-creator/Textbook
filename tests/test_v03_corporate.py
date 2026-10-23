"""第16—20章：独立有理数基准、支付守恒与模型边界。"""
from contextlib import redirect_stdout
from fractions import Fraction as F
import io
import math
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CorporateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            cls.lab = {n: runpy.run_path(str(ROOT/'labs'/f'ch{n:02d}.py'))
                       for n in range(16, 21)}

    def test_effective_rate_and_fee_cash_timing(self):
        ear = self.lab[16]['effective_rate'](.12, 12)
        self.assertAlmostEqual(ear, float(F(101,100)**12-1))
        # 净放款98、期末偿还105；使贷款NPV为零的是1/14，不是票面5%。
        self.assertAlmostEqual(self.lab[17]['npv']([98,-105],float(F(1,14))),0)
        with self.assertRaises(ValueError): self.lab[16]['effective_rate'](.12,True)
        with self.assertRaises(ValueError): self.lab[16]['effective_rate'](-2,2)

    def test_finite_annuity_equal_and_faster_growth(self):
        f=self.lab[16]['growing_annuity']
        self.assertAlmostEqual(f(10,.05,.05,3),float(F(200,7)))
        self.assertAlmostEqual(f(10,0,.1,3),float(F(331,10)))
        self.assertEqual(f(10,0,0,0),0)
        with self.assertRaises(ValueError): f(10,.05,.02,-1)

    def test_term_curve_independent_discount_factors(self):
        f=self.lab[16]['term_pv']
        prices=[F(100,103),F(2500,2678),F(25000,28119)]
        self.assertAlmostEqual(f([10]*3,[.03,.04,.05]),float(10*sum(prices)))
        with self.assertRaises(ValueError): f([10,10],[.03])
        with self.assertRaises(ValueError): f([10],[-1])

    def test_nominal_real_deterministic_path(self):
        f=self.lab[16]['term_pv']
        real_cash=[100,110,120]; real_rate=[.03,.04,.05]; infl=[.02,.03,.01]
        price=1; nominal_cash=[]
        for cf,p in zip(real_cash,infl):
            price*=1+p; nominal_cash.append(cf*price)
        nominal_rate=[(1+r)*(1+p)-1 for r,p in zip(real_rate,infl)]
        self.assertAlmostEqual(f(real_cash,real_rate),f(nominal_cash,nominal_rate))

    def test_cash_bridge_independent_cash_payments(self):
        x=self.lab[16]['cash_bridge'](40,10,10,.25,25,12,8)
        # EBITDA现金50，未融资税10；实际税7.5、利息10；再扣投资和占款。
        self.assertEqual(x['fcff'],50-10-25-12)
        self.assertEqual(x['fcfe'],50-7.5-10-25-12+8)
        self.assertEqual(x['cash_after_interest'],20.5)
        with self.assertRaises(ValueError):
            self.lab[16]['cash_bridge'](5,10,10,.25,25,12,8)

    def test_project_tax_residual_and_break_even(self):
        f=self.lab[17]['expansion']; npv=self.lab[17]['npv']
        self.assertEqual(f(),[-110,65,90])
        self.assertAlmostEqual(npv(f(),.1),float(F(2840,121)))
        # 解现金方程：-110 + X/1.1 + (X+25)/1.1² = 0。
        required_ocf=F(1081,21)
        revenue=(required_ocf+10)/F(3,4)
        self.assertAlmostEqual(npv(f(float(revenue)),.1),0)
        with self.assertRaises(ValueError): f(79)

    def test_multiple_irr_and_borrowing_direction(self):
        f=self.lab[17]['npv']; cash=[-100,230,-132]
        for r in [.1,.2]: self.assertAlmostEqual(f(cash,r),0)
        self.assertGreater(f(cash,.15),0)
        self.assertLess(f(cash,.05),0); self.assertLess(f(cash,.25),0)
        self.assertLess(f([100,-110],.05),0)
        self.assertGreater(f([100,-110],.2),0)

    def test_indivisible_budget_beats_greedy_ratio(self):
        f=self.lab[17]['select_projects']
        # A比率最高，但含A的两项组合均超预算；唯一可行双项BC的NPV8>5。
        self.assertEqual(f([(6,5),(5,4),(5,4)],10),dict(chosen=(1,2),cost=10,value=8))
        self.assertEqual(f([(1,-1)],10)['chosen'],())
        with self.assertRaises(ValueError): f([(-1,2)],10)

    def test_wait_option_state_payoffs_and_price(self):
        f=self.lab[17]['delay_option']; x=f(160,60,100,.5,.05,5)
        self.assertAlmostEqual(x['option'],float(F(200,7)))
        self.assertAlmostEqual(x['net'],float(F(165,7)))
        self.assertAlmostEqual(x['committed'],float(F(200,21)))
        self.assertEqual(f(160,60,100,0,.05)['option'],0)
        self.assertAlmostEqual(f(160,60,100,1,.05)['option'],float(F(400,7)))
        with self.assertRaises(ValueError): f(160,60,100,1.1,.05)

    def test_minimum_variance_and_constrained_solution(self):
        f=self.lab[18]['min_variance_weight']; v=self.lab[18]['portfolio_variance']
        w=f(.2,.3,.2); self.assertAlmostEqual(w,float(F(39,53)))
        # 独立二次型的平方配方：偏离最优点h，方差增加(53/500)h²。
        for h in [-.2,.1]:
            self.assertAlmostEqual(v(w+h,.2,.3,.2)-v(w,.2,.3,.2),float(F(53,500))*h*h)
        self.assertGreater(f(.1,.2,.9,False),1)
        self.assertEqual(f(.1,.2,.9),1)

    def test_covariance_degeneracy_and_hedge(self):
        f=self.lab[18]['min_variance_weight']; v=self.lab[18]['portfolio_variance']
        with self.assertRaises(ValueError): f(.2,.2,1)
        with self.assertRaises(ValueError): v(.5,.2,.3,1.01)
        self.assertAlmostEqual(v(.6,.2,.3,-1),0)

    def test_beta_orthogonal_noise_and_variance_denominators(self):
        x=[-.04,-.02,0,.02,.04]; noise=[.01,-.02,.02,-.02,.01]
        y=[.01+1.2*m+e for m,e in zip(x,noise)]
        b=self.lab[18]['beta_fit'](x,y)
        self.assertAlmostEqual(b['beta'],1.2); self.assertAlmostEqual(b['alpha'],.01)
        self.assertAlmostEqual(b['se'],math.sqrt(float(F(7,60))))
        self.assertAlmostEqual(b['residual_var'],float(F(7,20000)))
        self.assertAlmostEqual(b['asset_var'],1.2**2*b['market_var']+b['residual_var'])
        with self.assertRaises(ValueError): self.lab[18]['beta_fit']([1]*3,[1,2,3])

    def test_peer_beta_market_value_conversion(self):
        u=self.lab[18]['hamada_unlever']
        avg=(u(1.2,.5,.25)+u(1.5,1,.25))/2
        exact=(F(48,55)+F(6,7))/2
        self.assertAlmostEqual(avg,float(exact))
        target=avg*(1+.75*3/7)
        self.assertAlmostEqual(target,float(exact*F(37,28)))
        self.assertNotAlmostEqual(target,avg*(1+.75*.3))
        self.assertAlmostEqual(self.lab[18]['capital_cost'](.09,.05,.3,.25),.07425)

    def test_mm_wacc_preserved_when_equity_risk_changes(self):
        f=self.lab[19]['mm_no_tax']
        for d,kd in [(0,.05),(80,.05),(150,.08)]:
            x=f(200,d,.15,kd)
            self.assertAlmostEqual(x['wacc'],.15)
            # 总所需收益金额是资产风险决定的30，而不是固定股权成本。
            self.assertAlmostEqual(x['equity']*x['ke']+d*kd,30)
        self.assertAlmostEqual(f(200,80,.15,.05)['ke'],float(F(13,60)))
        with self.assertRaises(ValueError): f(200,200,.15,.05)

    def test_finite_tax_shield_not_perpetual_debt(self):
        x=self.lab[19]['shield_value']([80,60,40,20],.05,.25,.05)
        self.assertEqual(x['shields'],[1,.75,.5,.25])
        exact=sum(cf*F(20,21)**t for t,cf in enumerate([F(1),F(3,4),F(1,2),F(1,4)],1))
        self.assertAlmostEqual(x['pv'],float(exact)); self.assertLess(x['pv'],20)
        self.assertEqual(self.lab[19]['shield_value']([0,0],.05,.25,.05)['pv'],0)
        # APV增加税盾并扣融资费，不增加已公平定价的债务本金80。
        apv=self.lab[17]['npv']([-100,35,35,35,35],.1)+x['pv']-1
        self.assertAlmostEqual(apv,12.215538101422274)

    def test_repurchase_wealth_conservation_and_eps(self):
        f=self.lab[19]['repurchase']
        for price in [8,10,12]:
            x=f(100,10,20,price)
            self.assertAlmostEqual(x['seller_gain']+x['remaining_gain'],0)
            self.assertAlmostEqual(x['left']*x['price_after']+20,100)
        x=f(100,10,20,12)
        self.assertAlmostEqual(x['price_after'],9.6)
        self.assertAlmostEqual(9.5/x['left'],1.14)
        self.assertGreater(9.5/x['left'],10/10)
        with self.assertRaises(ValueError): f(100,10,20,1)

    def test_external_issue_value_and_ownership(self):
        f=self.lab[19]['issue_value']
        self.assertEqual(f(100,10,2,10),10)
        self.assertAlmostEqual(f(100,10,2,8,1,6),float(F(121,12)))
        # 老股比例下降，但本例老股总价值超过发行前100。
        self.assertGreater(10*f(100,10,2,8,1,6),100)

    def test_working_capital_net_and_gross_loss_adjustments(self):
        x=self.lab[20]['working_bridge'](30,40,20,120,80,70,100,75,5)
        self.assertEqual((x['ar'],x['inventory'],x['ap']),(45,50,25))
        self.assertEqual(x['profit']-x['delta_nwc'],100-75)
        gross_delta=(50+50-25)-(30+40-20)
        self.assertEqual(x['profit']+5-gross_delta,x['cash'])
        self.assertNotEqual(x['profit']+5-x['delta_nwc'],x['cash'])
        with self.assertRaises(ValueError):
            self.lab[20]['working_bridge'](0,0,0,0,0,1,0,0)

    def test_monthly_funding_conservation_and_capacity_gap(self):
        f=self.lab[20]['funding_path']; receipts=[0,0,40,40,40,40]
        rows=f(10,receipts,[35]*6,5,50)
        self.assertEqual([r['required_debt'] for r in rows],[30,65,60,55,50,45])
        self.assertEqual(max(r['gap'] for r in rows),15)
        for i,r in enumerate(rows,1):
            self.assertEqual(r['conditional_cash']-r['required_debt'],10+sum(receipts[:i])-35*i)
        base=f(10,[40]*6,[35]*6,5,50)
        self.assertEqual(base[-1]['conditional_cash'],40)
        self.assertEqual(base[-1]['required_debt'],0)

    def test_growth_same_equity_rollforward_three_denominators(self):
        f=self.lab[20]['retained_growth']
        for denominator,roe in [('begin',F(1,5)),('end',F(5,28)),('average',F(10,53))]:
            self.assertAlmostEqual(f(float(roe),.6,denominator),.12)
        self.assertEqual(f(.2,0,'end'),0)
        with self.assertRaises(ValueError): f(2,.5,'end')
        with self.assertRaises(ValueError): f(.2,.6,'unspecified')

    def test_discount_cash_base_and_common_payment_date(self):
        x=self.lab[20]['discount_cost'](.02,10,30)
        self.assertAlmostEqual(x['period'],float(F(1,49)))
        self.assertAlmostEqual(x['simple_annual'],float(F(73,196)))
        self.assertAlmostEqual(x['effective_annual'],(50/49)**(365/20)-1)
        funded_payment=98*(1+F(3,25)*F(20,365))
        self.assertLess(funded_payment,100)
        with self.assertRaises(ValueError): self.lab[20]['discount_cost'](.02,30,10)


if __name__=='__main__':
    unittest.main()
