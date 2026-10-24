"""第五批深化：三表、重构、盈利、会计质量与预测。"""
BODY, LAB, EXERCISES = {}, {}, {}

BODY[21] = r"""

## 21.6 利息分类改变CFO，不改变现金总额

本案例明确为一般非金融企业，依据R1现金流量表准则第8、15、16条：经营现金主表按直接法列示，附注提供利润到经营现金的调节，借款利息支付列筹资。金融企业、其他制度和特殊交易需另核。过去版本的21.5是利息支付后的中间现金量，不再标作本例报表CFO。

Y1收入150、应收增加5，假设无税价差、退款和其他应收调整，客户收现145亿元。成本费用合计120扣折旧6为114，再加存货增加2、减应付增加3，经营付现113；这一合并计算不把制造业营业成本直接当原料采购。实际所得税6.5全部列经营，直接法CFO=145−113−6.5=25.5。它与NI19.5+折旧6+利息4−净经营占款4相同。

利息列筹资时，CFF=净借款2−分红5−利息4=−7，合计25.5−10−7=8.5。若仅为分析比较把利息移入经营，则CFO下降4为21.5、CFF上升4为−3，总额仍8.5。分类标签不改变经济支付，但会改变“利润/经营现金”之类指标；跨制度横比前必须统一。

## 21.7 控制、合并与归母并非同一个百分比

合并范围依据控制判断，不能只凭持股是否超过50%作全部结论。本节非投资性主体、控制已经成立，无商誉、公允价值调整和内部交易。假设母公司现金50、对子公司投资48、负债0、权益98亿元；子公司现金10、存货30、固定资产60、负债40、权益60。母公司持股80%，投资账面48恰等于子公司净资产的80%。

合并时纳入子公司全部资产负债，再抵销投资48与对应子公司权益。集团资产50+100=150、负债40、归母权益98、少数股东权益12，合计150。不是把子公司资产100仅乘80%后逐项加总。若另一个完整年度母公司自有业务利润12、子公司利润10且无其他调整，合并利润22、归母20、少数股东2。

归母PE配归母普通股利润与对应市值；合并FCFF若覆盖子公司100%经营，权益桥接还须处理少数股东价值。少数股东的账面权益12不是自动等于其市场价值。合并表可见的现金也未必能由母公司自由调拨，应另看限制与子公司融资安排。

## 21.8 抵销内部销售与未实现利润

独立商品案例，忽略税与减值，单位万元：母公司把成本80的货物以120卖给全资子公司；子公司对外售出数量的60%，收入90，剩余40%尚在集团内。母公司个别利润40，子公司个别利润90−72=18，简单相加利润58。集团对外实现的成本其实只有80×60%=48，因此合并毛利42。

内部收入120要抵销，期末存货中的内部利润(120−80)×40%=16也要抵销；存货由子公司账面的48降为集团成本32，利润由58降42。内部货款即使已经付清，也没有让集团获得外部现金，更不会令剩余货物的利润变成已实现。真实场景还须处理所得税暂时性差异、上下游归属及内部损失是否表明真实减值，本例不覆盖这些复杂项目。

## 21.9 四张桥接表比一个平衡检查更有效

至少分别检查：现金余额变动；权益变动；固定资产原值/累计折旧/减值；应收总额/准备/回款。资产等于负债加权益可以被任意现金平衡项“修好”，但它解释不了现金从哪里来。Y1固定资产净额60+10−6=64，权益60+19.5−5=74.5，均应独立复算。

再设独立权益例，期初归母权益60，归母NI19.5、归母OCI−2、发行收款7、回购3、分红5，无其他变动，期末76.5亿元。只用NI与分红会少2；其中OCI与所有者交易都不是新增营业收入。回购和发行是否涉及费用、股份支付、库存股及少数股东变化须另建明细，不能一律归入利润。

## 21.10 业务证据如何进入历史底稿

先从年报业务章节写出客户付费对象、合同履约阶段、成本承担方与现金账期，再将其映射至收入、合同资产、存货及负债。政府客户的预算获批不自动等于企业收入；合同执行进度与客户支付安排是不同证据。

原值层保留报告期、发布日期、文档版本、单位、合并/母公司/归母范围、表名与位置；调整层另列抵销或重分类依据及方向。合并范围改变时，收入增长包含并表与有机增长，不可只用上年分母得出市场份额改善。量化处理中，同一公司同一期数据也可能存在多个披露版本，必须回到第2章的可用时间规则。来源与本批修正见[核验表](../../references/ALIGNMENT_V03_PART05.md)。
"""

LAB[21] = r"""
from math import isclose, isfinite

def historical_y1(interest_in_cfo=False):
    ni=(150-90-30-4)*.75
    received=150-(25-20)
    paid=(90+30-6)+(32-30)-(23-20)
    cfo=received-paid-6.5-(4 if interest_in_cfo else 0)
    cff=2-5-(0 if interest_in_cfo else 4)
    cash=10+cfo-10+cff
    ppe=60+10-6; equity=60+ni-5
    return dict(ni=ni,cfo=cfo,cfi=-10,cff=cff,cash=cash,ppe=ppe,
                equity=equity,assets=cash+25+32+ppe,claims=23+42+equity)

def equity_roll(begin,ni,oci=0,issue=0,buyback=0,dividend=0):
    if any(not isfinite(x) for x in (begin,ni,oci,issue,buyback,dividend)) or min(issue,buyback,dividend)<0:
        raise ValueError('金额有限，发行回购分红非负；亏损和负权益可以出现')
    return begin+ni+oci+issue-buyback-dividend

def simple_consolidation(parent_cash,investment,sub_assets,sub_debt,share):
    vals=(parent_cash,investment,sub_assets,sub_debt,share)
    if any(not isfinite(x) for x in vals) or min(vals)<0 or share>1 or sub_assets<sub_debt:
        raise ValueError('本例金额非负，持股0至1，子公司净资产非负')
    sub_equity=sub_assets-sub_debt
    if not isclose(investment,share*sub_equity):
        raise ValueError('本例仅处理无商誉、投资恰等于所占净资产的情况')
    # 控制已成立是题设，不从share自动推断控制。
    return dict(assets=parent_cash+sub_assets,debt=sub_debt,
                parent_equity=parent_cash+investment,nci=(1-share)*sub_equity)

def internal_goods(cost,transfer,external_revenue,sold_fraction):
    if any(not isfinite(x) for x in (cost,transfer,external_revenue,sold_fraction)) or min(cost,external_revenue)<0 or transfer<cost or not 0<=sold_fraction<=1:
        raise ValueError('无内部亏损/减值模型，数量销售比例须0至1')
    standalone_profit=transfer-cost+external_revenue-transfer*sold_fraction
    unrealized=(transfer-cost)*(1-sold_fraction)
    return dict(profit=standalone_profit-unrealized,
                inventory=cost*(1-sold_fraction),eliminated_profit=unrealized,
                revenue=external_revenue)

# %% 直接收付与三表勾稽
base=historical_y1(); alternative=historical_y1(True)
assert base['cfo']==25.5 and base['cff']==-7
assert base['cash']==18.5 and base['assets']==base['claims']==139.5
assert base['cash']==alternative['cash']
print({'一般企业现金分类':base,'利息后分析现金':alternative['cfo']})

# %% 控制后全额并表，再分少数股东
c=simple_consolidation(50,48,100,40,.8)
assert isclose(c['assets'],c['debt']+c['parent_equity']+c['nci'])
print({'合并资产负债亿元':c,'利润归属':{'合并':22,'归母':20,'少数':2}})

# %% 内部利润抵销与完整权益滚动
g=internal_goods(80,120,90,.6)
assert isclose(g['profit'],42) and isclose(g['inventory'],32)
assert equity_roll(60,19.5,-2,7,3,5)==76.5
print({'内部交易抵销万元':g,'完整期末权益亿元':76.5})
"""

