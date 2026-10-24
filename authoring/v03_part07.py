"""第七批深化：时点研究、基本面信号、诊断与可行组合。"""
BODY, LAB, EXERCISES = {}, {}, {}

BODY[31]=r"""

## 31.6 公开可知与系统实际可用是两个研究问题

同一财报需要保存经济期间、首次公开时间、版本公开时间、系统接收时间和处理完成时间。公开档案回放问“当时公众已经能知道什么”；生产系统复现问“这套系统当时真正拿到了什么”。两者都不能使用未来修订，但后者还受系统延迟约束。今日补采历史公告不必然构成公开信息回测泄漏，却不能冒充当年生产系统已经持有这些数据。

本实验设公开回放可用时间=版本公开时间+预设处理延迟；生产复现可用时间=max(版本公开时间,实际接收时间)+处理延迟。全部时间带时区，available_at≤decision_at才能选入。每个“证券永久ID、报告期、指标”键内，先过滤可用版本，再按公开时间和版本号选择；不按最新入库行覆盖，也不把不同公司拼成一条记录。

假设年度利润原值100万元于4月20日18:00公开，系统4月22日09:00才收到；修订95于8月1日18:00公开，次日收到。处理延迟30分钟。4月21日09:00的公开回放可用100，生产回放仍缺失；6月两者均100，9月均95。这里日期仅为假设事件时钟，未声明具体日期属于真实交易日。相同键、公开时间和版本号若对应不同值，直接拒绝，不能用文件行顺序决定“真相”。

## 31.7 选择股票、产生指令和实际成交分开

指数或行业成员记录至少有公告可知时间与生效区间。提前公告次月纳入不等于今日已经是成分股；反过来，未来剔除也不能删除其今日资格。交易资格与研究覆盖分开：停牌股票仍可能属于持仓和风险集合，只是不能成交。

证券代码会变化，永久ID和代码生效区间帮助避免把更名当新公司。策略数据库应区分上市资格、信号可得、目标持仓、实际成交和仍未平仓五个状态。未成交指令不能获得“目标权重收益”；缺少退市退出价格也不能把亏损记录整行删掉。

本章仅以人工给定的执行时隙演示：决策后处理完成，选第一个不早于允许时点且标为可成交的时隙。它不实现A股完整交易日历、涨跌停、停牌、最小交易单位或融券规则。真实研究需要对应日期的官方规则与证券事件，不能把教学布尔标记当市场撮合。

## 31.8 证券事件先进入持仓账本，再形成收益

单位元/股：以10元买1股，期间先一拆二，随后按新股每股派现.1元，不再投资，末价5.2元。期末资产=2×5.2+.2=10.6，收益6%。直接用5.2/10−1会得到−48%；若输入已经含拆分和分红的总收益序列，再加.2也会重复计算。配股认购、税、费用、合并换股和破产回收另建事件，不能靠一个复权因子名称推断全部含义。

“超额收益”也有两种常见口径。策略收益10%、基准5%时，算术主动收益是5个百分点；相对财富增长是1.10/1.05−1=4.761905%。多期比较要声明是逐期差值、累计财富比还是回归alpha；三者不能共用一个标签列。

## 31.9 训练标签必须在训练时已经完整发生

样本特征时点、入场时点、出场时点及标签最终可得时间各自保存。训练截止日C，只能使用标签可得时间≤C的样本，而不是特征时点≤C就全部训练。否则尚未发生的未来收益成为“历史训练数据”。

例如样本甲特征在1月、退出在4月、标签5月才核实；样本乙2月形成、3月退出且当日可得。3月底训练只能用乙。即使甲的特征更早，也不表示甲标签更早可用。若在历史交叉验证中训练和验证来自两侧，还需按收益区间处理重叠，并考虑信息滞后；第37章将展开，不能只随机打乱股票月份。

12个月滚动标签相邻会共享11个月支付路径。把股票数乘月份当有效独立样本量会高估证据；同时，删重叠和正确标准误也不能修复已经偷看的特征。

## 31.10 将研究协议变成可审计表

协议列市场与资格、经济机制、信号公式、形成时钟、执行规则、标签和基准、成本、缺失处理、模型选择记录及失败条件。新增版本不得静默替换旧结果。读者应能从最终持仓回溯到当时因子、输入字段与原公告，也能追踪哪些目标没有成交。

本章只构建最小时间和支付逻辑，不声称已取得A股完整历史数据库。和产业数据工作一样，字段数量不能替代口径；金融研究额外要求把“何时知道”和“何时能交易”纳入数据血缘。参考来源及方法边界见[第七批核验](../../references/ALIGNMENT_V03_PART07.md)。
"""
LAB[31]=r"""
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
"""
EXERCISES[31]=[
('年度利润100万元4月20日18:00公开，处理30分钟，4月20日15:00可用吗？','经济期间不是可用时钟。','不可用；公开回放最早18:30，成交仍由交易时隙和可成交性决定。'),
('同一公告系统4月22日09:00才收到，处理30分钟。4月21日09:00公开回放与生产复现分别如何？','两个研究对象。','公开回放可用100，生产不可用；生产最早4月22日09:30，不能把补采档案冒充历史实盘数据。'),
('4月原值100、8月修订95万元，6月与9月选哪个？','先按可用时点过滤。','6月100、9月95；保留原公告和版本，不把修订覆盖回6月。'),
('指数公告今日发布、下月生效，今日是否已属新指数？','公告与生效两维。','未生效不属于今日正式成分；预期纳入可另设事件策略，但不能混作当前成员。'),
('10元买1股，先拆成2股，每新股派.1元，末价5.2元，未再投资及无税费。收益？','股数和现金一起滚动。','末值10.6元，收益6%；原始价格比给−48%是错的，总收益价格又加现金会重复。'),
('策略10%、基准5%，算术主动收益和相对财富增长？','差值与比值不同。','前者5个百分点；后者1.10/1.05−1=4.761905%，必须写明标签定义。'),
('1月特征的标签4月退出、5月核实，3月底能用于训练吗？','训练时标签也必须已知。','不能；特征早不代表标签早，需按known≤训练截止筛选。'),
('同键、同公开时点、同版本有两个不同数值，代码应怎样？','不能按行顺序选真相。','拒绝并记录冲突，回到原披露核查；不得静默取最后一行。'),
('将“低估企业有超额收益”改成可审计研究协议。','范围、时点、标签、基准、成本。','事前定义当时资格股票池、公开财报/市值信号、月末形成及后续可成交时隙、下一月含分配净收益与行业匹配基准；保留缺失退出和搜索次数，规定何种样本外结果不支持机制。'),
('人工时隙09:30不可成交、10:00可成交；09:00决策、处理15分钟，最早何时？可否推及真实A股？','处理完成不等于立刻成交。','教学输入下10:00；真实日历、停牌及价格限制需另核，布尔标记不构成撮合引擎。'),
('12个月标签逐月形成，随机打乱股票月份切分有哪些问题？','收益区间与训练可知性。','相邻标签共享11个月路径；训练可能读取验证期间尚未发生的收益，且样本非独立。需先时间切分、按标签区间剔重及核可得时间，再选合适推断方法。'),
('未来价格缺失恰逢退市，能删行后报告幸存股票收益吗？','缺失可能就是损失机制。','不能作为全策略结果。核退市/换码/暂停及回收，保留持仓与退出规则，单列无法定价比例和敏感性，目标权重未成交也不能计其收益。')]

