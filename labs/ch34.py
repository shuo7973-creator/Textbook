"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, sqrt, isclose

def ranks(xs):
    if len(xs)<2 or any(not isfinite(x) for x in xs): raise ValueError('至少两个有限值')
    order=sorted(range(len(xs)),key=xs.__getitem__); result=[0.0]*len(xs); i=0
    while i<len(xs):
        j=i+1
        while j<len(xs) and xs[order[j]]==xs[order[i]]: j+=1
        for k in order[i:j]: result[k]=(i+1+j)/2
        i=j
    return result

def corr(x,y):
    if len(x)!=len(y) or len(x)<2 or any(not isfinite(v) for v in list(x)+list(y)):
        raise ValueError('等长有限配对')
    a=[v-sum(x)/len(x) for v in x]; b=[v-sum(y)/len(y) for v in y]
    aa=sum(v*v for v in a); bb=sum(v*v for v in b)
    if aa==0 or bb==0: raise ValueError('常数截面相关未定义')
    return sum(v*w for v,w in zip(a,b))/sqrt(aa*bb)

def industry_residual(values,groups):
    if len(values)!=len(groups) or not values or any(not isfinite(v) for v in values):
        raise ValueError('行业与数值须配对')
    means={}
    for g in set(groups):
        members=[v for v,h in zip(values,groups) if h==g]
        if len(members)<2: raise ValueError('教学协议要求行业至少两家公司')
        means[g]=sum(members)/len(members)
    return [v-means[g] for v,g in zip(values,groups)]

def neutral_diagnostic(x,y,groups):
    rx=industry_residual(x,groups); ry=industry_residual(y,groups)
    partial=corr(rx,ry)
    return {'raw':corr(x,y),'partial':partial,
            'slope':sum(a*b for a,b in zip(rx,ry))/sum(a*a for a in rx)}

def paired_ic(features,labels):
    ids=sorted(k for k in features.keys() & labels.keys()
               if features[k] is not None and labels[k] is not None)
    x=[features[k] for k in ids]; y=[labels[k] for k in ids]
    return {'ic':corr(ranks(x),ranks(y)),'paired':len(ids),
            'coverage':len(ids)/len(features) if features else 0}

def hac_mean(xs,lags):
    n=len(xs)
    if n<2 or not isinstance(lags,int) or not 0<=lags<n or any(not isfinite(x) for x in xs):
        raise ValueError('等间隔有限序列，带宽0至T−1')
    mean=sum(xs)/n; u=[x-mean for x in xs]
    gamma=[sum(u[t]*u[t-j] for t in range(j,n))/n for j in range(lags+1)]
    long_variance=gamma[0]+2*sum((1-j/(lags+1))*gamma[j] for j in range(1,lags+1))
    if long_variance < -1e-12: raise ValueError('数值方差异常')
    return {'mean':mean,'se':sqrt(max(0,long_variance)/n),'long_variance':long_variance}

# %% 两个行业：整体相关与行业内相关可以反向；收益为小数
result=neutral_diagnostic([1,3,10,14],[.01,.03,.06,.02],['A','A','B','B'])
assert isclose(result['raw'],7/sqrt(385)) and isclose(result['partial'],-.6)
assert isclose(result['slope'],-.006)
print({'行业诊断':result})

# %% 共同样本、平均秩与常数失败状态
ic=paired_ic({'a':1,'b':2,'c':3,'d':None},{'a':-.03,'b':-.02,'c':-.01,'d':.5})
assert isclose(ic['ic'],1) and ic['paired']==3 and isclose(ic['coverage'],.75)
assert ranks([10,10,30])==[1.5,1.5,3]
print({'共同样本IC':ic,'最高信号实际收益':-.01})

# %% 四期只作算术核对，不提供显著性判断
h=hac_mean([.1,.2,.3,.4],1)
assert isclose(h['se'],.0625)
print({'均值HAC':h,'L0':hac_mean([.1,.2,.3,.4],0)})
