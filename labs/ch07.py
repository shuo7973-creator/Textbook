"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose, log

def parameters(s, delta, n, g, alpha):
    if any(not isfinite(v) for v in (s,delta,n,g,alpha)):
        raise ValueError('参数必须有限')
    if not 0<s<1 or not 0<=delta<=1 or not 0<alpha<1 or n<=-1 or g<=-1:
        raise ValueError('储蓄、折旧、弹性与增长参数越界')
    B=(1+n)*(1+g); D=B-(1-delta)
    if D<=0:
        raise ValueError('本例正稳态要求维持系数大于零')
    return B,D

def solow_step(k, s=.2, delta=.1, n=0, g=0, alpha=.5):
    B,_=parameters(s,delta,n,g,alpha)
    if not isfinite(k) or k<0:
        raise ValueError('资本必须非负且有限')
    return ((1-delta)*k+s*k**alpha)/B

def steady(s=.2, delta=.1, n=0, g=0, alpha=.5):
    B,D=parameters(s,delta,n,g,alpha)
    k=(s/D)**(1/(1-alpha)); y=k**alpha
    lam=(1-delta+alpha*D)/B
    return dict(k=k,y=y,c=(1-s)*y,B=B,D=D,local_factor=lam,
                half_life=log(.5)/log(lam) if 0<lam<1 else None,
                golden_k=(alpha/D)**(1/(1-alpha)))

def growth_residual(gy,gk,gl,alpha):
    if any(not isfinite(v) or v<=-1 for v in (gy,gk,gl)) or not isfinite(alpha) or not 0<alpha<1:
        raise ValueError('增长因子须为正，弹性须在0到1之间')
    exact=(1+gy)/((1+gk)**alpha*(1+gl)**(1-alpha))-1
    return dict(exact=exact,linear=gy-alpha*gk-(1-alpha)*gl)

# %% 原稳态与改革：本期消费先下降
base=steady(); reform=steady(s=.3)
assert isclose(base['k'],4) and isclose(reform['k'],9)
assert isclose(solow_step(4,s=.3),4.2)
print({'原稳态':base,'新稳态':reform,'改革当期消费':.7*4**.5})

# %% 多条收敛路径：零资本边界另列
paths={}
for initial in (1.,4.,9.):
    k=initial; path=[k]
    for _ in range(600):
        k=solow_step(k); path.append(k)
    assert isclose(k,4,rel_tol=1e-8)
    paths[initial]={'前五期':path[:5],'最后一期':k}
assert solow_step(0)==0
print({'正初始资本收敛':paths,'零资本是另一固定点':True})

# %% 有效劳动增长与TFP：离散率不等于对数率
extended=steady(s=.3,delta=.05,n=.01,g=.02)
assert isclose(solow_step(extended['k'],s=.3,delta=.05,n=.01,g=.02),extended['k'])
residual=growth_residual(.05,.06,.01,.4)
print({'含人口技术增长':extended,'TFP精确与近似':residual,
       '平衡路径总量增速':1.01*1.02-1,'人口下降例总量增速':.98*1.03-1})