BODY[32]=r"""

## 32.6 一个名称背后可能是不同的利润

French资料的OP不是本书的NOPAT/NOA，也不是NI/平均权益。按本次读取的变量说明，其分子为收入扣营业成本、利息和销售管理费用，分母含账面权益与少数股东权益。INV使用相邻财年的总资产增长；B/M分组有指定的财年和市值月份。公式名相同不表示样本、期间或税口径相同。

独立假设亿元例：收入100、营业成本60、销售管理费用20、利息4、税25%，账面权益80、少数权益20、平均归母权益80、NOA75；为隔离定义，另假设利润12全属普通股。定义演示OP=(100−60−20−4)/(80+20)=16%；NI/平均权益=15%；税后经营利润15/NOA75=20%。这个简化数值不宣称真实合并表必然具备这样的少数收益结构，它只说明三个分子分母不可以替换。

复制学术因子还需核股票样本、规模交叉分组、断点、价值加权、形成与持有月份以及数据库修订。本书后续示例是自定义特征和构造实验，不因算出一个相同名称而成为原文复现。

## 32.7 价值因子的权利范围和符号合同

同一普通股权益可定义B/M、NI_TTM/M；同一经营范围可定义NOPAT/V_op、FCFF/V_op。归母权益不能配100%合并经营利润；把NI除EV会混入融资因素。TTM各期要使用形成日已经公开、范围可比较的版本，不能先用未来修订拼“最完整年度”。

负NI下E/P可以作为带符号的亏损特征，但它不是“低PE”排序的倒数捷径。负权益企业不纳入本章常规正B/M排名，单独记录；经营价值分母非正时，正收益率排序的经济解释也需重建。分子为0和数据缺失是两种状态，不能统一填0。

比率的量纲同样重要：利润以万元、价格市值以亿元，必须先换单位。上市公司流通市值与总普通股市值不可随意替换，股本、股价与财报范围要落在明确定义的估值日。

## 32.8 高ROE可能只是更高融资风险

两家公司经营资本均100亿元、税后经营收益均10。甲净融资负债0、权益100、NFE0，ROE10%；乙净融资负债50、权益50、税后NFE2.5，NI7.5、ROE15%。乙ROE高于甲，但经营回报同为10%，提高的5个百分点来自融资结构，不是经营优势的直接证据。

质量特征可以将经营盈利、现金转化、杠杆及盈利稳定性分开，避免反复奖励同一高杠杆。应计代理仍沿用第24章的现金分类合同：同一现金支付重分类会改变NI−CFO，却不自动改变质量。资产增长20%若含并购15个百分点，余下5个百分点也只能叫未解释的其余变化，尚不能直接认定有机投资。

## 32.9 从六个组合到高减低的透明算式

独立月度教学表：小规模低/中/高B/M组合收益1%/2%/3%，大规模分别.5%/1%/2%。设这些格内收益已按事前规则得到，则高减低=(3%+2%)/2−(1%+.5%)/2=1.75个百分点。两组高各+.5、两组低各−.5，总多头1、空头−1，净投入权重0、总绝对权重2。

这不是用零本金得到无穷收益；它是约定资本基准下的多空收益差，真实实施仍有保证金、融券、借贷、费用和容量。五因子SMB又综合多个排序体系，不能把这里一个B/M体系的小减大就冒称完整五因子SMB。A股难以建立某条空腿时，可研究多头相对基准，明确它已换了策略对象。

## 32.10 合成前固定方向、覆盖与信息增量

教学合成使用同一合格集合的平均并列排名，映射s=(rank−1)/(n−1)，高值为高分；低应计等反向指标需先调方向。若A/B/C的价值特征为.5/1/1.5、质量为.2/.1/.15，等权平均排名分数为.5/.25/.75。C最高是预定规则的输出，不证明它最有价值。

缺一个指标的公司若临时按剩余指标重分权重，相当于为不同公司使用不同模型。应事前定义完整样本、专门缺失模型或其他处理，并报告覆盖变化。行业分类、训练期相关性和去重规则在信号形成时可知；不利用未来收益调权。到第34章，比较原始、行业内和复合信号的诊断；到第36—40章，再检验实际资金和样本外结果。
"""
LAB[32]=r"""
from math import isfinite,isclose

def ratio(numerator,denominator):
    if not all(isfinite(x) for x in (numerator,denominator)) or denominator<=0:
        raise ValueError('比率要求有限输入和正分母，缺失须另记')
    return numerator/denominator

def factor_fields(book,market,ni,avg_equity,cfo,avg_assets,assets_now,assets_before):
    if book<=0: raise ValueError('常规B/M集合排除非正权益并记录')
    if not isfinite(assets_now) or assets_now<0: raise ValueError('总资产非负')
    return dict(bm=ratio(book,market),ep=ratio(ni,market),roe=ratio(ni,avg_equity),
                accrual=ratio(ni-cfo,avg_assets),investment=ratio(assets_now,assets_before)-1)

def profitability_definitions(revenue,cogs,sga,interest,book,minority,tax,avg_equity,noa):
    vals=(revenue,cogs,sga,interest,book,minority,tax,avg_equity,noa)
    if any(not isfinite(x) for x in vals) or min(revenue,cogs,sga,interest,minority)<0 or not 0<=tax<1:
        raise ValueError('教学输入域非法')
    ebit=revenue-cogs-sga
    if ebit<interest: raise ValueError('本例不建亏损税盾')
    return dict(op=ratio(ebit-interest,book+minority),roe=ratio((ebit-interest)*(1-tax),avg_equity),rnoa=ratio(ebit*(1-tax),noa))

def six_cell_spread(cells):
    keys={'SL','SN','SH','BL','BN','BH'}
    if set(cells)!=keys or any(not isfinite(r) or r< -1 for r in cells.values()): raise ValueError('六个同期间多头组合收益须齐全')
    high=(cells['SH']+cells['BH'])/2;low=(cells['SL']+cells['BL'])/2
    size=(cells['SL']+cells['SN']+cells['SH']-cells['BL']-cells['BN']-cells['BH'])/3
    return dict(high=high,low=low,spread=high-low,size_within_this_sort=size)

def rank_score(xs):
    if len(xs)<2 or any(x is None or not isfinite(x) for x in xs): raise ValueError('共同覆盖集合至少2个有限值')
    ordered=sorted(xs)
    ranks=[sum(i+1 for i,v in enumerate(ordered) if v==x)/ordered.count(x) for x in xs]
    return [(r-1)/(len(xs)-1) for r in ranks]

def composite(value,quality,weight=.5):
    if len(value)!=len(quality) or not isfinite(weight) or not 0<=weight<=1: raise ValueError('同样本与固定权重')
    a,b=rank_score(value),rank_score(quality)
    return [weight*x+(1-weight)*y for x,y in zip(a,b)]

# %% 定义相近不等于同一个因子
x=profitability_definitions(100,60,20,4,80,20,.25,80,75)
assert isclose(x['op'],.16) and isclose(x['roe'],.15) and isclose(x['rnoa'],.20)
print({'利润口径':x,'甲乙ROE融资差异':[10/100,7.5/50]})
# %% 六格组合的透明多空差；无融券与成本仿真
spread=six_cell_spread(dict(SL=.01,SN=.02,SH=.03,BL=.005,BN=.01,BH=.02))
assert isclose(spread['spread'],.0175)
print({'自定义六格':spread})
# %% 共同覆盖及事前固定合成
scores=composite([.5,1,1.5],[.2,.1,.15])
assert scores==[.5,.25,.75]
print({'A_B_C复合分数':scores,'财务特征':factor_fields(100,200,15,100,12,150,180,150)})
"""
EXERCISES[32]=[
('普通股权益100、市值200亿元，B/M及PB？','同一权利范围。','B/M=.5，PB2；含少数权益的合并总权益不能直接配归母市值。'),
('NI20、CFO8、平均资产100亿元，应计代理？若CFO因分类变11呢？','现金分类也改变比率。','原12%，重分类后9%；差3个百分点不自动代表经营或质量改善。'),
('收入100、成本60、销售管理20、利息4、账面权益80、少数权益20亿元，按本章OP定义求值。','不是税后经营利润/NOA。','OP=(100−60−20−4)/(80+20)=16%；该定义也不等于ROE。'),
('上题税25%、NI全部归普通股、平均归母权益80、NOA75亿元，ROE与RNOA？','分子分母对应。','NI12、ROE15%；NOPAT15、RNOA20%。合并范围和税是题设，不宜直接搬到真实报表。'),
('甲乙NOA均100、OI均10亿元；甲NFO0、乙NFO50且NFE2.5。ROE？','权益=NOA−NFO。','甲10%；乙权益50、NI7.5、ROE15%。高ROE可来自融资，经营回报都10%。'),
('总资产100升120亿元，并购带来15，能把20%全称有机投资吗？','增长桥而非名称。','不能。总增长20%，其余增量5仍需拆汇率、处置、重估等；不自动都是有机投资。'),
('小规模低/中/高收益1%/2%/3%，大规模.5%/1%/2%，高减低多少？','先规模组内高低再平均。','(3%+2%)/2−(1%+.5%)/2=1.75个百分点，尚未扣融券及交易成本。'),
('第7题多空权重各为多少，净0是不是不用本金？','收益差的资本基准。','两高各+.5、两低各−.5，净0、总绝对2；仍需保证金和融资，不能除以净0解释为无穷收益。'),
('价值.5/1/1.5，质量.2/.1/.15，A/B/C平均排名归一化再等权，分数？','rank映射到0至1。','价值分数0/.5/1，质量1/0/.5；复合.5/.25/.75。C最高只是固定规则输出，非真实收益证据。'),
('负NI、负权益、缺失值可以统一填0吗？','三个经济状态。','不能。负NI可留作亏损特征，常规正B/M排除负权益并报告；缺失不是零。还要检查经营价值和市值分母及单位。'),
('自定义B/M多空为何不能称完成Fama–French五因子复现？','完整构造与版本。','需核样本、断点、规模交叉、格内权重、财年/市值月、再平衡、数据版本，以及OP/INV定义；完整SMB还综合多个排序体系，不能只用本章一个六格表。'),
('公司缺质量指标时临时全部按价值排序，会怎样？','公司间模型权重改变。','改变了原等权规则，缺失可能带来选择偏差；须事前定义处理与覆盖报告，不能根据回测好坏临时换模型。')]