EXERCISES[21]=[
('无税赊销10万元、结转存货成本6，未收款。利润、资产与现金各如何变？','区分收入确认和收现。','利润及权益增4，应收增10、存货减6，资产净增4；现金0。间接调节4−10+6=0。'),
('Y1收入150、应收初20末25亿元，无其他调整，客户收款多少？','用期初应收加收入减期末。','145亿元。含税、退款、合同资产、汇率或合并变化存在时不能直接套。'),
('Y1现金经营付款113、收款145、实际税6.5、利息4亿元。利息列筹资时CFO多少？','经营部分不再减筹资利息。','25.5亿元；利息后分析现金是21.5，二者不可共用CFO标签。'),
('Y1净借款2、分红5、利息支付4、资本开支10亿元，接上题并用期初现金10求期末。','CFF包括利息。','CFF=−7、CFI=−10，现金增8.5，期末18.5亿元。'),
('固定资产初60、投资10、折旧6亿元，无其他变化，期末多少？','本例净额滚动。','64亿元；真实资产处置、减值、并购与汇率须另列。'),
('母公司自有业务NI12、80%控股子公司NI10亿元，无内部交易和其他调整，合并与归母NI？','合并不按80%缩放全部利润。','合并22、归母20、少数股东2亿元。控制已经成立是题设。'),
('期初归母权益60，NI19.5、OCI−2、发行7、回购3、分红5亿元，期末权益？','所有非利润变化也要列出。','76.5亿元；60+19.5−2+7−3−5。'),
('为什么把现金塞成A=L+E的平衡数不够？','恒等式之外需要交易证据。','它可能掩盖漏利息、税、资本开支或合并范围错误；须独立核现金、权益、资产和应收滚动，不明差额保留待查。'),
('母公司现金50、投资48、无负债；80%被控子公司资产100、负债40亿元，无商誉或其他调整，求合并资产及权益归属。','抵销投资与对应净资产。','集团资产150、负债40、归母权益98、少数股东12亿元；投资48抵销，不能将子公司各科目乘80%并表。'),
('集团内部将成本80的商品以120万元售出，购买子公司对外销售60%数量获收入90，其余未售，忽略税减值。合并毛利和库存多少？','未实现内部利润只对应剩余40%。','内部利润抵销16，合并毛利42、库存32万元；个别毛利合计58减16。外部收入90减集团成本48也得42。'),
('将本章利息4从筹资移到经营作分析对照，三类现金及期末现金如何变？','一个分类减，另一个加。','CFO25.5变21.5，CFF−7变−3，CFI−10不变，期末18.5不变；不是企业多了或少了4现金。'),
('构建一项“收入增长来自新收购”的证据链，并指出历史量化回测的版本限制。','报告范围和公开时间同时记录。','核对收购日、并表期、被购业务收入及抵销，另拆同范围有机增长；保存原文、报告期、发布日期、版本、范围、单位和调整。不得把后来的重述覆盖到披露前可交易信息集。')]

BODY[22]=r"""

## 22.6 分类变了，利润和资本必须一起变

本例NOA排除全部现金，是分析约定而非真实企业无需现金。若Y0、Y1均需最低经营现金5亿元，且现金无利息收入，则Y0 NOA从90到95、NFO从30到35，Y1 NOA从98到103、NFO从23.5到28.5，权益仍60与74.5。经营现金增加使可扣减债务的融资现金减少，因此NOA和NFO应同向增加，而不是一个增加一个减少。

期内经营现金固定5时，ΔNOA仍8、OI仍22.5，FCFF仍14.5；平均NOA却由94变99，RNOA由23.936170%降为22.727273%。若必要经营现金随业务上升，还须把其增加计入经营再投资。分类改变比率，不自动改变交易经济价值；现金收益、估值加回和回报分母须一致。

## 22.7 不同税项目不能统一乘有效税率

独立假设，单位万元：EBIT30，利息支出4、金融利息收入2；经营所得和可抵扣债务利息税率25%，金融利息收入税率20%，当期全部计税且税盾可用。经营税7.5，融资支出税盾1，金融收入税.4，总税6.9。OI=22.5，NFE=4−1−(2−.4)=1.4，NI=21.1。

若用全公司有效税率6.9/28统一分配，会重新改变经营与融资贡献。报表有效税率、边际税率和模型税盾率的用途不同。真实企业还可能有递延税、不可抵扣支出、境外税及一次性税调整，需要逐项保留证据，不通过“调税率”凑平NI。

## 22.8 从NOA变化回到现金的正负号

设OI_rep为利润表口径的税后经营收益，J为**未进入该收益、却增加NOA且不消耗本期现金**的净调整，且其他经营交易均被正确纳入，则FCF=OI_rep+J−ΔNOA。J是经逐项定义的桥接项，不是随意填平的差额。

在Y1原例基础上，若另有税后经营OCI增加NOA5亿元，ΔNOA为13、OI_rep仍22.5，则FCF=22.5+5−13=14.5。若损失5已经扣入OI，同时降低NOA5，则OI17.5、ΔNOA3，仍14.5；不能再额外加同一减值5。综合经营收益包含OCI时，则直接用OI_comp−ΔNOA，不能双加。

再看独立初始租赁确认：使用权经营资产与融资租赁负债同时增加20、当期未支付现金、无当期收益，则J20抵销ΔNOA20，现金为0。这不决定后续租赁本金与利息如何预测。反过来，现金15购买净经营资产15，且无其他差额，本来就形成FCF−15，不能因“收购”二字将15全数加回。企业合并还须桥接购买价、商誉、取得现金和承接金融负债，不能只看一个余额差。

## 22.9 自由现金最后去了哪里

在无OCI、非现金融资和其他所有者变动的简化体系，令d为分红加回购减发行收入，权益滚动ΔE=OI−NFE−d；又ΔE=ΔNOA−ΔNFO。整理得：

$$FCF=OI-\Delta NOA=d+NFE-\Delta NFO.$$

Y1为14.5=5+3−(23.5−30)：现金支付给股东5、税后净融资费用3，另有6.5用于减少净金融负债。净债务下降可以来自还债，也可以来自融资资产增加；本例债务增加2而现金增加8.5，净债务仍降6.5。不能仅看债务总额增加就说经营现金全被分掉了。

## 22.10 干净盈余、价值桥和可复核映射

普通权益滚动可写E1=E0+综合收益−净所有者分配，若含优先股、少数股东或不同范围收益则先分离。NI和综合收益不同不是报表错误；只有模型用的收益与权益变动不匹配，才破坏用于剩余收益估值的会计桥。

估值时，经营价值减融资负债市场价值加融资资产价值，与“经营价值减净金融负债价值”二选一使用。账面NFO用于历史回报分解，市场价值桥用于估值，两者不能自动等同。真实重构表每一科目只映射一次，同时标明税、范围、现金与非现金调整；未匹配的科目应拒绝输出而不是默认为经营。参见[核验表](../../references/ALIGNMENT_V03_PART05.md)。
"""

