"""第六批深化：估值边界、跨模型等价、倍数与反向识别。"""
BODY, LAB, EXERCISES = {}, {}, {}

BODY[26]=r"""

## 26.6 两条估值路径必须共享融资政策

在同一报告期、利息税盾可用且没有其他融资费用时，FCFE=FCFF−I(1−T)+ΔD。这个现金恒等式并不保证随意选的WACC和ke能给出相同价值。WACC的市场权重、税盾处理、未来债务政策及风险必须与FCFE预测一致；恒定权重与恒定债务金额一般不是同一政策。

独立永续教学例，单位亿元：每年FCFF12，债务市场价值40且金额不变，债务年利率5%，税率25%，利息当年支付且税盾可用，零净借款、无非经营资产。给定与该融资政策相容的ke10%，每年FCFE=12−2×.75=10.5，权益价值105；经营价值145。反推市场权重WACC=(105×.10+40×.05×.75)/145=12/145=8.275862%。于是12/WACC−40=105，两条路径相等。这个零增长、价值及债务均恒定的构造不能用来证明任意债务路径下恒定WACC适用。

若直接把WACC设成8%同时保留以上FCFE和ke，FCFF法给权益110而非105。差额来自不相容输入，不是某种估值方法“更乐观”。杠杆随期变化时，可逐期重估成本并说明税盾风险，或回到第19章APV；不能靠平均两个结果解决口径矛盾。

## 26.7 增长的价值方向与边际资本回报

令N为下一年NOPAT，R为未来新增投资的税后回报，k为经营资本成本。本节维持原有资产收益且新增资本在下一期产生收益，无独立效率增长。再投资I_t=bN_t，下一期增量利润RI_t，所以g=Rb。历史平均ROIC只有在能代表新投资回报时才可替代R。

将b=g/R代入稳态式，并在固定N、R、k下求偏导：

$$V=\frac{N(1-g/R)}{k-g},\qquad
\frac{\partial V}{\partial g}=\frac{N(1-k/R)}{(k-g)^2}.$$

因此R>k时增长增加价值，R=k时价值不随g变，R<k时更快扩张反而降低价值。本实验限制N>0、R>0、0≤g<k、g≤R，以表示无需外部净投入的成熟期；g>R并非数学上绝不可能，而是需要超过利润的再投资，超出本节成熟期假设。

例如N10、k8%、R6%，零增长价值125；g3%要求留存50%，FCFF5，价值100。增长降低25亿元价值，不意味着亏损，也不意味着负FCFF。若R=k=8%，g0或3%均为125。ROIC下降还可能同时改变原有资产利润，不能只移动公式中的R而把N无条件冻结。

## 26.8 稳态接续、逐期折现与终值审计

用d_t=1/∏_{j=1}^t(1+k_j)表示每一期的折现因子。显性期现金与T时点的终值按同一个d_T折现：V0=ΣFCFF_t d_t+TV_T d_T。k_j是第j个期间的必要回报，不是到第j年的零息收益率；两类利率不能直接互换。

独立例：前两年现金8、9亿元，期间回报8%、9%，第三年现金9.27，稳定期成本9%、增长3%。TV2=154.5，V0=8/1.08+(9+154.5)/(1.08×1.09)=146.296296。原26.3成本始终8%的案例仍为174.074074，不能混用两个终值。原例终值现值占经营价值约91.312057%；这是结构诊断而非概率或错误的自动证据。

接续表至少写出T末资本、T+1利润、再投资、资本变化及资本成本。若T末资本100，T+1开始所有资本回报回落到8%，则NOPAT应为8；g2%需再投资2，FCFF6，TV_T=100（k8%）。若仍用上一年的高利润15，却声称所有资本回报已降至8%，就是接续断裂。若仅新投资回报下降、旧资产仍赚超额收益，应另建存量和新增资本，不强制把两者混为一个R。

## 26.9 权利清单比“减净债务”更清楚

假设全部子公司经营价值180，未计入该值的富余现金20、非经营投资15，债务50、单列租赁负债10、少数股东权益市场价值12、优先权益8、已单独估计的员工期权索取价值5亿元，普通股10亿股。普通股价值=180+20+15−50−10−12−8−5=130亿元，每股13元。各项均是同一时点价值，且债务50不含另列租赁10。

不能既扣期权价值5，又不加行权收入便把所有潜在股数加到分母；也不能经营现金流已扣全部租赁租金，却直接再减全部租赁负债而不调整经营估值。这里采用期权价值单列扣除和租赁作为融资的体系，数值仅为桥接假设，不是期权或租赁定价结果。若债权优先级导致压力情景下偿付不足，应建违约支付模型，不能将负的简单权益残差解释成上市普通股可交易负价格。

## 26.10 估值输入的可验证合同

记录估值日、币种、名义/实际口径、报告范围、现金流时点、税盾、融资和稳态条件。每项桥接资产说明收益是否已在FCFF，索取权说明是否已在其他项目。中国案例从上一章实际报表CFO出发时，保留“利息列筹资，FCFF需扣利息税盾”的桥，不能误套另一制度的加回式。

本章稳定增长和现金分配推导为原创；主参考目录及可读作者资料见[第六批核验](../../references/ALIGNMENT_V03_PART06.md)。原始资料也需要审读：公开网页的文字若与其自身代数冲突，必须复算，不能以引用取代检查。
"""
LAB[26]=r"""
from math import isfinite, isclose

def stable_value(nopat, marginal_return, growth, cost):
    if any(not isfinite(x) for x in (nopat,marginal_return,growth,cost)):
        raise ValueError('输入须有限')
    if nopat<=0 or marginal_return<=0 or not 0<=growth<cost or growth>marginal_return:
        raise ValueError('本成熟期模型要求N>0、R>0、0<=g<k且g<=R')
    reinvest=nopat*growth/marginal_return
    return dict(reinvestment=reinvest,fcff=nopat-reinvest,value=(nopat-reinvest)/(cost-growth))

def discounted(cashflows,period_rates,terminal=0):
    if not cashflows or len(cashflows)!=len(period_rates): raise ValueError('期数相同且非空')
    if any(not isfinite(x) for x in [*cashflows,*period_rates,terminal]) or any(r<=-1 for r in period_rates):
        raise ValueError('金额有限、折现因子为正')
    factor=1; pv=0
    for cash,rate in zip(cashflows,period_rates):
        factor/=1+rate; pv+=cash*factor
    return dict(explicit=pv,terminal_pv=terminal*factor,value=pv+terminal*factor)

def perpetual_financing(fcff,debt,rd,tax,ke):
    if any(not isfinite(x) for x in (fcff,debt,rd,tax,ke)) or debt<0 or rd<0 or not 0<=tax<1 or ke<=0:
        raise ValueError('融资参数超域')
    fcfe=fcff-debt*rd*(1-tax)
    if fcfe<=0: raise ValueError('本例限正永续权益现金')
    equity=fcfe/ke; operations=equity+debt
    wacc=(equity*ke+debt*rd*(1-tax))/operations
    return dict(fcfe=fcfe,equity=equity,operations=operations,wacc=wacc)

def equity_bridge(operations,extra_assets,claims,shares):
    items=list(extra_assets)+list(claims)
    if any(not isfinite(x) for x in [operations,shares,*items]) or operations<0 or shares<=0 or any(x<0 for x in items):
        raise ValueError('价值非负、股数为正；资产及索取权先排重')
    equity=operations+sum(extra_assets)-sum(claims)
    if equity<0: raise ValueError('压力残差为负，转违约支付模型')
    return dict(equity=equity,per_share=equity/shares)

# %% 增长与回报的方向
base=stable_value(10,.10,.03,.08)
assert isclose(base['value'],140)
assert stable_value(10,.06,.03,.08)['value']<stable_value(10,.06,0,.08)['value']
assert isclose(stable_value(10,.08,.03,.08)['value'],125)
print({'稳定模型亿元':base})

# %% 终值时点与期间利率
constant=discounted([8,9],[.08,.08],9*1.03/(.08-.03))
changing=discounted([8,9],[.08,.09],9*1.03/(.09-.03))
assert isclose(constant['value'],174.074074074074)
print({'恒定成本':constant,'变动成本':changing,'原例终值占比':constant['terminal_pv']/constant['value']})

# %% 经营和股权两条路
fin=perpetual_financing(12,40,.05,.25,.10)
assert isclose(fin['equity'],105) and isclose(12/fin['wacc']-40,105)
print({'融资一致性':fin,'权利桥亿元':equity_bridge(180,[20,15],[50,10,12,8,5],10)})
"""
EXERCISES[26]=[
('一年FCFF20亿元、税后利息3、净借款2，FCFE多少？','先扣债权现金再加融资。','FCFE=20−3+2=19亿元；期间、税盾和索取权口径相同，不能据此任意指定ke。'),
('N10亿元、R10%、g3%、k8%，求再投资、FCFF和经营价值。','先由增长求投入。','b=.03/.10=.30，再投资3，FCFF7，价值7/.05=140亿元。'),
('固定N10亿元、k8%，R6%、g0和3%的价值分别多少？','低于成本的扩张。','g0时125；g3%时再投资5、FCFF5、价值100。增速上升降低价值25。'),
('前两年现金8和9亿元，成本均8%，之后增长3%。TV在哪一时点、价值多少？','分子属于第3年。','TV2=9.27/.05=185.4；V0=8/1.08+(9+185.4)/1.08²=174.074074亿元。'),
('上述现金不变，前两期成本8%、9%，稳定成本9%、增长3%，求价值。','区分期间成本和零息利率。','TV2=9.27/.06=154.5；V0=8/1.08+163.5/(1.08×1.09)=146.296296亿元。'),
('永续FCFF12亿元，D40、rd5%、T25%、零净借款、ke10%，求E及相容WACC。','先FCFE再市场权重。','FCFE10.5，E105，V145；WACC=(10.5+1.5)/145=8.275862%，FCFF法也得E105。'),
('经营180、富余现金20、非经营投资15，独立索取权50/10/12/8/5亿元，10亿股，求每股价值。','资产与负债不重复。','普通股价值215−85=130亿元，每股13元；需确认所有索取权互不重叠。'),
('T末资本100亿元，T+1所有资本回报8%、g2%、k8%，TV？','资本、利润和投入连起来。','NOPAT8，再投资2、FCFF6，TV100。不能再使用原高点利润15。'),
('推导固定N、R、k下价值对g的导数并说明R=k的情形。','对分子和分母同时求导。','dV/dg=N[(−1/R)(k−g)+(1−g/R)]/(k−g)²=N(1−k/R)/(k−g)²；R=k时V=N/k与g无关，前提仍为收敛与相容再投资。'),
('第4题终值现值占比是多少？能叫估值错误概率吗？','两者同一时点。','(185.4/1.08²)/174.074074=91.312057%；不是概率，只说明价值对远期假设依赖较大。'),
('分析现金已扣全部租金，还能直接减租赁负债吗？','支付与索取权配对。','不能机械再减。应先选择租赁作为经营或融资的一致体系，修正利润、折旧、再投资和现金流，避免同一支付在经营值和桥接中扣两遍。'),
('写一张FCFF与FCFE不等价的排查清单，并给本章反例。','同一预测不代表同一成本。','核税盾、净借款、市场杠杆、期限和非经营资产。本章若FCFE10.5配ke10%得105，而FCFF12配任意WACC8%减D40得110，是输入不一致，不能取平均为107.5。')]

