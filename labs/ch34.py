"""本章独立离线实验：全部输入为假设数据。"""

from math import sqrt, isclose
def ranks(xs):
    return [sum(i+1 for i,v in enumerate(sorted(xs)) if v==x)/xs.count(x) for x in xs]
def corr(x,y):
    assert len(x)==len(y) and len(x)>1
    a=[v-sum(x)/len(x) for v in x]; b=[v-sum(y)/len(y) for v in y]
    den=sqrt(sum(v*v for v in a)*sum(v*v for v in b))
    if den==0: raise ValueError('常数列无相关系数')
    return sum(u*v for u,v in zip(a,b))/den
ic=corr(ranks([1,2,3,4]),ranks([.03,.01,.04,.02]))
residual=[1-2,3-2,10-12,14-12]
assert isclose(ic,0) and ranks([1,1,3])==[1.5,1.5,3]
assert sum(residual[:2])==sum(residual[2:])==0
print({'RankIC':ic,'行业残差':residual})
