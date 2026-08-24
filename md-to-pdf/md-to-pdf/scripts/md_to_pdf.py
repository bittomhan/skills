#!/usr/bin/env python3
"""Convert Markdown to PDF with Chinese font support using markdown + weasyprint."""

import markdown
import sys
import os
from weasyprint import HTML

def md_to_pdf(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        sys.exit(1)
    
    if output_path is None:
        output_path = input_path.rsplit('.', 1)[0] + '.pdf'
    
    # Read markdown
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert MD → HTML with extensions
    extensions = [
        'tables',
        'fenced_code',
        'codehilite',
        'toc',
        'nl2br',
        'sane_lists',
    ]
    html_body = markdown.markdown(md_content, extensions=extensions)

    # Post-process: assign proportional column widths to each table.
    # weasyprint's table-layout:auto squeezes narrow columns to one CJK char per
    # line ("vertical text") when other columns hold long text. Fix: fixed layout
    # + colgroup widths proportional to max content length per column.
    import re as _re

    def _add_colgroups(html):
        # Table content width: A4 595pt - 2*2.2cm(62.4pt) margins ≈ 470pt
        TABLE_PT = 470.0
        CHAR_PT = 9.6   # CJK glyph advance at 9pt (~9.03) + slack
        PAD_PT = 16.0   # cell horizontal padding (~9pt) + borders + slack

        def disp_width(text):
            # CJK chars render ~full width; ASCII digits/letters ~0.6
            return sum(1.0 if ord(c) > 0x2E80 else 0.6 for c in text)

        def make_colgroup(m):
            table_html = m.group(0)
            rows = _re.findall(r'<tr>.*?</tr>', table_html, _re.DOTALL)
            if not rows:
                return table_html
            ncols = max(len(_re.findall(r'<t[dh]', row)) for row in rows)
            if ncols == 0:
                return table_html
            # per-column max display width, capped at 14 so long-text columns
            # cannot dominate; lower-clamped at 3 to avoid zero weights
            disp = [1.0] * ncols
            for row in rows:
                cells = _re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, _re.DOTALL)
                for i, cell in enumerate(cells[:ncols]):
                    text = _re.sub(r'<[^>]+>', '', cell).strip()
                    disp[i] = max(disp[i], min(disp_width(text), 14.0))
            disp = [max(x, 3.0) for x in disp]
            total = sum(disp)
            target = [x * 100.0 / total for x in disp]
            # content-driven floor: width to show the longest single line
            # unwrapped (never more than an equal share); ceiling per column:
            # what remains after every other column takes its floor
            equal = 100.0 / ncols
            floors = [min((d * CHAR_PT + PAD_PT) / TABLE_PT * 100.0, equal)
                      for d in disp]
            caps = [100.0 - sum(f for j, f in enumerate(floors) if j != i)
                    for i in range(ncols)]
            # water-filling: satisfy every floor first, then distribute the
            # remaining width proportional to (target - floor), capped.
            # NEVER renormalise afterwards — dividing by the clamped sum
            # erodes floors and re-breaks label columns (3+1 wraps).
            alloc = floors[:]
            want = [max(0.0, t - f) for t, f in zip(target, floors)]
            rest = 100.0 - sum(alloc)
            for _ in range(20):
                wsum = sum(want)
                if rest <= 0.01 or wsum <= 0.01:
                    break
                progressed = False
                for i in range(ncols):
                    if want[i] <= 0.001:
                        continue
                    share = rest * want[i] / wsum
                    room = max(0.0, caps[i] - alloc[i])
                    g = min(share, room, want[i])
                    if g > 0.0005:
                        alloc[i] += g
                        want[i] -= g
                        rest -= g
                        progressed = True
                if not progressed:
                    break
            if rest > 0.01:  # all capped: spread leftover evenly
                for i in range(ncols):
                    alloc[i] += rest / ncols
            cols = ''.join(
                f'<col style="width:{p:.1f}%">' for p in alloc
            )
            return table_html.replace('<table>', f'<table><colgroup>{cols}</colgroup>', 1)

        return _re.sub(r'<table>.*?</table>', make_colgroup, html, flags=_re.DOTALL)

    def _fix_h1_breaks(html):
        """Skip the forced page break before an H1 when everything between
        it and the previous H1 is only meta content (blockquote / hr).

        Root cause fixed 2026-08-20: a blanket `page-break-before: always`
        on every H1 leaves page 1 almost empty for the common
        "title H1 + short meta quote + first section H1" document pattern
        (same symptom as the 2026-08-14 merged-report cover-page issue).
        Rule: keep the break only if real content (paragraph / list / table /
        heading) appears between the two H1s.
        """
        parts = _re.split(r'(<h1\b[^>]*>.*?</h1>)', html, flags=_re.DOTALL)
        out = []
        for i, seg in enumerate(parts):
            if seg.startswith('<h1') and i > 1:
                # gap between the PREVIOUS h1 and this h1 sits at parts[i-1]
                prev = parts[i - 1]
                meta = _re.sub(r'<blockquote\b.*?</blockquote>', '', prev,
                               flags=_re.DOTALL)
                meta = _re.sub(r'<hr\s*/?>', '', meta)
                meta = _re.sub(r'\s+', '', meta)
                if not meta:
                    seg = _re.sub(r'<h1\b', '<h1 class="no-break"', seg,
                                  count=1)
            out.append(seg)
        return ''.join(out)

    html_body = _add_colgroups(html_body)
    html_body = _fix_h1_breaks(html_body)
    
    # CSS for Chinese PDF styling
    css = """
    @page {
        size: A4;
        margin: 2cm 2.2cm;
        @bottom-center {
            content: counter(page);
            font-size: 9pt;
            color: #999;
            font-family: "Noto Sans CJK SC", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
        }
    }
    
    body {
        font-family: "Noto Sans CJK SC", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
        font-size: 10.5pt;
        line-height: 1.7;
        color: #1a1a1a;
    }
    
    h1 {
        font-size: 18pt;
        font-weight: 700;
        margin-top: 1.2em;
        margin-bottom: 0.6em;
        border-bottom: 2px solid #2563eb;
        padding-bottom: 0.3em;
        page-break-before: always;
        color: #1e3a5f;
    }
    
    h1:first-of-type {
        page-break-before: avoid;
    }
    
    /* Meta-only sections (title + short quote block) flow on the same page;
       the script adds this class when the gap between two H1s holds only
       blockquote/hr (fix 2026-08-20: avoids a near-blank first page). */
    h1.no-break {
        page-break-before: avoid;
    }
    
    h2 {
        font-size: 14pt;
        font-weight: 700;
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #2563eb;
        break-after: avoid;
        page-break-after: avoid;
    }
    
    h3 {
        font-size: 12pt;
        font-weight: 600;
        margin-top: 0.8em;
        margin-bottom: 0.4em;
        color: #333;
        break-after: avoid;
        page-break-after: avoid;
    }
    
    blockquote {
        border-left: 3px solid #2563eb;
        margin: 0.8em 0;
        padding: 0.5em 1em;
        background: #f0f4ff;
        color: #374151;
    }
    
    blockquote p {
        margin: 0.3em 0;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.8em 0;
        font-size: 9pt;
        page-break-inside: auto;
        table-layout: fixed;
    }
    
    td, th {
        word-break: break-word;
        overflow-wrap: anywhere;
    }
    
    thead {
        display: table-header-group;
    }
    
    tr {
        page-break-inside: avoid;
    }
    
    th {
        background: #2563eb;
        color: white;
        padding: 5px 6px;
        text-align: left;
        font-weight: 600;
        font-size: 9pt;
    }
    
    td {
        padding: 4px 6px;
        border: 1px solid #d1d5db;
        vertical-align: top;
    }
    
    tr:nth-child(even) {
        background: #f9fafb;
    }
    
    code {
        background: #f3f4f6;
        padding: 1px 4px;
        border-radius: 3px;
        font-family: "SF Mono", "Menlo", "Consolas", monospace;
        font-size: 8.5pt;
    }
    
    pre {
        background: #1e293b;
        color: #e2e8f0;
        padding: 12px;
        border-radius: 6px;
        overflow-x: auto;
        font-size: 8pt;
        line-height: 1.5;
    }
    
    pre code {
        background: none;
        padding: 0;
        color: inherit;
        font-size: 8pt;
    }
    
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1.5em 0;
    }
    
    strong {
        color: #1e3a5f;
    }
    
    ul, ol {
        padding-left: 1.5em;
    }
    
    li {
        margin-bottom: 0.2em;
    }
    
    a {
        color: #2563eb;
        text-decoration: none;
    }
    
    .toc {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 1em;
        margin: 1em 0;
    }
    """
    
    # Full HTML document
    title = os.path.basename(input_path).rsplit('.', 1)[0]
    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""
    
    # Generate PDF
    print(f"Converting: {input_path}")
    print(f"Output:    {output_path}")
    HTML(string=html_doc).write_pdf(output_path)
    
    size_kb = os.path.getsize(output_path) / 1024
    print(f"Done: {output_path} ({size_kb:.0f} KB)")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <input.md> [output.pdf]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    md_to_pdf(input_file, output_file)
