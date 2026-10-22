"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
b0=100; ni1=12; d1=4; ke=.10; b1=b0+ni1-d1
ni2=10.8; liquidation=b1+ni2
ddm=d1/(1+ke)+liquidation/(1+ke)**2
ri=b0+(ni1-ke*b0)/(1+ke)+(ni2-ke*b1)/(1+ke)**2
assert isclose(ddm,ri) and isclose(ri,101.81818181818)
assert isclose(100+(12-.08*100)/.08,12/.08)
print({'股利价值':ddm,'剩余收益价值':ri,'经营价值':150})
