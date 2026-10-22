"""本章独立离线实验：全部输入为假设数据。"""

from math import floor, isclose
cash=1000.; buy=10.; fee=.001
qty=floor(cash/(buy*(1+fee)))
cash-=qty*buy*(1+fee)
marked=cash+qty*11
cash+=qty*11*(1-fee)
assert qty==99 and isclose(marked,1098.01)
assert isclose(cash,1096.921)
assert isclose(cash/1000-1,.096921)
print({'股数':qty,'卖出前净值':marked,'最终现金':cash,'净收益':cash/1000-1})
