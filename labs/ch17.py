"""本章独立离线实验：全部输入为假设数据。"""

from itertools import product
from math import isfinite, isclose

def npv(cash,r):
    if not cash or any(not isfinite(c) for c in cash) or not isfinite(r) or r<=-1:
        raise ValueError('现金序列非空有限，年复利增长因子正')
    return sum(c/(1+r)**t for t,c in enumerate(cash))

def expansion(revenue=100):
    if not isfinite(revenue) or revenue<80:
        raise ValueError('本例要求EBIT非负；亏损税需另设模型')
    ocf=(revenue-30-50)*.75+50
    return [-110,ocf,ocf+20*(1-.25)+10]

def select_projects(projects,budget):
    # 小型离散教学枚举；NPV已含各项目初始成本，不再扣一次。
    if not isfinite(budget) or budget<0 or len(projects)>20:
        raise ValueError('预算非负有限，教学枚举最多20项')
    if any(not isfinite(c) or c<0 or not isfinite(v) for c,v in projects):
        raise ValueError('项目成本非负、NPV有限')
    best=dict(chosen=(),cost=0,value=0)
    for flags in product((0,1),repeat=len(projects)):
        cost=sum(f*c for f,(c,v) in zip(flags,projects))
        value=sum(f*v for f,(c,v) in zip(flags,projects))
        if cost<=budget and value>best['value']:
            best=dict(chosen=tuple(i for i,f in enumerate(flags) if f),cost=cost,value=value)
    return best

def delay_option(v_hi,v_lo,investment,q,rf,fee=0):
    if any(not isfinite(x) for x in (v_hi,v_lo,investment,q,rf,fee)) or min(v_hi,v_lo,investment,fee)<0 or v_hi<v_lo or not 0<=q<=1 or rf<=-1:
        raise ValueError('状态、风险中性概率与增长因子超域')
    option=(q*max(v_hi-investment,0)+(1-q)*max(v_lo-investment,0))/(1+rf)
    committed=(q*(v_hi-investment)+(1-q)*(v_lo-investment))/(1+rf)
    return dict(option=option,net=option-fee,committed=committed)

# %% 扩产现金与收入门槛：末期回收单列
base=expansion(); r=.1
ann=1/1.1+1/1.1**2
breakeven=(110+10*ann-25/1.1**2)/(.75*ann)
assert isclose(npv(base,r),23.471074380165277)
assert abs(npv(expansion(breakeven),r))<1e-10
print({'假设万元现金流':base,'NPV':npv(base,r),'两年各期收入门槛万元':breakeven})

# %% 非常规符号和不可分割项目：展示排序失效
unusual=[-100,230,-132]
assert abs(npv(unusual,.1))<1e-10 and abs(npv(unusual,.2))<1e-10
chosen=select_projects([(6,5),(5,4),(5,4)],10)
assert chosen['chosen']==(1,2) and chosen['value']==8
print({'NPV曲线':[(r,npv(unusual,r)) for r in (.05,.1,.15,.2,.25)],'组合最优':chosen})

# %% 延迟投资权：风险中性概率不是历史频率
option=delay_option(160,60,100,.5,.05,5)
assert isclose(option['option'],200/7) and isclose(option['net'],165/7)
print({'假设独占权价值万元':option,'灵活性相对承诺价值':option['option']-option['committed']})
