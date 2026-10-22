"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
spend=12; life=3
amort=spend/life; carrying=spend-amort
earnings_difference=spend-amort
accrual=(20-8)/100
assert carrying==earnings_difference==8 and isclose(accrual,.12)
assert sum([amort]*life)==spend
print({'第一年资本化相对利润':earnings_difference,'期末资产':carrying,'应计率':accrual,'三年总费用':spend})
