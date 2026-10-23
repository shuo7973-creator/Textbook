"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def working_bridge(ar0,inventory0,ap0,sales,purchases,cogs,collections,payments,loss=0):
    vals=(ar0,inventory0,ap0,sales,purchases,cogs,collections,payments,loss)
    if any(not isfinite(x) or x<0 for x in vals):
        raise ValueError('本商品模型全部输入须非负有限')
    ar=ar0+sales-collections-loss
    inv=inventory0+purchases-cogs; ap=ap0+purchases-payments
    if min(ar,inv,ap)<0:
        raise ValueError('应收、库存或应付超出可用余额')
    delta=(ar+inv-ap)-(ar0+inventory0-ap0)
    return dict(ar=ar,inventory=inv,ap=ap,delta_nwc=delta,
                profit=sales-cogs-loss,cash=collections-payments)

def funding_path(initial,receipts,payments,floor,capacity):
    if not receipts or len(receipts)!=len(payments):
        raise ValueError('月收付须非空等长')
    if any(not isfinite(x) or x<0 for x in [initial,floor,capacity]+receipts+payments) or initial<floor:
        raise ValueError('本例初始现金不低于底线，金额非负有限')
    # 计算必要融资，不限制为实际可用提款；超额处明确报告缺口。
    cash=initial; debt=0; rows=[]
    for t,(received,paid) in enumerate(zip(receipts,payments),1):
        before=cash+received-paid
        draw=max(0,floor-before)
        repay=min(debt,max(0,before-floor))
        debt+=draw-repay; cash=before+draw-repay
        rows.append(dict(month=t,required_debt=debt,conditional_cash=cash,
                         draw_needed=draw,repay=repay,gap=max(0,debt-capacity)))
    return rows

def retained_growth(roe,retention,denominator='begin'):
    if not isfinite(roe) or roe<0 or not isfinite(retention) or not 0<=retention<=1:
        raise ValueError('本例ROE非负有限，留存率在0至1')
    x=roe*retention
    if denominator=='begin': return x
    if denominator=='end': divisor=1-x
    elif denominator=='average': divisor=1-x/2
    else: raise ValueError('分母须为begin、end或average')
    if divisor<=0: raise ValueError('给定口径无法得到正有限期末权益')
    return x/divisor

def discount_cost(discount,early_day,net_day):
    if any(not isfinite(x) for x in (discount,early_day,net_day)) or not 0<discount<1 or not 0<=early_day<net_day:
        raise ValueError('折扣在0至1，付款日须前早后晚')
    span=net_day-early_day; period=discount/(1-discount)
    return dict(period=period,simple_annual=period*365/span,
                effective_annual=(1+period)**(365/span)-1)

# %% 净NWC与减值：同一调整只能处理一次
bridge=working_bridge(30,40,20,120,80,70,100,75,5)
assert bridge==dict(ar=45,inventory=50,ap=25,delta_nwc=20,profit=45,cash=25)
assert bridge['profit']-bridge['delta_nwc']==bridge['cash']
print({'假设商品企业万元':bridge,'用采购239算DPO天':18/239*365})

# %% 月度延迟：必要融资不是实际可用融资
base=funding_path(10,[40]*6,[35]*6,5,50)
stress=funding_path(10,[0,0,40,40,40,40],[35]*6,5,50)
assert max(row['required_debt'] for row in stress)==65
assert max(row['gap'] for row in stress)==15 and stress[-1]['required_debt']==45
assert base[-1]['conditional_cash']==40 and base[-1]['required_debt']==0
print({'回款延迟两个月路径':stress,'第7和8月待收万元':80})

# %% 增长与商业信用：先统一分母和期间
g0=retained_growth(20/100,.6,'begin')
g1=retained_growth(20/112,.6,'end')
ga=retained_growth(20/106,.6,'average')
assert isclose(g0,g1) and isclose(g1,ga)
print({'同一权益增长':(g0,g1,ga),'2/10 net30成本':discount_cost(.02,10,30),
       '按12%借20天付折扣价后的还款':98*(1+.12*20/365)})
