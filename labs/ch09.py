"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
y1,y2,r,beta=100,80,.1,1
wealth=y1+y2/(1+r)
c1=wealth/(1+beta); c2=beta*(1+r)*c1
saving=y1-c1
assert isclose(c2,95) and isclose(c1+c2/(1+r),wealth)
inventory=20+100-90
assert inventory==30
print({'财富现值':wealth,'两期消费':(c1,c2),'第一期储蓄':saving,'期末库存':inventory})
