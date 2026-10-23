"""本章独立离线实验：全部输入为假设数据。"""

from math import sqrt, isclose, isfinite
from statistics import mean

def ols_one(x,y):
    if len(x)!=len(y) or len(x)<3 or any(not isfinite(v) for v in x+y):
        raise ValueError('需要至少3对有限数')
    xb,yb=mean(x),mean(y)
    sxx=sum((v-xb)**2 for v in x)
    if sxx==0:
        raise ValueError('常数解释变量不能识别斜率')
    beta=sum((a-xb)*(b-yb) for a,b in zip(x,y))/sxx
    alpha=yb-beta*xb
    residual=[b-alpha-beta*a for a,b in zip(x,y)]
    sse=sum(e*e for e in residual); s2=sse/(len(x)-2)
    return dict(alpha=alpha,beta=beta,residual=residual,sse=sse,s2=s2,
                se_beta=sqrt(s2/sxx),sxx=sxx,xbar=xb,n=len(x))

def ols_two(x,z,y):
    if len(x)!=len(z) or len(x)!=len(y) or len(x)<3:
        raise ValueError('两解释变量长度不一致或样本不足')
    if any(not isfinite(v) for values in (x,z,y) for v in values):
        raise ValueError('需要有限数')
    xc=[v-mean(x) for v in x]; zc=[v-mean(z) for v in z]; yc=[v-mean(y) for v in y]
    xx=sum(v*v for v in xc); zz=sum(v*v for v in zc); xz=sum(a*b for a,b in zip(xc,zc))
    xy=sum(a*b for a,b in zip(xc,yc)); zy=sum(a*b for a,b in zip(zc,yc))
    determinant=xx*zz-xz*xz
    if determinant<=1e-12*max(xx*zz,1e-30):
        raise ValueError('完全或近似共线，本教学解析器拒绝求解')
    beta=(xy*zz-zy*xz)/determinant; gamma=(zy*xx-xy*xz)/determinant
    alpha=mean(y)-beta*mean(x)-gamma*mean(z)
    return alpha,beta,gamma

# %% 手算OLS：高R平方与很宽的斜率区间可以同时出现
x=[1.,2.,3.]; y=[2.,3.,5.]; fit=ols_one(x,y)
critical=12.706 # df=1，双侧95%临界值的舍入值
interval=(fit['beta']-critical*fit['se_beta'],fit['beta']+critical*fit['se_beta'])
r2=1-fit['sse']/sum((v-mean(y))**2 for v in y)
assert isclose(fit['beta'],1.5) and isclose(fit['alpha'],1/3)
assert isclose(fit['sse'],1/6) and isclose(fit['se_beta'],sqrt(1/12))
assert isclose(sum(fit['residual']),0,abs_tol=1e-12)
assert isclose(sum(a*e for a,e in zip(x,fit['residual'])),0,abs_tol=1e-12)
assert interval[0]<0 and isclose(r2,27/28)
print({'OLS':fit,'R2':r2,'斜率区间':interval})

# %% 遗漏变量：已知模拟真关系，不等于现实自动可识别
x2=[1.,2.,3.,4.]; z=[1.,0.,2.,1.]
y2=[1+a+2*b for a,b in zip(x2,z)]
omitted=ols_one(x2,y2); full=ols_two(x2,z,y2)
assert isclose(omitted['beta'],1.4)
assert all(isclose(a,b) for a,b in zip(full,(1,1,2)))
assert isclose(sum(a*e for a,e in zip(x2,omitted['residual'])),0,abs_tol=1e-12)
print({'遗漏z斜率':omitted['beta'],'控制z后截距与系数':full})

# %% 差分中的差分：计算与反事实假设分开
treated_before,treated_after=50,65
control_before,control_after=40,45
did=(treated_after-treated_before)-(control_after-control_before)
assert did==10
print({'DiD':did,'解释条件':'无处理时两组趋势平行；无提前反应、溢出及同期差异冲击等'})
