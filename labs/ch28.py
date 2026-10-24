"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def justified_multiples(roe,g,ke):
    if any(not isfinite(x) for x in (roe,g,ke)) or roe<=0 or not 0<=g<ke or g>roe:
        raise ValueError('本稳态模型要求正ROE、可分配且收敛')
    payout=1-g/roe; pe=payout/(ke-g)
    return dict(payout=payout,forward_pe=pe,trailing_pe=pe*(1+g),pb=roe*pe)

def forward_ev_sales(margin,tax,roc,g,k):
    if any(not isfinite(x) for x in (margin,tax,roc,g,k)) or not 0<margin<=1 or not 0<=tax<1 or roc<=0 or not 0<=g<k or g>roc:
        raise ValueError('正利润成熟期参数超域')
    return margin*(1-tax)*(1-g/roc)/(k-g)

def aggregate_pe(caps,earnings):
    if not caps or len(caps)!=len(earnings) or any(not isfinite(x) for x in [*caps,*earnings]) or any(x<=0 for x in caps):
        raise ValueError('市值正且向量一致')
    total=sum(earnings)
    if total<=0: raise ValueError('整体利润非正，不输出可排序PE')
    return sum(caps)/total

def positive_pe_weights(caps,earnings):
    if any(e<=0 for e in earnings): raise ValueError('正权重演示不含亏损或零利润')
    total_pe=aggregate_pe(caps,earnings)
    pe=[m/e for m,e in zip(caps,earnings)]
    arithmetic=sum(m/sum(caps)*p for m,p in zip(caps,pe))
    harmonic=1/sum(m/sum(caps)/p for m,p in zip(caps,pe))
    profit_weighted=sum(e/sum(earnings)*p for e,p in zip(earnings,pe))
    return dict(aggregate=total_pe,cap_arithmetic=arithmetic,cap_harmonic=harmonic,profit_weighted=profit_weighted)

# %% 前瞻、历史与权益分母
x=justified_multiples(.15,.03,.10)
assert isclose(x['pb'],12/7) and isclose(x['forward_pe'],80/7)
assert isclose(forward_ev_sales(.15,.25,.15,.03,.09),1.5)
print({'稳态倍数':x,'经营收入倍数':1.5})

# %% 加总与正权重平均
weights=positive_pe_weights([100,200],[10,5])
assert weights['aggregate']==weights['profit_weighted']==20
assert isclose(weights['cap_harmonic'],20) and isclose(weights['cap_arithmetic'],30)
assert aggregate_pe([100,200],[10,-5])==60
print({'正利润汇总':weights,'含亏损整体PE':60})

# %% 相同现金的租赁展示
before=130/20; after=(130+60)/(20+12)
assert before==6.5 and after==5.9375
print({'经营租金口径':before,'融资租赁分析口径':after,'备注':'索取价值60是另给假设，非由租金12推得'})