LAB[22]=r"""
from math import isclose, isfinite

def reformulate(cash,ar,inventory,ppe,ap,debt,equity,operating_cash=0):
    vals=(cash,ar,inventory,ppe,ap,debt,equity,operating_cash)
    if any(not isfinite(x) for x in vals) or min(cash,ar,inventory,ppe,ap,debt,operating_cash)<0 or operating_cash>cash:
        raise ValueError('金额有限，经营现金不能超过现金，负权益允许')
    if not isclose(cash+ar+inventory+ppe,ap+debt+equity):
        raise ValueError('原始资产负债表不平衡')
    noa=ar+inventory+ppe+operating_cash-ap
    nfo=debt-(cash-operating_cash)
    return dict(noa=noa,nfo=nfo,equity=noa-nfo)

def allocate_tax(ebit,interest,financial_income,operating_rate,income_rate):
    vals=(ebit,interest,financial_income,operating_rate,income_rate)
    if any(not isfinite(x) for x in vals) or min(interest,financial_income)<0 or ebit<interest or not 0<=operating_rate<=1 or not 0<=income_rate<=1:
        raise ValueError('本例税前经营所得覆盖利息，税率0至1且税盾当期可用')
    operating_tax=ebit*operating_rate
    shield=interest*operating_rate; finance_tax=financial_income*income_rate
    total_tax=operating_tax-shield+finance_tax
    oi=ebit-operating_tax
    nfe=interest-shield-financial_income+finance_tax
    return dict(oi=oi,nfe=nfe,ni=oi-nfe,total_tax=total_tax)

def cash_from_noa(oi,noa0,noa1,noncash_outside_income=0):
    if any(not isfinite(x) for x in (oi,noa0,noa1,noncash_outside_income)):
        raise ValueError('桥接输入必须有限')
    return oi+noncash_outside_income-(noa1-noa0)

def fcff_from_cfo(cfo,capex,interest,tax,interest_in_cfo=False):
    if any(not isfinite(x) for x in (cfo,capex,interest,tax)) or min(capex,interest)<0 or not 0<=tax<=1:
        raise ValueError('本例资本开支和利息非负，税盾率0至1')
    return cfo-capex+(interest*(1-tax) if interest_in_cfo else -interest*tax)

# %% 分类不改变权益，经营现金改变NOA及NFO
y0=reformulate(10,20,30,60,20,40,60)
y1=reformulate(18.5,25,32,64,23,42,74.5)
shift=reformulate(18.5,25,32,64,23,42,74.5,5)
assert y1['noa']==98 and y1['nfo']==23.5
assert shift['noa']==103 and shift['nfo']==28.5
print({'Y0':y0,'Y1':y1,'保留经营现金5':shift})

# %% 税分配与两种报表现金分类
tax=allocate_tax(30,4,2,.25,.2)
assert isclose(tax['ni'],21.1) and isclose(tax['total_tax'],6.9)
assert fcff_from_cfo(25.5,10,4,.25)==14.5
assert fcff_from_cfo(21.5,10,4,.25,True)==14.5
print({'独立税例万元':tax,'基准FCFF亿元':14.5})

# %% OCI、损失、非现金租赁与现金投资不能同样加回
values=[cash_from_noa(22.5,90,103,5),cash_from_noa(17.5,90,93),
        cash_from_noa(0,100,120,20),cash_from_noa(0,100,115)]
assert values==[14.5,14.5,0,-15]
assert 5+3-(23.5-30)==14.5
print({'四个独立桥接结果':values,'股东分配加融资费用减净债务变化':14.5})
"""

EXERCISES[22]=[
('OA120、OL30、FO40、FA10亿元，求NOA、NFO和权益。','经营和融资分别净额。','NOA90、NFO30、权益60，假设目标权益范围与全部科目一致。'),
('在上题中把融资现金5改为经营现金，NOA、NFO、权益怎样变？','融资资产减少与经营资产增加同步。','NOA95、NFO35、权益仍60；不是NFO下降。现金收益与回报分母也须同步分类。'),
('EBIT30、利息4、金融收入2万元，经营和利息抵扣率25%、金融收入率20%，求OI、NFE、NI和税。','分别计算经营税、税盾和金融所得税。','经营税7.5，税盾1，金融税.4，总税6.9；OI22.5，NFE1.4，NI21.1万元。'),
('本例CFO25.5、资本开支10、利息4亿元，税25%、利息列筹资，FCFF多少？','经营税款已享受融资税盾。','25.5−4×25%−10=14.5亿元；不能再加税后利息。'),
('同样交易若分析性CFO已扣利息而为21.5亿元，怎样桥接FCFF？','恢复税后融资成本。','21.5+4×75%−10=14.5亿元。两种公式分别依赖各自分类和税现金假设。'),
('OI22.5、NOA初90末98亿元，无其他调整，自由现金多少？','收益减经营再投资。','14.5亿元；必须确认利润和NOA的覆盖范围相同。'),
('若上题额外税后经营OCI使NOA增加5而未进OI，FCF多少？','给OI和ΔNOA各自正确口径。','22.5+5−(103−90)=14.5亿元；若OI已包括OCI则不再加5。'),
('经营价值200、金融负债40、融资现金10亿元，普通权益价值？再加10现金对吗？','选择总债务或净债务的一条桥。','200−40+10=170，或200−30=170；再加10会重复。账面债务不自动等于市场价值。'),
('原OI22.5、ΔNOA8亿元，确认无税经营减值5并已经计入OI及资产，现金桥怎样变？','同一损失同时改变两端。','OI17.5、ΔNOA3，FCF仍14.5；若再额外加回5会重算。其余非现金调整仍需逐项核对。'),
('期初确认使用权资产/租赁负债各20万元且未付款，与现金15买净经营资产15有何不同？','未进收益的非现金资产增加与真实支付区别。','前者ΔNOA20、非现金调整J20，FCF0；后者ΔNOA15、J0，FCF−15。不能把所有取得资产都称为现金支出或都加回。'),
('由ΔE=OI−NFE−d和E=NOA−NFO推导自由现金用途式，并代入Y1。','消去ΔE。','FCF=d+NFE−ΔNFO=5+3−(23.5−30)=14.5亿元；债务虽增2，现金增8.5使净债务降6.5。需排除非现金融资等额外变化。'),
('设计一份可防止现金重复加回、OCI遗漏和少数股东错配的重构表。','科目映射与跨表调整成对保留。','记录原值、来源、范围、经营/融资归属、期初末、收益对应项、税、OCI/非现金调整及估值桥；每科目只归一次，先核原表平衡，再核目标权益及综合收益滚动，未匹配项待查。')]

