"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def forward_from_discount(s,dd,df):
    if any(not isfinite(x) or x<=0 for x in (s,dd,df)):
        raise ValueError('即期与两币种折现因子须正且有限')
    return s*df/dd

def executable_paths(sbid,sask,fbid,fask,dl,db,fl,fb):
    if any(not isfinite(x) or x<=0 for x in (sbid,sask,fbid,fask)) or sbid>sask or fbid>fask:
        raise ValueError('同向报价须正有限且bid不大于ask')
    if any(not isfinite(x) or x<=-1 for x in (dl,db,fl,fb)) or dl>db or fl>fb:
        raise ValueError('一年借贷累计因子正，借款率不低于出借率')
    return dict(borrow_domestic=fbid*(1+fl)/sask-(1+db),
                borrow_foreign=sbid*(1+dl)-fask*(1+fb))

def hedge_cash(actual,hedged,k,spot):
    # 有意允许超额套保，展示净空头风险；并非生产系统交易检查。
    if any(not isfinite(x) or x<0 for x in (actual,hedged)) or any(not isfinite(x) or x<=0 for x in (k,spot)):
        raise ValueError('外币收款和卖出额非负，汇率正且有限')
    return dict(cash=actual*spot+hedged*(k-spot),residual=actual-hedged)

def forward_value(q,k,new_f,dd):
    if not isfinite(q) or q<0 or any(not isfinite(x) or x<=0 for x in (k,new_f,dd)):
        raise ValueError('卖出数量非负，其余参数正且有限')
    return q*(k-new_f)*dd

# %% 两币种现值路径：用相同到期的折现因子
s=7; dd=1/1.02; df=1/1.05
fair=forward_from_discount(s,dd,df)
assert isclose(fair,6.8)
assert isclose(100*s*df,100*fair*dd)
half=forward_from_discount(7,1/(1+.02*.5),1/(1+.05*.5))
print({'假设一年F':fair,'一年两路径现值万元':(100*s*df,100*fair*dd),'半年单利F':half})

# %% 可执行套利腿：先用bid/ask与借贷条件
base=executable_paths(6.99,7.01,6.79,6.81,.02,.03,.05,.06)
shift=executable_paths(6.99,7.01,7.00,7.02,.02,.03,.05,.06)
assert max(base.values())<=0 and shift['borrow_domestic']>0
print({'基准到期本币净额':base,'改变远期后的条件净额':shift})

# %% 终点现金与中途市值：套保量也可能失配
full=[hedge_cash(100,100,6.8,st)['cash'] for st in (6.4,7.4)]
over=[hedge_cash(60,100,6.8,st)['cash'] for st in (6.4,7.4)]
value=forward_value(100,6.8,7,.99)
assert all(isclose(x,680) for x in full)
assert isclose(over[0],424) and isclose(over[1],384) and isclose(value,-19.8)
print({'匹配终点万元':full,'超额套保终点万元':over,'中途卖出远期价值万元':value})
