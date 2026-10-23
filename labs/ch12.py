"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def interest_margin(a,l,ra,rl):
    if any(not isfinite(x) for x in (a,l,ra,rl)) or a<=0 or l<0:
        raise ValueError('平均生息资产为正，负债非负，参数有限')
    nii=a*ra-l*rl
    return dict(nii=nii,nim=nii/a,spread=ra-rl)

def repair_sale(e,rwa,k,h,w=1,available=None):
    # 所得现金用于偿还负债，故不再给现金赋RWA；只模拟给定权重资产。
    values=(e,rwa,k,h,w)
    if any(not isfinite(x) for x in values) or e<0 or rwa<=0 or not 0<k<=1 or not 0<=h<1 or w<=0:
        raise ValueError('资本、风险权重、折价和目标超出教学域')
    if available is not None and (not isfinite(available) or available<0):
        raise ValueError('可卖资产必须非负有限')
    shortage=k*rwa-e
    if shortage<=0:
        return dict(sale=0,equity=e,rwa=rwa,ratio=e/rwa)
    if k*w<=h:
        raise ValueError('该处置无法修复资本缺口')
    x=shortage/(k*w-h)
    if rwa-w*x<=0 or e-h*x<0 or (available is not None and x>available):
        raise ValueError('处置解不可行')
    return dict(sale=x,equity=e-h*x,rwa=rwa-w*x,ratio=(e-h*x)/(rwa-w*x))

def liquidity_sale(cash,outflow,securities,h):
    if any(not isfinite(x) or x<0 for x in (cash,outflow,securities,h)) or h>=1:
        raise ValueError('金额非负、有限，折价小于1')
    need=max(0,outflow-cash)
    sold=min(securities,need/(1-h))
    raised=sold*(1-h)
    return dict(sold=sold,loss=sold*h,gap=max(0,need-raised),cash=max(0,cash+raised-outflow))

# %% 平均余额与重定价：净息差并非净利差
base=interest_margin(100,90,.05,.02)
delta=-100*.6*.005+90*.4*.003*.5
assert isclose(base['nii']+delta,2.954)
print({'假设亿元基准':base,'全年NII变化亿元':delta})

# %% 资本处置：解出折价后的真实出售量
repair=repair_sale(5,80,.1,.02,available=60)
assert isclose(repair['sale'],37.5) and isclose(repair['ratio'],.1)
print({'条件资本修复':repair,'错用出售30后的资本率':(5-.02*30)/(80-30)})

# %% 支付与损失：不能用正权益代替可支付现金
liq=liquidity_sale(10,25,40,.1)
assert isclose(liq['loss'],5/3) and liq['gap']==0
assert isclose(40-liq['sold']+50,67+8-liq['loss'])
short=liquidity_sale(10,25,10,.1)
assert isclose(short['gap'],6)
print({'证券充足':liq,'证券不足':short,'给定条件预期损失亿元':.02*.4*100})
