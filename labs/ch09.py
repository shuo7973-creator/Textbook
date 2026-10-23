"""本章独立离线实验：全部输入为假设数据。"""

from math import isfinite, isclose

def consumption(y1,y2,r=0,beta=1,borrowing_limit=None):
    if any(not isfinite(v) for v in (y1,y2,r,beta)) or min(y1,y2,beta)<=0 or r<=-1:
        raise ValueError('本例收入/偏好须正，利率须大于-1')
    if borrowing_limit is not None and (not isfinite(borrowing_limit) or borrowing_limit<0):
        raise ValueError('借款额度应非负或None表示无约束')
    wealth=y1+y2/(1+r); unconstrained=wealth/(1+beta)
    c1=unconstrained if borrowing_limit is None else min(unconstrained,y1+borrowing_limit)
    saving=y1-c1; c2=y2+(1+r)*saving
    if min(c1,c2)<=0:
        raise ValueError('对数效用要求两期消费为正')
    return dict(c1=c1,c2=c2,saving=saving,wealth=wealth,
                constrained=c1<unconstrained,
                euler_gap=1/c1-beta*(1+r)/c2,
                budget_residual=c1+c2/(1+r)-wealth)

def user_cost(q,r,delta,relative_growth):
    if any(not isfinite(v) for v in (q,r,delta,relative_growth)) or q<=0 or r<=-1 or not 0<=delta<=1 or relative_growth<=-1:
        raise ValueError('资本价格、利率或折旧参数非法')
    resale=(1-delta)*q*(1+relative_growth)
    exact=q*(1+r)-resale
    if exact<0:
        raise ValueError('负租金超出本无风险非负租金教学模型')
    return dict(exact=exact,approx=q*(r+delta-relative_growth),resale=resale)

def order_bridge(backlog,orders,cancellations,deliveries,stock,production,price,credit_share,ar0,old_collection):
    inputs=(backlog,orders,cancellations,deliveries,stock,production,price,credit_share,ar0,old_collection)
    if any(not isfinite(v) or v<0 for v in inputs) or price<=0 or credit_share>1 or old_collection>ar0:
        raise ValueError('业务输入或赊销比例非法')
    end_backlog=backlog+orders-cancellations-deliveries
    end_stock=stock+production-deliveries
    if min(end_backlog,end_stock)<0:
        raise ValueError('交付或取消超出可用订单/库存')
    revenue=deliveries*price
    cash=revenue*(1-credit_share)+old_collection
    ar=ar0+revenue*credit_share-old_collection
    return dict(backlog=end_backlog,stock=end_stock,revenue=revenue,cash=cash,ar=ar)

# %% 家庭：同样偏好、不同借贷约束
free=consumption(20,100); bound=consumption(20,100,borrowing_limit=0)
assert isclose(free['c1'],60) and bound['c1']==20
assert isclose(consumption(30,100)['c1']-free['c1'],5)
assert consumption(30,100,borrowing_limit=0)['c1']-bound['c1']==10
assert bound['euler_gap']>0 and abs(free['euler_gap'])<1e-12
print({'无约束':free,'禁止借款':bound,'原例':consumption(100,80,r=.1)})

# %% 资本服务：期末租金与相对价格
cost=user_cost(100,.04,.06,.02)
assert isclose(cost['exact'],8.12) and isclose(cost['approx'],8)
assert isclose(cost['exact']+cost['resale'],104)
print({'使用成本':cost,'单位':'每单位资本、每期、消费品计价'})

# %% 企业：台、万元/台与万元不能相加
bridge=order_bridge(30,100,10,80,20,90,2,.75,20,10)
assert bridge==dict(backlog=40,stock=30,revenue=160,cash=50,ar=130)
assert 20+bridge['revenue']-bridge['cash']==bridge['ar']
print({'订单和成品以台计，财务以万元计':bridge})
