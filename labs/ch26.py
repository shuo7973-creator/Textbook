"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
nopat=10; roic=.10; g=.03; wacc=.08
fcff=nopat*(1-g/roic); value=fcff/(wacc-g)
tv=9*1.03/(.08-.03); explicit=8/1.08+(9+tv)/1.08**2
assert isclose(value,140) and isclose(explicit,174.074074074074)
assert isclose((value+20-50)/10,11)
print({'稳定FCFF':fcff,'经营价值':value,'两阶段价值':explicit,'每股元':11})
