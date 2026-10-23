"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def equilibrium(G=20, money=40, c=.6, C0=20, T=20, I0=40,
                b=200, kappa=.5, h=400, spread=0,
                mode='money', target_rate=None, anchor_y=None, phi=0):
    values=(G,money,c,C0,T,I0,b,kappa,h,spread,phi)
    if any(not isfinite(v) for v in values) or not 0<c<1 or min(b,kappa,h)<=0 or money<0 or phi<0:
        raise ValueError('参数越界或非有限')
    autonomous=C0-c*T+I0+G
    if mode=='money':
        Y=(autonomous-b*spread+(b/h)*money)/(1-c+b*kappa/h)
        rate=(kappa*Y-money)/h
    elif mode=='rule':
        if target_rate is None or anchor_y is None or not all(isfinite(v) for v in (target_rate,anchor_y)):
            raise ValueError('反应规则需要固定的基准利率和产出')
        Y=(autonomous-b*(target_rate+spread)+b*phi*anchor_y)/(1-c+b*phi)
        rate=target_rate+phi*(Y-anchor_y)
    else:
        raise ValueError('未知政策闭合')
    C=C0+c*(Y-T); I=I0-b*(rate+spread); implied_money=kappa*Y-h*rate
    if min(Y,C,I,implied_money)<0:
        raise ValueError('线性解超出本模型非负总投资/消费/货币余额域')
    return dict(Y=Y,rate=rate,C=C,I=I,G=G,money=implied_money,
                goods_residual=Y-C-I-G)

def gap_model(demand=0, supply=0, eta=2, slope=.5):
    if any(not isfinite(v) for v in (demand,supply,eta,slope)) or eta<=0 or slope<=0:
        raise ValueError('冲击须有限，斜率须为正')
    y=(demand-eta*supply)/(1+eta*slope)
    inflation=slope*y+supply
    return dict(output_gap_pp=y,inflation_gap_pp=inflation)

# %% 双市场代回：总投资不能事后改成净投资
base=equilibrium(); fiscal=equilibrium(G=26.5)
assert isclose(base['Y'],135.3846153846154)
assert isclose(base['money'],40) and abs(base['goods_residual'])<1e-10
assert isclose(fiscal['Y']-base['Y'],10)
assert isclose(fiscal['rate']-base['rate'],.0125)
print({'基准':base,'固定货币财政扩张':fiscal})

# %% 固定利率、反应规则与信用利差
anchor=dict(mode='rule',target_rate=base['rate'],anchor_y=base['Y'])
pegged=equilibrium(G=26.5,**anchor)
reactive=equilibrium(G=26.5,phi=.001,**anchor)
credit=equilibrium(spread=.01,**anchor)
assert isclose(pegged['Y']-base['Y'],16.25)
assert isclose(pegged['money']-base['money'],8.125)
assert isclose(credit['Y']-base['Y'],-5)
assert fiscal['Y']<reactive['Y']<pegged['Y']
print({'固定利率':pegged,'反应规则':reactive,'利差冲击':credit})

# %% 两类冲击：相同通胀方向不是相同机制
demand=gap_model(demand=4); supply=gap_model(supply=2)
assert demand==dict(output_gap_pp=2,inflation_gap_pp=1)
assert supply==dict(output_gap_pp=-2,inflation_gap_pp=1)
try:
    equilibrium(c=.8,I0=30,b=1000,h=1000,money=20)
except ValueError:
    print('已拒绝旧参数的负总固定投资解；不改名、不截零')
else:
    raise AssertionError('投资口径边界失效')
print({'需求冲击':demand,'供给冲击':supply,'单位':'缺口百分点'})
