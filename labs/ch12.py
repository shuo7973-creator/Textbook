"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
assets,liabilities,equity,rwa=100,92,8,80
loss=3; equity_after=equity-loss
ratio=equity_after/rwa; target_rwa=equity_after/.10
assert assets-loss==liabilities+equity_after
assert isclose(ratio,.0625) and target_rwa==50
collateral=100; haircut_ltv=.6
gap=60-collateral*.8*haircut_ltv
assert isclose(gap,12)
print({'损失后权益':equity_after,'资本率':ratio,'目标RWA':target_rwa,'融资缺口':gap})
