"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def reverse_growth(value,nopat,roc,cost):
    if any(not isfinite(x) for x in (value,nopat,roc,cost)) or min(value,nopat,roc,cost)<=0:
        raise ValueError('反推模型输入为有限正值')
    a=value-nopat/roc; c=value*cost-nopat
    scale=max(value,nopat/roc,1)
    if abs(a)<=1e-12*scale:
        status='unidentified' if abs(c)<=1e-12*max(value*cost,nopat,1) else 'no_solution'
        return dict(status=status,growth=None)
    g=c/a
    if not 0<=g<cost or g>roc: return dict(status='outside_domain',growth=g)
    reconstructed=nopat*(1-g/roc)/(cost-g)
    if not isclose(reconstructed,value,rel_tol=1e-9,abs_tol=1e-9): raise ArithmeticError('反推代回残差过大')
    return dict(status='identified',growth=g,reconstructed=reconstructed)

def weighted(values,probabilities):
    if not values or len(values)!=len(probabilities) or any(not isfinite(x) for x in [*values,*probabilities]):
        raise ValueError('有限、等长、非空')
    if any(p<0 for p in probabilities) or not isclose(sum(probabilities),1,rel_tol=0,abs_tol=1e-12):
        raise ValueError('本实验要求穷尽互斥状态且概率和1')
    return sum(v*p for v,p in zip(values,probabilities))

def risk_neutral_price(payoffs,q,rf):
    if not isfinite(rf) or rf<=-1: raise ValueError('无风险增长因子正')
    return weighted(payoffs,q)/(1+rf)

def limited_liability(asset_payoffs,face,q,rf):
    if not isfinite(face) or face<0 or any(not isfinite(x) or x<0 for x in asset_payoffs):
        raise ValueError('资产和承诺支付非负')
    equity=[max(a-face,0) for a in asset_payoffs]
    debt=[min(a,face) for a in asset_payoffs]
    return dict(equity=risk_neutral_price(equity,q,rf),debt=risk_neutral_price(debt,q,rf),
                assets=risk_neutral_price(asset_payoffs,q,rf))

def posterior_good(prior,likelihood_good,likelihood_bad):
    if any(not isfinite(x) or not 0<=x<=1 for x in (prior,likelihood_good,likelihood_bad)):
        raise ValueError('概率0至1')
    denominator=prior*likelihood_good+(1-prior)*likelihood_bad
    if denominator==0: raise ValueError('该信号在模型下不可能发生')
    return prior*likelihood_good/denominator

# %% 反向识别的四种状态
cases=[reverse_growth(140,10,.10,.08),reverse_growth(100,10,.10,.08),
       reverse_growth(100,10,.10,.10),reverse_growth(120,10,.10,.08)]
assert [x['status'] for x in cases]==['identified','no_solution','unidentified','outside_domain']
assert isclose(cases[0]['growth'],.03)
print({'反向增长':cases,'资本成本9%':reverse_growth(140,10,.10,.09)})

# %% 真实概率与市场状态权重
price=risk_neutral_price([60,160],[.7,.3],.05)
physical_mean=weighted([60,160],[.5,.5]); expected_return=physical_mean/price-1
assert isclose(price,600/7) and isclose(expected_return,17/60)
print({'价格万元':price,'物理期望':physical_mean,'相容必要回报':expected_return})

# %% 有限责任与价值守恒
claims=limited_liability([40,160],80,[.5,.5],.05)
assert isclose(claims['equity']+claims['debt'],claims['assets'])
assert isclose(claims['equity'],800/21)
print({'逐状态索取权万元':claims})

# %% 新证据更新概率，不篡改历史
posterior=posterior_good(.5,.8,.2)
assert isclose(posterior,.8)
summary=weighted([160,80],[posterior,1-posterior])
assert isclose(summary,144)
print({'后验好状态':posterior,'条件价值摘要万元':summary})
