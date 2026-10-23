"""本章独立离线实验：全部输入为假设数据。"""

from datetime import date
from math import isfinite, isclose, sqrt
from statistics import mean

def group_returns(records):
    # 按证券计算区间价格收益；显式缺失断开序列；不处理企业行动。
    parsed=[]; keys=set()
    for entity, day, price in records:
        day=date.fromisoformat(day)
        if (entity,day) in keys:
            raise ValueError('重复证券日期')
        keys.add((entity,day))
        if price is not None and (not isfinite(price) or price<=0):
            raise ValueError('价格必须有限且为正，或显式缺失')
        parsed.append((entity,day,price))
    output=[]; previous={}
    for entity,day,price in sorted(parsed,key=lambda r:(r[0],r[1])):
        prior=previous.get(entity)
        if price is not None and prior is not None:
            old_day,old_price=prior
            output.append({'entity':entity,'start':old_day.isoformat(),
                           'end':day.isoformat(),'return':price/old_price-1})
        previous[entity]=None if price is None else (day,price)
    return output

def past_mean(values, window, decision_index):
    if not isinstance(window,int) or window<=0:
        raise ValueError('窗口必须为正整数')
    if not 0<=decision_index<=len(values):
        raise ValueError('决策索引越界')
    if decision_index<window:
        return None
    past=values[decision_index-window:decision_index]
    if any(v is None for v in past):
        return None
    if any(not isfinite(v) for v in past):
        raise ValueError('窗口包含非有限数')
    return mean(past)

def fit_scale(training):
    if len(training)<2 or any(not isfinite(v) for v in training):
        raise ValueError('训练列至少两个有限数')
    center=mean(training)
    scale=sqrt(mean([(v-center)**2 for v in training]))
    if scale==0:
        raise ValueError('常数列不能标准化')
    return center,scale

# %% 证券分组与错误串联
records=[('B','2025-01-03',45),('A','2025-01-02',100),
         ('B','2025-01-02',50),('A','2025-01-03',110)]
original=list(records); result=group_returns(records)
assert records==original and len(result)==2
assert isclose(result[0]['return'],.1) and isclose(result[1]['return'],-.1)
print({'正确分组':result,'跨证券错误收益':50/110-1})

# %% 窗口边界与缺失
assert past_mean([2,4,6,8],3,3)==4
assert past_mean([2,4,6,8],3,4)==6
assert past_mean([2,None,6,8],3,3) is None
gap=[('A','2025-01-01',100),('A','2025-01-02',None),('A','2025-01-03',110)]
assert group_returns(gap)==[]
print({'第四期开盘可用三期均值':4,'包含尚未知第四期后的均值':6})

# %% 训练标准化与未来泄漏
training=[1.,2.,3.]; center,scale=fit_scale(training)
honest=(10-center)/scale
leaked_center,leaked_scale=fit_scale(training+[10.])
leaked=(10-leaked_center)/leaked_scale
assert isclose(honest,8/sqrt(2/3)) and isclose(leaked,6/sqrt(12.5))
assert center==2 and leaked_center==4
print({'仅训练参数':(center,scale),'未来值的正确标准分':honest,'泄漏后的标准分':leaked})
