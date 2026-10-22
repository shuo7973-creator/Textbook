"""本章独立离线实验：全部输入为假设数据。"""

from statistics import mean, stdev
from math import sqrt, isclose
x=[.02,.04,-.01,.03]
m=mean(x); se=stdev(x)/sqrt(len(x))
ci=(m-3.182*se,m+3.182*se)
mixture=.6*.08+.4*(-.04)
false_positive=1-.95**20
assert isclose(m,.02) and isclose(mixture,.032)
assert ci[0]<0<ci[1] and false_positive>.6
print({'均值':m,'均值标准误':se,'正态假设t区间':ci,'混合均值':mixture,'20次误报概率':false_positive})