BODY[23]=r"""

## 23.6 不除以净债务，也能分解ROE

从NI=OI−NFE及NOA=E+NFO直接整理，可写：

$$ROE=RNOA+\frac{RNOA\,NFO-NFE}{E}.$$

本式只需NOA及E非零，不必先除以NFO。在平均净金融负债为0时，NBC=NFE/NFO无定义；公司仍可能同时有高息债务和低息金融资产，NFE并不必然为0。假设平均NOA100、NFO0、E100亿元，OI12、NFE1，ROE11%，而不是因“净债务为零”就断言等于RNOA12%。

净金融资产情形也应解释符号。NOA100、NFO−20、E120，OI12、NFE−.6，则净金融收入.6，ROE12.6/120=10.5%。RNOA12%、净金融资产收益率3%，持有低于经营回报的金融资产使整体权益回报较低。这不证明应把现金全投入经营，还需正NPV机会、现金需求和风险约束。

## 23.7 经营负债也影响资本回报

RNOA扣除了经营负债，不能据此称供应商融资免费。设平均经营资产OA、经营负债OL，NOA=OA−OL；选择明确的税后机会成本基准i，定义分析性资产回报ROOA=(OI+iOL)/OA。代数上有：

$$RNOA=ROOA+\frac{OL}{NOA}(ROOA-i).$$

假设OA120、OL30、OI15万元，i4%，则ROOA=(15+1.2)/120=13.5%，OL/NOA=1/3，RNOA=13.5%+(13.5%−4%)/3=16.666667%。此处1.2是用于分解的机会成本估计，不是报表已披露的实际利息；不能再从OI重复扣除。采购价格、折扣与账期可能共同变化，延长应付天数提高分母效率的同时也可能损害经营利润。

## 23.8 资本进入时间决定回报分母

假设年初投入资本100万元，10月1日新增120并开始经营，其余资本不变。采用月度均匀计时、前9月100后3月220，时间加权资本130；首尾平均则160。若全年NOPAT26，时间加权回报20%，首尾平均为16.25%。两者差异来自资本暴露时间，不代表企业额外赚了利润。

季度数据、并购时点与建设期可以要求更细加权。若母公司利润只纳入购买日以后，而资本分母却纳入全年被购资产，回报就错配。初期资本衡量上一期投入产生的利润，平均资本衡量期间平均占用，两种用途都可能合理，但不能用不同分母的历史数直接宣称回报改善。净资产为负或接近零时，展示金额桥通常比报一个极高百分比更有意义。

## 23.9 将回报变化分配给利润率和周转

RNOA=PM×ATO。若PM从15%降到12%，ATO从1.6升到2，两个时点RNOA均为24%。单看“利润率下降3个百分点”不能判定总回报下降；也不能把−3个百分点直接加上周转增加.4次，因为单位不同。

用两种顺序的平均分配交互项：利润率贡献ΔPM×(ATO0+ATO1)/2=−5.4个百分点，周转贡献ΔATO×(PM0+PM1)/2=+5.4个百分点。两者正好加总总变化0。该对称分解是描述性归因，不表示把账期改变会因果地提高5.4个百分点；同一竞争冲击可能同时改变PM和ATO。量化因子可分别记录水平和变化，但需统一行业、会计政策及可得时间。

## 23.10 账面经济利润如何接到投资价值

ROIC大于WACC可以作为价值创造线索，但单期账面比率不能替代现金估值。独立无税、无营运资本例：今天投资100万元、两年直线折旧各50、每年现金经营盈余60，期末资产无残值。每年NOPAT10；按期初资本100和50、资本成本10%，经济利润分别0和5。

DCF净现值=−100+60/1.1+60/1.1²=4.132231；经济利润现值=0/1.1+5/1.1²也为4.132231。勾稽依赖资本滚动、费用确认与现金一致，资本收费时点也须一致；若把平均资本75和25直接用于同一时点收费而不调整，将得到另一结果。第一年ROIC10%等于门槛并不表示整个两年项目NPV为0，未来资本回收和收益仍影响价值。参考范围见[核验表](../../references/ALIGNMENT_V03_PART05.md)。
"""

LAB[23]=r"""
from math import isclose, isfinite

def profitability(oi,nfe,noa,nfo):
    if any(not isfinite(x) for x in (oi,nfe,noa,nfo)) or noa<=0 or noa-nfo<=0:
        raise ValueError('本教学比较只接受正NOA与正权益，其他情形另作金额分析')
    equity=noa-nfo; rnoa=oi/noa
    leverage_effect=(rnoa*nfo-nfe)/equity
    return dict(rnoa=rnoa,roe=(oi-nfe)/equity,leverage_effect=leverage_effect,
                nbc=None if nfo==0 else nfe/nfo,flev=nfo/equity)

def operating_leverage(oa,ol,oi,benchmark):
    if any(not isfinite(x) for x in (oa,ol,oi,benchmark)) or not 0<=ol<oa or benchmark<0:
        raise ValueError('经营资产须超过非负经营负债，基准率非负')
    noa=oa-ol; rooa=(oi+benchmark*ol)/oa
    return dict(rooa=rooa,rnoa=oi/noa,olleverage=ol/noa,
                effect=ol/noa*(rooa-benchmark))

def weighted_capital(segments):
    if not segments or any(not isfinite(v) or not isfinite(w) or v<0 or w<=0 for v,w in segments):
        raise ValueError('资本非负，每段时长正且有限')
    return sum(v*w for v,w in segments)/sum(w for v,w in segments)

def margin_turnover(pm0,pm1,ato0,ato1):
    if any(not isfinite(x) for x in (pm0,pm1,ato0,ato1)) or min(ato0,ato1)<0:
        raise ValueError('输入有限，周转非负；利润率可为负')
    return dict(margin=(pm1-pm0)*(ato0+ato1)/2,
                turnover=(ato1-ato0)*(pm0+pm1)/2,total=pm1*ato1-pm0*ato0)

# %% 基准、零净债务及净金融资产
base=profitability(22.5,3,94,26.75)
zero=profitability(12,1,100,0); net_asset=profitability(12,-.6,100,-20)
assert isclose(base['roe'],base['rnoa']+base['leverage_effect'])
assert zero['nbc'] is None and isclose(zero['roe'],.11)
assert isclose(net_asset['roe'],.105)
print({'Y1回报':base,'零净债务':zero,'净金融资产':net_asset})

# %% 经营负债杠杆与资本暴露时间
op=operating_leverage(120,30,15,.04)
assert isclose(op['rnoa'],op['rooa']+op['effect'])
weighted=weighted_capital([(100,9),(220,3)])
assert weighted==130
print({'经营负债分解':op,'时间加权资本':weighted,'两种回报':(26/130,26/160)})

# %% 描述性归因与现金/经济利润两条估值
effects=margin_turnover(.15,.12,1.6,2)
assert isclose(effects['margin']+effects['turnover'],effects['total'],abs_tol=1e-12)
dcf=-100+60/1.1+60/1.1**2
ep=[10-.1*100,10-.1*50]
assert isclose(dcf,ep[0]/1.1+ep[1]/1.1**2)
print({'回报变化贡献':effects,'两年项目NPV':dcf,'期初资本收费的EP':ep})
"""

