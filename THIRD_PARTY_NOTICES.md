# Upstream attribution and contribution map

## Papa Parse (unchanged dependency)

- Project: Papa Parse, by Matthew Holt and contributors.
- Official repository: https://github.com/mholt/PapaParse
- Selected version: **5.5.3**. This is a deliberately pinned version; no claim that it is the newest release.
- Tag resolved through the GitHub API to commit: `a4f8b0f1e30bf08e44da96ff5575ffdae7aa9b12`.
- License: MIT; original notice is retained verbatim in `vendor/PapaParse.LICENSE`.
- Imported file: `vendor/papaparse.min.js`.
- Verified upstream Git blob SHA-1: `f31411042b80599f9dd6126ff8fd41f8fa8f68fb`.
- Local SHA-256: `3553fb8bdf5b8004ce5531e6827e81c8b34e7b3992677967754544064e97b016`.
- License-file Git blob SHA-1: `12f5b3503d99c72a03b654ac1b7ac51d6c408a05`.
- Retrieval/verification date: 2026-09-19.
- Modifications to upstream source: **none**. The exact blob hash is checked in the test suite.

The app uses Papa Parse for text-to-row CSV parsing, including quotation/escaping. Its network, worker and jQuery integrations are not used. The copy is embedded in `standalone.html` by the local build script, with the original source header and full MIT text retained.

## This project's incremental work

| File/layer | Attribution |
|---|---|
| `vendor/papaparse.min.js`, `vendor/PapaParse.LICENSE` | Upstream Papa Parse; not authored by this project |
| `src/core.js` | New validation, normalization, event and trigger analysis wrapper |
| `src/report.js` | New visualization and report generation |
| `src/app.js`, `src/style.css`, `index.html` | New application UI |
| `tools/`, `tests/` | New CLI, build script and test cases |
| `samples/` | Deterministically generated signals/reports; not customer or bench data |
| `assets/app-screenshot.png` | Screenshot of this application's synthetic demo |
| `standalone.html` | Generated bundle combining the above, not a separate original library |

New implementation was prepared with AI assistance. The maintainer has not yet supplied an independent code-review or real-hardware verification record. Do not represent this prototype as proof of measured board performance or unaided authorship of the upstream parser.

The application is MIT-licensed. The upstream copyright and MIT terms remain intact. A permissive license permits the specified reuse; it does not make upstream authorship or experimental results yours.
