"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
S,idom,ifor=7,.02,.05
F=S*(1+idom)/(1+ifor)
pv_foreign=100/(1+ifor)*S
pv_hedged=100*F/(1+idom)
assert isclose(F,6.8) and isclose(pv_foreign,pv_hedged)
unhedged=[100*s for s in [6.4,7.4]]
print({'远期汇率':F,'两路径本币现值':(pv_foreign,pv_hedged),'未套保':unhedged,'套保固定':100*F})
