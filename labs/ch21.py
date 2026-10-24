"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose, isfinite

def historical_y1(interest_in_cfo=False):
    ni=(150-90-30-4)*.75
    received=150-(25-20)
    paid=(90+30-6)+(32-30)-(23-20)
    cfo=received-paid-6.5-(4 if interest_in_cfo else 0)
    cff=2-5-(0 if interest_in_cfo else 4)
    cash=10+cfo-10+cff
    ppe=60+10-6; equity=60+ni-5
    return dict(ni=ni,cfo=cfo,cfi=-10,cff=cff,cash=cash,ppe=ppe,
                equity=equity,assets=cash+25+32+ppe,claims=23+42+equity)

def equity_roll(begin,ni,oci=0,issue=0,buyback=0,dividend=0):
    if any(not isfinite(x) for x in (begin,ni,oci,issue,buyback,dividend)) or min(issue,buyback,dividend)<0:
        raise ValueError('金额有限，发行回购分红非负；亏损和负权益可以出现')
    return begin+ni+oci+issue-buyback-dividend

def simple_consolidation(parent_cash,investment,sub_assets,sub_debt,share):
    vals=(parent_cash,investment,sub_assets,sub_debt,share)
    if any(not isfinite(x) for x in vals) or min(vals)<0 or share>1 or sub_assets<sub_debt:
        raise ValueError('本例金额非负，持股0至1，子公司净资产非负')
    sub_equity=sub_assets-sub_debt
    if not isclose(investment,share*sub_equity):
        raise ValueError('本例仅处理无商誉、投资恰等于所占净资产的情况')
    # 控制已成立是题设，不从share自动推断控制。
    return dict(assets=parent_cash+sub_assets,debt=sub_debt,
                parent_equity=parent_cash+investment,nci=(1-share)*sub_equity)

def internal_goods(cost,transfer,external_revenue,sold_fraction):
    if any(not isfinite(x) for x in (cost,transfer,external_revenue,sold_fraction)) or min(cost,external_revenue)<0 or transfer<cost or not 0<=sold_fraction<=1:
        raise ValueError('无内部亏损/减值模型，数量销售比例须0至1')
    standalone_profit=transfer-cost+external_revenue-transfer*sold_fraction
    unrealized=(transfer-cost)*(1-sold_fraction)
    return dict(profit=standalone_profit-unrealized,
                inventory=cost*(1-sold_fraction),eliminated_profit=unrealized,
                revenue=external_revenue)

# %% 直接收付与三表勾稽
base=historical_y1(); alternative=historical_y1(True)
assert base['cfo']==25.5 and base['cff']==-7
assert base['cash']==18.5 and base['assets']==base['claims']==139.5
assert base['cash']==alternative['cash']
print({'一般企业现金分类':base,'利息后分析现金':alternative['cfo']})

# %% 控制后全额并表，再分少数股东
c=simple_consolidation(50,48,100,40,.8)
assert isclose(c['assets'],c['debt']+c['parent_equity']+c['nci'])
print({'合并资产负债亿元':c,'利润归属':{'合并':22,'归母':20,'少数':2}})

# %% 内部利润抵销与完整权益滚动
g=internal_goods(80,120,90,.6)
assert isclose(g['profit'],42) and isclose(g['inventory'],32)
assert equity_roll(60,19.5,-2,7,3,5)==76.5
print({'内部交易抵销万元':g,'完整期末权益亿元':76.5})
