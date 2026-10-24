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
    for n in range(1, 41):
        expected = [f"CH{n:02d}-E{x:02d}" for x in range(1, 13 if n <= 30 else 9)]
        for relative in [f"workbook/ch{n:02d}.md", f"solutions/ch{n:02d}.md", f"solutions/ch{n:02d}-hints.md"]:
            path = ROOT / relative
            ids = re.findall(r"^## (CH\d{2}-E\d{2})\b", path.read_text(encoding="utf-8"), re.M)
            if n == 1 and relative.endswith("-hints.md"):
                ids = re.findall(r"^\| (CH01-E\d{2}) \|", path.read_text(encoding="utf-8"), re.M)
            if ids != expected:
                errors.append(f"Exercise IDs differ: {relative}")
        path = ROOT / f"textbook/part{(n-1)//5+1:02d}/ch{n:02d}.md"
        if not path.exists(): errors.append(f"Missing chapter {n}")
    syllabus = (ROOT / "curriculum/SYLLABUS.md").read_text(encoding="utf-8")
    numbers = [int(x) for x in re.findall(r"^### 第(\d+)章", syllabus, re.M)]
    if numbers != list(range(1, 41)):
        errors.append("Syllabus must contain each chapter 1 through 40 once, in order")
    notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if len(notebooks) != 40: errors.append("Expected 40 notebooks")
    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if notebook.get("nbformat") != 4: errors.append(f"Expected notebook v4: {path.name}")
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = cell["source"]
                compile("".join(source) if isinstance(source, list) else source, str(path), "exec")
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("PASS: local links, 40 chapter sets, 440 exercise/hint/solution triples, 40 notebook code syntax")


if __name__ == "__main__":
    main()
