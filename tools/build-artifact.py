#!/usr/bin/env python3
"""Emit an Artifact-ready copy of index.html.

The Artifact host supplies its own <!doctype>/<head>/<body> skeleton, so this
strips the document wrapper and keeps the title, font link, CDN script, styles
and page markup in order.

    python3 tools/build-artifact.py <output.html>
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "mission02-artifact.html")
s = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

for pat in (r"<!DOCTYPE html>\s*", r"<html[^>]*>\s*", r"</html>\s*",
            r"<head>\s*", r"</head>\s*", r"<body>\s*", r"</body>\s*",
            r'<meta charset="UTF-8">\s*', r'<meta name="viewport"[^>]*>\s*'):
    s = re.sub(pat, "", s, count=1)

open(out, "w", encoding="utf-8").write(s.strip() + "\n")
print("wrote", out, os.path.getsize(out) // 1024, "KB")
