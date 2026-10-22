"""本章独立离线实验：全部输入为假设数据。"""

from datetime import date
from math import isclose
cum = [20, 50, 81, 120]
quarters = [cum[0]] + [b-a for a,b in zip(cum, cum[1:])]
ttm = 120 + 72 - 50
versions = [(date(2024,4,20),100), (date(2024,8,1),95)]
cutoff = date(2024,6,1)
available = [row for row in versions if row[0] <= cutoff]
pit_value = max(available, key=lambda x:x[0])[1]
real_growth = 1.08/1.03-1
assert quarters == [20,30,31,39] and sum(quarters)==120
assert ttm==142 and pit_value==100
assert isclose((9+1-10)/10,0)
print({'单季':quarters,'TTM':ttm,'实时版本':pit_value,'实际增速':real_growth})
