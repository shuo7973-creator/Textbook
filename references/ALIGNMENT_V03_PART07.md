# v0.3第七批：第31—35章参考一致性核验

核查日期：2026-10-24（北京时间）。范围：五章基础正文和深化段落、60组题答、5份Python实验及Notebook。所有数值为原创假设样本，不代表A股实际因子收益、现行交易规则或投资建议。

## 核查层级

四本主教材全文仍未取得。本批完成出版方目录定位、公开一手方法资料的已列部分核对、独立推导和计算验证；没有把目录确认冒称逐页逐式对照。C采用英文完整版2025 Release，D采用英文第5版。量化实现超出主教材目录主题的部分另列技术来源，不虚构主教材章号或页码。

| 本书章 | 主教材主题定位 | 已核方法与独立工作 | 保留边界 |
| --- | --- | --- | --- |
| 31 研究协议 | D7主动投资、D18财报质量；C14市场效率与行为金融 | R1版本区间；双时钟、标签成熟、证券事件与执行时隙原创 | 未取得A股全历史公告、退市及交易资格库，未实现撮合引擎 |
| 32 基本面信号 | D12盈利、D13增长、D18质量；C12风险收益其他视角 | R2/R3的OP、INV和六组合定义；融资ROE、合成与覆盖独立构造 | 自定义六格表不是五因子完整复制，未复现真实收益 |
| 33 动量与状态 | C11—12、14；D19权益风险 | R4持有月与prior(2–12)窗口；R1版本；协方差聚合与状态缓冲独立推导 | 不复制CRSP缺失码处理，不将最终宏观数据当实时值 |
| 34 诊断 | C11—12及D7作经济背景 | R5平均秩与常数列、R6预处理泄漏、R7 Bartlett HAC；行业内对比原创 | 截距均值HAC非一般面板聚类；未进行多重检验校正或真实有效性检验 |
| 35 组合 | C11风险与组合；D19风险联系 | R8收缩形式；区间投影、两资产ERC、三资产反例和自融资费用独立推导 | 固定对角收缩非完整Ledoit–Wolf；未实现多资产约束求解及实际市场费用 |

## 实际读取来源及范围

