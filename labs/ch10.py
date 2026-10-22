"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
Y,C,G,I=1000,600,150,200
S=Y-C-G; NX=Y-C-I-G
real_depreciation=1.05/1.02-1
net0=(100-60)*7; net1=(100-60)*7.35
assert S-I==NX==50 and isclose(net1-net0,14)
print({'储蓄':S,'净出口':NX,'实际贬值':real_depreciation,'净外币流入折本币万元':(net0,net1)})
