"""本章独立离线实验：全部输入为假设数据。"""

from math import prod, isclose
# 每期特征在期初已知；returns仅在持仓确定后结算。全部为假设数据。
features=[[(.8,.6),(.4,.5)],[(.7,.8),(.5,.5)],[(.3,.4),(.9,.7)],[(.8,.7),(.4,.6)]]
returns=[(.04,.02),(-.03,.01),(.02,.01),(.02,.03)]
weights=[0.,0.]; wealth=1.; gross_wealth=1.; log=[]
for period,(rows,realized) in enumerate(zip(features,returns),1):
    scores=[.5*v+.5*q for v,q in rows]
    winner=max(range(2),key=lambda i:scores[i])
    target=[float(i==winner) for i in range(2)]
    traded=sum(abs(a-b) for a,b in zip(target,weights))
    cost=.001*traded; gross=realized[winner]
    wealth*=(1-cost)*(1+gross); gross_wealth*=1+gross
    log.append((period,winner,traded,cost,wealth)); weights=target
benchmark=prod(1+sum(row)/2 for row in returns)
assert [r[1] for r in log]==[0,0,1,0]
assert [r[2] for r in log]==[1.,0.,2.,2.]
assert isclose(gross_wealth,1.03926576) and wealth<gross_wealth
assert benchmark>wealth
print({'逐期账本':log,'净值':wealth,'毛净值':gross_wealth,'未计费等权参照':benchmark})