- **D目录**：[McGraw Hill，第5版目录](https://glencoe.mheducation.com/sites/0078025311/information_center_view0/table_of_contents.html)，©2013，ISBN0078025311。本次核对第7、12、13、18、19章及上下文顺序，只用于主题位置。
- **C目录**：[McGraw Hill，Corporate Finance](https://www.mheducation.com/highered/product/Corporate-Finance-Ross.html)。核对英文完整版第11章Return and Risk: The Capital Asset Pricing Model、第12章An Alternative View of Risk and Return、第14章Efficient Capital Markets and Behavioral Challenges。没有将精要版或译本章号直接代入。
- **R1**：[FRED API：Real-Time Periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html)。实际读取实时区间含义、默认当日信息、ALFRED历史版本及日期端点说明。网页未明确发布日期，访问日期如上；接口日期为日粒度，不据此声称具有分钟级中国宏观发布时间。本章公开/生产双时钟是原创数据库协议。
- **R2**：[Kenneth French：Five Factors (2×3)](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html)。读取样本范围、规模交叉排序、HML/RMW/CMA和SMB构造说明；仅核方法，没有下载或分析当期收益。美股NYSE/AMEX/NASDAQ定义不自动适配A股。
- **R3**：[Kenneth French：Variable Definitions](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html)。核对B/M对应财年及市值月份，OP的收入减成本、利息和SG&A及账面权益加少数权益分母，INV相邻财年总资产增长。网页未明示统一发布日期；按本次读取版本，不猜测历史定义变更日。
- **R4**：[Kenneth French：Momentum Factor (Mom)](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor.html)。读取持有月m的prior(2–12)、规模交叉和NYSE断点、价值加权及缺失约定。书中令m=t+1完成索引映射；代码严格拒绝窗口缺月，故不能称完整复制原方法。
- **R5**：[SciPy 1.14.0 rankdata](https://docs.scipy.org/doc/scipy-1.14.0/reference/generated/scipy.stats.rankdata.html)及[同版spearmanr](https://docs.scipy.org/doc/scipy-1.14.0/reference/generated/scipy.stats.spearmanr.html)。核对平均并列秩、常数输入相关未定义及小样本推断提醒。教学代码用标准库原创，未依赖SciPy运行，不把所引固定版称为当前最新版。
- **R6**：[scikit-learn：Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html)。实际读取数据泄漏、训练集拟合预处理、测试集仅变换和管道相关说明；本章另区分当期可知截面变换与跨期模型训练。未部署机器学习模型。
- **R7**：[statsmodels：sandwich_covariance源码文档](https://www.statsmodels.org/stable/_modules/statsmodels/stats/sandwich_covariance.html)。实际读取`weights_bartlett`及`S_hac_simple`，核对权重、等间隔序列及正负滞后交叉项。页面显示0.15.0；本书另从截距模型推导均值方差，带宽人工指定且不作小样本修正，不复制软件全部默认行为或代码。NBER Newey–West工作论文PDF访问返回403，未将其全文列为已读。
- **R8**：[scikit-learn：Covariance estimation](https://scikit-learn.org/stable/modules/covariance.html)。实际读取经验协方差与收缩部分，核对样本矩阵向结构目标混合的公式。其常用等方差单位阵目标与本书对角目标不同；Ledoit–Wolf需估计强度，本书固定λ没有冒称实现。正定性结论独立用二次型证明；不依赖网页非公式措辞代替数学检查。Ledoit作者`honey.pdf`与摘要页读取超时，未声称已读原论文。
- **R9**：[Boyd等：Multi-Period Trading via Convex Optimization，作者主页](https://web.stanford.edu/~boyd/papers/cvx_portfolio.html)，主页列2017年8月，Foundations and Trends in Optimization 3(1):1–76。本次只读取摘要及研究范围，确认风险、收益、交易与持有成本是联合问题；论文PDF未能取得。仅作为进阶阅读入口，不作为已完成其算法或全文审校的依据。

以上均不使用未核实的当前宏观数字、公司财务值或市场费率。未获取的全文、PDF失败和公开页面实际范围分别记录，不能以运行成功替代文献核验。

## 本批修订与计算核对

1. **公开与生产时钟分离**：历史公告可恢复当时公开信息，但不能证明特定系统当年已收到它。按公开版本筛选并保留系统延迟；测试等价时区、边界秒、未来修订不变性及不同证券隔离。
2. **OP、ROE、RNOA不混用**：同一假设样本分别16%、15%、20%；应计代理因现金分类变化可从12%到9%，并非质量自动改善。标准学术因子与教学自定义信号分开标识。
3. **动量时间索引和波动域**：t−11至t−1映射持有月m的m−12至m−2；11个月1%复利11.566835%。AR协方差累计针对对数收益和，σ为边际波动，12个月9.178502%与独立假设6.928203%不能混用。
4. **行业控制与相关分母**：四股样本整体交叉积.14、信号离差平方和110、收益离差平方和.0014，相关7/√385≈.356753；行业内相关−.6、斜率−.006。写作期曾把信号平方和手算成126，独立测试揭示后修正正文与断言，保留纠错记录。截尾残差可破坏行业内零和。
5. **HAC口径明确**：γj统一除T，四期L1标准误.0625；另以Bartlett核矩阵的双重求和独立验证L=0…3。四个观测只验算，不用于统计显著性结论；没有省略月份后假装等间隔。
6. **逆波动的条件细化**：修正基础正文概括。两风险资产、正权重及非零组合波动时，协方差项抵消，逆波动精确ERC；三资产反例贡献9/23、9/23、5/23。完全负相关零波动时贡献未定义；对冲资产可有负贡献。
7. **可行性与资金守恒**：无约束w39/53；加上限w.6；从漂移6/11出发限单边换手3%，w=.5754545。平坦目标不冒称唯一解，不可行约束直接拒绝。调仓前110万元、教学双侧.1%费率，扣费后109.99万元、卖5.005买4.995，差额.01支付费用。
8. **收缩对象可复现**：λ=.5、目标diag(S)，协方差.012变.006，最优w42/59；正定目标与正强度是正定性的充分条件，零方差目标仍可能奇异。没有把手选λ包装成最优强度估计。

新增28项独立基准和边界测试，含有理数证券事件账本、明确多空头寸、协方差全矩阵求和、组内双点差分、HAC核矩阵、网格风险比较及费用自融资解析解。所有题答和实验与正文同步生成。全书检查结果见[验证记录](../docs/VALIDATION.md)。

## 未完成与后续

四本主教材全文对照、独立学术审读和出版终审待补。第36—40章仍为待深化初稿，下一批处理成本、回测偏差、机器学习、研究工程与综合项目。没有取得真实A股完整PIT数据，没有实施可交易策略收益验证。Notebook普通Python执行与格式验证不等于Jupyter前端及内核验收。