EXERCISES[23]=[
('净利率5%、总资产周转2次、权益乘数3，ROE？','三个比率期间及平均分母须一致。','30%；是恒等式，不证明高ROE来自经营优势。'),
('RNOA12%、NBC6%、FLEV.5，求ROE及杠杆贡献。','spread乘净融资杠杆。','ROE15%，贡献3个百分点；不是3%的相对增长。'),
('RNOA4%、NBC6%、FLEV1，ROE？','负spread也被放大。','2%，杠杆贡献−2个百分点；不能只看负债成本低于股权成本。'),
('Y1平均NOA94、NFO26.75、权益67.25亿元，OI22.5、NFE3，求ROE和RNOA。','收益与资本范围统一。','ROE19.5/67.25=28.996283%，RNOA22.5/94=23.936170%；差约5.060112个百分点。'),
('NOA100、NFO0、OI12、NFE1亿元，ROE是否12%？','不用除以NFO的形式。','不是，E100、NI11，ROE11%；NBC无定义，净债务为零不能保证融资净费用为零。'),
('NOA100、NFO−20、OI12、NFE−.6亿元，ROE多少？','净金融收入为正。','E120、NI12.6，ROE10.5%；金融资产回报3%低于RNOA12%，但并不能据此忽视流动性需求。'),
('IC200、NOPAT24亿元、要求回报9%，经济利润？','资本收费与收益时点相同。','24−18=6亿元，ROIC12%、spread3个百分点；IC时间口径须明确。'),
('为什么不能将RNOA直接当成所有数据库的ROIC？','列出资本和收益的具体定义。','经营现金、商誉、租赁、税、少数股东及期初/平均资本处理可能不同；先核分子分母再比较。'),
('OA120、OL30、OI15万元，税后机会成本基准4%，推导并计算经营负债杠杆分解。','先定义ROOA=(OI+iOL)/OA。','ROOA13.5%，OL/NOA=1/3；RNOA=13.5%+(13.5%−4%)/3=16.666667%。1.2为基准隐含成本，不是已披露利息。'),
('资本前9月100、后3月220万元，NOPAT26，按月加权与首尾平均的回报？','新增资本只占用3个月。','加权资本130、回报20%；首尾平均160、回报16.25%。资本使用时间与利润覆盖必须相配。'),
('PM15%变12%、ATO1.6变2，给出对称分解。','把交互项平均分到两个变量。','利润率贡献−.03×1.8=−.054，周转贡献.4×.135=.054，总变化0，即各−5.4/+5.4个百分点；不是因果识别。'),
('无税项目期初投100、两年现金盈余各60、折旧各50、残值0万元，k10%。用DCF和期初资本经济利润核NPV。','资本依次100、50、0，NOPAT各10。','DCF4.132231万元；EP为0和5，现值5/1.1²=4.132231。不能未经时点调整改用平均资本收费，也不能仅凭首年ROIC等于k判NPV为零。')]

BODY[24]=r"""

## 24.6 研发资本化首先是确认条件，不是美化利润的开关

R2《企业会计准则第6号》区分研究与开发：研究阶段支出费用化；开发阶段能否确认资产取决于技术可行性、完成使用或出售意图、未来收益依据、资源保障和可靠计量等条件同时满足。过去已费用化的支出不能因后来成功就回写成报告资产。摊销从可供使用时开始，不能简单从支付时或立项时开始。

分析者为了可比性建立“研发资本”，与要求公司修改法定财报是两回事。应保留法定利润和资产，并另列分析重述、寿命假设及敏感性。经济寿命三年也不表示所有项目确定三年成功，失败、技术替代和维护投入会影响剩余价值。

## 24.7 研发批次滚动：不能只加回当年费用

独立无税分析例，Y1—Y3期初各投入12、15、18万元，每批当期可供使用，三年直线摊销，无期初研发资本和减值。Y1摊销4、期末资产8；Y2摊销4+5=9、资产8+15−9=14；Y3摊销4+5+6=15、资产14+18−15=17。相对全部费用化的当年利润差依次8、6、3。

若Y4、Y5不再投入，剩余摊销分别11与6，资产归零。五年摊销总额45等于三批总支出45，只是时间不同。只加回当年研发而不摊销旧批次会持续高估利润；只改利润不改NOA则会虚增回报。

再加一组税务假设：现金税始终允许支出当期全额扣除，税率25%，但分析资产按上述路径资本化，税基为0，不代表中国真实研发扣除规则。Y1分析递延税负债为8×25%=2、净经营资产增加6、分析税后利润也增加6。两端同时变化，FCF调整为6−6=0。若仅加税后利润而忘了研发资产及递延税，就会把会计重述误当新增现金。

## 24.8 应计因子必须记录定义与现金分类

NI−CFO是便于教学的现金流量表代理指标，不等于所有学术研究的应计定义。NI20、CFO8、平均资产100万元时为12%；若同一公司支付利息3原列经营、比较时改列筹资，CFO变11，应计率变9%，利润及总现金都没变。跨制度差异可能被误读成会计质量差异。

应计指标还会受并购导致的资产余额跳变、汇率、资产处置和合并范围影响。用资产负债表变动推应计与用现金流表推应计并非总相同；先规定目标、税和非现金事项，才可以谈哪个指标更合适。零或负平均资产、极端分母和缺失值不能直接输出0去参与排序。

历史研究使用首次可得版本，最新重述可用于事后解释但不得回填成当时已知。高应计作为预测信号需要样本外检验；它既不证明造假，也不自动提供可交易收益。本章不虚构样本系数或声称任何A股因子已经被验证。

## 24.9 扣非、核心盈利和预测盈利是三层概念

R4为证监会2023年12月22日公布的非经常性损益规则，用于所规定的披露分类；估值分析还需判断可持续性与资产变化，不能把分析师的调整表冒称法定扣非表。本书没有核定任何真实公司的扣非金额。政府补助是否符合例外条件不能仅凭“每年都有”判断；项目性质、标准、持续影响及披露依据须逐项核查。

假设报告NI24万元，包含税前设备出售收益8和独立诉讼损失2，二者按25%税率当期生效，分析判断两者不重复发生。预测基准NI=24−8×.75+2×.75=19.5。此时不是简单减8加2；也不能把已是税后金额再乘一次税率。设备已卖出，下一期产能、折旧和现金投资还须同时调整，不能只剔除收益却继续保留全部生产能力。

## 24.10 减值后的“改善”与证据分级

假设期初某资产账面100万元、剩余寿命5年、残值0、无税，发生减值40后余值60，仍用未来5年直线折旧，则每年折旧从20变12。在经营付现和收入未变时，后续利润每年高8，不代表竞争优势加强。分析可同时展示原资本基准和减值后资本回报，但不能把历史损失当作永远与价值无关。

核查表保留事实、合理解释、所需证据及结论强度。例：“应收增长快于收入”是事实；集中交付、信用期调整或回收恶化是竞争解释；合同、账龄和后续收款是证据。缺少证据时保留待核，不能据单比率写造假结论。对模型则落实为回款时间、损失率和收入确认情景，记录调整不确定性。来源及全文对照限制见[核验表](../../references/ALIGNMENT_V03_PART05.md)。
"""

