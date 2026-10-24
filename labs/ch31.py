"""本章独立离线实验：全部输入为假设数据。"""

from datetime import datetime,timedelta
from math import isfinite,isclose

def instant(s):
    x=datetime.fromisoformat(s)
    if x.utcoffset() is None: raise ValueError('时间必须有时区')
    return x

def asof_value(rows,key,cutoff,mode='public',latency_minutes=30):
    cutoff=instant(cutoff)
    if mode not in ('public','production') or not isfinite(latency_minutes) or latency_minutes<0:
        raise ValueError('回放模式或延迟非法')
    seen={}; candidates=[]
    for r in rows:
        if (r['sid'],r['period'],r['field'])!=key: continue
        pub=instant(r['published']); ingest=instant(r['ingested']); revision=r['revision']
        if not isinstance(revision,int) or revision<1 or not isfinite(r['value']): raise ValueError('版本和值非法')
        identity=(pub,revision)
        if identity in seen and seen[identity]!=r['value']: raise ValueError('同一版本数值冲突')
        seen[identity]=r['value']
        ready=(pub if mode=='public' else max(pub,ingest))+timedelta(minutes=latency_minutes)
        if ready<=cutoff: candidates.append((pub,revision,r['value']))
    return max(candidates,key=lambda x:(x[0],x[1]))[2] if candidates else None

def first_execution(slots,decision,latency_minutes=0):
    if not isfinite(latency_minutes) or latency_minutes<0: raise ValueError('延迟非负')
    ready=instant(decision)+timedelta(minutes=latency_minutes)
    times=[instant(t) for t,tradable in slots if tradable and instant(t)>=ready]
    return min(times).isoformat() if times else None

def eligible_labels(rows,cutoff):
    cutoff=instant(cutoff); result=[]
    for r in rows:
        start,end,known=map(instant,(r['entry'],r['exit'],r['known']))
        if not start<end<=known: raise ValueError('标签时序不成立')
        if known<=cutoff: result.append(r['id'])
    return result

def event_return(buy,final,split=1,dividend_per_new_share=0):
    if any(not isfinite(x) for x in (buy,final,split,dividend_per_new_share)) or buy<=0 or split<=0 or min(final,dividend_per_new_share)<0:
        raise ValueError('本例股价与拆分/股息域非法')
    return (split*final+split*dividend_per_new_share)/buy-1

ROWS=[dict(sid='A',period='Y0',field='NI',published='2025-04-20T18:00:00+08:00',ingested='2025-04-22T09:00:00+08:00',revision=1,value=100),
      dict(sid='A',period='Y0',field='NI',published='2025-08-01T18:00:00+08:00',ingested='2025-08-02T09:00:00+08:00',revision=2,value=95)]
KEY=('A','Y0','NI')
# %% 公开信息和实际生产时钟
assert asof_value(ROWS,KEY,'2025-04-21T09:00:00+08:00')==100
assert asof_value(ROWS,KEY,'2025-04-21T09:00:00+08:00','production') is None
assert asof_value(ROWS,KEY,'2025-06-01T00:00:00+08:00','production')==100
assert asof_value(ROWS,KEY,'2025-09-01T00:00:00+08:00')==95
print({'公开与生产首日差异':[100,None],'六月与九月':[100,95]})
# %% 执行时隙与证券事件；时隙由教学输入给定
slots=[('2025-04-21T09:30:00+08:00',False),('2025-04-21T10:00:00+08:00',True)]
assert first_execution(slots,'2025-04-21T09:00:00+08:00',15)==slots[1][0]
assert isclose(event_return(10,5.2,2,.1),.06)
print({'拆分与分红总收益':event_return(10,5.2,2,.1),'相对财富增长':1.10/1.05-1})
# %% 标签要到可得时点才能用于训练
labels=[dict(id='early_long',entry='2025-01-01T00:00:00+08:00',exit='2025-04-01T00:00:00+08:00',known='2025-05-01T00:00:00+08:00'),
        dict(id='later_short',entry='2025-02-01T00:00:00+08:00',exit='2025-03-01T00:00:00+08:00',known='2025-03-01T00:00:00+08:00')]
assert eligible_labels(labels,'2025-03-31T23:59:00+08:00')==['later_short']
print({'三月底可训练标签':['later_short']})