BODY[27]=r"""

## 27.6 有限预测期的尾项从哪里来

令I_t为与普通权益B_t完全衔接的综合收益，d_t为净股东分配，Q_t=∏(1+k_j)。干净盈余给d_t=I_t−B_t+B_(t−1)，RI_t=I_t−k_t B_(t−1)。于是：

$$\frac{d_t}{Q_t}=\frac{RI_t}{Q_t}+\frac{B_{t-1}}{Q_{t-1}}-\frac{B_t}{Q_t}.$$

逐期相加，中间账面项抵销；若T末分配后剩余股权价值为V_T，则：

$$V_0=B_0+\sum_{t=1}^{T}\frac{RI_t}{Q_t}+\frac{V_T-B_T}{Q_T}.$$

最后一项是剩余权利的价值溢价，不是再加一次全部V_T。有限预测不能无条件删掉它。无限期写成B0加RI现值还需尾项趋零、级数收敛以及相容的风险折现设定；仅有会计恒等式并不能完成风险定价。

独立亿元例，B0=100；两年I分别12、13，净分配4、5，B1=108、B2=116；期间ke10%、12%，T末分配后V2=150。RI1=2、RI2=.04，尾项34。直接价值4/1.1+(5+150)/(1.1×1.12)=129.448052；RI路径100+2/1.1+(.04+34)/1.232亦相同。把尾项删掉会漏掉34/1.232，而不是漏掉全部150/1.232。

## 27.7 干净盈余应包括什么收益

有OCI时以NI计算RI并直接套式，可能漏损益。独立一年例，B0=100、NI12、OCI−5、d4，故B1=103；分配后V1=110，ke10%。综合收益I=7，RI=−3，V0=100+(−3+110−103)/1.1=103.636364，等于(4+110)/1.1。

如果仍用NI得RI2，却使用已含OCI减少的B1=103，会多估5/1.1=4.545455。另一等价处理是保留NI并单列OCI的折现桥。不能把所有OCI默认归经营，也不能把发行收入当利润；经营版应回到第22章，分别核经营与融资的综合收益和非现金调整。

## 27.8 衰退的是超额收益，不是全部资本

设B0=100亿元，下一年RI1=4，之后RI按比例ω=.6逐年衰退，ke10%。在预测及尾项条件满足时，PV(RI)=4/(1.1−.6)=8，价值108。这里ω是RI持续系数而非利润增长率；要求|ω/(1+ke)|<1。若RI1为−4且其余同样，价值92，不能因此称股权无价值。

需要给衰退路径补上账本。一种构造是B恒为100，I_t=10+4×.6^(t−1)，每年全部分配；于是利润最终趋于10而非0，资本仍100。竞争耗尽超额收益不等于企业清算。若让资本增长，则应同时重算正常资本费用，不能仅给RI乘一个系数就声称业务预测已经完整。

## 27.9 同一经济现金如何容纳不同会计展示

独立两年例，基准B0=100，每年I12、分配12，B维持100；T末分配后价值100，ke10%。直接现金价值12/1.1+112/1.21=103.471074，RI两年各2。

若分析上在t0确认额外资产20，未来两年每年摊销10，现金、税和分配均不变，则调整B0=120、I1=I2=2，B1=110、B2=100。RI变为−10、−9，价值120−10/1.1−9/1.21=103.471074。初始资产增加被后续摊销和资本费用抵销；仅抬高账面值而不改未来利润会虚增价值。本例假定无税影响，不是法定会计处理或允许企业任意确认资产。

## 27.10 经营价值、资本成本与等价边界

将B替换为NOA、I替换为相容的综合经营收益，得到经营资本加异常经营收益和经营尾项。在应用WACC时仍须满足第26章关于融资政策和税盾的条件。第23章用于绩效描述的平均资本，不能未经时间修正直接放进这里的期初资本费用。

两模型对账应由独立现金和账本重建，不能先把终值倒算成差额再宣布吻合。差异可能来自不完整权益变动、不同风险假设、期中投入、资本范围或预测截断；同一代数体系下的等价并不证明预测准确。本章原始理论核查限公开论文的会计关系及估值推导，不把有限期实证比较解释为RI在任何场景都胜过DCF。
"""
LAB[27]=r"""
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
"""
EXERCISES[27]=[
('B0=100亿元、NI12、无OCI、ke10%，首年RI？','资本费用用期初。','12−.1×100=2亿元；不是净利润，也不是实际已付现金费用。'),
('B0=100、I12、净分配4亿元，B1？若分配含发行如何处理？','净分配可以为负。','B1=108；发行收入使净分配减少，不计入I，回购与分红增加净分配。'),
('两年I12/10.8、分配4/118.8、B0=100亿元，ke10%，清算后价值0。两种估值？','终端账面也为0。','RI2/0，价值100+2/1.1=101.818182；现金4/1.1+118.8/1.21相等。'),
('两年I12/13、分配4/5、B0=100亿元，期间成本10%/12%，分配后V2=150。求B2和尾项。','先滚动，再减账面。','B1=108、B2=116，尾项为V2−B2=34亿元，在t2折现，不是再加150。'),
('用第4题数据计算直接价值与RI价值。','RI2基于108及12%。','RI1=2，RI2=13−.12×108=.04。两法均129.448052亿元；现金路径4/1.1+155/1.232。'),
('一年B0=100、NI12、OCI−5、分配4、V1=110亿元，ke10%，价值？','综合收益7。','B1=103、RI=−3，价值100+(−3+7)/1.1=103.636364；直接为114/1.1。'),
('B0=100亿元，RI1=4、之后每年乘.6，ke10%，求价值。','几何级数比值.6/1.1。','PV(RI)=4/(1.1−.6)=8，价值108；ω=.6为持续系数，不是利润增速60%。'),
('期初资本与平均资本可以直接互换计算RI吗？','时间位置来自推导。','不可以。这里正常回报基于期初B；平均资本是绩效描述的另一个分母，期中投入需另建时点模型。'),
('从d=I−ΔB推导有限期RI式，说明何时可删尾项。','先除逐期累计折现因子。','d_t/Q_t=RI_t/Q_t+B_(t−1)/Q_(t−1)−B_t/Q_t；相加加上V_T/Q_T得B0+ΣRI_t/Q_t+(V_T−B_T)/Q_T。有限期V_T=B_T时尾项零；无限期需尾项极限零及收敛，不能默认。'),
('第6题若RI仍用NI计算，但B1保留103，会偏多少？','漏掉OCI的现值。','错误RI2替代−3，价值多5/1.1=4.545455亿元；应改用综合收益或单列OCI桥。'),
('基准B0=100、两年收益/分配各12、V2=100亿元、ke10%。t0分析资产加20，随后每年摊销10，无税和现金变化，验证价值。','调整账面、收益及费用基准。','基准价值103.471074。调整B0=120、B1=110、B2=100；收益各2，RI−10/−9；120−10/1.1−9/1.21=103.471074，不因展示而变。'),
('RI最终为零是否表示企业价值也为零？给持续经营构造。','正常回报仍有价值。','不表示。B恒100、ke10%、收益和分配恒10时RI0而价值100。RI4×.6^(t−1)可由收益10+该RI并全部分配构造，利润趋10、企业继续经营。')]

