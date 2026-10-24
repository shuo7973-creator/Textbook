"""本章独立离线实验：全部输入为假设数据。"""

from math import isclose, isfinite

def research_cohorts(spending,life,tax=0):
    if isinstance(life,bool) or not isinstance(life,int) or life<=0 or not spending:
        raise ValueError('寿命为正整数，期初可用支出序列非空')
    if any(not isfinite(x) or x<0 for x in spending) or not isfinite(tax) or not 0<=tax<=1:
        raise ValueError('支出非负，税率0至1；本例税务当期全额扣除')
    asset=0; rows=[]
    for year,current in enumerate(spending):
        amort=sum(spending[max(0,year-life+1):year+1])/life
        asset+=current-amort
        if abs(asset)<1e-12: asset=0
        dtl=asset*tax
        rows.append(dict(amort=amort,asset=asset,dtl=dtl,net_asset=asset-dtl,
                         profit_adjustment=(current-amort)*(1-tax)))
    return rows

def cash_accrual(ni,cfo,average_assets):
    if any(not isfinite(x) for x in (ni,cfo,average_assets)) or average_assets<=0:
        raise ValueError('同范围输入有限，平均资产为正；缺失不可填零')
    return (ni-cfo)/average_assets

def normalized_income(reported,removed_items):
    # 每项是待剔除的税前损益及其题设税率；负损益的剔除会增加利润。
    if not isfinite(reported) or any(not isfinite(v) or not isfinite(t) or not 0<=t<=1 for v,t in removed_items):
        raise ValueError('金额有限、税率0至1；税后项目不能重复乘税率')
    return reported-sum(v*(1-t) for v,t in removed_items)

def depreciation_after_loss(book,loss,remaining_years):
    if any(not isfinite(x) for x in (book,loss,remaining_years)) or not 0<=loss<=book or remaining_years<=0:
        raise ValueError('损失不超过账面，剩余寿命为正')
    return dict(before=book/remaining_years,after=(book-loss)/remaining_years)

# %% 研发按批次摊销，不只加回本年费用
rows=research_cohorts([12,15,18,0,0],3)
assert [r['amort'] for r in rows]==[4,9,15,11,6]
assert [r['asset'] for r in rows]==[8,14,17,6,0]
assert sum(r['amort'] for r in rows)==45
print({'无税分析研发滚动万元':rows})

# %% 税后收益与净资产同步，现金不变
tax_rows=research_cohorts([12,15,18,0,0],3,.25)
previous=0
for row in tax_rows:
    assert isclose(row['profit_adjustment'],row['net_asset']-previous)
    previous=row['net_asset']
print({'假设税制下研发调整':tax_rows})

# %% 分类、一次性项目与减值后利润
a=cash_accrual(20,8,100); b=cash_accrual(20,11,100)
core=normalized_income(24,[(8,.25),(-2,.25)])
dep=depreciation_after_loss(100,40,5)
assert isclose(a,.12) and isclose(b,.09) and core==19.5
assert dep==dict(before=20,after=12)
print({'同一现金分类的应计差别':(a,b),'分析预测NI':core,'减值后折旧':dep})
