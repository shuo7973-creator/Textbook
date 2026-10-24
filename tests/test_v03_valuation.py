"""第26—30章：独立现金、权益滚动、状态支付与边界验证。"""
from contextlib import redirect_stdout
from fractions import Fraction as F
import io
import math
from pathlib import Path
import runpy
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ValuationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            cls.lab={n:runpy.run_path(str(ROOT/'labs'/f'ch{n}.py')) for n in range(26,31)}

    def test_growth_reinvestment_from_capital_path(self):
        f=self.lab[26]['stable_value']; x=f(10,.1,.03,.08)
        # 从首期再投资3产生下一年利润增量.3，而非复制价值函数。
        capital=F(100); cash_pv=F(0); profit=F(10)
        for t in range(1,301):
            investment=profit*F(3,10)
            cash_pv+=(profit-investment)*(F(25,27)**t)
            capital+=investment;profit+=investment*F(1,10)
        self.assertAlmostEqual(float(cash_pv),x['value'],delta=.0001)
        self.assertAlmostEqual(x['reinvestment'],3)
        self.assertAlmostEqual(f(10,.08,.03,.08)['value'],125)
        self.assertLess(f(10,.06,.03,.08)['value'],f(10,.06,0,.08)['value'])

    def test_period_discount_and_terminal_time(self):
        f=self.lab[26]['discounted']; x=f([8,9],[.08,.09],154.5)
        exact=F(8)*F(25,27)+F(327,2)*F(25,27)*F(100,109)
        self.assertAlmostEqual(x['value'],float(exact))
        self.assertAlmostEqual(x['value'],146.2962962962963)
        self.assertAlmostEqual(f([-10,20],[0,.1])['value'],float(-10+F(200,11)))
        # 负现金不是非法输入；零期率也可用。
        with self.assertRaises(ValueError): f([1],[.1,.2])
        with self.assertRaises(ValueError): f([1],[-1])

    def test_matching_finance_equity_and_wacc(self):
        x=self.lab[26]['perpetual_financing'](12,40,.05,.25,.1)
        after_tax_interest=F(40)*F(1,20)*F(3,4)
        equity_cash=12-after_tax_interest
        self.assertEqual(x['fcfe'],float(equity_cash))
        self.assertEqual(x['equity'],105)
        self.assertAlmostEqual(x['wacc'],float(F(12,145)))
        self.assertAlmostEqual(12/x['wacc']-40,equity_cash/F(1,10))
        self.assertNotEqual(12/.08-40,x['equity'])

    def test_rights_bridge_and_negative_equity_domain(self):
        f=self.lab[26]['equity_bridge'];x=f(180,[20,15],[50,10,12,8,5],10)
        self.assertEqual(x['equity'],130);self.assertEqual(x['per_share'],13)
        with self.assertRaises(ValueError):f(10,[],[20],10)
        with self.assertRaises(ValueError):f(10,[],[],0)
        with self.assertRaises(ValueError):f(10,[math.nan],[],1)

    def test_mature_model_domain_and_growth_slope(self):
        f=self.lab[26]['stable_value']
        for args in [(10,.1,.08,.08),(10,.02,.03,.08),(10,.1,-.01,.08),(0,.1,.03,.08)]:
            with self.assertRaises(ValueError):f(*args)
        h=1e-6; num=(f(10,.1,.03+h,.08)['value']-f(10,.1,.03-h,.08)['value'])/(2*h)
        self.assertAlmostEqual(num,800,delta=.001)

    def test_finite_ri_independent_discounted_distributions(self):
        x=self.lab[27]['finite_ri'](100,[12,13],[4,5],[.1,.12],150)
        exact=F(4)*F(10,11)+F(155)*F(10,11)*F(25,28)
        self.assertEqual(x['book_end'],116)
        self.assertEqual(x['terminal_premium'],34)
        self.assertAlmostEqual(x['ri_value'],float(exact));self.assertAlmostEqual(x['ddm'],float(exact))
        self.assertAlmostEqual(x['rows'][1]['ri'],.04)

    def test_liquidation_and_new_equity_distributions(self):
        f=self.lab[27]['finite_ri']; x=f(100,[12,10.8],[4,118.8],[.1,.1],0)
        self.assertAlmostEqual(x['book_end'],0)
        self.assertAlmostEqual(x['ddm'],float(F(1120,11)))
        # 无业务收益，新股东投资20、期末资本120；不把发行认作收益。
        y=f(100,[0],[-20],[0],120)
        self.assertEqual(y['book_end'],120);self.assertEqual(y['ddm'],100)
        self.assertEqual(y['ri_value'],100)

    def test_oci_bridge_and_omission_error(self):
        x=self.lab[27]['finite_ri'](100,[7],[4],[.1],110)
        expected=F(1140,11)
        self.assertEqual(x['book_end'],103)
        self.assertAlmostEqual(x['ri_value'],float(expected))
        wrong=100+(2+110-103)/1.1
        self.assertAlmostEqual(wrong-x['ri_value'],float(F(50,11)))

    def test_accounting_restatement_telescopes(self):
        f=self.lab[27]['finite_ri'];a=f(100,[12,12],[12,12],[.1,.1],100);b=f(120,[2,2],[12,12],[.1,.1],100)
        exact=F(120,11)+F(11200,121)
        for value in [a['ri_value'],b['ri_value'],a['ddm'],b['ddm']]:self.assertAlmostEqual(value,float(exact))
        self.assertEqual([r['ri'] for r in b['rows']],[-10,-9])
        with self.assertRaises(ValueError): f(100,[12],[12,12],[.1],100)

    def test_fading_ri_and_cash_payouts(self):
        f=self.lab[27]['fading_ri']; ri_pv=sum(4*.6**(t-1)/1.1**t for t in range(1,150))
        self.assertAlmostEqual(f(100,4,.6,.1),100+ri_pv)
        self.assertEqual(f(100,-4,.6,.1),92)
        with self.assertRaises(ValueError):f(100,4,1.1,.1)

    def test_multiples_from_capital_and_dividend(self):
        x=self.lab[28]['justified_multiples'](.15,.03,.10)
        book=F(100);profit=book*F(3,20);investment=book*F(3,100)
        value=(profit-investment)/F(7,100)
        self.assertAlmostEqual(x['pb'],float(value/book))
        self.assertAlmostEqual(x['forward_pe'],float(value/profit))
        self.assertAlmostEqual(x['trailing_pe'],float(value/(profit/F(103,100))))
        with self.assertRaises(ValueError):self.lab[28]['justified_multiples'](.02,.03,.1)

    def test_sales_multiple_independent_cashflow(self):
        f=self.lab[28]['forward_ev_sales']
        revenue=F(100);nopat=revenue*F(15,100)*F(3,4);invest=nopat*F(1,5)
        cash=nopat-invest;value=cash/F(6,100)
        self.assertAlmostEqual(f(.15,.25,.15,.03,.09),float(value/revenue))
        self.assertAlmostEqual(f(.10,.25,.15,.03,.09),1)
        with self.assertRaises(ValueError):f(.15,1,.15,.03,.09)

    def test_aggregation_weight_identities(self):
        x=self.lab[28]['positive_pe_weights']([100,200],[10,5])
        self.assertEqual(x['aggregate'],20);self.assertEqual(x['profit_weighted'],20)
        self.assertAlmostEqual(x['cap_harmonic'],20);self.assertAlmostEqual(x['cap_arithmetic'],30)
        self.assertNotEqual(x['aggregate'],(10+40)/2)

    def test_loss_coverage_and_invalid_aggregate(self):
        f=self.lab[28]['aggregate_pe'];self.assertEqual(f([100,200],[10,-5]),60)
        for profits in [[10,-10],[10,-20]]:
            with self.assertRaises(ValueError): f([100,200],profits)
        with self.assertRaises(ValueError):self.lab[28]['positive_pe_weights']([100,200],[10,-5])
        with self.assertRaises(ValueError):f([100],[10,5])

    def test_lease_numerator_denominator_joint_change(self):
        x=self.lab[28]
        self.assertEqual(x['before'],float(F(13,2)));self.assertEqual(x['after'],float(F(95,16)))
        self.assertNotEqual(x['after'],130/32)
        self.assertNotEqual(x['after'],190/20)

    def test_bank_capital_equity_roll_and_shortfall(self):
        f=self.lab[29]['bank_capital'];a=f(10,1.2,110,.1);b=f(10,.5,110,.1)
        self.assertAlmostEqual(10+1.2-a['dividend'],11)
        self.assertAlmostEqual(10+.5+b['issuance'],11)
        self.assertEqual(b['dividend'],0);self.assertEqual(b['issuance'],.5)
        self.assertEqual(f(10,-12,0,.1)['issuance'],2)
        with self.assertRaises(ValueError):f(10,1,100,0)

    def test_cycle_cash_tax_nonlinearity(self):
        f=self.lab[29]['cash_tax_nopat']
        self.assertEqual(f(-10,.25),-10);self.assertEqual(f(50,.25),37.5)
        mean=(f(-10,.25)+f(50,.25))/2
        self.assertEqual(mean,13.75);self.assertEqual(f(20,.25)-mean,1.25)
        with self.assertRaises(ValueError):f(20,-.1)

    def test_resource_exhaustion_and_restoration(self):
        f=self.lab[29]['resource_value'];exact=F(300,11)+F(3000,121)+F(20000,1331)
        self.assertAlmostEqual(f([30,30,30],.1,5,15),float(exact))
        self.assertAlmostEqual(f([30,30,30],.1,5,0)-f([30,30,30],.1,5,15),float(F(15000,1331)))
        with self.assertRaises(ValueError):f([],.1,0,0)

    def test_fair_issue_conservation(self):
        x=self.lab[29]['growth_issue'](150,5,20,3,.15)
        discount=F(20,23)
        net=150*discount**5-20*discount**3
        self.assertAlmostEqual(x['old_today'],float(net));self.assertAlmostEqual(x['fair_net_pv'],float(net))
        self.assertAlmostEqual(x['new_fraction'],float(F(529,3000)))
        self.assertAlmostEqual(x['new_fraction']*x['post'],20)

    def test_discount_issue_value_transfer_and_domains(self):
        f=self.lab[29]['growth_issue'];fair=f(150,5,20,3,.15);cheap=f(150,5,20,3,.15,.8)
        # 公平融资前总股份设10，发行价格为公平每股价的八折。
        pre=150/(1.15**2)-20;issue_price=.8*pre/10;new_shares=20/issue_price
        old=10/(10+new_shares)*150/1.15**5
        self.assertAlmostEqual(cheap['old_today'],old);self.assertLess(old,fair['old_today'])
        for args in [(150,3,20,3,.15),(10,5,20,3,.15),(150,5,20,3,.15,0)]:
            with self.assertRaises(ValueError):f(*args)

    def test_reverse_identification_states(self):
        f=self.lab[30]['reverse_growth']
        self.assertAlmostEqual(f(140,10,.1,.08)['growth'],.03)
        self.assertEqual(f(100,10,.1,.08)['status'],'no_solution')
        self.assertEqual(f(100,10,.1,.1)['status'],'unidentified')
        self.assertEqual(f(120,10,.1,.08)['status'],'outside_domain')
        self.assertEqual(f(125,10,.08,.08)['status'],'unidentified')
        with self.assertRaises(ValueError):f(0,10,.1,.08)

    def test_reverse_price_and_cost_sensitivity(self):
        f=self.lab[30]['reverse_growth'];h=.001
        numerical=(f(140+h,10,.1,.08)['growth']-f(140-h,10,.1,.08)['growth'])/(2*h)
        self.assertAlmostEqual(numerical,.00125,places=10)
        self.assertAlmostEqual(f(140,10,.1,.09)['growth']-f(140,10,.1,.08)['growth'],.035)
        self.assertAlmostEqual(f(142,10,.1,.08)['growth'],float(F(17,525)))

    def test_risk_neutral_state_price_and_physical_return(self):
        f=self.lab[30]['risk_neutral_price'];x=f([60,160],[.7,.3],.05)
        # 两证券状态价格q=2/3与2/7，其和20/21为无风险贴现因子。
        independent=F(60)*F(2,3)+F(160)*F(2,7)
        self.assertAlmostEqual(x,float(independent));self.assertAlmostEqual(110/x-1,float(F(17,60)))
        self.assertNotAlmostEqual(x,110/1.05)

    def test_limited_liability_statewise_conservation(self):
        x=self.lab[30]['limited_liability']([40,160],80,[.5,.5],.05)
        self.assertAlmostEqual(x['equity'],float(F(800,21)))
        self.assertAlmostEqual(x['debt'],float(F(400,7)))
        self.assertAlmostEqual(x['assets'],x['equity']+x['debt'])
        self.assertNotAlmostEqual(x['equity'],(100-80)/1.05)
        y=self.lab[30]['limited_liability']([40,160],0,[.5,.5],.05)
        self.assertEqual(y['debt'],0);self.assertEqual(y['equity'],y['assets'])

    def test_bayes_and_probability_contract(self):
        f=self.lab[30]['posterior_good'];w=self.lab[30]['weighted']
        # 百个等权样本：好50中信号40，坏50中信号10。
        self.assertEqual(f(.5,.8,.2),40/50)
        self.assertAlmostEqual(w([160,80],[.8,.2]),144)
        self.assertEqual(f(0,.8,.2),0);self.assertEqual(f(1,.8,.2),1)
        with self.assertRaises(ValueError):f(.5,0,0)
        with self.assertRaises(ValueError):w([80,120],[.2,.5])
        with self.assertRaises(ValueError):w([80,120],[-.2,1.2])
        with self.assertRaises(ValueError):self.lab[30]['risk_neutral_price']([1],[1],-1)

if __name__=='__main__': unittest.main()
