# Case note: from raw samples to an auditable event report

**Type:** independent software demonstration, developed with AI assistance.  
**Evidence level:** automated tests and synthetic waveforms.  
**Real hardware / client deployment:** not yet validated; none claimed.

## Engineering question

How can a rail-voltage trace and an optional synchronous trigger trace be reduced to a readable event log without hiding bad data or presenting temporal association as proven causality?

## Design choices

Use a small, unmodified open-source CSV parser instead of claiming to invent CSV parsing. Put the new work in the engineering wrapper: explicit units, a specified hysteresis model, incomplete-event treatment, gap handling, trigger association and shareable reports. Keep calculations reusable from a CLI as well as the browser.

Reject malformed input instead of silently dropping rows. Keep short excluded events in the report. Separate visualization decimation from full-resolution analysis. Embed synthetic-origin labels in the screenshot, sample reports and README.

## Reproducible demonstration

`samples/synthetic-demo.csv` is generated from `demoCsv()` in `src/core.js`. It has 4,001 samples over 20 ms, two designed longer dips, one deliberately short dip and two trigger pulses. With the documented example settings, the software returns 3 raw events, 2 retained events, 1 filtered short event and 0 censored events. These values describe generated data only.

Run `npm test` for numerical, parsing, edge-case and CLI tests. See `docs/VALIDATION.md` for actual local test status and limitations.

## Attribution and human contribution

Papa Parse and its author retain their attribution. This repository's incremental work is the event-analysis/reporting application. An AI assistant performed the initial implementation and test runs. Independent maintainer review, instrument checks and future design changes should be recorded with actual commits and evidence. The current repository does not claim those steps have already occurred.

## Next evidence step

On an authorized, nonconfidential capture, compare the tool's extrema and event brackets against manual scope-cursor/CSV review. Record the exact scope model, firmware/export mode, sample interval, probe attenuation, source units, chosen thresholds and observed differences. No new board or instrument purchase is a prerequisite.
