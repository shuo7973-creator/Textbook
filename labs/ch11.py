"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
cash_ratio,reserve_ratio=.2,.1
multiplier=(1+cash_ratio)/(cash_ratio+reserve_ratio)
A={'loan':100,'reserve':150,'deposit':200,'equity':50}
A['loan']+=100; A['deposit']+=100
assert A['loan']+A['reserve']==A['deposit']+A['equity']
A['reserve']-=100; A['deposit']-=100
assert A['loan']+A['reserve']==A['deposit']+A['equity']
assert isclose(multiplier,4)
print({'示意乘数':multiplier,'付款后银行A':A,'银行B准备金与存款增量':100})
