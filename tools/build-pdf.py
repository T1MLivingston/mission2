#!/usr/bin/env python3
"""Inline the sample PDF into index.html.

Section A hands students a real document to open rather than a picture of one,
and the page has to keep working from a Chromebook's Downloads folder with no
assets beside it -- so the PDF travels inside the HTML as a data URI and the
page turns it into a blob URL at runtime.

    python3 tools/build-pdf.py            # re-inline assets/pdf/school-calendar.pdf

To swap the document, drop a new PDF at that path and run this again.  Keep it
small: whatever it weighs lands in every student's download.  A scanned page
re-saved at ~1100px wide and JPEG quality 82 lands around 250 KB.

The preview beside it is a plain JPEG of the first page, and it is what the card
and the enlarge view actually show.  A PDF in an <iframe> depends on a plugin
that a locked-down Chromebook or an embedded viewer may not run, and a blank
grey box in front of a class is worse than a picture; the real PDF is one click
further on, where the browser opens it in its own tab.
"""
import base64, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "assets" / "pdf" / "school-calendar.pdf"
PREVIEW = ROOT / "assets" / "pdf" / "school-calendar-preview.jpg"
INDEX = ROOT / "index.html"
START, END = "/* PDFDOC_START */", "/* PDFDOC_END */"


def inline(pdf_bytes, jpg_bytes):
    pdf = "data:application/pdf;base64," + base64.b64encode(pdf_bytes).decode("ascii")
    jpg = "data:image/jpeg;base64," + base64.b64encode(jpg_bytes).decode("ascii")
    block = (START + '\nconst SCHEDULE_PDF = "' + pdf + '";\n'
                   + 'const SCHEDULE_PDF_PAGE = "' + jpg + '";\n' + END)
    s = INDEX.read_text()
    a = s.index("\n" + START)
    b = s.index("\n" + END, a)
    assert a < b, "pdf markers out of order"
    INDEX.write_text(s[:a + 1] + block + s[b + 1 + len(END):])
    return len(pdf) + len(jpg)


if __name__ == "__main__":
    data = PDF.read_bytes()
    page = PREVIEW.read_bytes()
    print(f"{PDF.relative_to(ROOT)}  {len(data)/1024:.0f} KB")
    print(f"{PREVIEW.relative_to(ROOT)}  {len(page)/1024:.0f} KB")
    if len(data) + len(page) > 900 * 1024:
        sys.exit("that PDF is too heavy to inline -- shrink it first")
    print(f"inlined {inline(data, page)/1024:.0f} KB of data URI into index.html")