BODY[33]=r"""

## 33.6 把动量记法翻译成月份集合

本书在t月末形成信号，用t−11至t−1的11个月，跳过t，进入t+1持有月。French说明以持有月m命名，使用prior (2–12)收益；令m=t+1，则m−12至m−2恰等于t−11至t−1。记号平移后窗口一致，但其规模分组、断点、格内权重和缺失代码政策不是本章代码的全部内容。

程序必须对月份键逐项检查连续和唯一。缺一个月而把其余11个位置向前补齐，会悄悄改变窗口；把缺失填0又变成“当月收益0”的新经济假设。本章选择缺月报错，真实研究可用其他事前规则，但须披露。本例不接收CRSP特殊缺失码为普通收益，也不据此宣称学术复制。

窗口收益是∏(1+r_j)−1。允许−100%意味着持仓价值归零；低于−100%的普通无杠杆总收益不在本实验域内。退市回收和公司行动需先完成第31章收益账本，动量计算不能自动修复输入事件。

## 33.7 截面动量和时序趋势不是一个信号

同一组证券累计收益为−20%、−10%、−5%。截面排名最高的是−5%，但三者绝对趋势均为负；“相对强”不等于“上涨”。如果截面策略仍持有相对赢家，它承担的市场风险与“收益大于0才持有”的时序规则不同。二者的资金空置、基准和成本也不同。

实验只返回相对名次和正负方向，不根据这个三证券样本声称谁更赚钱。市场、行业与风格暴露要在组合权重上检验，不能以“动量”一个名称覆盖不同交易规则。

## 33.8 低波动不自动等于低beta

单资产beta=Cov(r_i,r_M)/Var(r_M)=ρ_iM σ_i/σ_M。假设同一频率、市场波动5%；资产A波动10%、相关.9，beta1.8；资产B波动20%、相关.2，beta.8。A自身波动较低，但对市场风险的线性暴露更高。相关系数、样本时间和收益口径不能遗漏。

年化平方根规则也有边界。若月度**对数收益**平稳，方差σ²，自协方差γ_j，则h个月累计对数收益方差为hσ²+2Σ_{j=1}^{h−1}(h−j)γ_j。对AR(1)协方差γ_j=σ²φ^j、|φ|<1，月波动2%、φ=.3，12个月波动约9.178502%，高于忽略自相关的6.928203%。这里σ是平稳边际标准差，不是AR创新标准差；结果针对对数收益和，不直接等于简单复合年度收益的标准差。

## 33.9 实时宏观状态保存观察期与版本

假设某增长指标5月观察值于6月发布为+1，8月修订为−.5。7月决策只能使用+1，9月才能用修订版−.5。为突出机制，本例只有一个观察期；真实滚动数据库先选决策日前已发布的观察，再按每个观察期选当时版本，不能把8月的修订值误当8月经济活动。

FRED/ALFRED的实时区间说明提供了“今天知道的历史”与“历史某时点知道的值”的区别，实际接口以日为粒度；它不能替代A股日内公告或中国宏观发布时间。中国研究需查国家统计局、央行等原发布及修订记录，历史版本缺失就保留缺口，不能制造精确实时档案。

标准化阈值若从全历史估计，也会把未来分布带回过去。固定经济阈值、仅过去滚动阈值或训练期冻结阈值应分别命名；连续变量、观察期、发布时点和状态共同保留，不能只存最后一个“繁荣/衰退”标签。

## 33.10 缓冲带减少切换，但不会自动创造预测力

设预先固定阈值h=.2，状态初始0；指标超过+h转+1，低于−h转−1，其余保持原状态，包括边界恰等于阈值。输入−.1、.1、−.05、.25、.05、−.25，状态为0、0、0、1、1、−1；只有两次切换。无缓冲的符号状态会在噪声附近反复变动。

减少切换可能降低交易，也可能延迟对真实拐点的反应。规则必须按时间顺序递推并明确初始状态，不能看完整周期后倒填状态。验证时与无状态基准保持相同股票池、标签、执行和成本，并报告各状态覆盖及样本量；阈值选择次数也算研究搜索。第34章的统计诊断与第35章的权重约束不能替代连续样本外检验。
"""
LAB[33]=r"""
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
"""
EXERCISES[33]=[
('t月末决策，按本书跳过最近月的动量包含哪些月份？','把预测月也列出。','用t−11至t−1共11个月，排除t，持有标签为t+1；真实成交时点仍另定。'),
('French以持有月m标prior(2–12)，与本章如何对应？','令m=t+1。','m−12至m−2=t−11至t−1。月份一致不代表规模断点、权重、缺失政策均已复制。'),
('11个月各1%，最后一个被跳过的月份−10%，跳月和全12个月收益？','复利乘积。','跳月11.566835%；全期1.01^11×.9−1=.410151%，两者不能看结果再选。'),
('窗口中少一个月，能用更早月份补够11条吗？','数量相同不等于日期相同。','不能默默补；它会改变经济窗口。本章报错，其他策略需事前定义缺失政策和覆盖统计。'),
('三证券过去收益−20%、−10%、−5%，截面赢家的绝对趋势？','相对名次与符号。','−5%相对最高，但绝对仍为负；截面动量和正收益才持仓的时序策略是不同对象。'),
('市场波动5%，A波动10%相关.9、B波动20%相关.2，同频率beta？','相关乘相对波动。','A1.8、B.8；低自身波动不保证低市场暴露。'),
('月度平稳对数波动2%、AR系数.3，12月累计波动与独立月近似？','累加自协方差。','精确协方差模型下9.178502%，独立月近似6.928203%；σ是边际标准差，不能换成创新标准差。'),
('5月观察值6月发布+1、8月修订−.5，7月与9月可用值？','观察期不同于发布时间。','7月+1，9月−.5；修订值仍属于5月，不是8月活动的新观察。'),
('推导h期对数收益和的方差，解释h−j权重。','双重求和按滞后分组。','Var(Σr)=ΣVar(r)+2Σ_{s<t}Cov(r_s,r_t)；平稳时滞后j共有h−j对，故hσ²+2Σ(h−j)γ_j。若AR协方差，γ_j=σ²φ^j。'),
('缓冲h=.2、初态0，输入−.1/.1/−.05/.25/.05/−.25，状态？','带内保留前态，严格越界才切换。','0/0/0/1/1/−1，共两次切换；带内不是每次归零，也不能用未来值倒填。'),
('用最终GDP和全样本分位阈值解释历史四象限，有哪些用途边界？','事后描述与实时策略。','可以作明确标注的事后描述；不能当可交易实时标签。实时版本和阈值都需只用当时信息，并保存连续变量及发布滞后。'),
('缓冲带换手更低，是否证明加入宏观状态有alpha？','预测、成本与搜索分开。','不证明。可能只是减少交易且延迟拐点；需同基准同执行的连续样本外净收益、风险、覆盖与换手比较，记录阈值搜索及失败区间。')]