LAB[24]=r"""
from math import isclose, isfinite

def research_cohorts(spending,life,tax=0):
    if isinstance(life,bool) or not isinstance(life,int) or life<=0 or not spending:
        raise ValueError('寿命为正整数，期初可用支出序列非空')
    if any(not isfinite(x) or x<0 for x in spending) or not isfinite(tax) or not 0<=tax<=1:
        raise ValueError('支出非负，税率0至1；本例税务当期全额扣除')
    asset=0; rows=[]
    for year,current in enumerate(spending):
        amort=sum(spending[max(0,year-life+1):year+1])/life
        asset+=current-amort
        if abs(asset)<1e-12: asset=0
        dtl=asset*tax
        rows.append(dict(amort=amort,asset=asset,dtl=dtl,net_asset=asset-dtl,
                         profit_adjustment=(current-amort)*(1-tax)))
    return rows

def cash_accrual(ni,cfo,average_assets):
    if any(not isfinite(x) for x in (ni,cfo,average_assets)) or average_assets<=0:
        raise ValueError('同范围输入有限，平均资产为正；缺失不可填零')
    return (ni-cfo)/average_assets

def normalized_income(reported,removed_items):
    # 每项是待剔除的税前损益及其题设税率；负损益的剔除会增加利润。
    if not isfinite(reported) or any(not isfinite(v) or not isfinite(t) or not 0<=t<=1 for v,t in removed_items):
        raise ValueError('金额有限、税率0至1；税后项目不能重复乘税率')
    return reported-sum(v*(1-t) for v,t in removed_items)

def depreciation_after_loss(book,loss,remaining_years):
    if any(not isfinite(x) for x in (book,loss,remaining_years)) or not 0<=loss<=book or remaining_years<=0:
        raise ValueError('损失不超过账面，剩余寿命为正')
    return dict(before=book/remaining_years,after=(book-loss)/remaining_years)

# %% 研发按批次摊销，不只加回本年费用
rows=research_cohorts([12,15,18,0,0],3)
assert [r['amort'] for r in rows]==[4,9,15,11,6]
assert [r['asset'] for r in rows]==[8,14,17,6,0]
assert sum(r['amort'] for r in rows)==45
print({'无税分析研发滚动万元':rows})

# %% 税后收益与净资产同步，现金不变
tax_rows=research_cohorts([12,15,18,0,0],3,.25)
previous=0
for row in tax_rows:
    assert isclose(row['profit_adjustment'],row['net_asset']-previous)
    previous=row['net_asset']
print({'假设税制下研发调整':tax_rows})

# %% 分类、一次性项目与减值后利润
a=cash_accrual(20,8,100); b=cash_accrual(20,11,100)
core=normalized_income(24,[(8,.25),(-2,.25)])
dep=depreciation_after_loss(100,40,5)
assert isclose(a,.12) and isclose(b,.09) and core==19.5
assert dep==dict(before=20,after=12)
print({'同一现金分类的应计差别':(a,b),'分析预测NI':core,'减值后折旧':dep})
"""

EXERCISES[24]=[
('NI15、CFO9、平均资产120万元，现金流代理应计率？','先核范围，再做差。','5%；不是所有论文的同一定义，须保留利息、税和合并分类。'),
('研究与开发阶段支出能否因预计未来增长而全部资本化？','区分法定确认与分析重述。','不能。研究支出费用化，开发需同时满足适用确认条件；分析性研发资本也要单列假设，不修改原始披露。'),
('无税分析重述：期初已可用研发18万元，三年直线摊销，首年利润与资产相对费用化差额？','完整一年的摊销为6。','利润高12、期末资产12，现金都支出18；可供使用时点改变则不能机械计全年摊销。'),
('收入增10%、应收增80%，可以直接认定造假吗？','观察与解释分开。','不能。核交付时点、账期、客户、账龄、合同资产和后续回款，保留竞争解释；比率只是线索。'),
('相同NI20、平均资产100万元，CFO由8重分类至11，应计率怎样变？','不把分类当经营改善。','12%变9%，差−3个百分点；总现金和利润可能完全未变。'),
('报告NI24万元，含税前资产处置收益8和诉讼损失2，两项税25%，均判断不重复，分析基准NI？','剔收益、加回损失，用税后影响。','24−6+1.5=19.5万元；此为预测调整，不自动等于法定扣非。'),
('资产100减值40万元、剩余5年、零残值，后续折旧和利润机械变化？','经营现金不变。','年折旧20变12，无税利润每年高8；不代表经营效率提高。'),
('重述财报更准确，能否替换历史回测中原披露数据？','知识可得日期。','不能回填至重述公开之前；原版本用于当时策略，重述用于后验分析并保留版本。'),
('Y1—Y3期初可用研发12/15/18万元，各摊三年、无税无减值，求每年摊销与期末资产。','按各批次存续寿命相加。','摊销4/9/15，期末资产8/14/17；利润相对费用化增加8/6/3。后两年无投入则摊11/6，资产归零。'),
('上题Y1假设现金税当期全额扣支出、税25%，分析资产税基0。资本化增加的DTL、净经营资产和税后利润？','账面资产8与税基0。','DTL2，净经营资产6，税后分析利润增加6；FCF增量6−6=0。该税制为假设，不能套作真实研发税务结论。'),
('为何卖设备收益剔除后，不能仍按原产能预测下一年？','利润、资产与现金三端相连。','处置减少生产资产与未来折旧，可能改变产能、维护和替换投资；只剔一次性收益却保留全部收入能力会高估持续价值，需同步经营预测。'),
('为“关联销售上升且回款放缓”建立四列核查表，并给出两种模型处理。','事实、竞争解释、证据、结论强度。','事实只写已披露比例与回款；解释为业务协同/账期变化或商业实质不足；核合同、可比价格及期后收款；结论随证据分级。可设回款延迟和信用损失情景，均标假设，不把模型压力值当已发生事实。')]

