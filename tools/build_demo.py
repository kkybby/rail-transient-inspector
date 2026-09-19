#!/usr/bin/env python3
"""Regenerate only documented synthetic examples and the offline application."""
from pathlib import Path
import subprocess
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    subprocess.run([sys.executable, str(ROOT / 'tools/fetch_vendor.py')], check=True)
    subprocess.run([sys.executable, str(ROOT / 'tools/build_standalone.py')], check=True)
    before = hashlib.sha256((ROOT / 'standalone.html').read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(ROOT / 'tools/build_standalone.py')], check=True)
    assert hashlib.sha256((ROOT / 'standalone.html').read_bytes()).hexdigest() == before
    samples = ROOT / 'samples'
    samples.mkdir(exist_ok=True)
    csv = subprocess.check_output(['node', '-e', "process.stdout.write(require('./src/core.js').demoCsv())"], cwd=ROOT)
    (samples / 'synthetic-demo.csv').write_bytes(csv)
    # These two paths are generated demo outputs, never user-provided captures.
    for name in ('demo-report.json', 'demo-report.html'):
        (samples / name).unlink(missing_ok=True)
    subprocess.run(['node', 'tools/analyze.cjs', '--demo', '--out', 'samples/demo-report.json', '--html', 'samples/demo-report.html'], cwd=ROOT, check=True)
    print('Offline build and synthetic examples generated; no hardware data used.')

if __name__ == '__main__':
    main()
