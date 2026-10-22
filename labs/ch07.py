"""本章独立离线实验：全部输入为假设数据。"""

from math import sqrt,isclose
def steady(s,delta): return (s/delta)**2
k=1.; path=[k]
for _ in range(1000):
    k=.9*k+.2*sqrt(k); path.append(k)
assert isclose(k,4,rel_tol=1e-8)
assert isclose(steady(.3,.1),9)
residual=.05-.4*.06-.6*.01
print({'k前五期':path[:5],'稳态':k,'储蓄提高后稳态':steady(.3,.1),'生产率残差':residual})
