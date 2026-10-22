# Notebook运行说明

[第1章Notebook](ch01_scenarios.ipynb)包含数据说明、经营现金流计算、利率隔离、经营情景、敏感性以及读者修改任务。

第2—40章依次为`ch02.ipynb`至`ch40.ipynb`，从[全书导航](../textbook/README.md)进入。每章包含假设说明、独立计算和复述任务；代码与`labs/chNN.py`由同一源稿生成，避免公式漂移。数据在代码中显式给定；第1章另使用JSON输入。

## 无额外依赖

在仓库根目录运行：

```bash
python scripts/run_notebook.py notebooks/ch01_scenarios.ipynb
```

该运行器在新Python进程中顺序执行本仓库Notebook的普通Python代码，不使用保存输出。它不是完整Jupyter内核，不处理魔法命令、小部件、富文本渲染或沙箱隔离；只运行自己信任的Notebook。

## 可选交互环境

建议使用独立环境安装Jupyter。Windows激活命令为`.venv\Scripts\activate`，macOS/Linux为`source .venv/bin/activate`。

先执行`python -m venv .venv`，再按操作系统执行上述激活命令。激活后执行：

```bash
python -m pip install -r requirements-notebook.txt
python -m jupyterlab
```

打开本章Notebook，选择新环境内核，然后“Restart Kernel and Run All”。本章代码能从仓库根目录或notebooks目录定位数据。

依赖是可选便利环境，不是已验证的跨平台锁文件；实际运行证据见[验证记录](../docs/VALIDATION.md)。核心实验不需要安装这些包。
