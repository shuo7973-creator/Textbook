"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
def nwc(revenue):
    cost=.6*revenue
    return revenue*30/365+cost*60/365-cost*30/365
base=nwc(365); growth=nwc(438)
funding=max(0,5-(10+40-45-8))
assert isclose(base,48) and isclose(growth-base,9.6)
assert funding==8
print({'NWC基准':base,'增长后':growth,'新增占款':growth-base,'最低融资需求':funding})
