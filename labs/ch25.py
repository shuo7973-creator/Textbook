"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
revenue=165; ebit=.2*revenue; interest=42*.05
ni=(ebit-interest)*.75
delta_nwc=(27.5+35.2-25.3)-(25+32-23)
cfo=ni+7-delta_nwc
cash=18.5+cfo-12-6
ppe=64+12-7; equity=74.5+ni-6
fcff=ebit*.75+7-12-delta_nwc
assets=cash+27.5+35.2+ppe
assert isclose(assets,25.3+42+equity)
assert isclose(fcff,16.35) and isclose(cash,27.275)
print({'NI':ni,'CFO':cfo,'现金':cash,'权益':equity,'资产':assets,'FCFF':fcff})
