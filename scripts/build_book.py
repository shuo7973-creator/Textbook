"""将结构化源稿机械排版为正文、题答、Notebook与独立实验。"""

import importlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def chapters():
    result = []
    for part in range(1, 9):
        module = importlib.import_module(f"authoring.part{part:02d}")
        result.extend(module.CHAPTERS)
    assert [c.number for c in result] == list(range(2, 41))
    return result


def artifacts(chapter):
    chapter.validate()
    n = chapter.number
    ident = f"ch{n:02d}"
    part = (n - 1) // 5 + 1
    preface = (f"# 第{n}章 {chapter.title}\n\n"
               f"状态：全书初稿v0.2。先修：{chapter.prerequisites}。\n\n"
               f"[练习册](../../workbook/{ident}.md)｜[提示](../../solutions/{ident}-hints.md)｜"
               f"[答案](../../solutions/{ident}.md)｜[Notebook](../../notebooks/{ident}.ipynb)\n\n"
               "本章数值、企业和策略样本均为假设教学数据，真实制度另给原始来源。核心阅读与手算建议分2—3次完成，进阶题另计。\n\n"
               "## 学习目标\n\n" + "\n".join(f"- {g}" for g in chapter.goals) + "\n\n")
    ending = (f"\n\n## 计算实验与复述\n\n"
              f"从仓库根目录运行 `python -m labs.{ident}` 或打开本章Notebook。"
              "先手算正文基准，再运行代码，改变一个输入并解释方向与边界。"
              "实验中的断言检查教学计算，不构成真实市场证据。\n\n"
              "退出题：用自己的话复述本章核心机制，说明一个使其失效的条件，"
              "并指出应用于真实中国宏观或A股数据时需要核实的一个字段。\n\n"
              f"## 参考阅读\n\n{chapter.reading}\n\n"
              "版次、原始资料与版本核查见[来源索引](../../references/SOURCES_V02.md)。"
              "外文教材按主题选读，未核实的页码和章号不作指定。\n")
    workbook = f"# 第{n}章练习册：{chapter.title}\n\n[正文](../textbook/part{part:02d}/{ident}.md)｜[提示](../solutions/{ident}-hints.md)｜[答案](../solutions/{ident}.md)\n\n"
    workbook += "共8题、100分。E01—E06为核心题，每题建议10—15分钟；E07—E08为进阶题，每题20—30分钟。每题12.5分。所有数值为假设数据，除另注外金额为人民币亿元、期间为一年，支付在期末。完整说明计算过程与适用条件。\n\n"
    hints = f"# 第{n}章分层提示\n\n先独立完成[练习](../workbook/{ident}.md)。\n\n"
    answers = f"# 第{n}章参考答案\n\n对应[练习册](../workbook/{ident}.md)。每题12.5分：核心推理或计算5分，步骤与口径5分，解释或边界2.5分；纯概念题按答案中的关键点分配。开放题允许不同结论，须给出可核查论据。\n\n"
    for i, (question, hint, answer) in enumerate(chapter.exercises, 1):
        label = f"CH{n:02d}-E{i:02d}"
        workbook += f"## {label}\n\n{question}\n\n"
        hints += f"## {label}\n\n{hint}\n\n"
        answers += f"## {label}\n\n{answer}\n\n"
    code = '"""本章独立离线实验：全部输入为假设数据。"""\n\n' + chapter.lab.strip() + "\n"
    notebook = {
        "cells": [
            {"cell_type": "markdown", "id": "intro", "metadata": {}, "source": [f"# 第{n}章：{chapter.title}\n", "全部输入为假设教学数据。先手算正文例题，再运行；修改一个参数后重新运行并解释。\n", "本实验不需要联网或第三方库。"]},
            {"cell_type": "code", "id": "experiment", "metadata": {}, "execution_count": None, "outputs": [], "source": code.splitlines(keepends=True)},
            {"cell_type": "markdown", "id": "reflection", "metadata": {}, "source": ["## 复述与迁移\n", "记录修改前后输入和结果，区分数学关系与经验规律。指出一个现实数据缺口或识别限制。不要把模拟输出描述为真实回测或政策效果。"]}
        ],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 5
    }
    return {
        f"textbook/part{part:02d}/{ident}.md": preface + chapter.body.strip() + ending,
        f"workbook/{ident}.md": workbook,
        f"solutions/{ident}-hints.md": hints,
        f"solutions/{ident}.md": answers,
        f"labs/{ident}.py": code,
        f"notebooks/{ident}.ipynb": json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
    }


def main():
    items = chapters()
    outputs = {}
    for chapter in items:
        outputs.update(artifacts(chapter))
    navigation = "# 全书阅读导航\n\n第1—40章均已有正文、练习和答案。v0.2为完整初稿，教学实验使用假设数据，真实市场项目按各自状态说明。\n\n| 章 | 正文 | 练习 | 答案 | 实验 |\n| --- | --- | --- | --- | --- |\n"
    navigation += "| 1 | [统一研究框架](part01/ch01.md) | [练习](../workbook/ch01.md) | [答案](../solutions/ch01.md) | [Notebook](../notebooks/ch01_scenarios.ipynb) |\n"
    for c in items:
        n = c.number
        navigation += f"| {n} | [{c.title}](part{(n-1)//5+1:02d}/ch{n:02d}.md) | [练习](../workbook/ch{n:02d}.md) | [答案](../solutions/ch{n:02d}.md) | [Notebook](../notebooks/ch{n:02d}.ipynb) |\n"
    outputs["textbook/README.md"] = navigation
    check = "--check" in sys.argv
    drift = []
    for relative, content in outputs.items():
        path = ROOT / relative
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if drift:
        raise SystemExit("Generated content differs: " + ", ".join(drift))
    print(f"{'Checked' if check else 'Built'} {len(outputs)} files from {len(items)} authored chapters")


if __name__ == "__main__":
    main()
