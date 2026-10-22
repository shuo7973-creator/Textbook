"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
cashflows=[-110,65,90]; rate=.1
npv=sum(c/(1+rate)**t for t,c in enumerate(cashflows))
assert isclose(npv,23.471074380165277)
A=-10+12/1.1; B=-100+115/1.1
assert B>A
print({'扩产NPV':npv,'项目A':A,'项目B':B,'税后残值':20*(1-.25)})