BODY[25]=r"""

## 25.6 量价驱动和资本约束要一起进入模型

收入恒等式R=ΣQ_iP_i只解释已确认销售，不保证订单全能交付。先定义销售数量、可用产能、交付与确认时间；生产数量还可能不同于销售数量，库存和成本需另行滚动。独立例：销量100万件、售价2元、产能120万件，收入200万元；将销量直接设130万件而不加外包、库存来源或扩产条件，模型应拒绝输出，不能靠提高利润率掩盖物理约束。

本章Y2财务底稿以亿元计，仍采用收入165、EBIT33等已列假设。为构造成本冲击，将165拆成现金变动成本99、现金固定经营费用26、折旧7，恰得EBIT33。这是新增的情景结构，不声称所有费用永久固定。期末应收、存货和应付是题设预测余额；由历史周转得到目标余额时，须经过第20章平均与期末口径的转换。

## 25.7 明确融资时点后，可以解析消除循环

令C_bar为只计期初债务利息、尚未计新增借款及其利息时的期末现金，最低期末现金M。新增借款B在年内平均占用比例α，年利率r，新增利息rαB；假设税盾当期足额可用、税率T、无费用和利率档位变化，则：

$$C_1=C_{bar}+B-(1-T)r\alpha B.$$

若C_bar<M且1−(1−T)rα>0，所需借款为B=(M−C_bar)/[1−(1−T)rα]。若本来充足，本模型B=0，保留超额现金，不自动还债。α=.5只代表约定的半年度加权暴露，不是所有借款都应按期初期末平均计算。借款越早、利率越高或税盾越弱，需要的融资越多。

对应固定点迭代B_next=缺口+(1−T)rαB，在系数绝对值小于1时才按此线性模型收敛。本章限制非负r和α，若系数达到1且缺口为正，继续追加借款不能净填缺口。授信不足、税前亏损、手续费或阶梯利率出现时须改变模型或报告不可行，而不是输出不存在的融资。

## 25.8 需求、成本与回款压力的完整联立

沿用Y2期初余额，压力假设收入比165低10%为148.5亿元；现金变动成本比例由60%升至66%，现金固定费用26、折旧7、资本开支12和分红6不变。于是EBIT=148.5×.34−26−7=17.49。为隔离积压效应，期末存货仍35.2、应付25.3；应收目标在收入六分之一基础上另增加20天销售额，即AR=148.5×(1/6+20/365)=32.886986。

这里“20天”仅用来构造年末额外应收目标，不冒充以平均余额计算的已实现DSO。NWC从34到42.786986，增加8.786986。仅计期初债务利息2.1时，NI11.5425，期末现金C_bar=10.255514。即使利润为正，也低于最低现金15。

若新增借款利率5%、α=.5、税25%，所需借款4.835145亿元，利息变2.220879，NI11.451841，年末债务46.835145、现金15。FCFF=17.49×.75+7−12−8.786986=−.669486，融资没有把经营自由现金变正。授信上限若只有4，缺的是相对本模型必要借款的.835145，模型拒绝称已达到15现金；按实际仅借4重算，现金缺口为.819486，两个“缺口”单位虽相同、经济定义却不同。

## 25.9 概率平均与终态约束

独立量价情景，两个状态概率各一半：销量80万件、价1.2元；销量120万件、价.8元。两状态收入都96万元，期望收入96；用平均销量100乘平均价格1却得100。数量和价格共同变化时不能用“平均驱动”替代逐情景计算，融资选择和税损处理等非线性还会放大差异。

稳定期关系也须说明时点。假设期初投入资本100、下一年NOPAT12，新增投资4在年末投入且其下一年增量回报12%，则次年NOPAT增加.48，增长4%；再投资率4/12=1/3，FCFF8。一般在稳定增量回报和该时点约定下，g=增量ROIC×再投资率。增长高于回报时再投资率可能超过100%，数学上并非自动不可能，但需要外部资金，不能同时假设无融资且持续高额派息。

## 25.10 模型验收应看残差和可行性

本章实验每个情景检查三条独立关系：资产减负债权益为0；期末现金减期初现金等于CFO+CFI+CFF；FCFF同时等于NOPAT+折旧−资本开支−ΔNWC与OI−ΔNOA。不要用现金平衡项让第一条成立，再据此宣称其他两条必然成立。

年度最低现金满足不代表年中从未短缺；这里没有模拟月内借款、契约和付款日。实际应用须把第20章月度现金预算接入，并区分未承诺额度、可提款额度和真实到账。模型交付包括假设来源、基准与压力差异、不可行情景及监测信号。后续第26—30章估值直接读取一致预测，不另外编造一组高增长低再投资的现金流。见[本批核验](../../references/ALIGNMENT_V03_PART05.md)。
"""

LAB[25]=r"""
from math import isclose, isfinite

def revenue_driver(quantity,price,capacity):
    if any(not isfinite(x) or x<0 for x in (quantity,price,capacity)) or quantity>capacity:
        raise ValueError('本例无外包和期初成品，销量不能超过可用产能')
    return quantity*price

def required_borrowing(cash_before,minimum,rate,tax,exposure,capacity):
    vals=(cash_before,minimum,rate,tax,exposure,capacity)
    if any(not isfinite(x) for x in vals) or min(minimum,rate,capacity)<0 or not 0<=tax<=1 or not 0<=exposure<=1:
        raise ValueError('输入有限，税率和年度暴露比例0至1')
    factor=1-(1-tax)*rate*exposure
    if factor<=0: raise ValueError('融资反馈系数不满足本线性解条件')
    draw=max(0,minimum-cash_before)/factor
    if draw>capacity+1e-10: raise ValueError('可提款额度不足，不能虚构借款闭合现金')
    return draw

def forecast(revenue=165,variable_ratio=.6,ar=None,inventory=35.2,ap=25.3,
             minimum=15,capacity=10,exposure=.5):
    if ar is None: ar=revenue/6
    vals=(revenue,variable_ratio,ar,inventory,ap,minimum,capacity,exposure)
    if any(not isfinite(x) for x in vals) or min(revenue,variable_ratio,ar,inventory,ap)<0:
        raise ValueError('教学经营输入有限且非负')
    # 亿人民币，完整Y2；固定现金经营费用26、折旧7、资本开支12、分红6。
    ebit=revenue*(1-variable_ratio)-26-7
    tax=.25; rate=.05; old_interest=42*rate
    if ebit<old_interest: raise ValueError('本例要求利息税盾可当期利用，亏损另建模型')
    dnwc=ar+inventory-ap-34
    ni_without_new=(ebit-old_interest)*(1-tax)
    cash_before=18.5+ni_without_new+7-dnwc-12-6
    draw=required_borrowing(cash_before,minimum,rate,tax,exposure,capacity)
    interest=old_interest+rate*exposure*draw
    if ebit<interest: raise ValueError('新增利息导致亏损，税模型超域')
    ni=(ebit-interest)*(1-tax)
    cfo=ni+7+interest-dnwc  # 支付利息列筹资，现金税等于当期税费用。
    cfi=-12; cff=draw-interest-6
    cash=18.5+cfo+cfi+cff
    ppe=64+12-7; debt=42+draw; equity=74.5+ni-6
    noa=ar+inventory+ppe-ap
    fcff=ebit*(1-tax)+7-12-dnwc
    assets=cash+ar+inventory+ppe; claims=ap+debt+equity
    if not isclose(assets,claims,abs_tol=1e-9): raise AssertionError('三表不平')
    if not isclose(fcff,ebit*(1-tax)-(noa-98),abs_tol=1e-9): raise AssertionError('NOA桥不平')
    if not isclose(fcff,cfo-interest*tax-12,abs_tol=1e-9): raise AssertionError('CFO桥不平')
    return dict(revenue=revenue,ebit=ebit,ni=ni,interest=interest,ar=ar,
                delta_nwc=dnwc,cfo=cfo,cfi=cfi,cff=cff,cash=cash,cash_before=cash_before,
                draw=draw,debt=debt,equity=equity,noa=noa,fcff=fcff,assets=assets,claims=claims)

# %% 基准Y2：经营、财报现金与NOA三条路径
base=forecast()
assert isclose(base['cfo'],28.875) and isclose(base['cash'],27.275)
assert isclose(base['assets'],158.975) and isclose(base['fcff'],16.35)
print({'Y2基准亿元':base})

# %% 联合压力：资金约束与利息反馈
stress_ar=148.5*(1/6+20/365)
stress=forecast(148.5,.66,stress_ar)
assert isclose(stress['cash'],15) and isclose(stress['draw'],4.835145275281394)
assert stress['ni']>0 and stress['fcff']<0
print({'Y2压力亿元':stress})
try:
    forecast(148.5,.66,stress_ar,capacity=4)
except ValueError as exc:
    print({'额度4不可行':str(exc)})
else:
    raise AssertionError('不能用不存在的授信填现金')

# %% 业务上限、情景平均与稳态再投资
assert revenue_driver(100,2,120)==200
expected=.5*revenue_driver(80,1.2,120)+.5*revenue_driver(120,.8,120)
assert expected==96 and expected!=100*1
print({'期望收入万元':expected,'稳态NOPAT':12,'再投资':4,'FCFF':8,'次年增长':.04})
"""

