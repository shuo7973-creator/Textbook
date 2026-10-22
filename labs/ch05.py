"""本章独立离线实验：全部输入为假设数据。"""

from statistics import mean
from math import isclose
x=[1.,2.,3.]; y=[2.,3.,5.]
xbar=mean(x); ybar=mean(y)
beta=sum((a-xbar)*(b-ybar) for a,b in zip(x,y))/sum((a-xbar)**2 for a in x)
alpha=ybar-beta*xbar
residual=[b-alpha-beta*a for a,b in zip(x,y)]
sse=sum(e*e for e in residual)
r2=1-sse/sum((b-ybar)**2 for b in y)
assert isclose(beta,1.5) and isclose(alpha,1/3)
assert isclose(sse,1/6) and isclose(r2,27/28)
print({'截距':alpha,'斜率':beta,'残差':residual,'R2':r2,'x=4预测':alpha+4*beta})
