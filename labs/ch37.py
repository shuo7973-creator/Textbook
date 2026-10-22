"""本章独立离线实验：全部输入为假设数据。"""

from math import prod, isclose
r=[.1,-.1,.1]
cheat=prod(1+max(x,0) for x in r)
lagged=[0]+[int(x>0) for x in r[:-1]]
honest=prod(1+w*x for w,x in zip(lagged,r))
true_return=(1.2+0)/2-1
assert isclose(cheat,1.21) and isclose(honest,.9)
assert isclose(true_return,-.4)
print({'偷看未来财富':cheat,'滞后规则财富':honest,'完整股票池收益':true_return,'误报示例':1-.95**20})
