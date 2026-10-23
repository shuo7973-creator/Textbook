"""本章独立离线实验：全部输入为假设数据。"""

from datetime import datetime
from math import isclose, isfinite

def timestamp(value):
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('时间必须包含时区')
    return result

def asof(rows, entity, period, cutoff):
    # 按本系统处理可得性选版本；输入为单一指标/币种合同。
    cutoff = timestamp(cutoff)
    selected = []
    keys = set()
    for row in rows:
        if (row['entity'], row['period']) != (entity, period):
            continue
        key = (row['entity'], row['period'], row['version'])
        if key in keys:
            raise ValueError('重复版本主键')
        keys.add(key)
        published, ready = timestamp(row['published']), timestamp(row['ready'])
        if ready < published or not isfinite(row['value']):
            raise ValueError('非法可用时间或数值')
        available = max(published, ready)
        if available <= cutoff:
            selected.append((available, row))
    if not selected:
        return None
    latest = max(t for t, _ in selected)
    winners = [row for t, row in selected if t == latest]
    if len(winners) != 1:
        raise ValueError('同一可用时刻多个版本，需人工核查')
    return dict(winners[0])

def ttm_from_selected(full, current_half, prior_half):
    rows = [full, current_half, prior_half]
    if any(row is None for row in rows):
        return None
    for field in ('entity', 'unit', 'basis'):
        if len({r[field] for r in rows}) != 1:
            raise ValueError('TTM组件口径不一致: ' + field)
    # 期间角色必须显式匹配，不能把任意三条记录相加。
    if [r['period'] for r in rows] != ['2024FY', '2025H1', '2024H1']:
        raise ValueError('本例仅支持2025半年末TTM')
    return full['value'] + current_half['value'] - prior_half['value']

def row(period, value, version, basis, published, ready):
    return dict(entity='CY001', period=period, value=value, version=version,
                basis=basis, unit='CNY亿元', published=published, ready=ready)

# %% 基准口径与版本：先手算142
old_time='2025-03-20T18:00:00+08:00'
new_time='2025-08-20T18:00:00+08:00'; new_ready='2025-08-20T18:10:00+08:00'
rows=[row('2024FY',120,'v1','old',old_time,old_time),
      row('2024H1',50,'v1','old',old_time,old_time),
      row('2024FY',118,'v2','comparable_v2',new_time,new_ready),
      row('2024H1',48,'v2','comparable_v2',new_time,new_ready),
      row('2025H1',72,'v1','comparable_v2',new_time,new_ready)]
periods=['2024FY','2025H1','2024H1']
cutoff='2025-09-01T09:00:00+08:00'
selected=[asof(rows,'CY001',p,cutoff) for p in periods]
ttm=ttm_from_selected(*selected)
assert ttm==142 and 120+72-48==144
print({'正确TTM亿元':ttm,'错误混用值':144,'所选版本':[r['version'] for r in selected]})

# %% 处理延迟与未来修订：过去信号不能变化
before=[asof(rows,'CY001',p,'2025-08-20T18:05:00+08:00') for p in periods]
assert ttm_from_selected(*before) is None
future=row('2024FY',117,'v3','comparable_v3','2025-10-01T18:00:00+08:00','2025-10-01T18:10:00+08:00')
assert asof(rows+[future],'CY001','2024FY',cutoff)==selected[0]
try:
    ttm_from_selected(rows[0],selected[1],selected[2])
except ValueError:
    print('已拒绝：不同可比基础的TTM拼接')
else:
    raise AssertionError('口径校验失效')

# %% 流量、平均存量与增长因子
cum=[20,50,81,120]
quarters=[cum[0]]+[b-a for a,b in zip(cum,cum[1:])]
weighted_assets=(9*80+3*120)/12
assert quarters==[20,30,31,39] and isclose(150/weighted_assets,5/3)
assert isclose(1.08/1.03-1,.04854368932038833)
print({'季度收入':quarters,'加权平均资产':weighted_assets,'周转率':150/weighted_assets,'环比1%的年化外推':1.01**4-1})
