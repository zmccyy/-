"""One-off: lay the homework folder out so each assignment is self-contained.

Run from the homework root:  python tools/reorganize.py
"""
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

MOVES = [
    ("extract_fft", "快速傅里叶变换与多项式乘法"),
    ("extract_closest", "最近点对"),
]

for src, dst in MOVES:
    if os.path.isdir(src):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.move(src, dst)
        print(f"moved {src}/ -> {dst}/")
    else:
        print(f"{src}/ already gone")

if os.path.isfile("_build_solutions.py"):
    shutil.move("_build_solutions.py", os.path.join("tools", "fill_solutions.py"))
    print("moved _build_solutions.py -> tools/fill_solutions.py")
if os.path.isfile("_run_tests.py"):
    os.remove("_run_tests.py")
    print("removed _run_tests.py (superseded by tools/run_otter_tests.py)")
if os.path.isdir("__pycache__"):
    shutil.rmtree("__pycache__")
    print("removed __pycache__/")

# Keep only the intended files in the assignment folders.
for folder, keep in [
    ("快速傅里叶变换与多项式乘法", {"fft.ipynb", "requirements.txt"}),
    ("最近点对", {"closest-pair.ipynb", "requirements.txt"}),
]:
    for entry in os.listdir(folder):
        if entry not in keep:
            path = os.path.join(folder, entry)
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            print(f"removed stray {path}")

print("\nfinal layout:")
for dirpath, dirnames, filenames in os.walk("."):
    dirnames[:] = sorted(d for d in dirnames if d not in {"submission"})
    depth = dirpath.count(os.sep)
    print("  " * depth + os.path.basename(dirpath) + "/")
    if "submission" in dirnames:
        dirnames.remove("submission")
        for f in sorted(os.listdir("submission")):
            print("  " * (depth + 1) + "submission/" + f)
    for f in sorted(filenames):
        print("  " * (depth + 1) + f)