BODY[28]=r"""

## 28.6 同一PE可以拆出不同的时间口径

对同一普通股权益，P0/E1是前瞻PE，P0/E0是历史PE，P0/B0是当前PB。只有E1=ROE_forward×B0时，PB=ROE_forward×PE_forward；若ROE用历史利润除平均权益，就不能机械套用这个等式。稳定EPS增长g且股数不变时，PE_trailing=(1+g)PE_forward。

用28.2的ROE15%、g3%、ke10%：PE_forward=11.428571，PE_trailing=11.771429，PB=1.714286。真实TTM利润、下一财年预测利润和未来12个月预测利润也并非同一期间。股数发生变化时，价格和每股收益的权益范围还需重建，不可默认公司总利润增速就是EPS增速。

## 28.7 收入倍数背后的利润和投入

PS=(P/E)×(E/S)在分子分母期间和范围一致、E非零时是代数恒等式，净利率包含融资影响；PS的权益分子与全部销售收入并非天然同一索取权层级，因此跨杠杆比较要特别谨慎。它不是“销量决定估值”的因果模型。若E为0，PS本身可能有定义，但不能把无穷PE乘零当作可计算表达式。

经营版本更便于对应投入：令下一年收入S1，税前经营利润率m，税率T，未来资本回报R，稳态g和k。NOPAT1=S1 m(1−T)，则：

$$\frac{V_0^{op}}{S_1}=\frac{m(1-T)(1-g/R)}{k-g}.$$

假设m15%、T25%、R15%、g3%、k9%，前瞻EV/S=1.5；收入100亿元对应经营价值150。若只把利润率降为10%而其余条件保持，倍数降至1。但现实中利润率下降也可能使R下降，届时必须同时重算再投资，不能把该单变量演示当完整情景。PS/EV/S等实务名称里的EV要用已经完成非经营项目调整的同范围价值。

## 28.8 整体PE与加权平均的严格关系

设市值M_i、正利润E_i，则整体PE=ΣM_i/ΣE_i。以利润权重a_i=E_i/ΣE_i，整体PE=Σa_i PE_i；以市值权重w_i=M_i/ΣM_i，又有整体PE=1/Σ(w_i/PE_i)，即市值加权调和平均，而非市值加权算术平均。

市值100/200、利润10/5亿元时，个股PE10/40，整体20，利润权重2/3与1/3，市值权重1/3与2/3；简单平均25、市值加权算术平均30均不是整体PE。若第二家公司亏损5，整体PE=300/(10−5)=60，只在总利润仍正时有这个数值含义；负利润使“正权重平均”解释失效。应报告亏损覆盖与盈利公司子样本，不能静默剔亏再称全组合估值。

## 28.9 EBITDA与租赁的分子分母联动

独立对照，现金业务完全相同：租金作为经营费用时，分析EV130亿元、EBITDA20，倍数6.5；若采用租赁作为融资的分析体系，假设需加入租赁索取价值60，并从EBITDA调出当年租金12，则分析EV190、EBITDA32，倍数5.9375。倍数下降没有产生新增现金或自动便宜。

这只是“价值分子与费用分母一起重构”的示意，不能据租金12就断言租赁负债必为60，也不能据会计变动自动断言经营DCF必增加60。实际需核合同支付、期限、税、使用权资产和后续再投资。对比较样本统一处理后，再解释利润率和增长；已资本化的研发、股份支付等也不能通过无理由加回把所有费用从估值中消失。

## 28.10 倍数研究与量化信号的连接

可比样本应先定义行业与业务条件，再冻结估值日、报告可用时间和预测版本。举例：A利润10亿元但次日才公布，B利润5已公开；今日构建PE只能使用A当时可获得的旧利润，不能为了横向整齐偷用次日数据。不同分析师预测也要保留出具日期与有效覆盖。

输出字段至少包括分子范围、分母期间、正负/接近零标识、亏损覆盖、异常调整、候选与剔除原因。行业标准化或回归残差能形成描述性相对信号，不能证明其收益来自错误定价；第31—35章再检验样本外表现。原始倍数和调整倍数同时保留，避免让数据清洗本身决定“低估”结论。
"""
LAB[28]=r"""
from math import isfinite, isclose

def justified_multiples(roe,g,ke):
    if any(not isfinite(x) for x in (roe,g,ke)) or roe<=0 or not 0<=g<ke or g>roe:
        raise ValueError('本稳态模型要求正ROE、可分配且收敛')
    payout=1-g/roe; pe=payout/(ke-g)
    return dict(payout=payout,forward_pe=pe,trailing_pe=pe*(1+g),pb=roe*pe)

def forward_ev_sales(margin,tax,roc,g,k):
    if any(not isfinite(x) for x in (margin,tax,roc,g,k)) or not 0<margin<=1 or not 0<=tax<1 or roc<=0 or not 0<=g<k or g>roc:
        raise ValueError('正利润成熟期参数超域')
    return margin*(1-tax)*(1-g/roc)/(k-g)

def aggregate_pe(caps,earnings):
    if not caps or len(caps)!=len(earnings) or any(not isfinite(x) for x in [*caps,*earnings]) or any(x<=0 for x in caps):
        raise ValueError('市值正且向量一致')
    total=sum(earnings)
    if total<=0: raise ValueError('整体利润非正，不输出可排序PE')
    return sum(caps)/total

def positive_pe_weights(caps,earnings):
    if any(e<=0 for e in earnings): raise ValueError('正权重演示不含亏损或零利润')
    total_pe=aggregate_pe(caps,earnings)
    pe=[m/e for m,e in zip(caps,earnings)]
    arithmetic=sum(m/sum(caps)*p for m,p in zip(caps,pe))
    harmonic=1/sum(m/sum(caps)/p for m,p in zip(caps,pe))
    profit_weighted=sum(e/sum(earnings)*p for e,p in zip(earnings,pe))
    return dict(aggregate=total_pe,cap_arithmetic=arithmetic,cap_harmonic=harmonic,profit_weighted=profit_weighted)

# %% 前瞻、历史与权益分母
x=justified_multiples(.15,.03,.10)
assert isclose(x['pb'],12/7) and isclose(x['forward_pe'],80/7)
assert isclose(forward_ev_sales(.15,.25,.15,.03,.09),1.5)
print({'稳态倍数':x,'经营收入倍数':1.5})

# %% 加总与正权重平均
weights=positive_pe_weights([100,200],[10,5])
assert weights['aggregate']==weights['profit_weighted']==20
assert isclose(weights['cap_harmonic'],20) and isclose(weights['cap_arithmetic'],30)
assert aggregate_pe([100,200],[10,-5])==60
print({'正利润汇总':weights,'含亏损整体PE':60})

# %% 相同现金的租赁展示
before=130/20; after=(130+60)/(20+12)
assert before==6.5 and after==5.9375
print({'经营租金口径':before,'融资租赁分析口径':after,'备注':'索取价值60是另给假设，非由租金12推得'})
"""
EXERCISES[28]=[
('普通股市值120亿元、合并利润15、少数股东利润3，无优先股。PE？','配归母普通利润。','120/(15−3)=10倍，不能用合并利润得到8倍后称更便宜。'),
('稳定ROE15%、g3%、ke10%，求分红率、前瞻PE和PB。','资本留存支持增长。','留存20%、分红80%；PE=.8/.07=11.428571，PB=.15×PE=1.714286。ROE为E1/B0。'),
('上题稳定EPS增长3%且股数不变，历史PE？','同一价格、不同利润。','PE_trailing=11.428571×1.03=11.771429；不是与前瞻PE一样。'),
('同期间PE12倍、归母净利率8%，PS？零利润可否照乘？','代数约分的条件。','PS=.96倍；E=0时PE无定义，不能用无穷乘零，但P/S仍可直接计算。'),
('前瞻收入100亿元、m15%、T25%、R15%、g3%、k9%，经营EV/S？','从FCFF推导。','NOPAT11.25，再投资2.25、FCFF9，价值150，EV/S=1.5倍。'),
('市值100/200亿元、利润10/5亿元，整体和简单平均PE？','先加总。','整体300/15=20，个股10/40，简单平均25；两者不可互换。'),
('相同市值下利润变10/−5亿元，整体PE多少，能否当正权重平均？','总利润与亏损覆盖。','总利润5、整体PE60；不是个股PE的正权重平均，须披露亏损公司，不能静默剔除。'),
('租金口径EV130、EBITDA20亿元，分析改列租赁索取价值60、租金12，重构倍数？','分子分母一起变。','原6.5；重构(130+60)/(20+12)=5.9375，并不代表现金增加或真实低估。'),
('推导整体PE的利润加权及市值加权调和表达，并复核第6题。','用M_i=PE_i E_i。','Σ(E_i/ΣE)PE_i=ΣM/ΣE；1/Σ[(M_i/ΣM)/PE_i]同样等于ΣM/ΣE。正利润下权重解释成立；本例均20，市值加权算术平均30。'),
('为何用历史NI/平均权益乘前瞻PE，不一定等于当前PB？','三个分母的时间。','PB=P0/B0要求配E1/B0及P0/E1；历史NI和平均权益均不相同。应先统一收益期间、权益时点和股数，不能用“ROE×PE”掩盖错配。'),
('两公司前瞻收入相同，利润率由15%降10%，其他第5题参数不变，倍数怎样变？边界？','条件敏感性不等于完整预测。','EV/S由1.5降至1；只有R、税、增长和成本真不变才成立。现实利润率下降可能改变R、信用风险和再投资，应联合重估。'),
('构建今日低PE名单时，A盈利在明日披露而B已披露，如何处理？','可用时间优先于报告期整齐。','使用A今日已公开版本或标记缺失，不引入明日利润；保存披露时间、预测版本、期间、范围、亏损处理和样本规则，再研究样本外表现。')]