BODY[34]=r"""

## 34.6 先固定有效样本，再决定变换

截面信号变换至少记录证券集合、原始有效数、缺失原因、异常值规则、变换参数与有效配对数。缺失不是零；把缺失盈利收益率补0，相当于给它一个真实经济判断。若决定用当期行业中位数填补，需说明为何可比，并另保留缺失指示变量和覆盖率，而不是让插补后的“100%覆盖”掩盖源数据质量。

普通正尺度标准化保持排序，但截尾可能制造并列值；平均秩需在截尾后的共同有效样本上重新计算。因子与收益分别对不同股票排名再拼接，通常不等于在共同股票集合上计算Spearman相关。实验仅显式删除None配对，NaN/无穷大视为错误，常数截面无法定义相关系数。

当期可知的全截面变换，与跨期预测模型的训练预处理是不同操作。前者可以使用决策时已经可得的当期股票信息；后者估计缩放、插补或降维参数时只用训练窗口，然后在验证和测试窗口冻结。不能以“截面标准化”之名使用未来月份的均值和方差。参数选择及缺失规则也属于研究决策，需要在看测试收益前固定。

## 34.7 中性化同时改变问题与样本内约束

控制行业后问的是“同一行业内部的信号差异，是否与收益差异相关”，不再是包括行业配置在内的总预测能力。设Z为行业虚拟变量空间，M为对该空间的残差算子。含行业控制的回归斜率等于β=(x'Mx)⁻¹x'My；也就是先对x、y分别残差化，再回归。只残差化x时，由正交性可得到同一斜率，但拿它与原始y计算相关，分母不同，不能称为相同的部分相关。

假设四家公司分属A、A、B、B行业，x=[1,3,10,14]，下一期简单收益y=[1%,3%,6%,2%]。原始Pearson相关为7/√385≈.356753；行业内去均值后，x残差=[−1,1,−2,2]，y残差=[−1%,1%,2%,−2%]，相关为−.6，斜率为−.006，即每一信号单位对应−.6个百分点收益。行业差异掩盖了负的行业内关系；这仍是样本相关，不是因果效应。

残差与行业虚拟变量正交，仅针对拟合时使用的样本和权重成立。随后再截尾或挑前10%持仓，约束可能丢失。例如某行业残差[−3,1,2]和为0，截到[−1,1]后变[−1,1,1]，和为1。要保证组合行业暴露，应直接对最终权重施加约束并验算，不能从“信号已经中性”推断“组合必然中性”。本实验采用组内等权去均值，至少两家公司，不冒充包含市值和多重暴露的完整加权回归。

## 34.8 IC、收益与经济规模是三张不同的成绩单

IC描述排序或线性联系，不等于可交易组合收益。给全部未来收益加同一常数，相关系数不变，单边多头收益却改变；给所有信号乘正数，排序不变，若策略把原始信号直接映射成杠杆，资金风险会改变。报告IC时还要报告持有期、权重规则、行业/规模控制、覆盖率与交易成本。

假设信号[1,2,3]对应收益[−3%,−2%,−1%]，Rank IC为1，但选最高信号仍亏1%。横截面选择正确不代表绝对收益为正。多空价差也不是无资本、无借券、无成本的收益承诺。第32章的排序组合定义与第35章的实际资金账本需要一并验证。

## 34.9 平均IC的标准误不能忽略时间依赖

设等间隔月度IC序列长度T，均值m，u_t=IC_t−m。采用分母T的样本自协方差γ_j=T⁻¹Σ(t=j+1…T)u_tu_(t−j)，Bartlett权重w_j=1−j/(L+1)。均值的HAC方差估计为[γ_0+2Σ(j=1…L)w_jγ_j]/T。本章只实现截距均值模型、人工指定带宽L、无小样本修正，不等于一般回归或面板聚类的全部标准误。

假设IC=[.1,.2,.3,.4]，m=.25，γ_0=.0125、γ_1=.003125。L=1时长期方差估计.015625，均值标准误.0625；L=0时为√(.0125/4)=.0559017。这里分母T不同于用T−1估计独立样本方差的常见t检验，不能混用两个公式。本例四个观测只核对算术，不足以作可靠显著性结论。

正序列相关可能增大均值不确定性，负相关可能降低它；不能把HAC理解为固定打折系数。重叠标签、持仓持续性与宏观状态都可能产生依赖。带宽、检验方向和候选因子数量应预先记录；HAC不消除数据窥探、多重尝试和结构突变。若月份缺失，不能删除空月后假装剩余值等间隔相邻；应先定义连续时间网格和有效处理方案。

## 34.10 诊断报告必须允许得出“不足以判断”

交付每期原始覆盖、共同配对数、并列比例、异常值处理、原始/中性化IC，以及跨期均值和明确标准误口径。行业只有一家、信号常数、标签未完成或样本不足时，返回未定义及原因，不把0伪装成成功估计。代码用异常阻止继续，研究报告可将异常转为带原因的缺失状态。

退出验收要解释“变换保持了什么、破坏了什么”：标准化保持正向排序；截尾不保证严格排序；去均值保证当前样本组内残差和为0；重新选股不保证该性质；HAC只调整既定序列的均值不确定性。诊断层给出证据强度，组合层才决定资金如何承担风险。
"""
LAB[34]=r"""
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
"""
EXERCISES[34]=[
('原始信号[1,None,3]，填行业中位数后是多少？覆盖率如何报告？','保留插补标记。','填为[1,2,3]；原始有效2/3，插补后可计算3/3，两者同时报告，不能说源数据已100%覆盖。'),
('对信号[10,10,30]求平均秩，常数信号的IC如何处理？','并列共享占据位置。','平均秩[1.5,1.5,3]；常数方差为0，IC未定义，应报原因而非置0。'),
('四公司行业A/A/B/B，x为1/3/10/14，行业内残差？','分别减行业均值。','均值2和12，残差[−1,1,−2,2]，每组和0。'),
('上题收益1%/3%/6%/2%，行业内收益残差及相关？','收益也残差化。','残差[−.01,.01,.02,−.02]；交叉积−.06，两平方和10和.001，相关−.6。'),
('第3—4题回归斜率？只残差化x会得到同一部分相关吗？','区分回归分子和相关分母。','斜率−.06/10=−.006；只残差化x时斜率相同，但原始y方差更大，相关分母不同，不是同一部分相关。'),
('行业残差[−3,1,2]截尾到[−1,1]，还中性吗？','检查组内和。','变[−1,1,1]、和1，已非组内均值0；再选股或非线性映射也可能破坏约束。'),
('信号1/2/3，收益−3%/−2%/−1%，Rank IC及最高组收益？','排序与绝对赚钱分开。','Rank IC=1，最高组仍−1%；正IC不能证明单边策略绝对盈利。'),
('IC .1/.2/.3/.4，按分母T求γ0、γ1和L1的HAC标准误。','去均值后配对滞后。','均值.25，γ0=.0125，γ1=.003125，权重.5，长期方差.015625，SE=.0625；四期仅作算术。'),
('上题L0的SE是多少？为何不等于普通样本t检验SE？','本章没有小样本修正。','√(.0125/4)=.0559017；普通独立样本方差通常分母T−1，口径不同。不得挑有利分母宣称显著。'),
('因子和收益各自删缺失、各自排名后再拼接，何时会出错？','共同证券集合。','各自样本不同会改变相对秩和间距；应先按永久ID匹配共同有效配对，再在该样本内排名并报告覆盖。'),
('用全部历史月份均值标准化，训练预测未来有何泄漏？当期截面标准化也一定泄漏吗？','参数时钟与信息集合。','跨期参数用了测试期信息；当期可知截面本身不必然泄漏，但数据、规则和参数选择必须在当时可用，不能混入未来收益。'),
('某月IC缺失，删掉该月后按相邻月做HAC是否妥当？HAC能解决试过1000个因子的问题吗？','时间网格与多重选择是两个问题。','不妥，删除后观测间隔改变，应定义完整月历处理方案；HAC只针对既定序列依赖，不修复多重选择、泄漏或结构突变。')]

