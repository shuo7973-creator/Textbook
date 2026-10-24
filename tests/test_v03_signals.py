"""第31—35章：版本事件、独立秩/协方差、可行区间和资金守恒。"""
from contextlib import redirect_stdout
from fractions import Fraction as F
import io
import math
from pathlib import Path
import runpy
import unittest

ROOT=Path(__file__).resolve().parents[1]

class SignalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            cls.lab={n:runpy.run_path(str(ROOT/'labs'/f'ch{n}.py')) for n in range(31,36)}

    def test_public_and_production_clock_boundary(self):
        m=self.lab[31];f=m['asof_value'];r=m['ROWS'];k=m['KEY']
        self.assertIsNone(f(r,k,'2025-04-20T18:29:59+08:00'))
        self.assertEqual(f(r,k,'2025-04-20T10:30:00+00:00'),100)
        self.assertIsNone(f(r,k,'2025-04-22T09:29:59+08:00','production'))
        self.assertEqual(f(r,k,'2025-04-22T09:30:00+08:00','production'),100)
        self.assertEqual(f(r,k,'2025-04-22T09:00:00+08:00','production',0),100)

    def test_future_versions_and_other_security_invariance(self):
        m=self.lab[31];f=m['asof_value'];r=m['ROWS'];k=m['KEY'];t='2025-06-01T00:00:00+08:00'
        self.assertEqual(f(r[:1],k,t),f(list(reversed(r)),k,t))
        other={**r[0],'sid':'B','value':999}
        self.assertEqual(f(r+[other],k,t),100)
        self.assertEqual(f(r,k,'2025-09-01T00:00:00+08:00'),95)
        with self.assertRaises(ValueError):f(r+[{**r[0],'value':101}],k,t)
        with self.assertRaises(ValueError):f(r,k,'2025-06-01T00:00:00')

    def test_execution_eligibility_is_not_target_weight(self):
        f=self.lab[31]['first_execution'];slots=[('2025-01-01T10:00:00+08:00',True),('2025-01-01T09:30:00+08:00',False)]
        self.assertEqual(f(slots,'2025-01-01T09:00:00+08:00',45),slots[0][0])
        self.assertIsNone(f(slots,'2025-01-01T10:00:01+08:00'))
        with self.assertRaises(ValueError):f(slots,'2025-01-01T09:00:00+08:00',-1)

    def test_labels_mature_before_training(self):
        m=self.lab[31];f=m['eligible_labels'];rows=m['labels']
        self.assertEqual(f(rows,'2025-03-31T23:59:00+08:00'),['later_short'])
        self.assertEqual(f(rows,'2025-05-01T00:00:00+08:00'),['early_long','later_short'])
        invalid={**rows[0],'known':'2025-02-01T00:00:00+08:00'}
        with self.assertRaises(ValueError):f([invalid],'2025-05-01T00:00:00+08:00')

    def test_corporate_actions_share_and_cash_ledger(self):
        f=self.lab[31]['event_return']
        shares=F(1)*2;cash=shares*F(1,10);end=shares*F(26,5)+cash
        self.assertAlmostEqual(f(10,5.2,2,.1),float(end/10-1))
        self.assertEqual(f(10,0),-1)
        self.assertAlmostEqual(float(F(11,10)/F(21,20)-1),1/21)
        with self.assertRaises(ValueError):f(10,5,0)

    def test_distinct_profitability_definitions(self):
        x=self.lab[32]['profitability_definitions'](100,60,20,4,80,20,.25,80,75)
        self.assertEqual(x['op'],float(F(16,100)))
        self.assertEqual(x['roe'],float(F(12,80)))
        self.assertEqual(x['rnoa'],float(F(15,75)))
        self.assertNotEqual(x['op'],x['rnoa'])

    def test_signed_earnings_and_financial_domains(self):
        f=self.lab[32]['factor_fields'];x=f(100,200,-10,100,5,150,180,150)
        self.assertEqual(x['ep'],-.05);self.assertEqual(x['accrual'],-.1)
        self.assertAlmostEqual(x['investment'],.2)
        for args in [(0,200,10,100,5,150,180,150),(100,0,10,100,5,150,180,150),(100,200,10,100,5,150,-1,150)]:
            with self.assertRaises(ValueError):f(*args)

    def test_six_cells_by_explicit_portfolio_positions(self):
        f=self.lab[32]['six_cell_spread'];cells=dict(SL=.01,SN=.02,SH=.03,BL=.005,BN=.01,BH=.02)
        x=f(cells);positions={'SH':F(1,2),'BH':F(1,2),'SL':-F(1,2),'BL':-F(1,2)}
        profit=sum(w*F(str(cells[k])) for k,w in positions.items())
        self.assertEqual(sum(positions.values()),0);self.assertEqual(sum(abs(w) for w in positions.values()),2)
        self.assertAlmostEqual(x['spread'],float(profit))
        self.assertAlmostEqual(x['size_within_this_sort'],1/120)
        with self.assertRaises(ValueError):f({'SL':.01})

    def test_composite_ties_common_coverage_and_permutation(self):
        m=self.lab[32];f=m['composite']
        self.assertEqual(f([.5,1,1.5],[.2,.1,.15]),[.5,.25,.75])
        self.assertEqual(f([1.5,.5,1],[.15,.2,.1]),[.75,.5,.25])
        self.assertEqual(m['rank_score']([5,5,5]),[.5,.5,.5])
        self.assertEqual(m['rank_score']([2,2,5]),[.25,.25,1])
        with self.assertRaises(ValueError):f([1,None],[2,3])

    def test_cash_classification_changes_proxy_not_profit(self):
        f=self.lab[32]['factor_fields'];base=(100,200,20,100)
        a=f(*base,8,100,120,100);b=f(*base,11,100,120,100)
        self.assertAlmostEqual(a['accrual']-b['accrual'],.03)
        self.assertEqual(a['roe'],b['roe']);self.assertEqual(a['ep'],b['ep'])

    def test_momentum_exact_dates_and_future_invariance(self):
        f=self.lab[33]['momentum'];months={m:.01 for m in range(1,12)}
        exact=F(101,100)**11-1
        self.assertAlmostEqual(f(months,12),float(exact))
        self.assertEqual(f({**months,12:-.99,13:100,0:.3},12),f(months,12))
        missing={k:v for k,v in months.items() if k!=6};missing[0]=.01
        with self.assertRaises(ValueError):f(missing,12)
        self.assertEqual(f({**months,6:-1},12),-1)

    def test_aggregate_vol_by_full_covariance_matrix(self):
        f=self.lab[33]['aggregate_log_vol']
        for phi in [F(3,10),F(-2,5),F(0)]:
            covsum=sum(F(1,2500)*phi**abs(i-j) for i in range(12) for j in range(12))
            self.assertAlmostEqual(f(.02,float(phi),12)**2,float(covsum))
        self.assertAlmostEqual(f(.02,.3,12),.0917850208705974)
        with self.assertRaises(ValueError):f(.02,1,12)

    def test_beta_not_ranked_by_total_volatility(self):
        f=self.lab[33]['beta_from_vol']
        self.assertAlmostEqual(f(.1,.05,.9),1.8);self.assertAlmostEqual(f(.2,.05,.2),.8)
        self.assertLess(f(.2,.05,-.2),0)
        with self.assertRaises(ValueError):f(.1,0,.5)

    def test_macro_vintages_and_newest_observation(self):
        m=self.lab[33];f=m['macro_asof'];r=m['releases'];cut='2025-07-01T00:00:00+08:00'
        self.assertEqual(f(r,cut),f(r[:1],cut))
        newer=('2025-06','2025-07-10T10:00:00+08:00',2)
        self.assertEqual(f(r+[newer],'2025-09-01T00:00:00+08:00'),2)
        self.assertIsNone(f(r,'2025-06-10T09:59:00+08:00'))
        with self.assertRaises(ValueError):f(r+[('2025-05',r[0][1],99)],cut)

    def test_hysteresis_prefix_and_boundary(self):
        f=self.lab[33]['hysteresis'];xs=[-.1,.1,-.05,.25,.05,-.25]
        full=f(xs,.2);self.assertEqual(full,[0,0,0,1,1,-1])
        self.assertEqual(f(xs[:4],.2),full[:4])
        self.assertEqual(f([.2,-.2],.2,1),[1,1])
        with self.assertRaises(ValueError):f(xs,0)

    def test_average_ranks_and_common_pairs(self):
        m=self.lab[34];self.assertEqual(m['ranks']([30,10,10,20]),[4,1.5,1.5,3])
        x=m['paired_ic']({'a':1,'b':2,'c':None,'d':99},{'a':.2,'b':.1,'c':.5})
        self.assertAlmostEqual(x['ic'],-1);self.assertEqual(x['paired'],2);self.assertEqual(x['coverage'],.5)
        with self.assertRaises(ValueError):m['corr']([1,1],[1,2])
        with self.assertRaises(ValueError):m['ranks']([1,math.nan])

    def test_partial_relation_by_within_pair_contrasts(self):
        x=self.lab[34]['neutral_diagnostic']([1,3,10,14],[.01,.03,.06,.02],['A','A','B','B'])
        # 组内双点差分的加权斜率：各组交叉积=ΔxΔy/2。
        cross=F(2)*F(2,100)/2+F(4)*F(-4,100)/2
        ss=F(2)**2/2+F(4)**2/2
        self.assertEqual(float(cross/ss),-.006)
        self.assertAlmostEqual(x['slope'],float(cross/ss))
        self.assertAlmostEqual(x['partial'],-.6);self.assertAlmostEqual(x['raw'],7/math.sqrt(385))

    def test_neutrality_lost_after_clipping(self):
        f=self.lab[34]['industry_residual'];res=f([0,4,5],['A']*3)
        self.assertEqual(res,[-3,1,2]);self.assertEqual(sum(res),0)
        self.assertEqual(sum(max(-1,min(1,x)) for x in res),1)
        with self.assertRaises(ValueError):f([1,2,3],['A','A','B'])

    def test_ic_shift_invariance_does_not_imply_profit(self):
        f=self.lab[34]['corr'];rank=self.lab[34]['ranks']
        loss=[-.03,-.02,-.01];gain=[v+.1 for v in loss]
        self.assertAlmostEqual(f(rank([1,2,3]),rank(loss)),1)
        self.assertAlmostEqual(f(rank([1,2,3]),rank(gain)),1)
        self.assertLess(loss[-1],0);self.assertGreater(gain[-1],0)

    def test_hac_by_bartlett_kernel_quadratic_form(self):
        f=self.lab[34]['hac_mean'];u=[F(-3,20),F(-1,20),F(1,20),F(3,20)]
        for bandwidth in range(4):
            # 核矩阵的双重求和独立于实验的自协方差滞后循环。
            variance=sum(u[i]*u[j]*max(F(0),1-F(abs(i-j),bandwidth+1)) for i in range(4) for j in range(4))/16
            self.assertAlmostEqual(f([.1,.2,.3,.4],bandwidth)['se']**2,float(variance))
        self.assertAlmostEqual(f([.1,.2,.3,.4],1)['se'],.0625)
        with self.assertRaises(ValueError):f([.1,.2],2)

    def test_minimum_variance_against_grid_and_constraints(self):
        m=self.lab[35];f=m['bounded_minimum'];v=m['variance2']
        x=f(.04,.09,.012);self.assertAlmostEqual(x['weight'],39/53)
        for i in range(1001):self.assertLessEqual(x['variance'],v(i/1000,.04,.09,.012)+1e-14)
        self.assertEqual(f(.04,.09,.012,.2,.6)['weight'],.6)
        self.assertAlmostEqual(f(.04,.09,.012,.2,.6,6/11,.03)['weight'],6/11+.03)
        with self.assertRaises(ValueError):f(.04,.09,.012,.8,1,.5,.1)

    def test_covariance_invalid_flat_and_perfect_correlation(self):
        m=self.lab[35];f=m['bounded_minimum']
        with self.assertRaises(ValueError):f(.04,.09,.08)
        x=f(.04,.04,.04,.2,.8)
        self.assertEqual(x['status'],'flat');self.assertEqual(x['interval'],(.2,.8))
        self.assertAlmostEqual(x['variance'],.04)
        self.assertEqual(f(.04,.09,.06)['weight'],1)
        self.assertAlmostEqual(m['variance2'](3,.04,.09,.06),0,places=14)

    def test_two_asset_erc_all_valid_correlations(self):
        f=self.lab[35]['risk_contributions2']
        for rho in [-.9,0,.2,.95,1]:
            rc=f(.6,.04,.09,rho*.2*.3)
            self.assertAlmostEqual(rc[0],rc[1])
        with self.assertRaises(ValueError):f(.5,.04,.04,-.04)

    def test_three_asset_inverse_vol_not_erc(self):
        m=self.lab[35];shares=m['shares']
        expected=[F(9,23),F(9,23),F(5,23)]
        for actual,exact in zip(shares,expected):self.assertAlmostEqual(actual,float(exact))
        self.assertNotAlmostEqual(shares[0],1/3)
        # 对角缩放不改变正定性，相关块特征值1.8/.2，第三维1。
        self.assertGreater(.01*.04-.016**2,0)

    def test_negative_risk_contribution_and_euler_sum(self):
        m=self.lab[35];rc=m['risk_contributions2'](.9,.04,.09,-.03)
        self.assertLess(rc[1],0)
        self.assertAlmostEqual(sum(rc),math.sqrt(m['variance2'](.9,.04,.09,-.03)))

    def test_shrinkage_targets_and_singular_case(self):
        m=self.lab[35];f=m['shrink2']
        shrunk=f(.04,.09,.012,.5);self.assertEqual(shrunk,(.04,.09,.006))
        self.assertAlmostEqual(m['bounded_minimum'](*shrunk)['weight'],42/59)
        self.assertEqual(f(0,.09,0,1),(0,.09,0))
        self.assertEqual(f(.04,.09,.012,0),(.04,.09,.012))
        with self.assertRaises(ValueError):f(.04,.09,.012,1.1)

    def test_rebalance_post_fee_cash_and_turnover(self):
        f=self.lab[35]['rebalance_values'];x=f([60,50],[.5,.5],.001)
        expected=[F(-1001,200),F(999,200)]
        self.assertAlmostEqual(x['after'],109.99);self.assertAlmostEqual(x['cost'],.01)
        for actual,exact in zip(x['trades'],expected):self.assertAlmostEqual(actual,float(exact))
        self.assertAlmostEqual(sum(x['trades'])+x['cost'],0,places=12)
        self.assertAlmostEqual(x['turnover'],float(F(1,22)))
        for h,trade in zip([60,50],x['trades']):self.assertAlmostEqual((h+trade)/x['after'],.5)

    def test_rebalance_zero_fee_no_trade_and_full_switch(self):
        f=self.lab[35]['rebalance_values']
        nofee=f([60,50],[.5,.5],0);self.assertEqual(nofee['after'],110)
        idle=f([60,50],[6/11,5/11],.001);self.assertAlmostEqual(idle['cost'],0)
        switched=f([100,0],[0,1],.01)
        # 全卖100，买V，费用.01(100+V)，V=99/1.01。
        self.assertAlmostEqual(switched['after'],float(F(9900,101)))
        self.assertAlmostEqual(sum(switched['trades'])+switched['cost'],0,places=12)
        for h,w,c in [([100],[.5],.01),([100],[1],1),([-1,101],[.5,.5],.01)]:
            with self.assertRaises(ValueError):f(h,w,c)

if __name__=='__main__':unittest.main()
