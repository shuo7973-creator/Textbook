"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
noa0=20+30+60-20; noa1=25+32+64-23
nfo0=40-10; nfo1=42-18.5
oi=30*.75; nfe=4*.75
fcff=oi-(noa1-noa0)
assert noa0-nfo0==60 and isclose(noa1-nfo1,74.5)
assert isclose(oi-nfe,19.5) and isclose(fcff,14.5)
assert isclose(fcff,oi+6-10-4)
print({'NOA':(noa0,noa1),'NFO':(nfo0,nfo1),'OI':oi,'NFE':nfe,'FCFF':fcff})
