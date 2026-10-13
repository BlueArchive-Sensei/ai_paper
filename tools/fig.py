#!/usr/bin/env python3
"""Helper for extracting figures from paper.pdf (uses poppler + ImageMagick only).

  fig.py captions PDF            list 'Figure N'/'Table N' caption lines: page, y-fraction
  fig.py preview PDF PAGE OUT    render page with a labelled 10% grid (for locating figures)
  fig.py crop PDF PAGE X0 Y0 X1 Y1 OUT [DPI]   crop by page fractions (0-1, origin top-left);
                                  OUT ending in .jpg is written as JPEG (use for photo-like figures);
                                  whitespace is trimmed and size capped at ~450KB by lowering dpi
"""
import re, subprocess, sys, tempfile, os

def sh(*a):
    subprocess.run(a, check=True)

def pagesize(pdf, page):
    out = subprocess.run(["pdfinfo", "-f", str(page), "-l", str(page), pdf],
                         capture_output=True, text=True, check=True).stdout
    m = re.search(r"Page\s+%d size:\s+([\d.]+) x ([\d.]+)" % page, out) or \
        re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", out)
    return float(m.group(1)), float(m.group(2))

def captions(pdf):
    html = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"],
                          capture_output=True, text=True, check=True).stdout
    for pm in re.finditer(r'<page width="([\d.]+)" height="([\d.]+)">(.*?)</page>', html, re.S):
        pno = html[:pm.start()].count("<page ") + 1
        W, H = float(pm.group(1)), float(pm.group(2))
        for lm in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', pm.group(3), re.S):
            words = re.findall(r">([^<]+)</word>", lm.group(5))
            text = " ".join(words)
            if re.match(r"^(Figure|Fig\.|Table|FIGURE|TABLE)\s*[A-Z]?\d+", text):
                print(f"p{pno}\ty={float(lm.group(2))/H:.3f}-{float(lm.group(4))/H:.3f}\tx={float(lm.group(1))/W:.2f}\t{text[:90]}")

def preview(pdf, page, out):
    with tempfile.TemporaryDirectory() as d:
        base = os.path.join(d, "p")
        sh("pdftoppm", "-r", "80", "-f", str(page), "-l", str(page), "-png", pdf, base)
        png = [f for f in os.listdir(d) if f.endswith(".png")][0]
        src = os.path.join(d, png)
        w, h = [int(x) for x in subprocess.run(["identify", "-format", "%w %h", src],
                capture_output=True, text=True, check=True).stdout.split()]
        cmd = ["convert", src, "-stroke", "rgba(255,0,0,0.5)", "-fill", "red", "-pointsize", "14"]
        for i in range(1, 10):
            x, y = int(w * i / 10), int(h * i / 10)
            cmd += ["-draw", f"line {x},0 {x},{h}", "-draw", f"line 0,{y} {w},{y}",
                    "-stroke", "none", "-draw", f"text {x+2},12 '{i/10:.1f}'",
                    "-draw", f"text 2,{y-2} '{i/10:.1f}'", "-stroke", "rgba(255,0,0,0.5)"]
        sh(*cmd, out)

def crop(pdf, page, x0, y0, x1, y1, out, dpi=150, max_kb=450):
    """Crop a page region (fractions of the page, origin top-left) to OUT (.png or .jpg).
    Whitespace around the content is trimmed automatically (+12px margin). If the file is larger than
    max_kb the resolution is lowered stepwise (never below 80 dpi)."""
    W, H = pagesize(pdf, page)
    ext = os.path.splitext(out)[1].lower()
    fmt = "-jpeg" if ext in (".jpg", ".jpeg") else "-png"
    tried = []
    for d in [dpi] + [x for x in (130, 110, 95, 80) if x < dpi]:
        s = d / 72.0
        px, py = int(x0 * W * s), int(y0 * H * s)
        pw, ph = int((x1 - x0) * W * s), int((y1 - y0) * H * s)
        cmd = ["pdftocairo", fmt] + (["-jpegopt", "quality=88"] if fmt == "-jpeg" else []) + [
            "-singlefile", "-r", str(d), "-f", str(page), "-l", str(page),
            "-x", str(px), "-y", str(py), "-W", str(pw), "-H", str(ph), pdf, os.path.splitext(out)[0]]
        sh(*cmd)
        sh("convert", out, "-trim", "+repage", "-bordercolor", "white", "-border", "12", "-quality", "88", out)
        kb = os.path.getsize(out) // 1024
        dims = subprocess.run(["identify", "-format", "%wx%h", out], capture_output=True, text=True).stdout
        tried.append((d, kb))
        if kb <= max_kb:
            break
    print(f"{out}: {dims}, {kb}KB, {d}dpi")


if __name__ == "__main__":
    c, a = sys.argv[1], sys.argv[2:]
    if c == "captions": captions(a[0])
    elif c == "preview": preview(a[0], int(a[1]), a[2])
    elif c == "crop": crop(a[0], int(a[1]), *map(float, a[2:6]), a[6], int(a[7]) if len(a) > 7 else 150)
