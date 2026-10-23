"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def mm_no_tax(vu,d,ku,kd):
    if any(not isfinite(x) for x in (vu,d,ku,kd)) or not 0<=d<vu or vu<=0:
        raise ValueError('企业价值为正且债务小于价值')
    equity=vu-d; ke=ku+(ku-kd)*d/equity
    return dict(equity=equity,ke=ke,wacc=equity/vu*ke+d/vu*kd)

def shield_value(begin_debt,kd,tax,discount):
    if not begin_debt or any(not isfinite(x) or x<0 for x in begin_debt) or any(not isfinite(x) for x in (kd,tax,discount)) or kd<0 or not 0<=tax<=1 or discount<=-1:
        raise ValueError('债务和利息非负，税率有效，折现因子正')
    shields=[d*kd*tax for d in begin_debt]
    return dict(shields=shields,pv=sum(cf/(1+discount)**t for t,cf in enumerate(shields,1)))

def repurchase(value,shares,cash,price):
    if any(not isfinite(x) for x in (value,shares,cash,price)) or value<=0 or shares<=0 or not 0<=cash<value or price<=0 or cash/price>=shares:
        raise ValueError('回购须保留正股数和正权益价值')
    bought=cash/price; left=shares-bought; before=value/shares
    return dict(bought=bought,left=left,price_after=(value-cash)/left,
                seller_gain=cash-bought*before,remaining_gain=(value-cash)-left*before)

def issue_value(value,shares,new_shares,issue_price,fee=0,project_npv=0):
    if any(not isfinite(x) for x in (value,shares,new_shares,issue_price,fee,project_npv)) or value<=0 or shares<=0 or new_shares<=0 or issue_price<=0 or fee<0:
        raise ValueError('价值股数和发行价为正，费用非负，输入有限')
    after=value+new_shares*issue_price-fee+project_npv
    if after<=0: raise ValueError('发行后权益价值须为正')
    return after/(shares+new_shares)

# %% 无税MM：股权风险调整抵消便宜债务
mm=mm_no_tax(200,80,.15,.05)
assert isclose(mm['ke'],13/60) and isclose(mm['wacc'],.15)
print({'假设万元无税MM':mm,'错误固定ke的WACC':.6*.15+.4*.05})

# %% 有限债务税盾与APV：按每期税盾折现
shield=shield_value([80,60,40,20],.05,.25,.05)
unlevered_npv=-100+sum(35/1.1**t for t in range(1,5))
apv=unlevered_npv+shield['pv']-1
assert shield['shields']==[1,.75,.5,.25]
print({'税盾万元':shield,'未杠杆NPV':unlevered_npv,'减融资费后APV':apv})

# %% 分配与发行：EPS和每股价值可能反向
outcomes={p:repurchase(100,10,20,p) for p in (8,10,12)}
for x in outcomes.values(): assert isclose(x['seller_gain']+x['remaining_gain'],0,abs_tol=1e-12)
eps=9.5/outcomes[12]['left']
issued=issue_value(100,10,2,8,1,6)
assert isclose(eps,1.14) and isclose(issued,121/12)
print({'万元与万股对应元每股':outcomes,'高价回购后EPS':eps,'含项目增发后每股价值':issued})
