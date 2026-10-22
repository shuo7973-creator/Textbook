"""本章独立离线实验：全部输入为假设数据。"""

from math import sqrt,isclose
w=.5; s1=.2; s2=.3; rho=.2
variance=w*w*s1*s1+(1-w)**2*s2*s2+2*w*(1-w)*rho*s1*s2
ke=.03+1.2*.05
wacc=.7*ke+.3*.05*(1-.25)
assert isclose(variance,.0385) and isclose(wacc,.07425)
print({'组合波动':sqrt(variance),'股权成本':ke,'WACC':wacc})
