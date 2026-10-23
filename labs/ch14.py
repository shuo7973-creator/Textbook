"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def debt_bridge(b,i,g,pd,sfa=0):
    if any(not isfinite(x) for x in (b,i,g,pd,sfa)) or b<0 or i<=-1 or g<=-1:
        raise ValueError('初始债务非负，名义增长因子为正，输入有限')
    nxt=(1+i)/(1+g)*b+pd+sfa
    if nxt<0:
        raise ValueError('本模型只处理非负债务；净资产需另定义')
    stable=(g-i)/(1+g)*b-sfa
    return dict(next=nxt,change=nxt-b,stable_pd=stable)

def repricing_saving(tranches,benchmark_cut,spread_rise,tax=0):
    # cut与rise均以非负小数表示；合计净下降可以为负。
    if any(not isfinite(x) or x<0 for x in (benchmark_cut,spread_rise,tax)) or tax>1:
        raise ValueError('降幅、加点升幅、有效当期税盾参数超域')
    exposure=0
    for amount,active_fraction in tranches:
        if not isfinite(amount) or amount<0 or not isfinite(active_fraction) or not 0<=active_fraction<=1:
            raise ValueError('本金非负、全年有效时间在0至1之间')
        exposure+=amount*active_fraction
    pretax=exposure*(benchmark_cut-spread_rise)
    return dict(exposure=exposure,pretax=pretax,aftertax=pretax*(1-tax))

def policy_surprise(outcomes,actual_bp):
    if not outcomes or not isfinite(actual_bp):
        raise ValueError('需要公告前概率分布与有限实际变动')
    if any(not isfinite(p) or p<0 or not isfinite(bp) for p,bp in outcomes):
        raise ValueError('概率非负、数值有限')
    if not isclose(sum(p for p,bp in outcomes),1,abs_tol=1e-12):
        raise ValueError('概率和须为1')
    expected=sum(p*bp for p,bp in outcomes)
    return dict(expected_bp=expected,surprise_bp=actual_bp-expected)

# %% 债务存量流量桥：所有赤字率以当期GDP计
base=debt_bridge(.6,.04,.06,.02,.01)
debt=600*1.04+1060*.02+1060*.01
assert isclose(base['next'],debt/1060)
assert isclose(base['next'],.6186792452830189)
assert isclose(debt_bridge(.6,.04,.06,base['stable_pd'],.01)['next'],.6)
print({'假设亿元债务':debt,'基准':base,'融资压力':debt_bridge(.6,.08,.02,.02,.01)})

# %% 重定价日历：当期税盾与合同加点须明确
saving=repricing_saving([(60,1),(40,.5)],.005,.002,tax=.25)
assert isclose(saving['aftertax'],.18)
print({'全年节省亿元':saving,'无当期税盾':repricing_saving([(60,1),(40,.5)],.005,.002)})

# %% 公告意外：加息为正、降息为负
surprise=policy_surprise([(.75,-25),(.25,0)],-25)
assert surprise==dict(expected_bp=-18.75,surprise_bp=-6.25)
print({'假设预期分布':surprise,'少宽松':policy_surprise([(1,-50)],-25)})
