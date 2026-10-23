"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose, sqrt

def price_quantity(p0, q0, p1, q1):
    vectors = (p0, q0, p1, q1)
    if not p0 or any(len(v) != len(p0) for v in vectors):
        raise ValueError('四个向量必须非空且等长')
    if any(not isfinite(x) or x <= 0 for v in vectors for x in v):
        raise ValueError('本教学合同要求正的有限价格和数量')
    v00=sum(p*q for p,q in zip(p0,q0)); v01=sum(p*q for p,q in zip(p0,q1))
    v10=sum(p*q for p,q in zip(p1,q0)); v11=sum(p*q for p,q in zip(p1,q1))
    ql,qp,pl,pp=v01/v00,v11/v10,v10/v00,v11/v01
    return dict(v00=v00,v01=v01,v10=v10,v11=v11,ql=ql,qp=qp,pl=pl,pp=pp,
                qf=sqrt(ql*qp),pf=sqrt(pl*pp))

def contribution(base, current):
    # 输入必须已经统一为可加总的实际量；NX可以为负。
    if not base or set(base) != set(current):
        raise ValueError('分项键必须相同且非空')
    if any(not isfinite(x) for d in (base,current) for x in d.values()):
        raise ValueError('分项必须有限')
    y0=sum(base.values()); change=sum(current.values())-y0
    if y0 <= 0:
        raise ValueError('基期GDP必须为正')
    rows={k:dict(delta=current[k]-base[k],
                 growth=None if base[k]<=0 else (current[k]-base[k])/base[k],
                 pull=(current[k]-base[k])/y0,
                 share=None if change==0 else (current[k]-base[k])/change) for k in base}
    return dict(growth=change/y0,rows=rows)

def diffusion(improve, same, worsen):
    if any(not isfinite(x) or x<0 for x in (improve,same,worsen)):
        raise ValueError('比例必须非负且有限')
    if not isclose(improve+same+worsen,1,abs_tol=1e-12):
        raise ValueError('三种比例须加总为1')
    return 100*(improve+.5*same)

# %% 价格与数量：先算四个交叉支出
indices=price_quantity([2,5],[10,4],[3,6],[12,5])
assert [indices[k] for k in ('v00','v01','v10','v11')]==[40,49,54,66]
assert isclose(indices['qf']*indices['pf'],66/40)
print({'两商品指数':indices,'全部为假设数据':True})

# %% 可加总实际量：拉动可算不意味着贡献率可算
base={'C':60,'I':25,'G':20,'NX':-5}
current={'C':63,'I':27,'G':21,'NX':-6}
growth=contribution(base,current)
assert isclose(sum(v['pull'] for v in growth['rows'].values()),.05)
zero=contribution({'C':60,'other':40},{'C':64,'other':36})
assert all(v['share'] is None for v in zero['rows'].values())
print({'增长贡献':growth,'零增长案例':zero,'两半年合计增速':225/220-1})

# %% 重估和扩散：不要把余额或方向当产出增速
book_change=30*3-20*2; holding=20*(3-2); inventory_flow=10*3
assert book_change==holding+inventory_flow==50
assert isclose(diffusion(.4,.35,.25),57.5)
print({'库存余额变化元':book_change,'持有收益元':holding,'存货变动元':inventory_flow,
       '一般扩散指数':diffusion(.4,.35,.25),'基期修订后的增长':110/105-1})
