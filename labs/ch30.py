"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
def implied_growth(v,n,r,k):
    if isclose(v,n/r): raise ValueError('不能由此式唯一识别')
    return (v*k-n)/(v-n/r)
g=implied_growth(140,10,.10,.08)
assert isclose(g,.03) and isclose(implied_growth(140,10,.10,.09),.065)
weighted=sum(p*v for p,v in zip([.25,.5,.25],[80,120,160]))
price_return=1.10*.95-1
assert weighted==120 and isclose(price_return,.045)
print({'隐含增长':g,'情景加权':weighted,'价格收益':price_return})
