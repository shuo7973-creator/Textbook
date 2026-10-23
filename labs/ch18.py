"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose, sqrt

def portfolio_variance(w,s1,s2,rho):
    if any(not isfinite(x) for x in (w,s1,s2,rho)) or min(s1,s2)<0 or not -1<=rho<=1:
        raise ValueError('波动非负，相关在−1至1，参数有限')
    return max(0,w*w*s1*s1+(1-w)**2*s2*s2+2*w*(1-w)*rho*s1*s2)

def min_variance_weight(s1,s2,rho,long_only=True):
    portfolio_variance(.5,s1,s2,rho)
    denominator=s1*s1+s2*s2-2*rho*s1*s2
    if denominator<=0:
        raise ValueError('不存在唯一最小方差权重')
    w=(s2*s2-rho*s1*s2)/denominator
    return min(1,max(0,w)) if long_only else w

def beta_fit(market,asset):
    if len(market)!=len(asset) or len(market)<3 or any(not isfinite(x) for x in market+asset):
        raise ValueError('同频超额收益须等长有限且至少3期')
    n=len(market); mx=sum(market)/n; my=sum(asset)/n
    sxx=sum((x-mx)**2 for x in market)
    if sxx<=0: raise ValueError('市场样本方差须正')
    beta=sum((x-mx)*(y-my) for x,y in zip(market,asset))/sxx
    alpha=my-beta*mx
    residual=[y-alpha-beta*x for x,y in zip(market,asset)]
    sse=sum(e*e for e in residual)
    return dict(beta=beta,alpha=alpha,market_var=sxx/(n-1),
                asset_var=sum((y-my)**2 for y in asset)/(n-1),residual_var=sse/(n-1),
                se=sqrt(sse/(n-2)/sxx))

def hamada_unlever(beta_l,de,tax):
    if any(not isfinite(x) for x in (beta_l,de,tax)) or de<0 or not 0<=tax<=1:
        raise ValueError('D/E非负，税率在0至1，参数有限')
    return beta_l/(1+(1-tax)*de)

def capital_cost(ke,kd,debt_weight,tax):
    if any(not isfinite(x) for x in (ke,kd,debt_weight,tax)) or not 0<=debt_weight<=1 or not 0<=tax<=1:
        raise ValueError('市场价值权重及可用税率在0至1')
    return (1-debt_weight)*ke+debt_weight*kd*(1-tax)

# %% 分散化：最小方差与等权比较
w=min_variance_weight(.2,.3,.2)
assert isclose(w,39/53)
print({'假设波动':True,'最小方差权重':w,'最小波动':sqrt(portfolio_variance(w,.2,.3,.2)),
       '等权波动':sqrt(portfolio_variance(.5,.2,.3,.2))})

# %% 样本beta：风险分解与标准误的分母不同
market=[-.04,-.02,0,.02,.04]; noise=[.01,-.02,.02,-.02,.01]
asset=[.01+1.2*x+e for x,e in zip(market,noise)]
fit=beta_fit(market,asset)
assert isclose(fit['beta'],1.2) and isclose(fit['alpha'],.01)
assert isclose(fit['asset_var'],fit['beta']**2*fit['market_var']+fit['residual_var'])
print({'仅5个月模拟数据':fit})

# %% 同行去杠杆：目标D/V不能当D/E
u=sum([hamada_unlever(1.2,.5,.25),hamada_unlever(1.5,1,.25)])/2
de=.3/.7; levered=u*(1+.75*de); ke=.03+levered*.05
wacc=capital_cost(.09,.05,.3,.25)
assert isclose(wacc,.07425)
print({'等权同行经营beta':u,'目标权益beta':levered,'假设年度ke':ke,'独立基准WACC':wacc})
