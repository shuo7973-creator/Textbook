"""第21—25章：独立收付、合并抵销、权益与资本滚动基准。"""
from contextlib import redirect_stdout
from fractions import Fraction as F
import io
import math
from pathlib import Path
import runpy
import unittest

ROOT=Path(__file__).resolve().parents[1]


class StatementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            cls.lab={n:runpy.run_path(str(ROOT/'labs'/f'ch{n:02d}.py')) for n in range(21,26)}

    def test_y1_direct_receipts_and_payments(self):
        x=self.lab[21]['historical_y1']()
        receipts=F(150)+20-25
        payments=F(120)-6+32-30-23+20
        self.assertEqual(x['cfo'],float(receipts-payments-F(13,2)))
        self.assertEqual(x['cash'],float(F(10)+receipts-payments-F(13,2)-10+2-5-4))
        self.assertEqual(x['assets'],x['claims'])
        self.assertEqual(x['equity'],74.5)

    def test_interest_reclassification_conserves_total_cash(self):
        f=self.lab[21]['historical_y1']; a=f(); b=f(True)
        self.assertEqual(a['cfo']-b['cfo'],4)
        self.assertEqual(a['cff']-b['cff'],-4)
        self.assertEqual(a['cash'],b['cash'])
        self.assertEqual(a['ni'],b['ni'])

    def test_comprehensive_equity_and_owner_transactions(self):
        f=self.lab[21]['equity_roll']
        self.assertEqual(f(60,19.5,-2,7,3,5),76.5)
        self.assertEqual(f(5,-10),-5)
        with self.assertRaises(ValueError): f(60,10,issue=-1)
        with self.assertRaises(ValueError): f(60,math.nan)

    def test_full_consolidation_and_minority_partition(self):
        x=self.lab[21]['simple_consolidation'](50,48,100,40,.8)
        self.assertEqual(x['assets'],150)
        self.assertAlmostEqual(x['nci'],12)
        self.assertAlmostEqual(x['assets']-x['debt'],x['parent_equity']+x['nci'])
        self.assertNotEqual(x['assets'],50+.8*100)
        with self.assertRaises(ValueError):
            self.lab[21]['simple_consolidation'](50,60,100,40,.8)

    def test_internal_sales_group_cost_and_unrealized_profit(self):
        f=self.lab[21]['internal_goods']
        for sold,revenue in [(0,0),(.6,90),(1,150)]:
            x=f(80,120,revenue,sold)
            self.assertAlmostEqual(x['profit'],revenue-80*sold)
            self.assertAlmostEqual(x['inventory']+80*sold,80)
        self.assertAlmostEqual(f(80,120,90,.6)['eliminated_profit'],16)
        with self.assertRaises(ValueError): f(80,120,90,1.2)

    def test_reformulation_preserves_equity_and_operating_cash(self):
        f=self.lab[22]['reformulate']; a=f(18.5,25,32,64,23,42,74.5)
        b=f(18.5,25,32,64,23,42,74.5,5)
        self.assertEqual((a['noa'],a['nfo']),(98,23.5))
        self.assertEqual((b['noa'],b['nfo']),(103,28.5))
        self.assertEqual(a['equity'],b['equity'])
        with self.assertRaises(ValueError): f(18.5,25,32,64,23,42,75)
        with self.assertRaises(ValueError): f(18.5,25,32,64,23,42,74.5,20)

    def test_tax_allocation_independent_net_income(self):
        x=self.lab[22]['allocate_tax'](30,4,2,.25,.2)
        direct_tax=F(30-4,4)+F(2,5)
        self.assertAlmostEqual(x['total_tax'],float(direct_tax))
        self.assertAlmostEqual(x['ni'],float(30-4+2-direct_tax))
        self.assertAlmostEqual(x['nfe'],1.4)
        with self.assertRaises(ValueError): self.lab[22]['allocate_tax'](3,4,2,.25,.2)

    def test_two_cfo_bridges_and_tax_shield_not_double_counted(self):
        f=self.lab[22]['fcff_from_cfo']
        self.assertEqual(f(25.5,10,4,.25),14.5)
        self.assertEqual(f(21.5,10,4,.25,True),14.5)
        self.assertNotEqual(f(25.5,10,4,.25,True),14.5)
        self.assertEqual(f(25.5,10,4,0),15.5)

    def test_oci_and_impairment_cash_bridge(self):
        f=self.lab[22]['cash_from_noa']
        self.assertEqual(f(22.5,90,98),14.5)
        self.assertEqual(f(22.5,90,103,5),14.5)
        self.assertEqual(f(27.5,90,103),14.5)
        self.assertEqual(f(17.5,90,93),14.5)
        self.assertNotEqual(f(17.5,90,93,5),14.5)

    def test_noncash_lease_vs_cash_asset_purchase(self):
        f=self.lab[22]['cash_from_noa']
        self.assertEqual(f(0,100,120,20),0)
        self.assertEqual(f(0,100,115),-15)
        # 基准融资用途由股东/债权人现金与净金融资产滚动独立得到。
        self.assertEqual(5+3-(23.5-30),f(22.5,90,98))

    def test_zero_net_debt_and_net_financial_assets(self):
        f=self.lab[23]['profitability']; a=f(12,1,100,0); b=f(12,-.6,100,-20)
        self.assertIsNone(a['nbc']); self.assertAlmostEqual(a['roe'],.11)
        self.assertAlmostEqual(a['leverage_effect'],-.01)
        self.assertAlmostEqual(b['roe'],float(F(21,200)))
        self.assertAlmostEqual(b['nbc'],.03)

    def test_baseline_roe_fraction_and_denominator_domain(self):
        x=self.lab[23]['profitability'](22.5,3,94,26.75)
        self.assertAlmostEqual(x['roe'],float(F(78,269)))
        self.assertAlmostEqual(x['rnoa'],float(F(45,188)))
        self.assertAlmostEqual(x['roe'],x['rnoa']+x['leverage_effect'])
        with self.assertRaises(ValueError): self.lab[23]['profitability'](12,1,100,100)

    def test_operating_liability_leverage_identity(self):
        x=self.lab[23]['operating_leverage'](120,30,15,.04)
        self.assertAlmostEqual(x['rooa'],float(F(27,200)))
        self.assertAlmostEqual(x['effect'],float(F(19,600)))
        self.assertAlmostEqual(x['rnoa'],float(F(1,6)))
        with self.assertRaises(ValueError): self.lab[23]['operating_leverage'](30,30,15,.04)

    def test_time_weighted_capital(self):
        f=self.lab[23]['weighted_capital']
        self.assertEqual(f([(100,9),(220,3)]),130)
        self.assertEqual(f([(100,3),(100,6),(220,3)]),130)
        self.assertEqual(26/f([(100,9),(220,3)]),.2)
        with self.assertRaises(ValueError): f([(100,0)])

    def test_symmetric_margin_turnover_decomposition(self):
        f=self.lab[23]['margin_turnover']; x=f(.15,.12,1.6,2)
        self.assertAlmostEqual(x['margin'],-.054)
        self.assertAlmostEqual(x['turnover'],.054)
        self.assertAlmostEqual(x['total'],0)
        reverse=f(.12,.15,2,1.6)
        self.assertAlmostEqual(reverse['margin'],-x['margin'])
        # 同时变化且总变化非零，防止仅验证完全相消样本。
        y=f(.1,.16,1,1.5)
        self.assertAlmostEqual(y['margin']+y['turnover'],.14)

    def test_economic_profit_cashflow_equivalence(self):
        cash_npv=-100+F(600,11)+F(6000,121)
        ep_pv=F(5)*F(10,11)**2
        self.assertEqual(cash_npv,ep_pv)
        self.assertAlmostEqual(self.lab[23]['dcf'],float(ep_pv))

    def test_research_cohort_expense_and_asset_conservation(self):
        rows=self.lab[24]['research_cohorts']([12,15,18,0,0],3)
        self.assertEqual([r['asset'] for r in rows],[8,14,17,6,0])
        self.assertEqual([r['amort'] for r in rows],[4,9,15,11,6])
        self.assertEqual(sum(r['amort'] for r in rows),45)
        self.assertEqual(sum(r['profit_adjustment'] for r in rows),0)
        self.assertEqual(self.lab[24]['research_cohorts']([12,15],1)[-1]['asset'],0)

    def test_research_tax_net_assets_and_fcf_invariance(self):
        rows=self.lab[24]['research_cohorts']([12,15,18,0,0],3,.25)
        self.assertEqual(rows[0]['dtl'],2)
        self.assertEqual([r['net_asset'] for r in rows],[6,10.5,12.75,4.5,0])
        self.assertEqual([r['profit_adjustment'] for r in rows],[6,4.5,2.25,-8.25,-4.5])
        with self.assertRaises(ValueError): self.lab[24]['research_cohorts']([12],0)

    def test_accrual_classification_and_invalid_denominator(self):
        f=self.lab[24]['cash_accrual']
        self.assertAlmostEqual(f(20,8,100)-f(20,11,100),.03)
        for denominator in [0,-1,math.nan]:
            with self.assertRaises(ValueError): f(20,8,denominator)

    def test_normalization_tax_and_post_impairment_earnings(self):
        f=self.lab[24]['normalized_income']
        self.assertEqual(f(24,[(8,.25),(-2,.25)]),19.5)
        self.assertEqual(f(24,[(6,0),(-1.5,0)]),19.5)
        x=self.lab[24]['depreciation_after_loss'](100,40,5)
        self.assertEqual(x['before']-x['after'],8)
        with self.assertRaises(ValueError): self.lab[24]['depreciation_after_loss'](100,101,5)

    def test_baseline_forecast_direct_cash_and_three_statements(self):
        x=self.lab[25]['forecast']()
        received=F(165)-F(5,2)
        paid=F(99)+26+F(16,5)-F(23,10)
        tax=F(309,10)*F(1,4)
        self.assertAlmostEqual(x['cfo'],float(received-paid-tax))
        self.assertAlmostEqual(x['cash'],27.275)
        self.assertAlmostEqual(x['fcff'],16.35)
        self.assertAlmostEqual(x['assets'],158.975)
        self.assertEqual(x['draw'],0)

    def test_borrowing_feedback_exact_solution_and_repayment_equation(self):
        f=self.lab[25]['required_borrowing']; draw=f(10,15,.08,.25,.5,10)
        self.assertAlmostEqual(draw,float(F(500,97)))
        self.assertAlmostEqual(10+draw-.75*.08*.5*draw,15)
        self.assertEqual(f(20,15,.08,.25,.5,10),0)
        self.assertEqual(f(10,15,.08,.25,0,10),5)
        self.assertGreater(f(10,15,.08,0,.5,10),draw)
        with self.assertRaises(ValueError): f(10,15,2,0,1,100)

    def test_stress_independent_fraction_cashflow(self):
        revenue=F(297,2); ar=revenue*(F(1,6)+F(20,365))
        dnwc=ar+F(176,5)-F(253,10)-34
        ebit=revenue*F(17,50)-33
        old_interest=F(21,10)
        cash_before=F(37,2)+(ebit-old_interest)*F(3,4)+7-dnwc-12-6
        draw=(15-cash_before)/F(157,160)
        interest=old_interest+draw/F(40)
        cash_tax=(ebit-interest)/4
        direct_cfo=revenue-(ar-25)-(revenue*F(33,50)+26+F(16,5)-F(23,10))-cash_tax
        x=self.lab[25]['forecast'](float(revenue),.66,float(ar))
        self.assertAlmostEqual(x['draw'],float(draw))
        self.assertAlmostEqual(x['cfo'],float(direct_cfo))
        self.assertAlmostEqual(x['cash'],15)
        self.assertGreater(x['ni'],0); self.assertLess(x['fcff'],0)
        self.assertAlmostEqual(x['assets'],x['claims'])

    def test_infeasible_funding_and_loss_tax_domain(self):
        f=self.lab[25]['forecast']; ar=148.5*(1/6+20/365)
        with self.assertRaises(ValueError): f(148.5,.66,ar,capacity=4)
        with self.assertRaises(ValueError): f(50,.9)
        x=f(148.5,.66,ar)
        # 缺必要借款与缺期末现金的区别：后者还反映少借时少付的税后利息。
        self.assertAlmostEqual((x['draw']-4)*.98125,15-(x['cash_before']+4*.98125))

    def test_quantity_capacity_and_scenario_expectation(self):
        f=self.lab[25]['revenue_driver']
        self.assertEqual(f(100,2,120),200)
        with self.assertRaises(ValueError): f(130,2,120)
        expectation=.5*f(80,1.2,120)+.5*f(120,.8,120)
        self.assertEqual(expectation,96)
        self.assertNotEqual(expectation,100*1)


if __name__=='__main__':
    unittest.main()
