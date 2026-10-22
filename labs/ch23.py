"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
noa,nfo,equity=94,26.75,67.25
rnoa=22.5/noa; nbc=3/nfo; flev=nfo/equity
roe=19.5/equity
assert isclose(roe,rnoa+flev*(rnoa-nbc))
assert isclose(rnoa,.15*(150/94))
ep=12-.08*100
assert ep==4
print({'RNOA':rnoa,'NBC':nbc,'FLEV':flev,'ROE':roe,'经济利润':ep})
