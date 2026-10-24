"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite,isclose

def ratio(numerator,denominator):
    if not all(isfinite(x) for x in (numerator,denominator)) or denominator<=0:
        raise ValueError('比率要求有限输入和正分母，缺失须另记')
    return numerator/denominator

def factor_fields(book,market,ni,avg_equity,cfo,avg_assets,assets_now,assets_before):
    if book<=0: raise ValueError('常规B/M集合排除非正权益并记录')
    if not isfinite(assets_now) or assets_now<0: raise ValueError('总资产非负')
    return dict(bm=ratio(book,market),ep=ratio(ni,market),roe=ratio(ni,avg_equity),
                accrual=ratio(ni-cfo,avg_assets),investment=ratio(assets_now,assets_before)-1)

def profitability_definitions(revenue,cogs,sga,interest,book,minority,tax,avg_equity,noa):
    vals=(revenue,cogs,sga,interest,book,minority,tax,avg_equity,noa)
    if any(not isfinite(x) for x in vals) or min(revenue,cogs,sga,interest,minority)<0 or not 0<=tax<1:
        raise ValueError('教学输入域非法')
    ebit=revenue-cogs-sga
    if ebit<interest: raise ValueError('本例不建亏损税盾')
    return dict(op=ratio(ebit-interest,book+minority),roe=ratio((ebit-interest)*(1-tax),avg_equity),rnoa=ratio(ebit*(1-tax),noa))

def six_cell_spread(cells):
    keys={'SL','SN','SH','BL','BN','BH'}
    if set(cells)!=keys or any(not isfinite(r) or r< -1 for r in cells.values()): raise ValueError('六个同期间多头组合收益须齐全')
    high=(cells['SH']+cells['BH'])/2;low=(cells['SL']+cells['BL'])/2
    size=(cells['SL']+cells['SN']+cells['SH']-cells['BL']-cells['BN']-cells['BH'])/3
    return dict(high=high,low=low,spread=high-low,size_within_this_sort=size)

def rank_score(xs):
    if len(xs)<2 or any(x is None or not isfinite(x) for x in xs): raise ValueError('共同覆盖集合至少2个有限值')
    ordered=sorted(xs)
    ranks=[sum(i+1 for i,v in enumerate(ordered) if v==x)/ordered.count(x) for x in xs]
    return [(r-1)/(len(xs)-1) for r in ranks]

def composite(value,quality,weight=.5):
    if len(value)!=len(quality) or not isfinite(weight) or not 0<=weight<=1: raise ValueError('同样本与固定权重')
    a,b=rank_score(value),rank_score(quality)
    return [weight*x+(1-weight)*y for x,y in zip(a,b)]

# %% 定义相近不等于同一个因子
x=profitability_definitions(100,60,20,4,80,20,.25,80,75)
assert isclose(x['op'],.16) and isclose(x['roe'],.15) and isclose(x['rnoa'],.20)
print({'利润口径':x,'甲乙ROE融资差异':[10/100,7.5/50]})
# %% 六格组合的透明多空差；无融券与成本仿真
spread=six_cell_spread(dict(SL=.01,SN=.02,SH=.03,BL=.005,BN=.01,BH=.02))
assert isclose(spread['spread'],.0175)
print({'自定义六格':spread})
# %% 共同覆盖及事前固定合成
scores=composite([.5,1,1.5],[.2,.1,.15])
assert scores==[.5,.25,.75]
print({'A_B_C复合分数':scores,'财务特征':factor_fields(100,200,15,100,12,150,180,150)})
