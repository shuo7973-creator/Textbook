"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose, isfinite

def profitability(oi,nfe,noa,nfo):
    if any(not isfinite(x) for x in (oi,nfe,noa,nfo)) or noa<=0 or noa-nfo<=0:
        raise ValueError('本教学比较只接受正NOA与正权益，其他情形另作金额分析')
    equity=noa-nfo; rnoa=oi/noa
    leverage_effect=(rnoa*nfo-nfe)/equity
    return dict(rnoa=rnoa,roe=(oi-nfe)/equity,leverage_effect=leverage_effect,
                nbc=None if nfo==0 else nfe/nfo,flev=nfo/equity)

def operating_leverage(oa,ol,oi,benchmark):
    if any(not isfinite(x) for x in (oa,ol,oi,benchmark)) or not 0<=ol<oa or benchmark<0:
        raise ValueError('经营资产须超过非负经营负债，基准率非负')
    noa=oa-ol; rooa=(oi+benchmark*ol)/oa
    return dict(rooa=rooa,rnoa=oi/noa,olleverage=ol/noa,
                effect=ol/noa*(rooa-benchmark))

def weighted_capital(segments):
    if not segments or any(not isfinite(v) or not isfinite(w) or v<0 or w<=0 for v,w in segments):
        raise ValueError('资本非负，每段时长正且有限')
    return sum(v*w for v,w in segments)/sum(w for v,w in segments)

def margin_turnover(pm0,pm1,ato0,ato1):
    if any(not isfinite(x) for x in (pm0,pm1,ato0,ato1)) or min(ato0,ato1)<0:
        raise ValueError('输入有限，周转非负；利润率可为负')
    return dict(margin=(pm1-pm0)*(ato0+ato1)/2,
                turnover=(ato1-ato0)*(pm0+pm1)/2,total=pm1*ato1-pm0*ato0)

# %% 基准、零净债务及净金融资产
base=profitability(22.5,3,94,26.75)
zero=profitability(12,1,100,0); net_asset=profitability(12,-.6,100,-20)
assert isclose(base['roe'],base['rnoa']+base['leverage_effect'])
assert zero['nbc'] is None and isclose(zero['roe'],.11)
assert isclose(net_asset['roe'],.105)
print({'Y1回报':base,'零净债务':zero,'净金融资产':net_asset})

# %% 经营负债杠杆与资本暴露时间
op=operating_leverage(120,30,15,.04)
assert isclose(op['rnoa'],op['rooa']+op['effect'])
weighted=weighted_capital([(100,9),(220,3)])
assert weighted==130
print({'经营负债分解':op,'时间加权资本':weighted,'两种回报':(26/130,26/160)})

# %% 描述性归因与现金/经济利润两条估值
effects=margin_turnover(.15,.12,1.6,2)
assert isclose(effects['margin']+effects['turnover'],effects['total'],abs_tol=1e-12)
dcf=-100+60/1.1+60/1.1**2
ep=[10-.1*100,10-.1*50]
assert isclose(dcf,ep[0]/1.1+ep[1]/1.1**2)
print({'回报变化贡献':effects,'两年项目NPV':dcf,'期初资本收费的EP':ep})
