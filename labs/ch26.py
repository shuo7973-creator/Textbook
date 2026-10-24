"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def stable_value(nopat, marginal_return, growth, cost):
    if any(not isfinite(x) for x in (nopat,marginal_return,growth,cost)):
        raise ValueError('输入须有限')
    if nopat<=0 or marginal_return<=0 or not 0<=growth<cost or growth>marginal_return:
        raise ValueError('本成熟期模型要求N>0、R>0、0<=g<k且g<=R')
    reinvest=nopat*growth/marginal_return
    return dict(reinvestment=reinvest,fcff=nopat-reinvest,value=(nopat-reinvest)/(cost-growth))

def discounted(cashflows,period_rates,terminal=0):
    if not cashflows or len(cashflows)!=len(period_rates): raise ValueError('期数相同且非空')
    if any(not isfinite(x) for x in [*cashflows,*period_rates,terminal]) or any(r<=-1 for r in period_rates):
        raise ValueError('金额有限、折现因子为正')
    factor=1; pv=0
    for cash,rate in zip(cashflows,period_rates):
        factor/=1+rate; pv+=cash*factor
    return dict(explicit=pv,terminal_pv=terminal*factor,value=pv+terminal*factor)

def perpetual_financing(fcff,debt,rd,tax,ke):
    if any(not isfinite(x) for x in (fcff,debt,rd,tax,ke)) or debt<0 or rd<0 or not 0<=tax<1 or ke<=0:
        raise ValueError('融资参数超域')
    fcfe=fcff-debt*rd*(1-tax)
    if fcfe<=0: raise ValueError('本例限正永续权益现金')
    equity=fcfe/ke; operations=equity+debt
    wacc=(equity*ke+debt*rd*(1-tax))/operations
    return dict(fcfe=fcfe,equity=equity,operations=operations,wacc=wacc)

def equity_bridge(operations,extra_assets,claims,shares):
    items=list(extra_assets)+list(claims)
    if any(not isfinite(x) for x in [operations,shares,*items]) or operations<0 or shares<=0 or any(x<0 for x in items):
        raise ValueError('价值非负、股数为正；资产及索取权先排重')
    equity=operations+sum(extra_assets)-sum(claims)
    if equity<0: raise ValueError('压力残差为负，转违约支付模型')
    return dict(equity=equity,per_share=equity/shares)

# %% 增长与回报的方向
base=stable_value(10,.10,.03,.08)
assert isclose(base['value'],140)
assert stable_value(10,.06,.03,.08)['value']<stable_value(10,.06,0,.08)['value']
assert isclose(stable_value(10,.08,.03,.08)['value'],125)
print({'稳定模型亿元':base})

# %% 终值时点与期间利率
constant=discounted([8,9],[.08,.08],9*1.03/(.08-.03))
changing=discounted([8,9],[.08,.09],9*1.03/(.09-.03))
assert isclose(constant['value'],174.074074074074)
print({'恒定成本':constant,'变动成本':changing,'原例终值占比':constant['terminal_pv']/constant['value']})

# %% 经营和股权两条路
fin=perpetual_financing(12,40,.05,.25,.10)
assert isclose(fin['equity'],105) and isclose(12/fin['wacc']-40,105)
print({'融资一致性':fin,'权利桥亿元':equity_bridge(180,[20,15],[50,10,12,8,5],10)})
