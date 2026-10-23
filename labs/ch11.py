"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def bank_change(bank, **changes):
    keys={'loan','reserve','deposit','equity'}
    if set(bank)!=keys or not set(changes)<=keys:
        raise ValueError('必须使用约定银行账本字段')
    result={k:bank[k]+changes.get(k,0) for k in keys}
    if any(not isfinite(v) for v in result.values()):
        raise ValueError('金额必须有限')
    if min(result[k] for k in ('loan','reserve','deposit'))<0:
        raise ValueError('贷款、准备金、存款不得为负；缺口需另建融资交易')
    if not isclose(result['loan']+result['reserve'],result['deposit']+result['equity'],abs_tol=1e-9):
        raise ValueError('借贷不平衡')
    return result

def multiplier(c,r):
    if any(not isfinite(x) or x<0 for x in (c,r)) or c+r==0:
        raise ValueError('比率非负、有限且分母非零；以D>0为前提')
    return (1+c)/(c+r)

def comparable_growth(old0,old1,added0,added1):
    if any(not isfinite(x) or x<0 for x in (old0,old1,added0,added1)) or old0<=0:
        raise ValueError('本例金额非负，旧口径基数为正')
    return dict(old=old1/old0-1,new=(old1+added1)/(old0+added0)-1,
                mismatched=(old1+added1)/old0-1)

# %% 贷款、跨行支付：全体系准备金守恒
A=dict(loan=100,reserve=150,deposit=200,equity=50)
B=dict(loan=100,reserve=50,deposit=120,equity=30)
A=bank_change(A,loan=100,deposit=100)
A=bank_change(A,reserve=-100,deposit=-100)
B=bank_change(B,reserve=100,deposit=100)
assert A['reserve']+B['reserve']==200
assert A['deposit']+B['deposit']==420
print({'假设账本万元':(A,B),'说明':'借款人后续还款资金须来自已有存款转移'})

# %% 还本与新损失：存款和权益的不同变化
A=bank_change(A,loan=-40,deposit=-40)
after_repay=A.copy()
A=bank_change(A,loan=-20,equity=-20)
assert A['deposit']==after_repay['deposit'] and A['equity']==30
assert A['deposit']+B['deposit']==380
print({'还本后':after_repay,'未预提损失确认后':A})

# %% 指标口径：新旧基数与比率条件
growth=comparable_growth(100,110,30,40)
assert isclose(growth['new'],2/13)
assert isclose(multiplier(.2,.1),4) and isclose(multiplier(.2,.2),3)
print({'假设亿元口径桥':growth,'贷款桥期末':100+30-20-5})