EXERCISES[25]=[
('销量增10%、价格降5%，收入增速？','增长因子相乘。','4.5%，不是精确5%；还需能交付并满足收入确认条件。'),
('无外包、无期初成品，销量目标130万件、可用产能120万件，能直接预测收入吗？','约束先于利润表。','不能，应调整销量或补扩产/外包/库存来源和时点；模型应拒绝不可能的数量。'),
('Y2收入165亿元、现金变动成本60%、现金固定费用26、折旧7、期初债务42利率5%、税25%，NI？','先EBIT，再利息和税。','EBIT33、利息2.1、NI23.175亿元，假设税盾可用，无新增借款利息。'),
('Y2应收27.5、存货35.2、应付25.3亿元，Y1经营NWC34，增量多少？','目标期末余额减同口径期初。','3.4亿元；不能拿平均周转余额不经转换就替代期末。'),
('上题NI23.175、折旧7、利息2.1亿元，利息列筹资，CFO？','先把筹资利息从NI中调出。','23.175+7+2.1−3.4=28.875亿元；税费用与经营税现金相同是题设。'),
('由Y2 CFO28.875、利息2.1、税25%、资本开支12亿元求FCFF。','CFO含融资利息税盾。','28.875−.525−12=16.35亿元，亦等于24.75−(106.4−98)。'),
('C_bar10、最低现金15亿元，新增年率8%、平均暴露半年度、税25%，需借多少？','新增利息也占用融资。','5/(1−.75×.08×.5)=5.154639亿元；年末现金15，需额度可用和税盾假设成立。'),
('为什么年度现金满足最低值，不代表全年没有短缺？','报告期内时点。','客户可能年末才付款，工资和到期债先支付；必须接入月度或每日预算、额度和契约，年度解不保证路径可行。'),
('推导新增借款利息反馈的闭式解及迭代收敛条件。','C1=C_bar+B−税后新增利息。','B=(M−C_bar)/(1−(1−T)rα)，适用于正缺口与正分母；固定点系数(1−T)rα绝对值小于1才按该线性迭代收敛。无缺口时本模型B0，另行定义偿债政策。'),
('正文压力情景C_bar10.255514、M15亿元、r5%、T25%、α.5。额度4是否足够？两种缺口如何区分？','必要借款与只借4后的现金差不同。','全精度必要借款4.835145，额度少.835145；仅借4的现金短缺为4.744486−4×.98125=.819486亿元。模型不能假称已满足15。'),
('两个等概率情景：80万件×1.2元和120万件×.8元。期望收入等于均量乘均价吗？','先逐状态算再加权。','期望96万元，均量100×均价1=100万元，两者不同；量价协变，不能把平均输入当平均结果。'),
('期初资本100、NOPAT12万元，年末投资4，增量回报12%从次年体现。求次年NOPAT增长及当年FCFF，并列估值检查。','增长由新资本回报支持。','次年增.48即4%，再投资率1/3，FCFF8。核对投入时点、资本滚动、增量回报、维持投资和融资能力；不能同时任意指定高增长、低再投资与高派息。')]

READING={
21:'D英文5版第2章财报导论、第8章通过财报理解业务，第9章权益表选读；C英文完整版2025 Release第2章财报与现金流。重点：业务、现金分类、权益范围及内部交易。R1/R3核对中国准则，见[第五批核验](../../references/ALIGNMENT_V03_PART05.md)。',
22:'D英文5版第9—11章：权益、资产负债表和利润表、现金流量表分析。重点：NOA/NFO、税分配、综合收益及现金桥；R5仅选读经营/融资分解部分。见[第五批核验](../../references/ALIGNMENT_V03_PART05.md)。',
23:'D英文5版第12章盈利能力、第13章增长与可持续盈利；C第3章财务分析与模型。重点：经营和融资杠杆、资本分母与增长质量；R5核对杠杆关系，原创计算见[核验](../../references/ALIGNMENT_V03_PART05.md)。',
24:'D英文5版第17章会计价值与经济价值、第18章财报质量，第13章持续盈利选读。R2核研发确认与摊销时点，R4核非经常性损益披露边界；分析重述与法定报表分开。见[核验](../../references/ALIGNMENT_V03_PART05.md)。',
25:'D英文5版第16章完整信息预测、估值与商业战略，第15章简单预测选读；C第3章财务模型、第26章短期财务规划。重点：经营驱动、融资联立与期末约束；原创压力模型见[核验](../../references/ALIGNMENT_V03_PART05.md)。'
}
EXIT={
21:'提交Y1直接收付、间接调节与权益滚动，E03、E09、E10需解释分类和合并范围。',
22:'提交科目映射、两种现金分类桥与非现金调整表；E04、E09、E11不得重复计算税盾或减值。',
23:'提交经营/融资回报、时间加权资本和描述性归因；E05、E10、E12需说明分母与收费时点。',
24:'提交研发批次、分析税与资产桥、四列表核查；E09、E10、E12需区分会计重述、现金和证据。',
25:'提交基准和压力三表、所需借款、不可行情景及监测变量；E06、E09、E10需通过一致性与授信检查。'
}

def deepen(chapters):
    for chapter in chapters:
        n=chapter.number
        chapter.body+=BODY[n]
        chapter.lab=LAB[n]
        chapter.exercises=EXERCISES[n]
        chapter.reading=READING[n]
        chapter.edition='v0.3第五批深化稿（第21—25章）'
        chapter.study_note='建议3次、每次60—90分钟：先画交易与三表桥，再推导和手算，最后运行实验并改变边界。明确报告期、支付分类、税、合并范围与资本分母；报表平衡不替代经济证据。'
        chapter.exit_task=EXIT[n]+' 核心题建议至少48/64分，修正关键口径后进入估值篇。'
