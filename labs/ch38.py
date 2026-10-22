"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
from statistics import mean, stdev
eligible=[t for t in range(1,7) if t+2<7]
r=[.1,-.2,.1]; wealth=1.; peak=1.; dd=0.
for x in r:
    wealth*=1+x; peak=max(peak,wealth); dd=min(dd,wealth/peak-1)
assert eligible==[1,2,3,4]
assert isclose(wealth,.968) and isclose(dd,-.20)
print({'清除后训练月':eligible,'终值':wealth,'最大回撤':dd,'期均收益':mean(r),'样本波动':stdev(r)})
