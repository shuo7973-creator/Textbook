# 宏观、企业价值与量化研究

**一套面向有金融基础读者的中文系列教材、练习册与计算实验。**

从经济机制出发，经由企业经营、财报与估值，形成可以用数据检验的投资假设。

## 当前版本：v0.3第五批深化稿（已深化第1—25章）

- 8篇40章均有正文、推导与算例、练习、独立提示、参考答案和计算实验。
- 第1—25章已分五批深化推导、反例、12题分层练习与分步实验；第26—40章保留v0.2初稿，等待后续批次深化。
- 全书420道习题：第1—25章每章12题，第26—40章每章8题；40份Notebook与对应Python实验。
- 新增基础附录和跨章财务案例核对表，保留6个阶段项目与毕业项目任务书。
- 本批完成已列范围的概念、条件和计算校核，四本主教材的全文逐页对照及出版审校仍未完成。全部计算案例为假设数据；PDF/网页构建和真实市场项目待后续交付。

## 开始阅读

| 入口 | 用途 |
| --- | --- |
| [全书40章导航](textbook/README.md) | 逐章进入正文、练习、答案与实验 |
| [课程总纲](curriculum/SYLLABUS.md) | 40章的知识范围、学习结果、练习与阅读主题 |
| [学习路线与先修关系](curriculum/ROADMAP.md) | 系统路线、专题路线、30天复习映射 |
| [第1章：统一研究框架](textbook/part01/ch01.md) | 从降息问题建立宏观—经营—价值—检验框架 |
| [第1章练习册](workbook/ch01.md) | 12题；核心题与进阶题分层 |
| [第1章提示](solutions/ch01-hints.md) | 卡住时先看提示 |
| [第1章答案](solutions/ch01.md) | 推导、完整计算、开放题评分标准 |
| [第1章Notebook](notebooks/ch01_scenarios.ipynb) | 修改假设并复核结果 |
| [项目任务书](projects/README.md) | 6个阶段项目和毕业项目 |
| [参考书与来源](references/READING_MAP.md) | 四本主教材的版本、章节及阅读映射 |
| [第1—5章参考一致性核验](references/ALIGNMENT_V03_PART01.md) | 版本差异、概念条件、独立算例及未核查范围 |
| [第6—10章参考一致性核验](references/ALIGNMENT_V03_PART02.md) | 核算、增长、IS—LM、消费投资与开放经济；修正项和原始来源 |
| [第11—15章参考一致性核验](references/ALIGNMENT_V03_PART03.md) | 货币记账、资本与流动性、债券曲线、政策时点和可执行外汇路径 |
| [第16—20章参考一致性核验](references/ALIGNMENT_V03_PART04.md) | 现金流与资本预算、风险及融资估值、营运资本和增长口径 |
| [第21—25章参考一致性核验](references/ALIGNMENT_V03_PART05.md) | 三表现金分类、报表重构、盈利与会计质量、融资反馈预测 |
| [v0.3深化进度](docs/ITERATION_V03.md) | 八个批次的交付和验收状态 |
| [原始资料索引](references/SOURCES_V02.md) | 官方统计、货币口径、交易制度与方法来源 |
| [基础附录](appendices/FOUNDATIONS.md) | 微积分、概率、矩阵、Python、会计和连续案例 |

## 如何使用

建议先读正文，再独立完成核心题，最后用实验核对。每章按“理解—推导—手算—编码—解释—反例”推进。完整路线按掌握程度学习；30天路线是选读复习，不代表完成全书。

正文面向本科高年级至金融硕士复习。必要数学在正文与基础附录解释；完整参考教材用于扩展证明和专题深读。第1章仅需要代数、百分比和折现的初步知识。章末原书阅读按主题指定，未核实的章号或页码不作精确引用。

## 运行第一个实验

核心实验使用 Python 标准库，无第三方包或网络依赖。建议 Python 3.11及以上；实际验证环境见[验证记录](docs/VALIDATION.md)。从仓库根目录执行：

```bash
python -m labs.ch01_scenarios
python -m unittest discover -s tests -v
python scripts/check_content.py
python scripts/run_notebook.py notebooks/ch01_scenarios.ipynb
python -m labs.ch26
python scripts/validate_book.py
```

最后一条命令在一个新Python进程中按顺序执行本仓库Notebook的代码单元，不等同于启动Jupyter内核。Notebook也可直接在Jupyter或支持Notebook的编辑器中打开；可选环境安装见[实验说明](notebooks/README.md)。

## 项目约定

- 每章区分事实、假设、模型推论和实证结论；计算注明单位、期间和现金流时点。
- 真实数据须记录来源、发布日期、当时可用版本与获取方式；示例数据见[数据字典](data/README.md)。
- 教材制作进度与学习者掌握进度分开。发布章节不会自动标记任何人的学习完成状态。
- 每篇完成后再整体验收。PDF和网页版为后续交付；当前以可直接阅读的Markdown与Notebook为主。
- 第2—40章的可维护源稿位于`authoring/`；修改源稿后运行`python scripts/build_book.py`生成正文、题答和Notebook，再用`--check`检查一致性。
- [编写规范与验收标准](docs/EDITORIAL_GUIDE.md)、[版本路线](docs/RELEASE_PLAN.md)、[来源与权利说明](NOTICE.md)。

## 设计参考

本项目参考 [QuantWeft · 量化经纬](https://github.com/YuxiaoMa66/quantweft) 的正文、练习、Notebook与项目配套思路；本批次教材文字、题目、模拟数据和代码独立编写，没有复制其教材或代码。经典教材作为延伸阅读，不随仓库分发。
