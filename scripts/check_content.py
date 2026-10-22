"""本版本内容完整性检查：链接、题答、章号及公开示例口径。

只检查本地路径链接，不声称验证外网链接或金融结论。
"""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    markdown_files = sorted(ROOT.rglob("*.md"))
    for path in markdown_files:
        if ".venv" in path.parts or ".git" in path.parts:
            continue
        body = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#") or target.startswith("mailto:"):
                continue
            destination = target.split("#", 1)[0]
            if destination and not (path.parent / destination).exists():
                errors.append(f"Broken local link: {path.relative_to(ROOT)} -> {target}")
    def ids(path):
        return re.findall(r"^## (CH01-E\d{2})\b", path.read_text(encoding="utf-8"), re.M)
    exercises = ids(ROOT / "workbook/ch01.md")
    answers = ids(ROOT / "solutions/ch01.md")
    expected = [f"CH01-E{x:02d}" for x in range(1, 13)]
    if exercises != expected or answers != expected:
        errors.append("Exercises and solutions must each contain E01 through E12 exactly once")
    syllabus = (ROOT / "curriculum/SYLLABUS.md").read_text(encoding="utf-8")
    numbers = [int(x) for x in re.findall(r"^### 第(\d+)章", syllabus, re.M)]
    if numbers != list(range(1, 41)):
        errors.append("Syllabus must contain each chapter 1 through 40 once, in order")
    notebook = json.loads((ROOT / "notebooks/ch01_scenarios.ipynb").read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4:
        errors.append("Expected notebook v4")
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            source = cell["source"]
            compile("".join(source) if isinstance(source, list) else source, "notebook", "exec")
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("PASS: local links, 40 planned chapters, 12 exercise/solution pairs, notebook code syntax")


if __name__ == "__main__":
    main()
