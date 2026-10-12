# 作业目录说明

## 目录结构

```
homework/
├── 快速傅里叶变换与多项式乘法/
│   ├── fft.ipynb          ← 答题文件（代码已填好）
│   └── requirements.txt
├── 最近点对/
│   ├── closest-pair.ipynb ← 答题文件（代码已填好）
│   └── requirements.txt
├── submission/            ← 交这里的压缩包
│   ├── 快速傅里叶变换与多项式乘法.zip
│   └── 最近点对.zip
├── 快速傅里叶变换与多项式乘法.zip   ← 老师发的原始包，未改动
├── 最近点对.zip                     ← 老师发的原始包，未改动
└── tools/                 ← 辅助脚本，不属于作业内容，不用提交
    ├── run_otter_tests.py   本地复现 notebook 里嵌的评分测试（通用）
    ├── fill_solutions.py    本次填代码的记录（可重复运行，幂等）
    └── reorganize.py        本次整理目录用的一次性脚本
```

上面的作业文件夹名对应的就是老师给的压缩包名——`快速傅里叶变换与多项式乘法/` 来自
`快速傅里叶变换与多项式乘法.zip`，`最近点对/` 来自 `最近点对.zip`。每个作业一个文件夹，
**答题文件就是该文件夹里的 `.ipynb`**。

## 用 VS Code 生成官方提交包

1. 用 VS Code **打开某个作业文件夹**（例如 `快速傅里叶变换与多项式乘法`），不要打开整个
   `homework`——内核的工作目录默认是「打开的文件夹」，`!pip install -r requirements.txt`
   是相对路径。
2. 选内核：`cs131232`（python 3.8，装了 `requirements.txt` 里的包，尤其 `otter-grader==4.4.1`）。
3. **不要改文件名**（notebook 里写死了 `otter.Notebook("fft.ipynb")`）。
4. Run All。最后一格 `grader.export(pdf=False, force_save=True, run_tests=True)` 会在同目录
   生成 otter 官方格式的提交包。
5. 注意：FFT 那本「运行时间比较」单元格会跑到 n=10⁴ 的朴素 O(n²) 多项式乘法，
   **要跑约 10 秒到几分钟**，属正常现象。

> 如果只是想交，`submission/` 里的两个 zip 可直接提交（已本地验证 7/7 通过）。

## 本地验证（不装 otter 也能跑）

这些 notebook 的评分测试是**明文嵌在 `metadata.otter.tests` 里的**，所以可以直接读出来、本地复现：

```bash
cd C:/Users/Shero_Wang/Desktop/homework

# 列出有哪些测试、各多少分
python tools/run_otter_tests.py --list "快速傅里叶变换与多项式乘法/fft.ipynb"

# 打印测试源码（看清评分标准：断言、返回顺序、时间限制）
python tools/run_otter_tests.py --dump "最近点对/closest-pair.ipynb"

# 跑测试：先按顺序执行 notebook 的代码单元格，再复现嵌入的测试
python tools/run_otter_tests.py "快速傅里叶变换与多项式乘法/fft.ipynb" "最近点对/closest-pair.ipynb"

# 只跑部分测试 / 跳过很慢的单元格
python tools/run_otter_tests.py --only q1,q2 "最近点对/closest-pair.ipynb"
python tools/run_otter_tests.py --skip-substr 'poly_multiply_naive(poly1' "快速傅里叶变换与多项式乘法/fft.ipynb"
```

全部通过时退出码为 0，否则为 1。

当前状态（2026-10-12）：

| 作业 | 测试 | 结果 |
|---|---|---|
| 快速傅里叶变换与多项式乘法 | q1.1 / q1.2 / q1.3 / q1.4 | 4/4 PASS |
| 最近点对 | q1 / q2 / q6 | 3/3 PASS |

## 以后加新作业

老师发的包按同样方式处理即可，保持这份目录约定：

1. 新压缩包放到 `homework/` 根目录（原包不删、不改）。
2. 解压到一个**与该压缩包同名的文件夹**，填好 `.ipynb` 里的代码。
3. 用 `python tools/run_otter_tests.py "新作业文件夹/xxx.ipynb"` 验证到全 PASS。
4. 把该作业的 `.ipynb` + `requirements.txt` 打成 zip 放进 `submission/`，文件名沿用老师给的包名。
