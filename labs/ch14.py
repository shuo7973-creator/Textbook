"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
b=.6; i=.04; g=.06; pd=.02
next_b=(1+i)/(1+g)*b+pd
stabilizing_pd=b-(1+i)/(1+g)*b
saving=100*.005*(1-.25)
assert isclose(saving,.375) and next_b>b
print({'债务率':next_b,'稳定债务率允许初级赤字':stabilizing_pd,'全年税后节省':saving,'半年':saving/2})
