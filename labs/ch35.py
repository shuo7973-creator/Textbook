"""本章独立离线实验：全部输入为假设数据。"""

from math import sqrt, isclose
a=.2**2; b=.3**2; c=.2*.2*.3
w=(b-c)/(a+b-2*c)
def variance(x): return x*x*a+(1-x)**2*b+2*x*(1-x)*c
v=variance(w); vol=sqrt(v)
rc1=w*(a*w+c*(1-w))/vol
rc2=(1-w)*(c*w+b*(1-w))/vol
assert isclose(w,.7358490566037735) and isclose(rc1+rc2,vol)
assert all(v<=variance(i/1000)+1e-12 for i in range(1001))
print({'资产1权重':w,'波动':vol,'风险贡献':[rc1,rc2]})
