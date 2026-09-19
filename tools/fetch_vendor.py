#!/usr/bin/env python3
"""Restore the pinned upstream CSV parser, verifying bytes before writing.
Only needed when vendor/papaparse.min.js is missing. Never fetches 'latest'.
"""
from pathlib import Path
import hashlib
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://raw.githubusercontent.com/mholt/PapaParse/a4f8b0f1e30bf08e44da96ff5575ffdae7aa9b12/papaparse.min.js'
EXPECTED = '3553fb8bdf5b8004ce5531e6827e81c8b34e7b3992677967754544064e97b016'
DEST = ROOT / 'vendor/papaparse.min.js'

def main():
    if DEST.exists():
        data = DEST.read_bytes()
    else:
        with urllib.request.urlopen(URL, timeout=30) as response:
            data = response.read(100_001)
        if len(data) > 100_000:
            raise SystemExit('Refusing oversized dependency response.')
    if hashlib.sha256(data).hexdigest() != EXPECTED:
        raise SystemExit('Dependency integrity mismatch; nothing was written.')
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(data)
    print('Verified Papa Parse 5.5.3, unchanged upstream bytes.')

if __name__ == '__main__':
    main()
