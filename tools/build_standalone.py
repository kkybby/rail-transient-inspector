#!/usr/bin/env python3
"""Create one offline HTML file with hash-based CSP. Python 3, standard library only."""
from pathlib import Path
import base64
import hashlib
import html
import re
ROOT = Path(__file__).resolve().parents[1]
def csp_hash(text):
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode('utf-8')).digest()).decode() + "'"
def build():
    page = (ROOT / 'index.html').read_text()
    script_paths = ['vendor/papaparse.min.js', 'src/core.js', 'src/report.js', 'src/app.js']
    scripts = [(ROOT / path).read_text() for path in script_paths]
    css = (ROOT / 'src/style.css').read_text()
    for path in script_paths:
        page = page.replace(f'<script src="{path}" defer></script>', '')
    page = page.replace('<link rel="stylesheet" href="src/style.css">', '<style>' + css + '</style>')
    policy = "default-src 'none'; script-src " + ' '.join(csp_hash(s) for s in scripts) + "; style-src " + csp_hash(css) + "; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"
    page = re.sub(r'(<meta http-equiv="Content-Security-Policy" content=")[^"]*', lambda m: m.group(1) + policy, page)
    page = page.replace('href="index.html"', 'href="#"')
    page = page.replace('<a href="README.md">Project README</a><a href="docs/ALGORITHM.md">Method &amp; limitations</a><a href="THIRD_PARTY_NOTICES.md">Open-source attribution</a>', '<a href="#offline-notes">Method &amp; attribution</a>')
    notes = '<details id="offline-notes"><summary>Method, evidence &amp; attribution</summary><p>Enter an event strictly below trip; end it at or above recovery. Crossing times are linearly interpolated. No interpolation across gaps larger than the chosen median-spacing multiplier. Censored events are retained even when shorter than the minimum-duration filter. Trigger matching is preceding-edge, same-segment, within-window only. This does not diagnose a reset or its cause.</p><p>All built-in signals are generated, not measured. Code was AI-assisted; independent human engineering review and physical validation remain pending. CSV parser: Papa Parse 5.5.3, unchanged from upstream commit a4f8b0f1e30bf08e44da96ff5575ffdae7aa9b12. Application logic, tests and reporting are this project\'s additions.</p><pre>' + html.escape((ROOT/'LICENSE').read_text() + '\n\nPAPA PARSE UPSTREAM LICENSE\n\n' + (ROOT/'vendor/PapaParse.LICENSE').read_text()) + '</pre></details>'
    page = page.replace('</main>', notes + '</main>')
    page = page.replace('</body>', '\n'.join('<script>' + s + '</script>' for s in scripts) + '\n</body>')
    destination = ROOT / 'standalone.html'
    destination.write_text(page)
    print(destination)
if __name__ == '__main__':
    build()
