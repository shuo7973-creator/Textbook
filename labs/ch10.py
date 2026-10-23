"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def national_accounts(Y,C,G,I,npi=0,nsi=0):
    if any(not isfinite(v) for v in (Y,C,G,I,npi,nsi)) or Y<=0:
        raise ValueError('金额须有限，GDP须正')
    nx=Y-C-G-I; gndi=Y+npi+nsi; savings=gndi-C-G
    return dict(nx=nx,gndi=gndi,savings=savings,ca=nx+npi+nsi,si=savings-I)

def external_bridge(ca,ka,asset_transactions,liability_transactions,nfa0,valuation=0,other=0):
    values=(ca,ka,asset_transactions,liability_transactions,nfa0,valuation,other)
    if any(not isfinite(v) for v in values):
        raise ValueError('交易和头寸须有限')
    outward=asset_transactions-liability_transactions
    credit=-outward; errors=outward-(ca+ka)
    return dict(fa_out=outward,fa_credit=credit,errors=errors,
                bop_residual=ca+ka+credit+errors,nfa1=nfa0+outward+valuation+other)

def real_fx_change(e0,e1,p0,p1,pstar0,pstar1):
    if any(not isfinite(v) or v<=0 for v in (e0,e1,p0,p1,pstar0,pstar1)):
        raise ValueError('汇率与价格指数必须为正且有限')
    return (e1/e0)*(pstar1/pstar0)/(p1/p0)-1

def settlement(export,imports,spot,debt=0,forward_amount=0,forward_rate=None):
    # export/imports/debt/forward_amount为同日万美元，报价元/美元，结果万元。
    if any(not isfinite(v) or v<0 for v in (export,imports,debt,forward_amount)) or not isfinite(spot) or spot<=0:
        raise ValueError('收支需非负有限，报价需正')
    net=export-imports-debt
    if net<0 or forward_amount>net:
        raise ValueError('本例仅支持正净收款且不超额卖出远期')
    if forward_amount and (forward_rate is None or not isfinite(forward_rate) or forward_rate<=0):
        raise ValueError('远期结算需有效报价')
    hedged=forward_amount*forward_rate if forward_amount else 0
    return hedged+(net-forward_amount)*spot

# %% 资源、收入与交易：三个余额不同
accounts=national_accounts(1000,600,150,200,-10,5)
assert accounts==dict(nx=50,gndi=995,savings=245,ca=45,si=45)
position=external_bridge(45,1,54,8,100,-8,2)
assert position['errors']==0 and position['nfa1']==140
print({'国民账户':accounts,'头寸桥':position})

# %% 双符号记账：残差不是识别结果
bop=external_bridge(28,2,40,8,100)
assert bop['fa_out']==32 and bop['fa_credit']==-32 and bop['errors']==2
assert bop['bop_residual']==0
print({'符号及净误差遗漏':bop,'报价提高10%的倒数变化':6/6.6-1,
       '名义变5%本国价格变2%的实际变化':real_fx_change(7,7.35,100,102,100,100)})

# %% 外需与汇率：交互后净敞口也改变
v00=settlement(100,60,7); v01=settlement(100,60,7.35)
v10=settlement(90,60,7); v11=settlement(90,60,7.35)
interaction=v11-v10-v01+v00
assert isclose(v11-v00,-59.5) and isclose(interaction,-3.5)
hedged=settlement(90,60,7.35,debt=10,forward_amount=10,forward_rate=7.1)
assert isclose(hedged,144.5)
print({'四角点万元':(v00,v01,v10,v11),'交互万元':interaction,
       '扣到期本金并部分远期后的结算万元':hedged})
