#!/home/utils/Python-3.12.11/bin/python3.12
r"""Lint Markdown for things that render wrongly on GitHub (CommonMark + GFM tables + $math$).

Usage: mdlint.py FILE_OR_DIR [...]   (exit code 1 if any ERROR)

Needs markdown-it-py and mdit-py-plugins (pip3 install --user markdown-it-py mdit-py-plugins).

Codes
  E-EMPH   literal ** / __ / ~~ / *x* left in text: emphasis did not parse
           (typically `**注意：**文字` - closing ** after punctuation and before a CJK letter;
           fix by moving the punctuation outside the bold, or add a space, or drop the bold)
  E-MATH   stray `$` left in text: inline math did not parse (space after the opening $, digit right
           after the closing $, `$` inside a table cell with an unescaped `|`, ...)
  E-TABLE  table row has a different number of cells than the header (unescaped `|` in a cell)
  E-TABLEBR table starts directly under a paragraph line (needs a blank line before it)
  E-HTML   raw tag that GitHub strips (e.g. <think>, <answer>, <M>); wrap in backticks
  E-LINK   relative link / image target does not exist
  E-ANCHOR link to #fragment that matches no heading of the target file (GitHub slug rules)
  E-ALT    image with empty alt text
  E-H1     file does not have exactly one H1 / heading levels skip
  E-FENCE  unbalanced ``` fence
  E-MACRO  LaTeX macro / environment GitHub's MathJax does not define (\bm, \mathbbm, \argmax, \newcommand ...)
  E-MBRACE unbalanced { } or \left/\right or \begin/\end inside a math expression
  W-MATHLIST  `$$` block inside a list item (fragile on GitHub; prefer top level or inline $..$)
  W-SPACE  trailing spaces / tabs / CRLF / 2+ blank lines / no final newline
"""
import os, re, sys, urllib.parse
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

ALLOWED_TAGS = {"details", "summary", "br", "sub", "sup", "a", "img", "kbd", "b", "i", "em", "strong",
                "code", "pre", "p", "div", "span", "hr", "table", "thead", "tbody", "tr", "th", "td",
                "ul", "ol", "li", "blockquote", "del", "ins", "s", "strike", "picture", "source",
                "h1", "h2", "h3", "h4", "h5", "h6", "dl", "dt", "dd", "figure", "figcaption",
                "caption", "abbr", "small", "var", "samp", "tt", "q", "cite", "u", "center",
                "details", "rp", "rt", "ruby", "bdo", "wbr", "video"}

md = (MarkdownIt("commonmark", {"html": True}).enable("table").enable("strikethrough")
      .use(dollarmath_plugin, allow_space=False, allow_digits=False, double_inline=True))


def iter_md(paths):
    for p in paths:
        if os.path.isdir(p):
            for r, ds, fs in os.walk(p):
                ds[:] = [d for d in ds if d not in (".git", "source", "node_modules")]
                for f in sorted(fs):
                    if f.endswith(".md"):
                        yield os.path.join(r, f)
        else:
            yield p


BAD_MACROS = re.compile(r"\\(bm|mathbbm|mathds|argmax|argmin|textsc|newcommand|renewcommand|DeclareMathOperator|"
                        r"E|R|N|Z|P|KL|eqref|label|ref|cref|boldmath|"
                        r"qed|proof|intertext|nonumber|notag|hfill|vspace)(?![A-Za-z])")


def check_math(expr):
    errs = []
    m = BAD_MACROS.search(expr)
    if m: errs.append(f"unsupported macro \\{m.group(1)}")
    e = re.sub(r"\\[{}]", "", expr)
    if e.count("{") != e.count("}"): errs.append("unbalanced braces")
    if len(re.findall(r"\\left(?![A-Za-z])", expr)) != len(re.findall(r"\\right(?![A-Za-z])", expr)): errs.append("\\left/\\right mismatch")
    if sorted(re.findall(r"\\begin\{(\w+\*?)\}", expr)) != sorted(re.findall(r"\\end\{(\w+\*?)\}", expr)): errs.append("begin/end mismatch")
    return errs


_slug_cache = {}


def slugs_of(path):
    """GitHub heading anchors of a markdown file (lowercase, punctuation dropped, spaces -> '-', dup suffix)."""
    if path in _slug_cache: return _slug_cache[path]
    out, seen = set(), {}
    try:
        fence = False
        src = open(path, encoding="utf-8").read()
        out.update(re.findall(r'<a\s+(?:id|name)="([^"]+)"', src))
        for l in src.split("\n"):
            if re.match(r"^\s*(```|~~~)", l): fence = not fence
            m = None if fence else re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", l)
            if not m: continue
            t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", m.group(1))
            t = re.sub(r"[`*_~]|<[^>]+>", "", t) if False else re.sub(r"<[^>]+>", "", t).replace("`", "").replace("*", "")
            sl = re.sub(r"[^\w\- ]", "", t.lower(), flags=re.UNICODE).replace(" ", "-")
            n = seen.get(sl, 0)
            seen[sl] = n + 1
            out.add(sl if n == 0 else f"{sl}-{n}")
    except OSError:
        pass
    _slug_cache[path] = out
    return out


def count_cells(line):
    line = line.strip()
    # drop code spans, escaped pipes
    line = re.sub(r"`[^`]*`", "", line)
    line = line.replace("\\|", "")
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return line.count("|") + 1


