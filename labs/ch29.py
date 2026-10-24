"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def bank_capital(capital,income,rwa_next,target):
    if any(not isfinite(x) for x in (capital,income,rwa_next,target)) or capital<0 or rwa_next<0 or not 0<target<=1:
        raise ValueError('目标比例和资本输入超域')
    required=rwa_next*target; capacity=capital+income-required
    return dict(required=required,net_distribution=capacity,dividend=max(0,capacity),issuance=max(0,-capacity))

def cash_tax_nopat(ebit,tax):
    if not isfinite(ebit) or not isfinite(tax) or not 0<=tax<1: raise ValueError('税参数超域')
    return ebit-max(ebit,0)*tax

def resource_value(operating_cash,rate,salvage,restoration):
    if not operating_cash or any(not isfinite(x) for x in [*operating_cash,rate,salvage,restoration]) or rate<=-1 or min(salvage,restoration)<0:
        raise ValueError('有限现金期及终结项须有效')
    cash=list(operating_cash);cash[-1]+=salvage-restoration
    return sum(c/(1+rate)**t for t,c in enumerate(cash,1))

def growth_issue(terminal,terminal_year,issue,issue_year,ke,issue_price_fraction=1):
    if not isinstance(terminal_year,int) or not isinstance(issue_year,int) or not 0<issue_year<terminal_year:
        raise ValueError('年末融资必须早于退出')
    if any(not isfinite(x) for x in (terminal,issue,ke,issue_price_fraction)) or min(terminal,issue)<0 or ke<=-1 or not 0<issue_price_fraction<=1:
        raise ValueError('融资或成本参数超域')
    post=terminal/(1+ke)**(terminal_year-issue_year); pre=post-issue
    if pre<=0: raise ValueError('此模型只覆盖融资前有正价值的成长企业')
    sold=issue/(issue_price_fraction*pre+issue)
    old_today=(1-sold)*terminal/(1+ke)**terminal_year
    return dict(pre=pre,post=post,new_fraction=sold,old_today=old_today,
                fair_net_pv=terminal/(1+ke)**terminal_year-issue/(1+ke)**issue_year)

# %% 资本支撑分红与净注资
base=bank_capital(10,1.2,110,.1); stress=bank_capital(10,.5,110,.1)
assert isclose(base['dividend'],.2) and isclose(stress['issuance'],.5)
print({'银行假设资本亿元':base,'利润压力':stress})

# %% 周期税与资源寿命
mean_nopat=sum(cash_tax_nopat(e,.25) for e in [-10,50])/2
assert mean_nopat==13.75 and cash_tax_nopat(20,.25)==15
resource=resource_value([30,30,30],.1,5,15)
print({'逐状态税后均值':mean_nopat,'资源价值亿元':resource})

# %% 公平融资与折价稀释
fair=growth_issue(150,5,20,3,.15)
cheap=growth_issue(150,5,20,3,.15,.8)
assert isclose(fair['old_today'],fair['fair_net_pv'])
assert cheap['old_today']<fair['old_today']
print({'公平注资':fair,'折价发行':cheap,'含少数分部归母':80+50-10-30-8})
