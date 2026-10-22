"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
ni=(150-90-30-4)*.75
cfo=ni+6-5-2+3
cash=10+cfo-10+2-5
ppe=60+10-6; equity=60+ni-5
assets=cash+25+32+ppe; claims=23+42+equity
assert isclose(ni,19.5) and isclose(cfo,21.5)
assert isclose(cash,18.5) and isclose(assets,claims)
print({'利润':ni,'CFO':cfo,'现金':cash,'资产':assets,'权益':equity})
