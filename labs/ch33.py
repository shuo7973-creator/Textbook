"""本章独立离线实验：全部输入为假设数据。"""

from math import prod, isclose, sqrt
from statistics import stdev
months=[.01]*11+[-.10]
skip=prod(1+r for r in months[:-1])-1
full=prod(1+r for r in months)-1
vol=stdev(months)*sqrt(12)
assert isclose(skip,.1156683466653166)
assert isclose(full,.004101511998785)
assert skip>full and vol>0
print({'跳过最近月动量':skip,'完整窗口':full,'月波动年化近似':vol})