BODY[35]=r"""

## 35.6 最小方差解必须连同可行域交付

两资产权重w和1−w，方差a、b、协方差c，V(w)=aw²+b(1−w)²+2cw(1−w)。协方差矩阵有效要求a,b≥0、c²≤ab。令D=a+b−2c=Var(r1−r2)≥0；D>0时驻点w*=(b−c)/D，完成平方后V(w)=V(w*)+D(w−w*)²。因此约束仅为闭区间[l,u]时，最优解是把w*投影到这个区间，不需要通用数值求解器。

D=0时，由半正定性可得a=b=c，所有权重风险相同；程序应返回“平坦目标”和可行区间，按预设规则选一个权重，不能除以0后声称找到了唯一解。相关为1且两波动不同则D仍可能大于0：允许卖空时可用对冲得到零方差；限制多头时通常选低波动资产。这是理想模型对完全线性关系的结果，不保证未来估计关系精确保持。

假设年波动20%、30%、相关.2，a=.04、b=.09、c=.012，无其他约束最优w=39/53=.735849，年波动约.180565。若个股约束.2≤w≤.6，则选.6，年波动√.03456=.185903。约束提高该模型内最小风险，但也可能减少估计误差和不可实施暴露；不能只比较目标函数数值而不比较估计可靠性。

## 35.7 换手约束的参照物是漂移持仓

前期各50万元，价格变化后60和50万元，调仓前净值110万元，参考权重w0=6/11。两资产满仓、忽略费用对净值的影响时，单边换手定义τ=.5Σ|目标权重−漂移权重|=|w−w0|。τ≤.03便得到区间[w0−.03,w0+.03]；与.2≤w≤.6相交后，上端为.5754545，故最小方差解被限制在该端点，年波动约.187965。

区间为空表示不可行。例如要求w≥.8，同时从w0=.5最多变动.1，没有可行组合。降低限制、卖出受限股票、引入现金都有不同经济含义，必须按预先约定处理，不能静默裁剪出一个仍不满足约束的订单。本章解析区间只涵盖两资产、多头、满仓及权重式换手，未解决多资产行业约束与真实费用联合优化。

## 35.8 逆波动权重与等风险贡献：两资产的特殊结论

组合波动σp>0时，资产i的波动风险贡献RC_i=w_i(Σw)_i/σp，各项相加等于σp；有对冲作用的资产贡献可能为负。两风险资产、波动均为正、权重均为正时，RC1=RC2中的协方差交叉项抵消，得到w²σ1²=(1−w)²σ2²，所以w=σ2/(σ1+σ2)。这正是归一化逆波动权重，并不要求相关系数为0。完全负相关且按该权重抵消到σp=0时，除以σp的贡献定义失效，需单独说明。

三资产一般不再有此结论。假设年波动10%、20%、30%，只有资产1和2的相关为.8，其余两对为0。逆波动权重为[6/11,3/11,2/11]，三项“权重×波动”相同，但风险贡献占比为[9/23,9/23,5/23]，约39.13%、39.13%、21.74%，并非各1/3。若相关矩阵各行和相同且贡献定义有效，逆波动才会给出等贡献；等相关是一个充分例子。本节修正把“两资产成立”与“一般多资产不成立”混成一句的粗略说法。

风险贡献是给定协方差与权重的分解，不是风险的因果归属；样本矩阵变化会改变它。年化简单收益协方差也依赖时间聚合假设，第33章已说明平方根时间规则的限制。

## 35.9 收缩改善条件数需要检查目标矩阵

设S半正定，F半正定，0≤λ≤1，则(1−λ)S+λF半正定；对任意向量z，二次型是两个非负数的加权和。若F正定且λ>0，混合矩阵正定。但F本身奇异时，不能保证可逆，例如零方差资产在对角目标中仍然是零。无效、非半正定的原始估计也不应在未记录原因的情况下靠收缩掩盖。

本实验取F=diag(S)，λ=.5，保留a=.04、b=.09，把c=.012压到.006，最小方差w=(.09−.006)/(.13−.012)=42/59=.711864。它是指定强度的对角收缩演示；不是自动估计最优强度的Ledoit–Wolf实现，也不是scikit-learn文档中常见的F=tr(S)/p×I等方差目标。两种目标不同，应在报告里写出矩阵而不是只写“做了收缩”。

## 35.10 费用进入现金守恒，而不只写在收益率后面

继续使用调仓前资产市值[60,50]万元，目标是扣费后各50%。假设无外部出入金、可分割交易、同一成交价格、每单位买入或卖出金额均收费c=.001，无其他费用或冲击。这是教学费率，并非A股实际费率表。设扣费后净值V'，自融资条件为V'=110−cΣ|w_iV'−持仓市值_i|。

解得V'=109.99万元，每项54.995万元；卖出资产1金额5.005、买入资产2金额4.995，总成交10，费用.01。卖出−买入=.01正好支付费用，目标权重基于扣费后净值，现金残差为0。若机械地各交易5万元再另扣费，就必须说明费用从何处支付以及扣费后权重变化。

本例总成交额/调仓前净值=10/110=.090909；按半总成交额定义的单边换手=.0454545。不同系统也会用买入额或卖出额定义单边换手，费用存在时二者不完全相等，所以名称后必须附公式。旧目标50/50虽然不变，实际成交绝不是0。

实验通过单调方程二分求扣费后净值：在满仓多头、目标和为1、0≤c<1条件下，F(V)=V+cΣ|w_iV−h_i|−Σh_i严格递增，有唯一根。它没有模拟成交量容量、买卖不同费率、离散股数、价格冲击或现金仓位；扩展这些条件必须重新建立资金账本，而非直接套本例。
"""
LAB[35]=r"""
from math import sqrt, isclose, isfinite

def covariance2(a,b,c):
    if any(not isfinite(x) for x in (a,b,c)) or a<0 or b<0 or c*c>a*b+1e-14*max(a*b,c*c,1e-300):
        raise ValueError('协方差矩阵须半正定')
    return a,b,c

def variance2(w,a,b,c):
    covariance2(a,b,c)
    if not isfinite(w): raise ValueError('权重须有限')
    return a*w*w+b*(1-w)**2+2*c*w*(1-w)

def bounded_minimum(a,b,c,lower=0,upper=1,reference=None,turnover=None):
    covariance2(a,b,c)
    if not all(isfinite(v) for v in (lower,upper)) or not 0<=lower<=upper<=1:
        raise ValueError('多头权重区间错误')
    if turnover is not None:
        if reference is None or not isfinite(reference) or not 0<=reference<=1 or not isfinite(turnover) or turnover<0:
            raise ValueError('换手需合法参照持仓')
        lower=max(lower,reference-turnover); upper=min(upper,reference+turnover)
    if lower>upper: raise ValueError('约束不可行')
    d=a+b-2*c
    if d<=1e-14*max(a,b,abs(c),1e-300):
        w=(lower+upper)/2; status='flat'
    else:
        w=min(upper,max(lower,(b-c)/d)); status='unique'
    return {'weight':w,'variance':variance2(w,a,b,c),'status':status,'interval':(lower,upper)}

def risk_contributions2(w,a,b,c):
    v=variance2(w,a,b,c)
    if v<=0: raise ValueError('零波动时贡献未定义')
    vol=sqrt(v)
    return [w*(a*w+c*(1-w))/vol,(1-w)*(c*w+b*(1-w))/vol]

def shrink2(a,b,c,lam):
    covariance2(a,b,c)
    if not isfinite(lam) or not 0<=lam<=1: raise ValueError('收缩强度0至1')
    return a,b,(1-lam)*c

def rebalance_values(holdings,target,fee):
    if len(holdings)!=len(target) or not holdings or any(not isfinite(x) or x<0 for x in list(holdings)+list(target)):
        raise ValueError('非负持仓与目标须配对')
    pre=sum(holdings)
    if pre<=0 or not isclose(sum(target),1,rel_tol=0,abs_tol=1e-12) or not isfinite(fee) or not 0<=fee<1:
        raise ValueError('正净值、满仓目标、0至1费率')
    lo=0.0; hi=pre
    for _ in range(100):
        mid=(lo+hi)/2
        residual=mid+fee*sum(abs(w*mid-h) for w,h in zip(target,holdings))-pre
        if residual>0: hi=mid
        else: lo=mid
    after=(lo+hi)/2; trades=[w*after-h for w,h in zip(target,holdings)]
    gross=sum(abs(x) for x in trades); cost=fee*gross
    return {'after':after,'trades':trades,'cost':cost,'gross':gross,'turnover':gross/(2*pre)}

# %% 无约束、多头上限与漂移换手限制
base=bounded_minimum(.04,.09,.012)
capped=bounded_minimum(.04,.09,.012,.2,.6)
limited=bounded_minimum(.04,.09,.012,.2,.6,6/11,.03)
assert isclose(base['weight'],39/53) and isclose(capped['weight'],.6)
assert isclose(limited['weight'],6/11+.03)
assert all(base['variance']<=variance2(i/1000,.04,.09,.012)+1e-12 for i in range(1001))
print({'最小风险':base,'权重上限':capped,'换手限制':limited})

# %% 两资产逆波动精确ERC；三资产反例，所用相关矩阵半正定
rc=risk_contributions2(.6,.04,.09,.012)
assert isclose(rc[0],rc[1])
weights=[6/11,3/11,2/11]; cov=[[.01,.016,0],[.016,.04,0],[0,0,.09]]
product=[sum(row[j]*weights[j] for j in range(3)) for row in cov]
variance=sum(w*x for w,x in zip(weights,product))
shares=[w*x/variance for w,x in zip(weights,product)]
assert all(isclose(x,y) for x,y in zip(shares,[9/23,9/23,5/23]))
print({'两资产RC':rc,'三资产逆波动风险占比':shares})

# %% 指定对角收缩，不称为最优Ledoit–Wolf估计
shrunk=bounded_minimum(*shrink2(.04,.09,.012,.5))
assert isclose(shrunk['weight'],42/59)
print({'对角收缩':shrunk})

# %% 万元：扣费后目标权重与资金守恒
ledger=rebalance_values([60,50],[.5,.5],.001)
assert isclose(ledger['after'],109.99) and isclose(ledger['cost'],.01)
assert isclose(sum(ledger['trades'])+ledger['cost'],0,abs_tol=1e-12)
print({'调仓账本万元':ledger})
"""
EXERCISES[35]=[
('年波动20%/30%、相关.2，求协方差和无约束最小方差权重。','检查矩阵与分母。','c=.012，D=.106，w=.078/.106=39/53=.735849；另一资产14/53，矩阵半正定。'),
('上题加.2≤w≤.6，最优权重与年波动？','利用凸二次函数的区间投影。','w=.6，方差.03456，波动.185903；不是强行重新归一化两个独立裁剪权重。'),
('a=b=c=.04时为何没有唯一风险最优权重？','D=Var(r1−r2)。','D=0，V(w)=.04；整个可行区间均最优，需记录平坦目标及预设选点规则。'),
('协方差a=.04、b=.09、c=.08能直接优化吗？','行列式。','不能，c²=.0064>ab=.0036，矩阵非半正定，对应相关超过1；应拒绝输入。'),
('漂移持仓60/50万元，单边换手上限3%，再加w在.2到.6，最优w？','相对于6/11，不是旧目标.5。','交集[6/11−.03,6/11+.03]，无约束解在上方，故w=.5754545；波动约.187965。'),
('w≥.8，参照w0=.5、换手最多.1，有解吗？','求约束交集。','无解，[.8,1]与[.4,.6]不交；应输出不可行及预设处理，不得静默违反约束。'),
('推导两资产等风险贡献权重。相关改变是否必然使逆波动失效？','协方差交叉项抵消。','正权重、正波动且组合波动非零时，w²σ1²=(1−w)²σ2²，w=σ2/(σ1+σ2)，任意有效相关均成立；完全负相关零波动情形贡献未定义。'),
('三资产波动.1/.2/.3，相关仅ρ12=.8，其余0，逆波动风险占比？','先令每项加权波动相同。','权重6/11、3/11、2/11；方差贡献比例1.8:1.8:1，归一化9/23、9/23、5/23，不是等贡献。'),
('对第1题协方差做λ=.5的对角收缩，最优w？为何不是完整Ledoit–Wolf？','仅压低非对角项。','c=.006，w=.084/.118=42/59=.711864；λ人工指定且目标diag(S)，未估计最优强度，也不同于等方差单位阵目标。'),
('半正定样本和目标混合一定正定吗？','考察共同零空间。','不一定；目标正定且λ>0是充分条件。若两者同方向方差均为0，混合仍奇异。'),
('60/50万元持仓调到扣费后50/50，买卖均收.1%，求净值、交易与费用。','费用从卖出净额支付。','净值109.99，各54.995；卖5.005、买4.995、总成交10、费用.01万元，卖减买正好覆盖费用。'),
('上题总成交比例、半总成交单边换手？原目标未变为何不能记0？','分母用调仓前110万元。','总成交/净值=10/110=.090909，半总成交=.0454545；价格漂移改变实际权重，恢复旧目标仍交易。买/卖单侧与半总成交定义在有费用时并非完全相同。')]

