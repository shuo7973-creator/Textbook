"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose, isfinite

def revenue_driver(quantity,price,capacity):
    if any(not isfinite(x) or x<0 for x in (quantity,price,capacity)) or quantity>capacity:
        raise ValueError('本例无外包和期初成品，销量不能超过可用产能')
    return quantity*price

def required_borrowing(cash_before,minimum,rate,tax,exposure,capacity):
    vals=(cash_before,minimum,rate,tax,exposure,capacity)
    if any(not isfinite(x) for x in vals) or min(minimum,rate,capacity)<0 or not 0<=tax<=1 or not 0<=exposure<=1:
        raise ValueError('输入有限，税率和年度暴露比例0至1')
    factor=1-(1-tax)*rate*exposure
    if factor<=0: raise ValueError('融资反馈系数不满足本线性解条件')
    draw=max(0,minimum-cash_before)/factor
    if draw>capacity+1e-10: raise ValueError('可提款额度不足，不能虚构借款闭合现金')
    return draw

def forecast(revenue=165,variable_ratio=.6,ar=None,inventory=35.2,ap=25.3,
             minimum=15,capacity=10,exposure=.5):
    if ar is None: ar=revenue/6
    vals=(revenue,variable_ratio,ar,inventory,ap,minimum,capacity,exposure)
    if any(not isfinite(x) for x in vals) or min(revenue,variable_ratio,ar,inventory,ap)<0:
        raise ValueError('教学经营输入有限且非负')
    # 亿人民币，完整Y2；固定现金经营费用26、折旧7、资本开支12、分红6。
    ebit=revenue*(1-variable_ratio)-26-7
    tax=.25; rate=.05; old_interest=42*rate
    if ebit<old_interest: raise ValueError('本例要求利息税盾可当期利用，亏损另建模型')
    dnwc=ar+inventory-ap-34
    ni_without_new=(ebit-old_interest)*(1-tax)
    cash_before=18.5+ni_without_new+7-dnwc-12-6
    draw=required_borrowing(cash_before,minimum,rate,tax,exposure,capacity)
    interest=old_interest+rate*exposure*draw
    if ebit<interest: raise ValueError('新增利息导致亏损，税模型超域')
    ni=(ebit-interest)*(1-tax)
    cfo=ni+7+interest-dnwc  # 支付利息列筹资，现金税等于当期税费用。
    cfi=-12; cff=draw-interest-6
    cash=18.5+cfo+cfi+cff
    ppe=64+12-7; debt=42+draw; equity=74.5+ni-6
    noa=ar+inventory+ppe-ap
    fcff=ebit*(1-tax)+7-12-dnwc
    assets=cash+ar+inventory+ppe; claims=ap+debt+equity
    if not isclose(assets,claims,abs_tol=1e-9): raise AssertionError('三表不平')
    if not isclose(fcff,ebit*(1-tax)-(noa-98),abs_tol=1e-9): raise AssertionError('NOA桥不平')
    if not isclose(fcff,cfo-interest*tax-12,abs_tol=1e-9): raise AssertionError('CFO桥不平')
    return dict(revenue=revenue,ebit=ebit,ni=ni,interest=interest,ar=ar,
                delta_nwc=dnwc,cfo=cfo,cfi=cfi,cff=cff,cash=cash,cash_before=cash_before,
                draw=draw,debt=debt,equity=equity,noa=noa,fcff=fcff,assets=assets,claims=claims)

# %% 基准Y2：经营、财报现金与NOA三条路径
base=forecast()
assert isclose(base['cfo'],28.875) and isclose(base['cash'],27.275)
assert isclose(base['assets'],158.975) and isclose(base['fcff'],16.35)
print({'Y2基准亿元':base})

# %% 联合压力：资金约束与利息反馈
stress_ar=148.5*(1/6+20/365)
stress=forecast(148.5,.66,stress_ar)
assert isclose(stress['cash'],15) and isclose(stress['draw'],4.835145275281394)
assert stress['ni']>0 and stress['fcff']<0
print({'Y2压力亿元':stress})
try:
    forecast(148.5,.66,stress_ar,capacity=4)
except ValueError as exc:
    print({'额度4不可行':str(exc)})
else:
    raise AssertionError('不能用不存在的授信填现金')

# %% 业务上限、情景平均与稳态再投资
assert revenue_driver(100,2,120)==200
expected=.5*revenue_driver(80,1.2,120)+.5*revenue_driver(120,.8,120)
assert expected==96 and expected!=100*1
print({'期望收入万元':expected,'稳态NOPAT':12,'再投资':4,'FCFF':8,'次年增长':.04})
