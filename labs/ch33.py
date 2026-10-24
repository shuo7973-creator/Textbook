"""本章独立离线实验：全部输入为假设数据。"""

from math import prod,sqrt,isfinite,isclose
from datetime import datetime

def momentum(month_returns,decision_month):
    if not isinstance(decision_month,int): raise ValueError('月份索引为整数')
    selected=list(range(decision_month-11,decision_month))
    if any(m not in month_returns for m in selected): raise ValueError('规定窗口缺月，不能滑动补齐或填零')
    xs=[month_returns[m] for m in selected]
    if any(not isfinite(r) or r< -1 for r in xs): raise ValueError('收益须有限且不低于-100%')
    return prod(1+r for r in xs)-1

def beta_from_vol(vol,market_vol,correlation):
    if any(not isfinite(x) for x in (vol,market_vol,correlation)) or vol<0 or market_vol<=0 or not -1<=correlation<=1:
        raise ValueError('波动/相关系数非法')
    return correlation*vol/market_vol

def aggregate_log_vol(sigma,phi,horizon):
    if not isinstance(horizon,int) or horizon<1 or not isfinite(sigma) or sigma<0 or not isfinite(phi) or abs(phi)>=1:
        raise ValueError('平稳AR协方差域、正整数期数')
    variance=sigma*sigma*(horizon+2*sum((horizon-j)*phi**j for j in range(1,horizon)))
    return sqrt(max(variance,0))

def macro_asof(rows,cutoff):
    c=datetime.fromisoformat(cutoff)
    if c.utcoffset() is None: raise ValueError('时间须带时区')
    available=[];seen={}
    for observation,release,value in rows:
        t=datetime.fromisoformat(release)
        if t.utcoffset() is None or not isfinite(value): raise ValueError('发布时点或值非法')
        key=(observation,t)
        if key in seen and seen[key]!=value: raise ValueError('同一观察和发布时点冲突')
        seen[key]=value
        if t<=c: available.append((observation,t,value))
    return max(available,key=lambda x:(x[0],x[1]))[2] if available else None

def hysteresis(values,band,initial=0):
    if not isfinite(band) or band<=0 or initial not in (-1,0,1) or any(not isfinite(x) for x in values):
        raise ValueError('缓冲带正、状态有效、数值有限')
    state=initial;out=[]
    for x in values:
        if x>band: state=1
        elif x< -band: state=-1
        out.append(state)
    return out

# %% 精确月份集合，最近月和未来数据都不进入
months={m:.01 for m in range(1,12)};months[12]=-.10
assert isclose(momentum(months,12),.1156683466653166)
assert momentum({**months,12:.99,13:9},12)==momentum(months,12)
print({'跳月动量':momentum(months,12),'三个负收益的最高者':max([-.2,-.1,-.05])})
# %% 低波动与beta、自相关累计波动
assert isclose(beta_from_vol(.1,.05,.9),1.8)
assert isclose(beta_from_vol(.2,.05,.2),.8)
vol=aggregate_log_vol(.02,.3,12)
assert vol>.02*sqrt(12)
print({'累计对数波动':vol,'独立月近似':.02*sqrt(12)})
# %% 同一观察期在不同公开版本下的状态
releases=[('2025-05','2025-06-10T10:00:00+08:00',1),('2025-05','2025-08-10T10:00:00+08:00',-.5)]
assert macro_asof(releases,'2025-07-01T00:00:00+08:00')==1
assert macro_asof(releases,'2025-09-01T00:00:00+08:00')==-.5
states=hysteresis([-.1,.1,-.05,.25,.05,-.25],.2)
assert states==[0,0,0,1,1,-1]
print({'实时版本':[1,-.5],'缓冲状态':states})
