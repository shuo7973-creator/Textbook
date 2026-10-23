"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose, sqrt

def cashflows_ok(cf):
    if not cf or any(not isfinite(c) or c<0 for c in cf) or not any(c>0 for c in cf):
        raise ValueError('现金流须非负有限且至少一项为正')

def bond_price(cf,y):
    cashflows_ok(cf)
    if not isfinite(y) or y<=-1:
        raise ValueError('年复利收益率须大于−1且有限')
    return sum(c/(1+y)**t for t,c in enumerate(cf,1))

def risk(cf,y):
    p=bond_price(cf,y)
    dm=sum(t*c/(1+y)**t for t,c in enumerate(cf,1))/p
    conv=sum(t*(t+1)*c/(1+y)**(t+2) for t,c in enumerate(cf,1))/p
    return dict(price=p,macaulay=dm,modified=dm/(1+y),convexity=conv,dv01=p*dm/(1+y)*.0001)

def ytm(cf,p,low=-.9,high=1):
    cashflows_ok(cf)
    if not all(isfinite(x) for x in (p,low,high)) or p<=0 or not -1<low<high:
        raise ValueError('价格正且有限，搜索区间有效')
    if not bond_price(cf,high)<=p<=bond_price(cf,low):
        raise ValueError('搜索区间未包住解，请显式扩大区间')
    for _ in range(100):
        mid=(low+high)/2
        if bond_price(cf,mid)>p: low=mid
        else: high=mid
    return (low+high)/2

def bootstrap(rows):
    # 第n行恰好有n个年末支付，末项为正；输入全价。
    if not rows:
        raise ValueError('至少一只债券')
    d=[]
    for n,(cf,p) in enumerate(rows,1):
        cashflows_ok(cf)
        if len(cf)!=n or cf[-1]<=0 or not isfinite(p) or p<=0:
            raise ValueError('须为可逐期剥离的正价格三角系统')
        last=(p-sum(c*x for c,x in zip(cf[:-1],d)))/cf[-1]
        if last<=0 or not isfinite(last):
            raise ValueError('非正或非有限折现因子，核查输入')
        d.append(last)
    return d

def zero_reprice(value,years,old,new):
    if any(not isfinite(x) for x in (value,years,old,new)) or value<0 or years<=0 or min(old,new)<=-1:
        raise ValueError('零息债价值、期限与年复利收益率超域')
    return value*((1+old)/(1+new))**years

# %% 曲线剥离：用全精度价格，显示时再四舍五入
discounts=[1/1.03,1/1.04**2,1/1.045**3]
rows=[([103],100),([4,104],4*discounts[0]+104*discounts[1]),
      ([5,5,105],5*discounts[0]+5*discounts[1]+105*discounts[2])]
curve=bootstrap(rows)
assert all(isclose(a,b) for a,b in zip(curve,discounts))
print({'假设每面值100元价格':[p for cf,p in rows],
       '年复利即期率':[d**(-1/t)-1 for t,d in enumerate(curve,1)]})

# %% 久期和终点财富：两种风险不同
cf=[5,105]; y=.04; metrics=risk(cf,y); p=metrics['price']
h=.0001
finite_dv01=(bond_price(cf,y-h)-bond_price(cf,y+h))/2
assert abs(finite_dv01-metrics['dv01'])<1e-8
assert isclose(ytm(cf,p),y)
approx=p*(1-metrics['modified']*.001+.5*metrics['convexity']*.001**2)
assert abs(approx-bond_price(cf,.041))<1e-5
print({'利率风险':metrics,'零再投资实现年化':sqrt(110/p)-1,
       '4%再投资实现年化':sqrt(110.2/p)-1})

# %% 曲线扭转及风险中性信用：不把局部近似当完整风险
barbell=zero_reprice(50,1,.04,.05)+zero_reprice(50,3,.04,.03)
bullet=zero_reprice(100,2,.04,.04)
credit_price=(.98*105+.02*40)/1.03
credit_spread=105/credit_price-1-.03
assert bullet==100 and barbell>100
print({'同初始久期扭转后价值':(bullet,barbell),'风险中性教学债价':credit_price,
       '承诺YTM利差bp':credit_spread*10000})
