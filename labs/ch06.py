"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
base_p=[2,5]; base_q=[10,4]; new_p=[3,6]; new_q=[12,5]
base=sum(p*q for p,q in zip(base_p,base_q))
nominal=sum(p*q for p,q in zip(new_p,new_q))
real=sum(p*q for p,q in zip(base_p,new_q))
cpi=sum(p*q for p,q in zip(new_p,base_q))/base
contributions=[3,2,1,-1]
assert base==40 and nominal==66 and real==49
assert isclose(real/base-1,.225) and sum(contributions)==5
print({'实际增长':real/base-1,'平减指数':nominal/real,'固定篮子指数':cpi,'季度1%年化':1.01**4-1})