def lint(path):
    out = []
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    lines = text.split("\n")

    def add(code, ln, msg):
        out.append((code, ln, msg))

    if b"\r" in raw: add("W-SPACE", 1, "CRLF line endings")
    if not text.endswith("\n") or text.endswith("\n\n"): add("W-SPACE", len(lines), "file must end with exactly one newline")
    infence = False
    nfence = 0
    for i, l in enumerate(lines, 1):
        if re.match(r"^\s*(```|~~~)", l):
            nfence += 1
            infence = not infence
        if not infence and (l != l.rstrip(" \t") and not l.endswith("  ") ):
            add("W-SPACE", i, "trailing whitespace")
        if "\t" in l and not infence: add("W-SPACE", i, "tab character")
        if not infence and i > 2 and l == "" and lines[i - 2] == "" and lines[i - 3] != "":
            add("W-SPACE", i, "consecutive blank lines")
    if nfence % 2: add("E-FENCE", len(lines), "odd number of code fences")

    # table directly under paragraph
    infence = False
    for i, l in enumerate(lines):
        if re.match(r"^\s*(```|~~~)", l): infence = not infence
        if infence: continue
        if re.match(r"^\s*\|.*\|\s*$", l) and i > 0:
            prev = lines[i - 1]
            if prev.strip() and not re.match(r"^\s*\|", prev) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1] if i + 1 < len(lines) else ""):
                add("E-TABLEBR", i + 1, "table header must be preceded by a blank line")

    toks = md.parse(text.replace("\\$", "\x01"))  # escaped dollar signs are literal text, not math delimiters
    base = os.path.dirname(path)
    h1 = 0
    last_level = 0

    def walk(tokens, in_list=False, in_quote=False):
        nonlocal h1, last_level
        depth_list = 0
        for t in tokens:
            ln = (t.map[0] + 1) if t.map else 0
            if t.type == "heading_open":
                lvl = int(t.tag[1])
                if lvl == 1: h1 += 1
                if last_level and lvl > last_level + 1:
                    add("E-H1", ln, f"heading level jumps h{last_level}->h{lvl}")
                last_level = lvl
            if t.type in ("bullet_list_open", "ordered_list_open"): depth_list += 1
            if t.type in ("bullet_list_close", "ordered_list_close"): depth_list -= 1
            if t.type == "math_block" and depth_list > 0:
                add("W-MATHLIST", ln, "display math inside list item")
            if t.type in ("math_block", "math_block_label"):
                for er in check_math(t.content): add("E-MACRO" if "macro" in er else "E-MBRACE", ln, er + f" in: {t.content.strip()[:50]!r}")
            if t.type == "table_open":
                rows = text.split("\n")[t.map[0]:t.map[1]]
                rows = [r for r in rows if not re.match(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$", r)]
                n0 = count_cells(rows[0])
                for k, r in enumerate(rows[1:], 1):
                    if count_cells(r) != n0:
                        add("E-TABLE", t.map[0] + 1 + k + 1, f"row has {count_cells(r)} cells, header has {n0}: {r.strip()[:60]}")
            if t.type == "html_block":
                for m in re.finditer(r"</?([A-Za-z][A-Za-z0-9-]*)", t.content):
                    if m.group(1).lower() not in ALLOWED_TAGS:
                        add("E-HTML", ln, f"tag <{m.group(1)}> will be stripped")
            if t.type == "inline" and t.children:
                for c in t.children:
                    if c.type in ("math_inline", "math_inline_double"):
                        for er in check_math(c.content): add("E-MACRO" if "macro" in er else "E-MBRACE", ln, er + f" in: {c.content.strip()[:50]!r}")
                    if c.type == "text":
                        s = c.content
                        if re.search(r"\*\*|__|~~", s) or re.search(r"(?<![\w*])\*[^\s*][^*\n]*[^\s*]\*(?![\w*])", s):
                            add("E-EMPH", ln, f"unparsed emphasis marker in: {s[:70]!r}")
                        if "$" in s:
                            add("E-MATH", ln, f"stray $ in: {s[:70]!r}")
                    elif c.type == "html_inline":
                        m = re.match(r"</?([A-Za-z][A-Za-z0-9-]*)", c.content)
                        if m and m.group(1).lower() not in ALLOWED_TAGS:
                            add("E-HTML", ln, f"tag {c.content[:30]!r} will be stripped")
                    elif c.type in ("link_open", "image"):
                        href = c.attrGet("href") if c.type == "link_open" else c.attrGet("src")
                        if c.type == "image" and not (c.content or "").strip():
                            add("E-ALT", ln, f"image without alt: {href}")
                        if href and c.type == "link_open" and "#" in href and not re.match(r"^(https?:|mailto:)", href):
                            fpart, frag = href.split("#", 1)
                            tgt = path if not fpart else os.path.join(base, urllib.parse.unquote(fpart))
                            if tgt.endswith(".md") and os.path.exists(tgt) and urllib.parse.unquote(frag).lower() not in slugs_of(tgt):
                                add("E-ANCHOR", ln, f"no heading for anchor #{frag} in {os.path.basename(tgt)}")
                        if href and not re.match(r"^(https?:|mailto:|#)", href):
                            target = urllib.parse.unquote(href.split("#")[0].split("?")[0])
                            if target and not os.path.exists(os.path.join(base, target)):
                                add("E-LINK", ln, f"missing target {href}")
        return

    walk(toks)
    if h1 != 1: add("E-H1", 1, f"expected exactly one H1, found {h1}")
    return out


def main(argv):
    bad = 0
    nfiles = 0
    for p in iter_md(argv):
        nfiles += 1
        for code, ln, msg in lint(p):
            print(f"{p}:{ln}: [{code}] {msg}")
            if code.startswith("E-"): bad += 1
    print(f"-- {nfiles} files, {bad} errors", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
