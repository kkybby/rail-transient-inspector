# Validation record · 2026-09-19

## Actual software checks

- Runtime: Node.js v22.16.0; Python 3.13.5.
- Browser automation: Playwright 1.57.0.
- Browser: Chromium 144.0.7559.96 built on Debian GNU/Linux 13 (trixie).
- Node command: `node --test tests/*.test.cjs`.
- Result: **38 tests, 38 passed, 0 failed, 0 skipped**.
- Optional UI command: `python tests/browser_smoke.py`.
- UI result: all scripted smoke checks passed; no JavaScript page errors; no network requests observed.

The browser suite injects the exact `standalone.html` bundle using Playwright `set_content` on a blank document. Direct navigation to both `file://` and a local HTTP server was blocked by this preparation environment's administrative browser policy. We did not modify or bypass that policy. End-user URL/file navigation, Firefox, Safari, production hosting have **not** been validated by those preparation checks. GitHub CI is tracked separately below. SHA-256 uses Web Crypto where available; an opaque `set_content` origin may return `null`. The CLI fingerprint was validated independently using Node's crypto module.

## What the tests cover

Analytical crossing times; threshold equality; hysteresis chatter; left/right-censored captures; entirely low captures; complete short-event filtering; retained censored short events; gap splitting; rising/falling triggers; no future-trigger or cross-gap association; invalid thresholds; duplicate/reversed time; missing/nonfinite cells; quoted/BOM CSV; semicolon decimal-comma data; explicit preamble handling; mandatory units; wrong column counts; malformed quotes; sample/file limits; 150,000-sample capture; deterministic demo; safe HTML escaping; exact upstream blob hash; time-shift invariance; CLI output, validation, no-overwrite behavior and custom input.

Browser smoke checks exercise demo event counts, stale-result/export invalidation, changed thresholds, JSON export, mandatory units after import, custom CSV analysis, malformed CSV blocking, demo reset and 390px responsive layout. Exported HTML generation/escaping is tested at the Node layer. We have not performed a full browser accessibility audit or adversarial security assessment.

## Reference synthetic result

The committed demo has 4,001 samples across 20 ms, with 5 µs median spacing. At nominal 3.3 V, trip 3.0 V, recovery 3.08 V and a 20 µs minimum duration, it yields 3 raw events, 2 retained events and 1 excluded short complete event. No event is boundary-censored.

These numbers describe a mathematical signal constructed by the project. They are **not a physical board measurement**, a device rating or a timing guarantee. Full numbers and input fingerprint are in `samples/demo-report.json`.

## Evidence still required

1. Independent maintainer review of algorithm, implementation and test expectations.
2. One authorized real capture with instrument/export version, units, probe scale, test condition and source revision recorded.
3. Manual comparison of sampled minima, threshold brackets and event classification.
4. Documentation of any mismatch and regression tests before claiming instrument-format support.

No physical scope, NanoVNA, tinySA, PCB, firmware image or customer's design was used in these checks. No hardware performance, certification, commercial deployment, safety or root-cause claim is supported by this release.

## GitHub publication verification

The repository workflow reruns the Node suite and Chromium smoke checks. Consult the actual Actions run and the generated `docs/node-test-run.txt` and `docs/browser-smoke-run.txt`; no passing status is inferred from configuration alone. The optional browser runner accepts `RTI_ARTIFACT_DIR` for controlled screenshot output. Analysis code is unchanged from the prepared v0.1.0 package.