BODY[29]=r"""

## 29.6 银行的可分配能力要经过资本约束

银行利润不等于可立即分给股东的现金，账面普通权益与可计入监管的资本也不等同。独立简化教学例：期初可用资本C0=10亿元，目标资本/RWA比例h=10%，下一年末RWA=110，利润NI1=1.2全部转化为可用资本，无OCI、扣减或其他工具。目标资本11，最大净分配为C0+NI1−h×RWA1=.2。

若NI降为.5，结果为−.5，含义是需要净注资.5或降低风险资产，不能把它设为分红0后继续保持原增长。若不注资且不分红，最高RWA=(10+.5)/.10=105。现实还需流动性、杠杆率、缓冲、压力测试及分红限制等独立约束；h=10%仅是假设管理目标，绝非当前中国法定门槛。

同一银行资本积累模型可连接DDM或RI，但未来普通股分配、权益范围和监管资本桥要完整；不能从“PB低于1”直接推断低估。29.2的稳定ROE例另有固定增长假设，不应把这里10%的RWA扩张直接塞入它4%的权益增长。

## 29.7 周期正常化要保留税的非线性

周期利润应同时处理价格、数量、单位成本和投入，而不只选择一个好看的历史均值。假设两个等概率年度状态EBIT为−10和50亿元，税率25%，损失当期无退税且本例不考虑未来税损利用，则税后经营利润分别−10和37.5，期望13.75。先平均EBIT为20再乘.75得15，多估1.25。

这不是说亏损永远没有税价值；真实税损结转要跟踪未来可抵扣利润、时限和法律条件。本节只是明确关闭该渠道，用来说明非线性下“先平均、后计税”不等于“逐状态计税、再平均”。稳定正常化需要生产周期和资本需求证据，并明确估计是在看一个平均年度还是预测一条完整周期路径。

## 29.8 有限寿命资产不能偷接永续价值

资源项目例，单位亿元，未来三年末经营自由现金分别30、30、30，第三年耗尽；最后处置回收5、复垦支付15，均已按相同税后口径，成本10%，没有其他资产或债务。现金实际为30、30、20，价值67.092412；结束后没有经营终值。

若另在第三年加入30/10%=300的永续终值，就给不存在的储量附加225.394440的现值。若账面已经确认复垦预计负债，不能在现金流中扣15后又在权益桥机械扣同一义务；但折现率、税和偿付时点不同的义务仍需单独核实。有限矿权续期、资源替代或新矿投资若确有证据，应作为新投资和现金预测，而非免费延寿。

## 29.9 成长注资：净现金分配与稀释必须二选一致

延续29.4，Y5末总股权价值150亿元，Y3末需注资20，其他分配为0，整个构造采用ke15%，且投资成功及融资可得是条件假设。Y3注资后的价值为150/1.15²=113.421550，融资前价值93.421550。若新股按公平价值发行，新投资者占20/113.421550=17.633333%，原股东保留82.366667%。

原股东不参加注资时，其Y5权益份额折回今天恰为61.426186；原股东认缴全部注资时，总股权净现金分配的现值也为150/1.15⁵−20/1.15³=61.426186。二者代表相同公平交易下的价值守恒，不代表每个股东都必须补款。若发行按融资前公平价值的80%定价，给相同20新钱更多股份，原股东今日剩余价值降至58.832646。融资折价使价值转移，不能再用公平注资扣减公式冒充原股东实际价值。

未来估值150、注资20和成本15%是条件预测，不含失败概率；真实成长企业要单列失败/回收、融资中断及契约，不应把高折现率和同一失败损失重复惩罚。

## 29.10 分部估值的权利与共同费用

若两个分部的100%经营价值80、50亿元，总部费用现值10尚未分摊，两分部所对应的集团净债务30，归属于外部少数股东的权益价值8，则归母普通股价值82。若第二分部已经按母公司持股比例折算，就不能再扣相同少数价值；共同品牌收益、内部交易和协同收益也只能计一次。

建立分部矩阵：每行列估值方法、范围、时点、现金/债务是否已处理、总部费用是否已分摊、少数权利和可独立验证的资料。金融子公司用权益价值而工业分部用经营价值时，应先按各自债务范围调整再汇总，避免集团层再次扣金融存款。方法选择由业务和权利决定，不由希望得到的目标价决定。
"""
LAB[29]=r"""
from math import isfinite, isclose

def bank_capital(capital,income,rwa_next,target):
    if any(not isfinite(x) for x in (capital,income,rwa_next,target)) or capital<0 or rwa_next<0 or not 0<target<=1:
        raise ValueError('目标比例和资本输入超域')
    required=rwa_next*target; capacity=capital+income-required
    return dict(required=required,net_distribution=capacity,dividend=max(0,capacity),issuance=max(0,-capacity))

def cash_tax_nopat(ebit,tax):
    if not isfinite(ebit) or not isfinite(tax) or not 0<=tax<1: raise ValueError('税参数超域')
    return ebit-max(ebit,0)*tax

def resource_value(operating_cash,rate,salvage,restoration):
    if not operating_cash or any(not isfinite(x) for x in [*operating_cash,rate,salvage,restoration]) or rate<=-1 or min(salvage,restoration)<0:
        raise ValueError('有限现金期及终结项须有效')
    cash=list(operating_cash);cash[-1]+=salvage-restoration
    return sum(c/(1+rate)**t for t,c in enumerate(cash,1))

def growth_issue(terminal,terminal_year,issue,issue_year,ke,issue_price_fraction=1):
    if not isinstance(terminal_year,int) or not isinstance(issue_year,int) or not 0<issue_year<terminal_year:
        raise ValueError('年末融资必须早于退出')
    if any(not isfinite(x) for x in (terminal,issue,ke,issue_price_fraction)) or min(terminal,issue)<0 or ke<=-1 or not 0<issue_price_fraction<=1:
        raise ValueError('融资或成本参数超域')
    post=terminal/(1+ke)**(terminal_year-issue_year); pre=post-issue
    if pre<=0: raise ValueError('此模型只覆盖融资前有正价值的成长企业')
    sold=issue/(issue_price_fraction*pre+issue)
    old_today=(1-sold)*terminal/(1+ke)**terminal_year
    return dict(pre=pre,post=post,new_fraction=sold,old_today=old_today,
                fair_net_pv=terminal/(1+ke)**terminal_year-issue/(1+ke)**issue_year)

# %% 资本支撑分红与净注资
base=bank_capital(10,1.2,110,.1); stress=bank_capital(10,.5,110,.1)
assert isclose(base['dividend'],.2) and isclose(stress['issuance'],.5)
print({'银行假设资本亿元':base,'利润压力':stress})

# %% 周期税与资源寿命
mean_nopat=sum(cash_tax_nopat(e,.25) for e in [-10,50])/2
assert mean_nopat==13.75 and cash_tax_nopat(20,.25)==15
resource=resource_value([30,30,30],.1,5,15)
print({'逐状态税后均值':mean_nopat,'资源价值亿元':resource})

# %% 公平融资与折价稀释
fair=growth_issue(150,5,20,3,.15)
cheap=growth_issue(150,5,20,3,.15,.8)
assert isclose(fair['old_today'],fair['fair_net_pv'])
assert cheap['old_today']<fair['old_today']
print({'公平注资':fair,'折价发行':cheap,'含少数分部归母':80+50-10-30-8})
"""
EXERCISES[29]=[
('稳定银行ROE12%、g4%、ke10%，账面权益100亿元。留存和价值？','先核增长资本。','留存1/3，分红率2/3，PB=(.12−.04)/(.10−.04)=4/3，价值133.333333；仅限资本滚动相容的简化稳态。'),
('可用资本10、NI1.2、下一年RWA110亿元，假设目标资本比例10%，最大净分配？','不是当前法定比率。','目标资本11，净分配10+1.2−11=.2亿元，无其他扣减或工具是前提。'),
('上题NI降至.5亿元，仍要扩至RWA110，缺什么？若不融资呢？','利润不足以补资本。','需净注资.5亿元；不融资不分红则最大RWA=10.5/.1=105，不能把负分配截成0后仍保留110。'),
('销量100、单价2、单位变动成本1.2、固定费40，单位按正文亿元，EBIT？价格2.5时呢？','固定成本放大利润变化。','正常EBIT100×.8−40=40，高点100×1.3−40=90；不能无条件永续高点。'),
('两等概率状态EBIT−10/50亿元，T25%，亏损无当期税退或未来税价值，期望NOPAT？','逐状态计税。','−10与37.5平均13.75；平均EBIT20再税后得15，多1.25，不同于同一预测。'),
('三年末经营现金各30亿元，末期处置5、复垦15，耗尽后无业务，成本10%，价值？','末年现金20。','30/1.1+30/1.21+20/1.331=67.092412亿元；不存在免费永续终值。'),
('Y5股权150亿元，Y3注资20，成本15%，其他分配0，公平交易下现有权益净价值？','注资也是股东现金。','150/1.15⁵−20/1.15³=61.426186亿元；需要融资可得与公平定价假设。'),
('两分部100%经营值80/50、未分摊总部10、净债务30、少数价值8亿元，归母价值？','相同范围且各扣一次。','80+50−10−30−8=82亿元；若分部已按持股折算或已扣债，必须重做桥。'),
('推导第7题公平发行的新股占比，验证未认缴原股东的价值。','先算融资后Y3价值。','post=150/1.15²=113.421550，pre=93.421550，新钱份额20/post=17.633333%；原份额×150/1.15⁵=61.426186，与净分配法相等。'),
('第9题按融资前公平价值80%发行、同样融20亿元，对原股东怎样影响？','发行定价不改变既定退出总值。','新股占比20/(.8×93.421550+20)，原份额按退出折现后58.832646亿元，低于公平发行61.426186。差额为价值转移，不能重复扣注资。'),
('复垦15已入第6题末期现金，还要在权益桥减同一负债吗？','同一义务只计一次。','不能机械重复减。先核已扣现金覆盖的义务、税和时点；若另有未计义务才补充。无限期终值还需真实储量或新增投资。'),
('为银行、资源和成长企业各写一个可证伪条件。','约束落在现金与资本。','银行：信用损失后资本不足且融资不可得；资源：矿权/储量缩短并产生复垦支付；成长：单位经济或获客回收不达标，融资缺口超额度。分别修正分配、寿命和资金路径，不用统一PE掩盖差异。')]

