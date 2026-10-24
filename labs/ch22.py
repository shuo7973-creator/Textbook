"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose, isfinite

def reformulate(cash,ar,inventory,ppe,ap,debt,equity,operating_cash=0):
    vals=(cash,ar,inventory,ppe,ap,debt,equity,operating_cash)
    if any(not isfinite(x) for x in vals) or min(cash,ar,inventory,ppe,ap,debt,operating_cash)<0 or operating_cash>cash:
        raise ValueError('金额有限，经营现金不能超过现金，负权益允许')
    if not isclose(cash+ar+inventory+ppe,ap+debt+equity):
        raise ValueError('原始资产负债表不平衡')
    noa=ar+inventory+ppe+operating_cash-ap
    nfo=debt-(cash-operating_cash)
    return dict(noa=noa,nfo=nfo,equity=noa-nfo)

def allocate_tax(ebit,interest,financial_income,operating_rate,income_rate):
    vals=(ebit,interest,financial_income,operating_rate,income_rate)
    if any(not isfinite(x) for x in vals) or min(interest,financial_income)<0 or ebit<interest or not 0<=operating_rate<=1 or not 0<=income_rate<=1:
        raise ValueError('本例税前经营所得覆盖利息，税率0至1且税盾当期可用')
    operating_tax=ebit*operating_rate
    shield=interest*operating_rate; finance_tax=financial_income*income_rate
    total_tax=operating_tax-shield+finance_tax
    oi=ebit-operating_tax
    nfe=interest-shield-financial_income+finance_tax
    return dict(oi=oi,nfe=nfe,ni=oi-nfe,total_tax=total_tax)

def cash_from_noa(oi,noa0,noa1,noncash_outside_income=0):
    if any(not isfinite(x) for x in (oi,noa0,noa1,noncash_outside_income)):
        raise ValueError('桥接输入必须有限')
    return oi+noncash_outside_income-(noa1-noa0)

def fcff_from_cfo(cfo,capex,interest,tax,interest_in_cfo=False):
    if any(not isfinite(x) for x in (cfo,capex,interest,tax)) or min(capex,interest)<0 or not 0<=tax<=1:
        raise ValueError('本例资本开支和利息非负，税盾率0至1')
    return cfo-capex+(interest*(1-tax) if interest_in_cfo else -interest*tax)

# %% 分类不改变权益，经营现金改变NOA及NFO
y0=reformulate(10,20,30,60,20,40,60)
y1=reformulate(18.5,25,32,64,23,42,74.5)
shift=reformulate(18.5,25,32,64,23,42,74.5,5)
assert y1['noa']==98 and y1['nfo']==23.5
assert shift['noa']==103 and shift['nfo']==28.5
print({'Y0':y0,'Y1':y1,'保留经营现金5':shift})

# %% 税分配与两种报表现金分类
tax=allocate_tax(30,4,2,.25,.2)
assert isclose(tax['ni'],21.1) and isclose(tax['total_tax'],6.9)
assert fcff_from_cfo(25.5,10,4,.25)==14.5
assert fcff_from_cfo(21.5,10,4,.25,True)==14.5
print({'独立税例万元':tax,'基准FCFF亿元':14.5})

# %% OCI、损失、非现金租赁与现金投资不能同样加回
values=[cash_from_noa(22.5,90,103,5),cash_from_noa(17.5,90,93),
        cash_from_noa(0,100,120,20),cash_from_noa(0,100,115)]
assert values==[14.5,14.5,0,-15]
assert 5+3-(23.5-30)==14.5
print({'四个独立桥接结果':values,'股东分配加融资费用减净债务变化':14.5})
