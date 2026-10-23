"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose, log1p, expm1

def effective_rate(apr,m):
    if isinstance(m,bool) or not isinstance(m,int) or m<=0 or not isfinite(apr) or apr/m<=-1:
        raise ValueError('复利次数须为正整数，每期增长因子须正且有限')
    return expm1(m*log1p(apr/m))

def growing_annuity(c1,r,g,n):
    # 有限期直接求和，也覆盖r=g和非常接近的情形。
    if isinstance(n,bool) or not isinstance(n,int) or n<0:
        raise ValueError('期数须为非负整数')
    if any(not isfinite(x) for x in (c1,r,g)) or c1<0 or min(r,g)<=-1:
        raise ValueError('现金非负有限，两个增长因子正')
    return sum(c1*(1+g)**(t-1)/(1+r)**t for t in range(1,n+1))

def term_pv(cash,period_rates):
    if len(cash)!=len(period_rates) or not cash:
        raise ValueError('每期现金与单期率须非空等长')
    if any(not isfinite(x) for x in cash) or any(not isfinite(r) or r<=-1 for r in period_rates):
        raise ValueError('现金有限，单期增长因子正且有限')
    factor=1; result=0
    for cf,r in zip(cash,period_rates):
        factor*=1+r
        result+=cf/factor
    return result

def cash_bridge(ebit,depreciation,interest,tax,capex,delta_nwc,net_borrowing):
    values=(ebit,depreciation,interest,tax,capex,delta_nwc,net_borrowing)
    if any(not isfinite(x) for x in values) or min(depreciation,interest,capex)<0 or not 0<=tax<=1 or ebit<interest:
        raise ValueError('本例限制税前利润非负、利息税盾可用；参数需有限')
    ni=(ebit-interest)*(1-tax)
    cash_after_interest=ni+depreciation-delta_nwc
    fcff=ebit*(1-tax)+depreciation-capex-delta_nwc
    fcfe=ni+depreciation-capex-delta_nwc+net_borrowing
    return dict(ni=ni,cash_after_interest=cash_after_interest,fcff=fcff,fcfe=fcfe)

# %% 期间利率与有限增长年金：先画支付时间
equal=growing_annuity(10,.05,.05,3)
assert isclose(equal,30/1.05)
curve=term_pv([10,10,10],[.03,.04,.05])
print({'全部假设万元':True,'APR12%按月复利EAR':effective_rate(.12,12),'r等于g有限年金':equal,'期间曲线现值':curve})

# %% 现金桥：利润、融资前和权益现金分别核对
bridge=cash_bridge(40,10,10,.25,25,12,8)
assert bridge==dict(ni=22.5,cash_after_interest=20.5,fcff=3,fcfe=3.5)
assert isclose(bridge['cash_after_interest']+10*.75-25,bridge['fcff'])
assert isclose(bridge['fcff']-10*.75+8,bridge['fcfe'])
print(bridge)

# %% 名义实际：按确定价格路径逐期换算
real=[100,110,120]; infl=[.02,.03,.01]; rr=[.03,.04,.05]
prices=1; nominal=[]
for cf,pi in zip(real,infl):
    prices*=1+pi; nominal.append(cf*prices)
nr=[(1+r)*(1+pi)-1 for r,pi in zip(rr,infl)]
assert isclose(term_pv(real,rr),term_pv(nominal,nr))
print({'实际路径PV':term_pv(real,rr),'名义路径PV':term_pv(nominal,nr),'手续费后单期融资成本':105/98-1})
