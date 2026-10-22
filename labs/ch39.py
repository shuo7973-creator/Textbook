"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose
x=[-1,0,1]; y=[-2,0,2]
def ridge(lam):
    assert lam>=0
    return sum(a*b for a,b in zip(x,y))/(sum(a*a for a in x)+lam)
ols=ridge(0); regularized=ridge(2)
train_mse=lambda b: sum((v-b*u)**2 for u,v in zip(x,y))/len(x)
assert isclose(ols,2) and isclose(regularized,1)
assert isclose(train_mse(ols),0) and isclose(train_mse(regularized),2/3)
print({'OLS斜率':ols,'岭斜率':regularized,'OLS训练MSE':train_mse(ols),'岭训练MSE':train_mse(regularized)})
