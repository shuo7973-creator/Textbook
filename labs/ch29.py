"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
pb=(.12-.04)/(.10-.04)
normal=100*(2-1.2)-40; peak=100*(2.5-1.2)-40
terminal=100*.10*15; pv=terminal/1.15**5-20/1.15**3
assert isclose(pb,4/3) and isclose(normal,40) and isclose(peak,90)
assert isclose(80+50-10-30,90)
print({'银行PB':pb,'正常EBIT':normal,'高点EBIT':peak,'成长净现值':pv,'分部权益':90})
