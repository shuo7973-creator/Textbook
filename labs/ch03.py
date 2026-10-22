"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
def returns(prices):
    if len(prices)<2 or any(p<=0 for p in prices):
        raise ValueError('需要至少两个正价格')
    return [b/a-1 for a,b in zip(prices,prices[1:])]
prices=[100,110,99]
r=returns(prices)
wealth=100
for value in r: wealth*=1+value
x=[1,2,3,4,5]
rolling=[None,None]+[sum(x[i-2:i+1])/3 for i in range(2,len(x))]
lagged=[None]+rolling[:-1]
assert isclose(wealth,99) and isclose(sum(r),0,abs_tol=1e-12)
assert rolling==[None,None,2,3,4] and lagged[-1]==3
try: returns([100,0])
except ValueError: pass
else: raise AssertionError('未拦截非法价格')
print({'收益':r,'财富':wealth,'滚动':rolling,'开盘可用滞后值':lagged})
