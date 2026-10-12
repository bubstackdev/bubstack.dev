#!/usr/bin/env python3
"""Render face-hugger/docs/privacy.md (the source of truth) into privacy.html here. Handles the Markdown that file
uses: headings, paragraphs, links and bold. Run from this folder after the policy changes:

  python3 build-privacy.py ../../face-hugger/docs/privacy.md
"""
from html import escape
from pathlib import Path
import re
import sys

source = Path(sys.argv[1] if len(sys.argv) > 1 else '../../face-hugger/docs/privacy.md')
lines = source.read_text(encoding='utf-8').split('\n')


def inline(text):
    text = escape(text, quote=False)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'<a href="{escape(m[2])}">{m[1]}</a>', text)


body, title, paragraph = [], 'Privacy policy', []


def flush():
    if paragraph:
        body.append(f'<p>{inline(" ".join(paragraph))}</p>')
        paragraph.clear()


for line in lines:
    if line.startswith('# '):
        flush()
        title = line[2:].strip()
    elif line.startswith('## '):
        flush()
        body.append(f'</section>\n<section><h2>{inline(line[3:].strip())}</h2>')
    elif not line.strip():
        flush()
    else:
        paragraph.append(line.strip())
flush()

html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · Bubstack</title>
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="../assets/face-hugger.png">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="shell topbar">
    <a class="brand" href="../"><img src="../assets/bub.png" alt="" width="40" height="40">Bubstack</a>
    <nav class="nav" aria-label="Face Hugger"><a href="./">Help</a><a href="privacy.html" aria-current="page">Privacy</a></nav>
  </header>
  <main id="main" class="shell doc">
    <h1>{escape(title)}</h1>
    <section>{"".join(body)}</section>
  </main>
  <footer class="shell footer">
    <p><a href="../">Bubstack</a> · <a href="./">Face Hugger help</a></p>
  </footer>
</body>
</html>
'''
# The first heading opens a section that the wrapper already opened; drop the empty one.
html = html.replace('<section></section>\n', '', 1)
Path(__file__).with_name('privacy.html').write_text(html, encoding='utf-8')
print(f'Wrote privacy.html from {source}')
