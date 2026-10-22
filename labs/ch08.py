"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
def equilibrium(G, real_money=20):
    Y=(20-.8*20+30+G+real_money)/(.2+.5)
    i=(.5*Y-real_money)/1000
    return Y,i
y0,i0=equilibrium(20); y1,i1=equilibrium(27)
assert isclose(y1-y0,10) and isclose(i1-i0,.005)
assert isclose(y0,20+.8*(y0-20)+30-1000*i0+20)
print({'基准':(y0,i0),'财政扩张':(y1,i1),'财政乘数':(y1-y0)/7})
