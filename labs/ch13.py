"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
cf=[5,105]; y=.04
def price(rate): return sum(c/(1+rate)**t for t,c in enumerate(cf,1))
p=price(y)
duration=sum(t*c/(1+y)**t for t,c in enumerate(cf,1))/p
modified=duration/(1+y)
convexity=sum(t*(t+1)*c/(1+y)**(t+2) for t,c in enumerate(cf,1))/p
forward=1.04**2/1.03-1
change=.001
approx=p*(1-modified*change+.5*convexity*change**2)
assert isclose(p,101.8860946745562)
assert abs(approx-price(y+change))<.00001
print({'债价':p,'Macaulay久期':duration,'修正久期':modified,'远期':forward,'真实与近似':(price(y+change),approx)})
