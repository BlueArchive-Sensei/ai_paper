#!/home/utils/Python-3.12.11/bin/python3.12
"""Per-paper statistics for the audit report: python tools/audit.py > table.md

For each paper directory prints characters, H2 count, images referenced, Markdown tables, display math
blocks, lint errors (tools/mdlint.py rules) and whether every file in rendered_figures/ is referenced.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdlint

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows, tot = [], dict(chars=0, h2=0, imgs=0, tables=0, math=0, files=0, errs=0)
for d in sorted(os.listdir(root)):
    p = os.path.join(root, d, "论文中文解读.md")
    if not os.path.isfile(p):
        continue
    text = open(p, encoding="utf-8").read()
    toks = mdlint.md.parse(text)
    h2 = sum(1 for t in toks if t.type == "heading_open" and t.tag == "h2")
    tables = sum(1 for t in toks if t.type == "table_open")
    maths = sum(1 for t in toks if t.type == "math_block")
    refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    figdir = os.path.join(root, d, "rendered_figures")
    files = sorted(os.listdir(figdir)) if os.path.isdir(figdir) else []
    used = {os.path.basename(r) for r in refs}
    unused = [f for f in files if f not in used]
    errs = sum(1 for c, _, _ in mdlint.lint(p) if c.startswith("E-"))
    errs += sum(1 for c, _, _ in mdlint.lint(os.path.join(root, d, "论文概要.md")) if c.startswith("E-"))
    rows.append((d, len(text), h2, len(refs), tables, maths, errs, len(unused)))
    for k, v in zip(("chars", "h2", "imgs", "tables", "math", "errs"), (len(text), h2, len(refs), tables, maths, errs)):
        tot[k] += v
    tot["files"] += len(files)

print("| 目录 | 字符数 | H2 | 图片引用 | 表格 | 公式块 | 格式错误 | 未引用的图片文件 |")
print("|---|---:|---:|---:|---:|---:|---:|---:|")
for d, c, h, i, t, m, e, u in rows:
    print(f"| `{d}` | {c} | {h} | {i} | {t} | {m} | {e} | {u} |")
print()
print(f"合计：{len(rows)} 篇，字符 {tot['chars']}，H2 {tot['h2']}，图片引用 {tot['imgs']}，图片文件 {tot['files']}，"
      f"表格 {tot['tables']}，公式块 {tot['math']}，格式错误 {tot['errs']}", file=sys.stderr)
