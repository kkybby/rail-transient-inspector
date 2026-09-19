/* Rail Transient Inspector | MIT | AI-assisted application code. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('../vendor/papaparse.min.js'));
  else root.RailInspector = factory(root.Papa);
})(typeof globalThis !== 'undefined' ? globalThis : this, function (Papa) {
  'use strict';
  const VERSION = '0.1.0';
  const MAX_BYTES = 10 * 1024 * 1024;
  const MAX_SAMPLES = 200000;
  const TIME_UNITS = Object.freeze({s: 1, ms: 1e-3, us: 1e-6, ns: 1e-9});
  const VOLTAGE_UNITS = Object.freeze({V: 1, mV: 1e-3});
  function fail(message) { throw new Error(message); }
  function finite(value, name) {
    if (typeof value !== 'number' || !Number.isFinite(value)) fail(name + ' must be a finite number.');
    return value;
  }
  function numeric(value, decimal, label) {
    let s = String(value).trim();
    if (!['.', ','].includes(decimal)) fail('Choose a decimal separator.');
    if (decimal === ',') { if (s.includes('.')) fail(label + ': mixed decimal separators.'); s = s.replace(',', '.'); }
    if (!/^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$/.test(s)) fail(label + ': missing or invalid numeric cell.');
    return finite(Number(s), label);
  }
  function parseTable(text, options = {}) {
    if (typeof text !== 'string') fail('CSV input must be text.');
    if (new TextEncoder().encode(text).length > MAX_BYTES) fail('CSV exceeds the 10 MiB limit.');
    const skip = options.skip_lines ?? 0;
    if (!Number.isInteger(skip) || skip < 0 || skip > 1000) fail('Preamble lines must be an integer between 0 and 1000.');
    let delimiter = options.delimiter ?? '';
    if (!['', ',', ';', '\t', '|'].includes(delimiter)) fail('Unsupported delimiter.');
    const body = text.replace(/^\uFEFF/, '').split(/\r\n|\r|\n/).slice(skip).join('\n');
    if (!delimiter) {
      // Header-consistent detection avoids mistaking decimal commas for delimiters.
      const candidates = [',', ';', '\t', '|'].filter(d => {
        const trial = Papa.parse(body, {delimiter: d, header: false, dynamicTyping: false,
          preview: 20, skipEmptyLines: 'greedy', worker: false, download: false});
        const width = trial.data[0]?.length || 0;
        return !trial.errors.length && width >= 2 && trial.data.length >= 3 &&
          trial.data.every(row => row.length === width);
      });
      if (candidates.length !== 1) fail('Unable to identify one consistent delimiter. Choose a delimiter and check preamble lines.');
      delimiter = candidates[0];
    }
    const parsed = Papa.parse(body, {header: false, dynamicTyping: false, delimiter,
      skipEmptyLines: false, delimitersToGuess: [',', ';', '\t', '|'], worker: false, download: false});
    if (parsed.errors.length) fail('CSV parse error: ' + parsed.errors[0].message + ' Choose the delimiter explicitly when auto-detection is ambiguous.');
    let blankRows = 0;
    const records = parsed.data.map((cells, i) => ({cells, record: i + 1 + skip})).filter(r => {
      if (r.cells.every(c => String(c).trim() === '')) { blankRows++; return false; } return true;
    });
    if (records.length < 3) fail('CSV needs a header and at least two numeric samples.');
    const headers = records.shift().cells.map(c => String(c).trim());
    if (headers.length < 2 || headers.some(h => !h) || new Set(headers).size !== headers.length) fail('Use at least two non-empty, unique column headers.');
    if (records.length > MAX_SAMPLES) fail('CSV exceeds the 200,000 sample limit.');
    for (const r of records) if (r.cells.length !== headers.length) fail('CSV record ' + r.record + ': column count differs from header. No rows were silently dropped.');
    return {headers, records, delimiter: parsed.meta.delimiter, blank_rows_skipped: blankRows, preamble_lines_skipped: skip};
  }
  function toSamples(table, mapping) {
    const {time_column, voltage_column, trigger_column = '', time_unit, voltage_unit,
      trigger_unit = 'V', decimal = '.'} = mapping;
    const tc = table.headers.indexOf(time_column), vc = table.headers.indexOf(voltage_column);
    const gc = trigger_column ? table.headers.indexOf(trigger_column) : -1;
    if (tc < 0 || vc < 0 || tc === vc) fail('Choose different, valid time and rail-voltage columns.');
    if (trigger_column && (gc < 0 || gc === tc || gc === vc)) fail('Choose a separate, valid trigger column.');
    if (!Object.hasOwn(TIME_UNITS, time_unit) || !Object.hasOwn(VOLTAGE_UNITS, voltage_unit)) fail('Confirm the CSV time and voltage units. Units are never inferred from magnitudes.');
    if (gc >= 0 && !Object.hasOwn(VOLTAGE_UNITS, trigger_unit)) fail('Confirm trigger voltage units.');
    const samples = table.records.map(r => {
      const s = {t: numeric(r.cells[tc], decimal, 'Record ' + r.record + ' time') * TIME_UNITS[time_unit],
        v: numeric(r.cells[vc], decimal, 'Record ' + r.record + ' rail') * VOLTAGE_UNITS[voltage_unit]};
      if (gc >= 0) s.trigger = numeric(r.cells[gc], decimal, 'Record ' + r.record + ' trigger') * VOLTAGE_UNITS[trigger_unit];
      return s;
    });
    validateSamples(samples);
    return samples;
  }
  function validateSamples(samples) {
    if (!Array.isArray(samples) || samples.length < 2 || samples.length > MAX_SAMPLES) fail('Provide 2 to 200,000 samples.');
    const trigger = Object.hasOwn(samples[0], 'trigger');
    for (let i = 0; i < samples.length; i++) {
      const s = samples[i]; finite(s.t, 'Time at sample ' + i); finite(s.v, 'Voltage at sample ' + i);
      if (Object.hasOwn(s, 'trigger') !== trigger) fail('Trigger channel has missing samples.');
      if (trigger) finite(s.trigger, 'Trigger at sample ' + i);
      if (i && !(s.t > samples[i - 1].t)) fail('Time must be strictly increasing. Duplicate timestamps and segmented/time-reset captures are not sorted or repaired.');
    }
    if (!Number.isFinite(samples.at(-1).t - samples[0].t)) fail('Capture time span overflows.');
  }
  function validateConfig(input) {
    const c = Object.assign({min_duration_s: 0, gap_factor: 3, trigger_level_v: 1.65,
      trigger_edge: 'rising', trigger_window_s: 0.002}, input);
    for (const key of ['nominal_v', 'trip_v', 'recover_v', 'min_duration_s', 'gap_factor', 'trigger_level_v', 'trigger_window_s']) finite(c[key], key);
    if (!(c.nominal_v > 0 && c.trip_v > 0 && c.trip_v < c.recover_v && c.recover_v <= c.nominal_v)) fail('Thresholds must satisfy 0 < trip < recovery <= nominal.');
    if (c.min_duration_s < 0 || c.trigger_window_s < 0 || c.gap_factor <= 1) fail('Duration/window must be non-negative; gap factor must exceed 1.');
    if (!['rising', 'falling'].includes(c.trigger_edge)) fail('Trigger edge must be rising or falling.');
    return c;
  }
  function median(values) {
    const a = [...values].sort((x, y) => x - y), i = Math.floor(a.length / 2);
    return a.length % 2 ? a[i] : a[i - 1] / 2 + a[i] / 2;
  }
  function crossTime(a, b, key, level) {
    const fraction = (level - a[key]) / (b[key] - a[key]);
    return a.t + Math.max(0, Math.min(1, fraction)) * (b.t - a.t);
  }
  function analyze(samples, input) {
    validateSamples(samples);
    const c = validateConfig(input), deltas = samples.slice(1).map((s, i) => s.t - samples[i].t);
    const dt = median(deltas), gapLimit = dt * c.gap_factor;
    const gaps = [], triggers = [], raw = []; let current = null, segment = 0;
    let minimum = Infinity, maximum = -Infinity, observedSpan = 0, minAt = 0;
    function finish(end, rightCensored, reason, bracket) {
      if (!current) return;
      current.end_s = end; current.duration_s = Math.max(0, end - current.start_s);
      current.right_censored = rightCensored; current.end_reason = reason; current.end_bracket_s = bracket;
      current.complete = !(current.left_censored || rightCensored);
      current.drop_from_nominal_v = Math.max(0, c.nominal_v - current.minimum_v);
      raw.push(current); current = null;
    }
    for (let i = 0; i < samples.length; i++) {
      const s = samples[i], prev = i ? samples[i - 1] : null;
      const gap = prev && s.t - prev.t > gapLimit;
      if (s.v < minimum) { minimum = s.v; minAt = s.t; } maximum = Math.max(maximum, s.v);
      if (gap) {
        finish(prev.t, true, 'sampling_gap', null);
        gaps.push({after_index: i - 1, before_index: i, start_s: prev.t, end_s: s.t, duration_s: s.t - prev.t}); segment++;
      } else if (prev) observedSpan += s.t - prev.t;
      const continuousPrev = prev && !gap ? prev : null;
      if (continuousPrev && Object.hasOwn(s, 'trigger')) {
        const rise = prev.trigger < c.trigger_level_v && s.trigger >= c.trigger_level_v;
        const fall = prev.trigger > c.trigger_level_v && s.trigger <= c.trigger_level_v;
        if ((c.trigger_edge === 'rising' && rise) || (c.trigger_edge === 'falling' && fall))
          triggers.push({time_s: crossTime(prev, s, 'trigger', c.trigger_level_v), segment,
            bracket_s: [prev.t, s.t], edge: c.trigger_edge});
      }
      if (!current && s.v < c.trip_v) {
        current = {start_s: continuousPrev ? crossTime(prev, s, 'v', c.trip_v) : s.t,
          start_bracket_s: continuousPrev ? [prev.t, s.t] : null,
          left_censored: !continuousPrev, minimum_v: s.v, minimum_at_s: s.t,
          below_trip_sample_count: 1, segment, trigger_s: null, trigger_lag_s: null};
      } else if (current) {
        if (s.v < current.minimum_v) { current.minimum_v = s.v; current.minimum_at_s = s.t; }
        if (s.v < c.trip_v) current.below_trip_sample_count++;
        if (s.v >= c.recover_v) finish(crossTime(prev, s, 'v', c.recover_v), false, 'recovery_crossing', [prev.t, s.t]);
      }
    }
    finish(samples.at(-1).t, true, 'capture_end', null);
    let triggerIndex = -1;
    for (const e of raw) {
      while (triggerIndex + 1 < triggers.length && triggers[triggerIndex + 1].time_s <= e.start_s) triggerIndex++;
      const t = triggers[triggerIndex];
      if (!e.left_censored && t && t.segment === e.segment && e.start_s - t.time_s <= c.trigger_window_s) {
        e.trigger_s = t.time_s; e.trigger_lag_s = e.start_s - t.time_s;
      }
      // Incomplete events cannot be safely discarded by an observed-duration filter.
      e.kept = !e.complete || e.duration_s + 1e-15 >= c.min_duration_s;
    }
    const events = raw.filter(e => e.kept).map((e, i) => Object.assign({id: i + 1}, e));
    const warnings = [];
    if (gaps.length) warnings.push(gaps.length + ' sampling gap(s): no interpolation or trigger matching across gaps.');
    if (deltas.some(d => Math.abs(d - dt) > dt * 0.05)) warnings.push('Sample spacing varies by more than 5% of the median; inspect the timebase.');
    const incomplete = events.filter(e => !e.complete).length;
    if (incomplete) warnings.push(incomplete + ' event(s) touch a capture boundary or gap. Their observed durations are lower bounds under the interpolation model.');
    if (events.some(e => e.below_trip_sample_count < 3)) warnings.push('Some events contain fewer than 3 samples below trip. Short transients are poorly resolved.');
    if (raw.length !== events.length) warnings.push((raw.length - events.length) + ' complete event(s) excluded by the minimum-duration filter; the capture minimum still includes them.');
    if (Object.hasOwn(samples[0], 'trigger') && !triggers.length) warnings.push('No selected trigger edges found at the chosen trigger level.');
    warnings.push('Thresholds are user-defined analysis limits, not verified MCU reset specifications. Temporal association does not establish a reset or its cause.');
    return {schema_version: 1, tool: 'Rail Transient Inspector', version: VERSION, configuration: c,
      capture: {sample_count: samples.length, start_s: samples[0].t, end_s: samples.at(-1).t,
        span_s: samples.at(-1).t - samples[0].t, observed_span_s: observedSpan,
        median_sample_interval_s: dt, max_sample_interval_s: deltas.reduce((a, b) => Math.max(a, b), 0),
        minimum_v: minimum, minimum_at_s: minAt, maximum_v: maximum,
        peak_to_peak_v: maximum - minimum, drop_from_nominal_v: Math.max(0, c.nominal_v - minimum),
        continuous_regions: segment + 1},
      event_counts: {raw: raw.length, kept: events.length, excluded_short_complete: raw.length - events.length, incomplete},
      events, excluded_events: raw.filter(e => !e.kept), triggers, gaps, warnings};
  }
  function demoCsv() {
    const rows = ['time_s,rail_v,trigger_v'];
    for (let i = 0; i <= 4000; i++) {
      const t = i * 0.000005, ms = t * 1000;
      let v = 3.3 + 0.006 * Math.sin(i * 0.19) + 0.003 * Math.sin(i * 0.91);
      if (ms >= 5 && ms < 5.22) v -= 0.66 * (ms - 5) / 0.22;
      if (ms >= 5.22 && ms < 7.15) v -= 0.66 * Math.exp(-(ms - 5.22) / 0.73);
      if (ms >= 12.6 && ms < 12.73) v -= 0.44 * (ms - 12.6) / 0.13;
      if (ms >= 12.73 && ms < 13.65) v -= 0.44 * Math.exp(-(ms - 12.73) / 0.34);
      if (i === 3300) v = 2.97;
      const trigger = ((ms >= 4.8 && ms < 5.8) || (ms >= 12.4 && ms < 13.4)) ? 3.3 : 0;
      rows.push(t.toFixed(9) + ',' + v.toFixed(6) + ',' + trigger.toFixed(3));
    }
    return rows.join('\n') + '\n';
  }
  return Object.freeze({VERSION, MAX_BYTES, MAX_SAMPLES, TIME_UNITS, VOLTAGE_UNITS,
    parseTable, toSamples, analyze, validateConfig, demoCsv});
});
