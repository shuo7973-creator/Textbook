"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
roe=.15; g=.03; ke=.10; payout=1-g/roe
pe=payout/(ke-g); pb=roe*pe
ev=100+40-10
assert isclose(pe,11.42857142857) and isclose(pb,1.714285714286)
assert isclose(ev/20,6.5)
aggregate=(100+200)/(10+5); mean_pe=(100/10+200/5)/2
assert aggregate==20 and mean_pe==25
print({'前瞻PE':pe,'PB':pb,'EV_EBITDA':ev/20,'整体PE':aggregate,'平均PE':mean_pe})
