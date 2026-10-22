# v0.1验证记录

本文件记录首批样章的实际检查；检查通过不等于整套教材完成，也不等于真实市场研究有效。

## 已执行，2026-10-22

环境：Linux，Python 3.12.14。核心路径只用标准库。

| 检查 | 命令或方法 | 结果 |
| --- | --- | --- |
| 三情景及敏感性 | `python -m labs.ch01_scenarios` | 通过，结果与正文及答案核对 |
| 财务模型检查 | `python -m unittest discover -s tests -v` | 11项通过：手算基准、营运资本释放、回收时点、贴现输入、税模型边界、顺序、价值桥接等 |
| Notebook代码 | `python scripts/run_notebook.py notebooks/ch01_scenarios.ipynb` | 5个代码单元在新Python进程按序执行，全部断言通过 |
| 内容结构 | `python scripts/check_content.py` | 本地链接、40章规划、12对题答及Notebook代码语法通过 |
| Notebook文件格式 | `nbformat.validate`，nbformat 5.11.1 | 通过v4格式校验 |

关键基准：经营价值50.636739亿元，需求改善54.285586亿元，需求疲弱46.328237亿元；营运资本比例25%的修改实验价值48.469407亿元。计算保留全精度，显示时舍入。

## 交互内核验证未完成

曾使用隔离环境的nbclient 0.11.0、ipykernel 7.4.0启动独立Jupyter内核；运行环境拒绝内核通信所需的套接字操作，TCP和本地IPC均未成功。因此本版本只声称Notebook格式校验和代码顺序执行成功，不声称完整Jupyter内核或前端交互已验证。独立标准库运行器可用于本章全部计算。

## 验证边界

本版没有下载真实行情或财报，没有执行真实策略回测，没有构建PDF或网页版。Python普通代码执行不自动代表在所有操作系统及Jupyter前端完成验证。
