"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def finite_ri(book0,income,distributions,rates,terminal_value):
    if not income or not len(income)==len(distributions)==len(rates): raise ValueError('期间向量不一致')
    if any(not isfinite(x) for x in [book0,*income,*distributions,*rates,terminal_value]) or any(k<=-1 for k in rates):
        raise ValueError('输入有限且折现因子为正')
    book=book0; factor=1; ddm=0; ri_value=book0; rows=[]
    for i,d,k in zip(income,distributions,rates):
        residual=i-k*book; end=book+i-d; factor/=1+k
        ddm+=d*factor; ri_value+=residual*factor
        rows.append(dict(begin=book,income=i,distribution=d,end=end,ri=residual))
        book=end
    premium=terminal_value-book
    return dict(ddm=ddm+terminal_value*factor,ri_value=ri_value+premium*factor,
                terminal_premium=premium,book_end=book,rows=rows)

def fading_ri(book0,ri1,persistence,ke):
    if any(not isfinite(x) for x in (book0,ri1,persistence,ke)) or ke<=0 or not 0<=persistence<1+ke:
        raise ValueError('此例要求正成本、非负且收敛的RI持续系数')
    return book0+ri1/(1+ke-persistence)

# %% 有限预测期和未分配的终端权益
x=finite_ri(100,[12,13],[4,5],[.10,.12],150)
assert isclose(x['ddm'],x['ri_value']) and isclose(x['terminal_premium'],34)
liquidation=finite_ri(100,[12,10.8],[4,118.8],[.10,.10],0)
assert isclose(liquidation['ddm'],101.818181818182)
print({'有限期亿元':x,'清算亿元':liquidation['ddm']})

# %% OCI与完整权益收益
oci=finite_ri(100,[12-5],[4],[.10],110)
assert isclose(oci['ddm'],oci['ri_value']) and oci['book_end']==103
print({'含OCI亿元':oci})

# %% 会计重述不改变现金权利
base=finite_ri(100,[12,12],[12,12],[.10,.10],100)
restated=finite_ri(120,[2,2],[12,12],[.10,.10],100)
assert isclose(base['ri_value'],restated['ri_value'])
assert isclose(fading_ri(100,4,.6,.1),108)
print({'原口径':base['ri_value'],'重述口径':restated['ri_value'],'衰退RI价值':108})