BODY[30]=r"""

## 30.6 零分母对应两种完全不同的问题

从Vk−Vg=N−Ng/R得到g(V−N/R)=Vk−N。令A=V−N/R、C=Vk−N。A不为0时有代数候选g=C/A，但还必须满足正利润、再投资和稳定收敛条件。A=0且C≠0时无解；A=C=0时原方程失去识别力，可行域内许多g都给同一价值。

亿元例：V100、N10、R10%、k8%，A0、C−2，因此没有可行增长能产生100。交叉相乘后若取g=k使原式成为0/0也不算解。改k为10%则A=C=0，所有0≤g<10%都给价值100。这比笼统说“分母零、不能唯一识别”更精确。

对非奇异情形，程序应代回原价值式核对残差，并验证g<k、g≤R。本章成熟期不允许负g，所以V120、N10、R10%、k8%得到g−2%时返回超出模型，而非冒称市场一定预期萎缩；若要研究衰退，需另建资本释放和退出条件。

## 30.7 隐含增长对价格和资本成本有多敏感

固定N、R、k，对价格求导：

$$\frac{\partial g}{\partial V}=\frac{N(1-k/R)}{(V-N/R)^2},\qquad
\frac{\partial g}{\partial k}=\frac{V}{V-N/R}.$$

V140、N10、R10%、k8%时，g3%；dg/dV=.00125/亿元，所以附近价格升1亿元约提高g .125个百分点；精确V142得3.238095%，V138得2.736842%，变化不完全对称。dg/dk=3.5，k上升1个百分点在本式中使g上升3.5个百分点，得到6.5%。价格分母接近N/R时，逆问题可能极不稳定，不能用更多小数位掩盖识别脆弱。

这张表应与业务可行域并排：所需新增产能、份额、再投资率和融资能否支持隐含增长？一个候选g即使通过数学域检查，也未必通过业务检验。公开市场价格反推的是有条件假设，不是投资者真实心理的直接测量。

## 30.8 情景概率、状态价格与风险补偿

对下一期随机现金X，物理概率下E[X]只是期望现金，通常还未完成风险定价。可以用相容的必要回报折现，也可以用市场状态价格q_s定价V=Σq_sX_s；无风险利率r_f下，归一化风险中性概率Q_s=(1+r_f)q_s。两种路径不能混用概率与成本。

原创一期间可复制市场例，单位万元：两状态支付60/160，物理概率各.5，市场给定风险中性概率.7/.3，无风险率5%。物理期望110，风险中性期望90，价格90/1.05=85.714286。对应物理期望回报110/85.714286−1=28.333333%，用它折现110也得相同价格；直接用无风险率折现物理期望会得到104.761905，错误多19.047619。

这一构造说明“有概率”不等于“已经风险调整”，不提供真实A股的风险中性概率估计。对未来多期情景，若人为给各情景一套不同k，再用主观概率平均模型价值，其结果首先是条件估值的加权摘要，不自动是无套利价格。要宣称风险定价，应解释概率测度、状态相关风险和折现的一致性；生存概率与高贴现率也不能重复覆盖同一风险。

## 30.9 股权的有限责任先逐状态计算

一年末资产价值两个状态40/160万元，债务承诺到期支付80，无破产成本。股权支付为max(A−80,0)，即0/80；债权支付min(A,80)，即40/80。先平均资产100再扣80得20，但按各.5权重算股权支付期望为40，因为有限责任的正部函数非线性。

若这两个.5明确为风险中性概率、无风险率5%，股权价值40/1.05=38.095238，债权价值60/1.05=57.142857，总和95.238095等于资产价值100/1.05。价值桥中的债务应为57.142857的市场价值，不是到期面值80；正是逐状态支付决定债务折价。不能把经营价值减债面值的负残差简单截零，再声称完成了期权估值。本例是一期支付教学，不是完整结构化信用模型。

## 30.10 将证据更新写成规则，而非改目标价故事

可以用一张事前登记卡连接估值与第31章量化研究：固定估值日、版本、业务论点、参数区间、反证指标、观察窗口、数据延迟与更新规则。每次新证据到达，先保留旧预测，再记录哪个参数因何变动；不利用未来财报回填旧的低估标签。

独立贝叶斯教学例，先验好状态概率.5；某信号在好/坏状态出现的概率分别.8/.2。观察信号后好状态概率=.5×.8/(.5×.8+.5×.2)=.8。若两种条件模型价值为160/80万元，其摘要由120变144；该计算假设条件似然可信，不是把行业经验编成数据，更不是证明股票必上涨。若信号在两状态下都不可能发生，分母0，应要求新模型而非输出概率。

单次情景区间不等于频率置信区间，也不等于投资收益分布。验收需要交付可重算价值、条件假设、替代解释、融资生存边界和更新日志；模拟计算、参考理论和真实证据分开保存。
"""
LAB[30]=r"""
from math import isfinite, isclose

def reverse_growth(value,nopat,roc,cost):
    if any(not isfinite(x) for x in (value,nopat,roc,cost)) or min(value,nopat,roc,cost)<=0:
        raise ValueError('反推模型输入为有限正值')
    a=value-nopat/roc; c=value*cost-nopat
    scale=max(value,nopat/roc,1)
    if abs(a)<=1e-12*scale:
        status='unidentified' if abs(c)<=1e-12*max(value*cost,nopat,1) else 'no_solution'
        return dict(status=status,growth=None)
    g=c/a
    if not 0<=g<cost or g>roc: return dict(status='outside_domain',growth=g)
    reconstructed=nopat*(1-g/roc)/(cost-g)
    if not isclose(reconstructed,value,rel_tol=1e-9,abs_tol=1e-9): raise ArithmeticError('反推代回残差过大')
    return dict(status='identified',growth=g,reconstructed=reconstructed)

def weighted(values,probabilities):
    if not values or len(values)!=len(probabilities) or any(not isfinite(x) for x in [*values,*probabilities]):
        raise ValueError('有限、等长、非空')
    if any(p<0 for p in probabilities) or not isclose(sum(probabilities),1,rel_tol=0,abs_tol=1e-12):
        raise ValueError('本实验要求穷尽互斥状态且概率和1')
    return sum(v*p for v,p in zip(values,probabilities))

def risk_neutral_price(payoffs,q,rf):
    if not isfinite(rf) or rf<=-1: raise ValueError('无风险增长因子正')
    return weighted(payoffs,q)/(1+rf)

def limited_liability(asset_payoffs,face,q,rf):
    if not isfinite(face) or face<0 or any(not isfinite(x) or x<0 for x in asset_payoffs):
        raise ValueError('资产和承诺支付非负')
    equity=[max(a-face,0) for a in asset_payoffs]
    debt=[min(a,face) for a in asset_payoffs]
    return dict(equity=risk_neutral_price(equity,q,rf),debt=risk_neutral_price(debt,q,rf),
                assets=risk_neutral_price(asset_payoffs,q,rf))

def posterior_good(prior,likelihood_good,likelihood_bad):
    if any(not isfinite(x) or not 0<=x<=1 for x in (prior,likelihood_good,likelihood_bad)):
        raise ValueError('概率0至1')
    denominator=prior*likelihood_good+(1-prior)*likelihood_bad
    if denominator==0: raise ValueError('该信号在模型下不可能发生')
    return prior*likelihood_good/denominator

# %% 反向识别的四种状态
cases=[reverse_growth(140,10,.10,.08),reverse_growth(100,10,.10,.08),
       reverse_growth(100,10,.10,.10),reverse_growth(120,10,.10,.08)]
assert [x['status'] for x in cases]==['identified','no_solution','unidentified','outside_domain']
assert isclose(cases[0]['growth'],.03)
print({'反向增长':cases,'资本成本9%':reverse_growth(140,10,.10,.09)})

# %% 真实概率与市场状态权重
price=risk_neutral_price([60,160],[.7,.3],.05)
physical_mean=weighted([60,160],[.5,.5]); expected_return=physical_mean/price-1
assert isclose(price,600/7) and isclose(expected_return,17/60)
print({'价格万元':price,'物理期望':physical_mean,'相容必要回报':expected_return})

# %% 有限责任与价值守恒
claims=limited_liability([40,160],80,[.5,.5],.05)
assert isclose(claims['equity']+claims['debt'],claims['assets'])
assert isclose(claims['equity'],800/21)
print({'逐状态索取权万元':claims})

# %% 新证据更新概率，不篡改历史
posterior=posterior_good(.5,.8,.2)
assert isclose(posterior,.8)
summary=weighted([160,80],[posterior,1-posterior])
assert isclose(summary,144)
print({'后验好状态':posterior,'条件价值摘要万元':summary})
"""
EXERCISES[30]=[
('V140、N10亿元、R10%、k8%，反求稳态g并代回。','先写原式再交叉相乘。','g=(11.2−10)/(140−100)=3%；再投资率30%，7/.05=140，满足0≤g<k且g≤R。'),
('第1题仅k变9%，g变多少？','相同价格需要不同条件。','g=(12.6−10)/40=6.5%；说明反推依赖成本，而非直接测得市场心理。'),
('V100、N10亿元、R10%，k8%时零分母代表什么？k10%时呢？','同时看常数项。','前者A0、C−2，无解；后者A=C=0，0≤g<10%均可，无法识别。不能把二者都叫无限多解。'),
('V120、N10亿元、R10%、k8%，代数g？本章模型接收吗？','检查允许的经济域。','g=(9.6−10)/20=−2%，超出本章非负增长成熟期模型。若研究衰退需扩展资本释放与寿命，不能默默通过。'),
('今天条件价值80/120/160万元，主观概率.25/.5/.25，摘要？它是置信区间吗？','区分算术和证据。','加权120万元；不是置信区间，必须记录主观概率和同一估值口径，不能自动称为无套利价格。'),
('两状态一年后支付60/160万元，风险中性概率.7/.3，rf5%，价格？','概率测度已给定。','风险中性期望90，价格90/1.05=85.714286万元。不能改用物理概率后仍无风险折现。'),
('上题物理概率各.5，物理期望和相容期望回报？','从既定价格反推。','物理期望110，期望回报110/85.714286−1=28.333333%；110按此折现还原价格。'),
('资产到期40/160万元，债面值80，股债两状态支付？','逐状态执行有限责任。','股权0/80，债权40/80，每状态相加还原资产；先平均资产再取正部会错。'),
('推导g对V、k的偏导，并计算第1题附近的敏感性。','商法则，固定其他输入。','dg/dV=N(1−k/R)/(V−N/R)²=.00125/亿元；dg/dk=V/(V−N/R)=3.5。V升1亿元局部g升.125个百分点，k升1个百分点g升3.5个百分点。接近奇点时不可依赖线性近似。'),
('第8题若风险中性概率各.5、rf5%，股债价值及总和？','债用市场价值，不是面值。','股权40/1.05=38.095238，债权60/1.05=57.142857，总95.238095万元，等于资产100/1.05。'),
('好状态先验.5，信号在好/坏状态似然.8/.2。后验及条件价值160/80万元的摘要？','用贝叶斯分母。','后验=.4/(.4+.1)=.8；摘要.8×160+.2×80=144万元。似然是假设，非真实统计证据；两似然为0时不可更新。'),
('EPS增10%、PE降5%，价格收益多少？如何把反向估值连接回测？','精确乘积、公开时间。','价格收益1.10×.95−1=4.5%，未含分红。保存当时价格、利润版本、固定成本与反推域，未来证据只更新新时点；不得回填旧标签或把条件摘要当必然收益。')]

