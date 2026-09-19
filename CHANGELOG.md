# Changelog

## 0.1.0 · 2026-09-19 (initial locally tested release)

- Added offline browser UI and CLI for CSV voltage-dip analysis.
- Added explicit units, strict data validation and header-consistent delimiter detection.
- Added hysteresis, duration filtering, capture-boundary/gap handling and trigger association.
- Added HTML/JSON reports, synthetic data and deterministic tests.
- Bundled unmodified Papa Parse 5.5.3 with upstream license and provenance.
- Physical instrument validation remains pending. Live GitHub CI is tracked in Actions.

## Repository packaging, 2026-09-19

- Add hash-verified dependency restore and deterministic demo-build scripts.
- Add read-only test job and separate main-branch generated-file publication job.
- Preserve the v0.1.0 analysis engine, upstream license and synthetic-data boundaries.