READING={
31:'D英文5版第7章估值与主动投资、第18章财报质量，C英文完整版2025 Release第14章市场效率与行为金融按主题选读。R1的实时信息区间用于时点概念；数据库协议与事件账本为原创。见[第七批核验](../../references/ALIGNMENT_V03_PART07.md)。',
32:'D英文5版第12章盈利能力、第13章增长、第18章财报质量；C第12章风险收益的其他视角。选读R2/R3作者数据字典，重点核对OP、INV与2×3排序，不把自定义信号当标准因子复制。见[核验](../../references/ALIGNMENT_V03_PART07.md)。',
33:'C英文完整版2025 Release第11章收益风险与CAPM、第12章其他风险视角、第14章市场效率；D第19章权益风险。选读R4动量窗口与R1历史版本说明，时间聚合推导为原创。见[核验](../../references/ALIGNMENT_V03_PART07.md)。',
34:'C第11—12章风险收益、D第7章主动投资作经济背景；排名、预处理及HAC另读R5/R6/R7官方技术文档，不能冒称四本主教材均讲授这些实现细节。见[核验](../../references/ALIGNMENT_V03_PART07.md)。',
35:'C英文完整版2025 Release第11章组合与风险收益；D第19章权益风险作联系。R8选读协方差估计，R9仅作组合交易问题的研究入口；两资产推导、风险反例与扣费后账本为原创。见[核验](../../references/ALIGNMENT_V03_PART07.md)。'
}
EXIT={
31:'提交双时钟版本表、可交易时隙与标签成熟表；E01、E05、E09需证明历史结果不受未来修订污染。',
32:'提交指标定义表、覆盖报告与六组合权重；E03、E07、E10需区分会计口径、收益率与组合复制。',
33:'提交逐月窗口、宏观版本和状态切换日志；E01、E05、E09需解释时间索引、协方差与未知未来。',
34:'提交共同样本、行业残差与HAC口径报告；E04、E08、E12需完成独立计算并识别统计证据边界。',
35:'提交可行区间、风险贡献与调仓现金账本；E05、E07、E11必须通过约束、例外条件及资金守恒检查。'
}

def deepen(chapters):
    for c in chapters:
        n=c.number
        c.body+=BODY[n]; c.lab=LAB[n]; c.exercises=EXERCISES[n]; c.reading=READING[n]
        c.edition='v0.3第七批深化稿（第31—35章）'
        c.study_note='建议分3次、每次60—90分钟：先固定信息时点、指标与样本协议，再手算因子和诊断，最后运行约束、泄漏反例及资金对账。全部数字为假设教学数据。'
        c.exit_task=EXIT[n]+' 核心题建议至少48/64分，修正关键错误后进入可复现回测篇。'