READING={
26:'D英文5版第4章现金与应计及DCF、第14章经营价值；C英文完整版2025 Release第4、13、18章，分别选读折现、资本成本及杠杆企业估值。R1/R2公开作者材料用于增长和终值关系，核查边界见[第六批核验](../../references/ALIGNMENT_V03_PART06.md)。',
27:'D英文5版第5章账面价值估值、第14章经营价值，第9章权益表选读；C第9章股利估值作对照。R3公开论文仅读会计关系与剩余收益理论部分，本章有限期推导和例题原创。见[核验](../../references/ALIGNMENT_V03_PART06.md)。',
28:'D英文5版第3章财报与估值、第5—6章账面及盈利定价、第14章经营倍数；C第9章股票估值。R4/R5公开讲义核对PB与销售倍数的定义和稳态结构，不引用旧海外样本为当前A股证据。见[核验](../../references/ALIGNMENT_V03_PART06.md)。',
29:'D英文5版第16章完整预测与战略、第19—20章股权和信用风险按主题选读；C第20章融资、第29章并购、第30章财务困境选读。行业适配补R6作者金融企业讲义；不把D目录冒称含独立银行估值专章。见[核验](../../references/ALIGNMENT_V03_PART06.md)。',
30:'D英文5版第7章估值与主动投资、第15章简单预测与估值，C第7章风险分析。R7公开作者稿选读情景、决策树与风险调整；反向识别、状态支付和证据更新为原创演示。见[核验](../../references/ALIGNMENT_V03_PART06.md)。'
}
EXIT={
26:'提交同一融资预测的FCFF/FCFE对账、终值接续与权利桥；E05、E06、E09需通过时点和增长条件检查。',
27:'提交逐期B、I、d、RI及终端溢价表；E05、E09、E11必须与独立现金路径一致。',
28:'提交原始及调整倍数、期间合同与亏损覆盖；E05、E09、E10需解释定义和聚合边界。',
29:'提交银行资本缺口、有限寿命现金及成长融资稀释；E03、E09、E10不能用虚构资金填平。',
30:'提交反推状态、敏感性、逐状态索取权和证据日志；E03、E09、E10需区分无解、不可识别与风险定价。'
}

def deepen(chapters):
    for c in chapters:
        n=c.number
        c.body+=BODY[n]; c.lab=LAB[n]; c.exercises=EXERCISES[n];c.reading=READING[n]
        c.edition='v0.3第六批深化稿（第26—30章）'
        c.study_note='建议分3次、每次60—90分钟：先定义价值对象并画现金时点，再独立推导与手算，最后运行对账实验、检查奇点和经济可行域。原始市场数据与假设样本分开。'
        c.exit_task=EXIT[n]+' 核心题建议至少48/64分，修正关键错误后进入基本面量化篇。'
