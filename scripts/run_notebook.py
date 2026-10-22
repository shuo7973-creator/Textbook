"""执行本仓库可信Notebook的普通Python代码；不实现Jupyter魔法和显示协议。

每次命令在独立进程中顺序执行全部代码单元，不保存或信任已有输出。
"""

import json
from pathlib import Path
import subprocess
import sys


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/run_notebook.py NOTEBOOK.ipynb")
    root = Path(__file__).resolve().parents[1]
    notebook_path = Path(sys.argv[1]).resolve()
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4:
        raise ValueError("Only notebook format 4 is supported")
    program = []
    for index, cell in enumerate(notebook["cells"], 1):
        if cell["cell_type"] == "code":
            source = cell["source"]
            source = "".join(source) if isinstance(source, list) else source
            program.append(f"print('--- cell {index} ---')\n{source}")
    subprocess.run([sys.executable, "-c", "\n\n".join(program)], cwd=root, check=True,
                   timeout=60)
    print("All ordinary Python cells executed in a fresh Python process.")


if __name__ == "__main__":
    main()
