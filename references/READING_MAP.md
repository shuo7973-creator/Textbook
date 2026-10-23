# 主教材、版次与阅读映射

核查日期：2026-10-23。这里核对的是出版方书目与公开目录，不表示取得或逐页审读整本教材。中文译本按章名对应，不直接套用英文版章号；不编造页码。参考书不随仓库分发。第1—5章的具体版本标识、方法来源及核查边界见[一致性核验表](ALIGNMENT_V03_PART01.md)。

## 四本主教材

| 代号 | 参考版本 | 作用 | 官方入口 |
| --- | --- | --- | --- |
| A | N. Gregory Mankiw, *Macroeconomics*, 英文11版 | 宏观理论、增长、波动与开放经济 | [Macmillan目录](https://store.macmillanlearning.com/us/product/Macroeconomics/p/1319387993) |
| B | Frederic S. Mishkin, *The Economics of Money, Banking, and Financial Markets*, 英文13版美国版，电子书ISBN 9780136893929 | 利率、银行、货币与政策传导 | [Pearson目录](https://www.pearson.com/en-us/subject-catalog/p/economics-of-money-banking-and-financial-markets-the/P200000005989/9780136893929) |
| C | Ross等, *Corporate Finance*, 英文完整版2025 Release | 现金流、资本预算、风险、融资与分配 | [McGraw Hill目录](https://www.mheducation.com/highered/product/Corporate-Finance-Ross.html) |
| D | Stephen H. Penman, *Financial Statement Analysis and Security Valuation*, 英文5版 | 财报重构、盈利与增长、预测及价值锚定 | [出版方5版目录](https://glencoe.mheducation.com/sites/0078025311/information_center_view0/table_of_contents.html) |

这是学习用参考版，不声称为各书最新版。C使用出版方release标识，不与精要版或其他分册混同。

B的美国版第25章为货币政策传导机制；13版全球版该主题为第26章，见[官方全球版目录](https://www.pearson.com/en-au/media/fwvdzehg/9781292409481-toc.pdf)。本仓库B章号默认美国版；其他地区版按主题映射。

## 全书主题映射

| 本书篇章 | 主要阅读主题 |
| --- | --- |
| 第一篇 | A导论与数据；B金融市场导论；C现金流；统计与编程以官方文档、原始论文和独立讲义补充 |
| 第二篇 | A国民收入、增长、经济波动、消费投资与开放经济；中国统计口径补官方说明 |
| 第三篇 | B银行、利率、货币供给、政策与国际金融；A财政及政府债务 |
| 第四篇 | C现值、投资决策、风险与资本成本、资本结构、分配、营运资本 |
| 第五篇 | D商业活动、财报重构、盈利能力、增长、会计质量与完整预测 |
| 第六篇 | D账面价值与盈利估值、经营价值；C现金流估值；F/G为实务延伸 |
| 第七篇 | D盈利与估值口径；Q基本面因子、截面研究与组合构建 |
| 第八篇 | Q回测、验证、绩效、风险和研究工程；关键方法增补原始论文 |

第2—40章已在各章末给出主题阅读范围。只有实际核实的参考章号才列出；不同译本按章名映射，不把整本书列成单章必读。新增官方来源见[版本索引](SOURCES_V02.md)。

## 第1章已核对章号

| 阅读层次 | 参考章节 | 本章选读范围 |
| --- | --- | --- |
| 核心 | A第1章 | 研究问题、模型和经济学思考方式 |
| 核心 | C第1、2、4章 | 财务目标、利润与现金流、现值与折现 |
| 补充 | D第1章 | 投资、价值与价格的关系 |
| 补充 | B第1、4、25章 | 金融市场、利率含义与货币政策传导 |

只选与当前问题有关的小节；正文自含推导，没有教材也能完成本章模拟练习。

## 实务与量化延伸

第11—15章的逐章章号和选读见[第三批一致性核验表](ALIGNMENT_V03_PART03.md)：B3/14/19对应货币，B9/10/12对应银行，B4—6对应利率，B15—16/24—25对应政策，B17—18对应国际金融；A4/17/18、C8/25/31按相关主题补充。公开原始资料与原创扩展的范围在表中分别记录。

第16—20章见[第四批一致性核验表](ALIGNMENT_V03_PART04.md)：C1/2/4与D4对应现金流和时间价值，C5—7对应资本预算，C11/13对应风险与成本，C16—19对应融资和分配，C3/26—28对应财务规划及营运资本；C12/20/29/30选读。C仍采用英文完整版2025 Release，D为英文5版。IFRS概览、MIT讲义和作者公开资料仅用于表中已读范围，不能替代主教材全文对照。

第6—10章新增的逐章范围、官方方法资料与独立计算见[第二批一致性核验表](ALIGNMENT_V03_PART02.md)。本批A章号对应英文11版：第6章读A2—3，第7章读A8—10，第8章读A11—13及A15，第9章读A20，第10章读A6及A14；C的第4—6章补充现值与资本预算。不把公开目录定位写成已取得教材正文。

- F：Koller、Goedhart、Wessels等，*Valuation: Measuring and Managing the Value of Companies*，作为价值创造、预测与估值的按主题延伸；具体版次待相应章编写时核查。
- G：Aswath Damodaran，*Investment Valuation*，作为估值方法与行业边界的延伸；免费资源可从[作者教学入口](https://pages.stern.nyu.edu/~adamodar/)查找，后续按实际使用材料逐项核查。
- Q：[QuantWeft课程大纲](https://github.com/YuxiaoMa66/quantweft/blob/main/editions/zh/resources/syllabus.md)及[多因子项目说明](https://github.com/YuxiaoMa66/quantweft/blob/main/projects/project04/README.md)。参考其教学组织、时点口径与验证意识。项目自身区分构造实验与真实市场研究，本书也保持这种区别。

## 原始资料策略

中国宏观优先国家统计局、央行、财政部、海关等正式发布；公司分析优先交易所、巨潮和公司投资者关系披露。后续真实案例逐项记录文档标题、报告期、发布日期、版本与链接。实时数据获取途径不等于已取得历史PIT数据；未知项保留未知。
