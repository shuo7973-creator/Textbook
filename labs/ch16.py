"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
cash=10; rate=.1; years=3
direct=sum(cash/(1+rate)**t for t in range(1,years+1))
annuity=cash*(1-(1+rate)**(-years))/rate
due=annuity*(1+rate)
nominal=(1.03*1.02)-1
assert isclose(direct,annuity)
assert isclose(102/(1+nominal),100/1.03)
print({'普通年金':annuity,'先付年金':due,'有效年率':1.01**12-1,'名义利率':nominal})
