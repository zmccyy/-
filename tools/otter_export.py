"""Produce the official otter submission zip by running the notebook's own export cell.

Run it with the 3.8 venv that has otter-grader installed:

    .venv38/Scripts/python.exe tools/otter_export.py "快速傅里叶变换与多项式乘法/fft.ipynb"

It chdirs into the notebook's folder first, so that both
`grader = otter.Notebook("fft.ipynb")` and the cell's relative
`pip install -r requirements.txt` resolve, then calls

    grader.export(pdf=False, force_save=True, run_tests=True)

which is exactly what the notebook's last cell does: it runs every
`grader.check(...)` cell and writes the submission zip next to the notebook.

Note: this needs the notebook to be able to reach a package index, because its
first cells run `pip install -r requirements.txt`. Set PIP_INDEX_URL to a fast
mirror if pypi.org is slow on your network.
"""
import os
import sys

# The notebook's first cells run `pip install -r requirements.txt` inside the kernel, and
# pypi.org is throttled to a crawl on this network, so point pip at a fast mirror and make
# sure the kernel's `!pip` resolves to *this* venv's pip rather than a global one. Both are
# setdefaults, so anything you export beforehand still wins.
os.environ.setdefault("PIP_INDEX_URL", "https://mirrors.aliyun.com/pypi/simple/")
os.environ.setdefault("PIP_TRUSTED_HOST", "mirrors.aliyun.com")
os.environ["PATH"] = os.path.dirname(sys.executable) + os.pathsep + os.environ.get("PATH", "")

import otter


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2

    notebook = os.path.abspath(argv[1])
    if not os.path.isfile(notebook):
        print(f"no such notebook: {notebook}")
        return 2

    folder, name = os.path.dirname(notebook), os.path.basename(notebook)
    os.chdir(folder)
    print(f"otter {otter.__version__} | python {sys.version.split()[0]} | cwd={folder}")
    print(f"pip index: {os.environ['PIP_INDEX_URL']}")
    print(f"exporting {name} ...\n")

    before = set(os.listdir(folder))
    grader = otter.Notebook(name)
    grader.export(pdf=False, force_save=True, run_tests=True)
    after = set(os.listdir(folder))

    new = sorted(after - before)
    print(f"\nnew files next to the notebook: {new if new else '(none - check for an overwritten zip)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
