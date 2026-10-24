"""本章独立离线实验：全部输入为假设数据。"""

from math import sqrt, isclose, isfinite

def covariance2(a,b,c):
    if any(not isfinite(x) for x in (a,b,c)) or a<0 or b<0 or c*c>a*b+1e-14*max(a*b,c*c,1e-300):
        raise ValueError('协方差矩阵须半正定')
    return a,b,c

def variance2(w,a,b,c):
    covariance2(a,b,c)
    if not isfinite(w): raise ValueError('权重须有限')
    return a*w*w+b*(1-w)**2+2*c*w*(1-w)

def bounded_minimum(a,b,c,lower=0,upper=1,reference=None,turnover=None):
    covariance2(a,b,c)
    if not all(isfinite(v) for v in (lower,upper)) or not 0<=lower<=upper<=1:
        raise ValueError('多头权重区间错误')
    if turnover is not None:
        if reference is None or not isfinite(reference) or not 0<=reference<=1 or not isfinite(turnover) or turnover<0:
            raise ValueError('换手需合法参照持仓')
        lower=max(lower,reference-turnover); upper=min(upper,reference+turnover)
    if lower>upper: raise ValueError('约束不可行')
    d=a+b-2*c
    if d<=1e-14*max(a,b,abs(c),1e-300):
        w=(lower+upper)/2; status='flat'
    else:
        w=min(upper,max(lower,(b-c)/d)); status='unique'
    return {'weight':w,'variance':variance2(w,a,b,c),'status':status,'interval':(lower,upper)}

def risk_contributions2(w,a,b,c):
    v=variance2(w,a,b,c)
    if v<=0: raise ValueError('零波动时贡献未定义')
    vol=sqrt(v)
    return [w*(a*w+c*(1-w))/vol,(1-w)*(c*w+b*(1-w))/vol]

def shrink2(a,b,c,lam):
    covariance2(a,b,c)
    if not isfinite(lam) or not 0<=lam<=1: raise ValueError('收缩强度0至1')
    return a,b,(1-lam)*c

def rebalance_values(holdings,target,fee):
    if len(holdings)!=len(target) or not holdings or any(not isfinite(x) or x<0 for x in list(holdings)+list(target)):
        raise ValueError('非负持仓与目标须配对')
    pre=sum(holdings)
    if pre<=0 or not isclose(sum(target),1,rel_tol=0,abs_tol=1e-12) or not isfinite(fee) or not 0<=fee<1:
        raise ValueError('正净值、满仓目标、0至1费率')
    lo=0.0; hi=pre
    for _ in range(100):
        mid=(lo+hi)/2
        residual=mid+fee*sum(abs(w*mid-h) for w,h in zip(target,holdings))-pre
        if residual>0: hi=mid
        else: lo=mid
    after=(lo+hi)/2; trades=[w*after-h for w,h in zip(target,holdings)]
    gross=sum(abs(x) for x in trades); cost=fee*gross
    return {'after':after,'trades':trades,'cost':cost,'gross':gross,'turnover':gross/(2*pre)}

# %% 无约束、多头上限与漂移换手限制
base=bounded_minimum(.04,.09,.012)
capped=bounded_minimum(.04,.09,.012,.2,.6)
limited=bounded_minimum(.04,.09,.012,.2,.6,6/11,.03)
assert isclose(base['weight'],39/53) and isclose(capped['weight'],.6)
assert isclose(limited['weight'],6/11+.03)
assert all(base['variance']<=variance2(i/1000,.04,.09,.012)+1e-12 for i in range(1001))
print({'最小风险':base,'权重上限':capped,'换手限制':limited})

# %% 两资产逆波动精确ERC；三资产反例，所用相关矩阵半正定
rc=risk_contributions2(.6,.04,.09,.012)
assert isclose(rc[0],rc[1])
weights=[6/11,3/11,2/11]; cov=[[.01,.016,0],[.016,.04,0],[0,0,.09]]
product=[sum(row[j]*weights[j] for j in range(3)) for row in cov]
variance=sum(w*x for w,x in zip(weights,product))
shares=[w*x/variance for w,x in zip(weights,product)]
assert all(isclose(x,y) for x,y in zip(shares,[9/23,9/23,5/23]))
print({'两资产RC':rc,'三资产逆波动风险占比':shares})

# %% 指定对角收缩，不称为最优Ledoit–Wolf估计
shrunk=bounded_minimum(*shrink2(.04,.09,.012,.5))
assert isclose(shrunk['weight'],42/59)
print({'对角收缩':shrunk})

# %% 万元：扣费后目标权重与资金守恒
ledger=rebalance_values([60,50],[.5,.5],.001)
assert isclose(ledger['after'],109.99) and isclose(ledger['cost'],.01)
assert isclose(sum(ledger['trades'])+ledger['cost'],0,abs_tol=1e-12)
print({'调仓账本万元':ledger})
