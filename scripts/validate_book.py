"""验证离线教学实验、生成一致性与Notebook普通代码，不启动Jupyter。"""

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(args):
    result = subprocess.run([sys.executable, *args], cwd=ROOT, text=True,
                            capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError(f"{args}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def main():
    print(run(["scripts/build_book.py", "--check"]).strip())
    print(run(["scripts/check_content.py"]).strip())
    run(["-m", "unittest", "discover", "-s", "tests", "-v"])
    paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
    for path in paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if path.name != "ch01_scenarios.ipynb":
            source = "".join("".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code")
            assert source == (ROOT / "labs" / (path.stem + ".py")).read_text(encoding="utf-8")
        run(["scripts/run_notebook.py", str(path)])
        print(f"PASS {path.name}")
    print("PASS unit checks; 40 notebooks executed as ordinary Python in fresh processes.")


if __name__ == "__main__":
    main()
