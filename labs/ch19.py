"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
VU,D,T=200,80,.25
VL=VU+T*D
fair=(100+2*10)/(10+2)
discounted=(100+2*8)/(10+2)
acquisition_npv=50+15-5-65
assert VL==220 and fair==10 and isclose(discounted,116/12)
assert acquisition_npv==-5
print({'含税盾价值':VL,'公允增发每股':fair,'折价增发每股':discounted,'并购NPV':acquisition_npv})
