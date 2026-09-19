# Method and interpretation

This document specifies **this application's algorithm**, not a semiconductor specification.

## 1. Input and normalization

The exact vendored Papa Parse version is listed in `THIRD_PARTY_NOTICES.md`. We use its string-to-row parser, never its network-download feature. The wrapper tests candidate delimiters against a consistent header and up to 20 nonblank records. Ambiguous detection stops; explicit delimiter selection remains available. A full parse checks every row width.

Preamble removal is explicit. Headers must be unique and nonempty. Blank records can be skipped, with a count; partially empty data rows fail validation. Selected data cells must be finite decimal/scientific numeric values. Decimal comma is selectable; thousands separators and mixed formats are not supported. Time/voltage units are mandatory. No magnitude-based guessing occurs.

Normalize to seconds and volts. Time must be strictly increasing. Segmented captures that restart time must be exported as separate files. The app neither sorts nor repairs the data.

## 2. Sampling gaps

Let `dt_med` be the median of positive adjacent time intervals. An interval longer than `gap_factor * dt_med` splits the capture into continuous regions. The default factor of 3 is an adjustable **analysis heuristic**, not an instrument guarantee. This detects relative gaps; uniformly sparse data can still be under-sampled without triggering it. Sampling variation greater than 5% of the median creates a warning; that percentage is also a diagnostic heuristic.

Do not interpolate voltage or trigger edges across a detected gap. Close an active event at the last sample before the gap and mark its right edge censored. If the first sample after a gap is already below trip, start a new left-censored event there.

## 3. Hysteresis-defined event

Require `0 < trip < recovery <= nominal`. Start an inactive event at the first sample strictly below trip. Keep it active until a sample is at or above recovery. Oscillation around trip alone does not repeatedly split the same event.

Within one continuous region, estimate a crossing time by linear interpolation:

`t_cross = t0 + (threshold - v0) / (v1 - v0) * (t1 - t0)`

Record the bracketing sample times. This is a piecewise-linear model of the exported samples. It does not recover unobserved high-frequency events or add timing accuracy to the instrument. Multiple true crossings between samples are possible.

Event duration is **trip entry to recovery**. It includes time in the hysteresis band and is not identical to total time strictly below trip. Record the minimum sampled voltage and its sample timestamp. Drop from nominal is `max(0, nominal - minimum)` and is referenced to a user-entered value.

At capture start/end or gaps, flag a censored boundary. Observed duration is a lower bound within the chosen model and known segment; the full event duration is unknown. Keep these events even if their observed duration is below the filter, because their complete duration is unavailable.

## 4. Duration filtering

Discard only complete events with model duration below `min_duration_s`. Preserve them in `excluded_events`, and show raw/kept/excluded counts. This filter is a relevance setting, not proof that excluded transients are noise or harmless. Global capture extrema still include excluded events.

## 5. Trigger association

Optionally find rising (`previous < level`, `current >= level`) or falling (`previous > level`, `current <= level`) edges. Interpolate only across adjacent samples within one segment. For each non-left-censored event, select the most recent preceding edge in the same segment and within `trigger_window_s`. Otherwise lag is `null`.

A preceding trigger does not establish causality, MCU reset, motor activation, or software state. Trigger identity, channel skew, logic thresholds and input polarity are the operator's responsibility. A noisy trigger may produce multiple edges; this version does not debounce the trigger channel.

## 6. Plot versus full-resolution metrics

Compute metrics using every accepted sample. The chart reduces points by retaining first/minimum/maximum/last samples in each display bucket, in chronological order and separately across gaps. Up to 2,000 event/gap overlays, 1,000 trigger markers and 200 event rows are displayed. Full event results remain in JSON and in the report's structured-result details.

This plot is a review aid. It is not a substitute for raw data or a high-bandwidth acquisition.

## 7. Deliberately not implemented

Automatic root-cause attribution; chip brownout specification lookup; loop stability inference; efficiency/power calculations from voltage alone; spectral analysis; probe compensation; automatic clipping detection; vendor-specific binary formats; multi-capture statistics; analog trigger debouncing; regulator compensation recommendations.

## Parser reference

Papa Parse documentation: https://www.papaparse.com/docs
Upstream pinned source: https://github.com/mholt/PapaParse/tree/a4f8b0f1e30bf08e44da96ff5575ffdae7aa9b12
